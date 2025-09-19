# Safety Guidelines for Databricks Operations

## Risk Classification

### Low Risk Operations
Operations that are safe to execute without confirmation:
- Reading data (`SELECT` queries, `databricks fs cat`)
- Listing resources (`databricks clusters list`, `databricks jobs list`)
- Getting resource details (`databricks clusters get`)
- Workspace browsing (`databricks workspace list`)

### Medium Risk Operations
Operations that modify resources but are generally recoverable:
- Creating resources (`databricks clusters create`)
- Starting/stopping compute (`databricks clusters start/stop`)
- Installing libraries (`databricks libraries install`)
- Uploading files (`databricks workspace import`)

### High Risk Operations
Operations that can cause data loss or significant cost:
- Deleting resources (`databricks clusters delete`, `databricks workspace delete`)
- Terminating jobs (`databricks jobs cancel-run`)
- Modifying production resources
- Operations affecting shared resources

## Safety Patterns

### Always Confirm Before
1. **Deleting any resource**
   ```bash
   # Always confirm before deletion
   echo "Are you sure you want to delete cluster $CLUSTER_ID? (y/N)"
   read confirmation
   if [[ "$confirmation" == "y" ]]; then
       databricks clusters delete --cluster-id $CLUSTER_ID
   fi
   ```

2. **Modifying production environments**
   ```bash
   # Check target environment
   if [[ "$TARGET" == "prod" ]]; then
       echo "WARNING: Deploying to PRODUCTION. Confirm? (y/N)"
       read confirmation
       [[ "$confirmation" != "y" ]] && exit 1
   fi
   ```

3. **Bulk operations**
   ```bash
   # Show what will be affected before bulk operations
   echo "The following clusters will be terminated:"
   databricks clusters list --output json | jq -r '.clusters[] | select(.state=="RUNNING") | .cluster_name'
   echo "Continue? (y/N)"
   ```

### Permission Validation
```bash
# Test permissions before operations
if ! databricks workspace list > /dev/null 2>&1; then
    echo "Error: No workspace access. Check authentication."
    exit 1
fi

# Verify cluster access before operations
if ! databricks clusters get --cluster-id $CLUSTER_ID > /dev/null 2>&1; then
    echo "Error: Cannot access cluster $CLUSTER_ID"
    exit 1
fi
```

### Environment Isolation
```bash
# Use explicit profile for production
if [[ "$ENV" == "prod" ]]; then
    DATABRICKS_PROFILE="production"
    export DATABRICKS_PROFILE
fi

# Validate environment before proceeding
CURRENT_HOST=$(databricks auth describe | grep Host | awk '{print $2}')
if [[ "$CURRENT_HOST" != "$EXPECTED_HOST" ]]; then
    echo "Error: Connected to wrong workspace!"
    echo "Expected: $EXPECTED_HOST"
    echo "Current: $CURRENT_HOST"
    exit 1
fi
```

## Resource Management Safety

### Cluster Safety
```bash
# Check cluster cost before creation
NODE_COUNT=$(jq -r '.num_workers' cluster-config.json)
if [[ $NODE_COUNT -gt 10 ]]; then
    echo "WARNING: Large cluster ($NODE_COUNT workers) requested"
    echo "Estimated cost: High. Continue? (y/N)"
    read confirmation
    [[ "$confirmation" != "y" ]] && exit 1
fi

# Set autotermination for development clusters
jq '.autotermination_minutes = 60' cluster-config.json > temp.json
mv temp.json cluster-config.json
```

### Job Safety
```bash
# Validate job configuration before creation
if ! databricks bundle validate; then
    echo "Job configuration is invalid. Fix errors before deployment."
    exit 1
fi

# Check for production data access in dev jobs
if grep -q "prod_catalog" job-config.json && [[ "$ENV" == "dev" ]]; then
    echo "WARNING: Dev job accessing production data"
    exit 1
fi
```

## Data Access Safety

### Unity Catalog Operations
```bash
# Verify catalog access before operations
CATALOG="my_catalog"
if ! databricks sql query --query "SHOW CATALOGS" | grep -q "$CATALOG"; then
    echo "Error: No access to catalog $CATALOG"
    exit 1
fi

# Check permissions before writing
TABLE="catalog.schema.table"
if ! databricks sql query --query "DESCRIBE TABLE $TABLE" > /dev/null 2>&1; then
    echo "Warning: Cannot access table $TABLE"
    echo "Check permissions before proceeding"
fi
```

### File Operations
```bash
# Backup before overwriting
if databricks fs ls "dbfs:/path/to/file.txt" > /dev/null 2>&1; then
    echo "File exists. Creating backup..."
    databricks fs cp "dbfs:/path/to/file.txt" "dbfs:/path/to/file.txt.backup.$(date +%Y%m%d)"
fi

# Validate file paths
if [[ "$FILE_PATH" == dbfs://* ]]; then
    echo "Writing to DBFS: $FILE_PATH"
    echo "This will be accessible to all workspace users. Continue? (y/N)"
fi
```

## Error Handling and Recovery

### Rollback Patterns
```bash
# Save current state before changes
ORIGINAL_CONFIG=$(databricks jobs get --job-id $JOB_ID)

# Apply changes with rollback on failure
if ! databricks jobs update --job-id $JOB_ID --json-file new-config.json; then
    echo "Update failed. Rolling back..."
    echo "$ORIGINAL_CONFIG" | databricks jobs update --job-id $JOB_ID --json-file -
fi
```

### Validation Checks
```bash
# Validate deployment after changes
sleep 30  # Allow time for deployment
if ! databricks jobs get --job-id $JOB_ID | grep -q "SUCCESS"; then
    echo "Deployment validation failed"
    # Trigger rollback procedure
fi
```

## Least Privilege Patterns

### Service Principal Usage
```bash
# Use minimal permissions for automation
# Create service principal with only required permissions
SP_ID=$(databricks service-principals create --display-name "CI/CD Pipeline" | jq -r .id)

# Grant only necessary permissions
# databricks permissions update --object-type jobs --object-id $JOB_ID --service-principal-id $SP_ID --permission CAN_MANAGE
```

### Profile Separation
```bash
# Use different profiles for different environments
alias db-dev="databricks --profile dev"
alias db-staging="databricks --profile staging"
alias db-prod="databricks --profile prod"

# Always specify profile explicitly in scripts
PROFILE="${ENV:-dev}"
databricks --profile "$PROFILE" jobs list
```

## Common Safety Mistakes to Avoid

1. **Never hardcode production tokens in scripts**
2. **Don't use admin tokens for automation**
3. **Always validate target environment**
4. **Don't skip confirmation for destructive operations**
5. **Avoid wildcard deletions without verification**
6. **Don't ignore permission errors**
7. **Always set resource limits (autotermination, timeouts)**
8. **Don't deploy without validation**

## Emergency Procedures

### Incident Response
```bash
# Stop all running jobs in emergency
databricks jobs list --output json | \
    jq -r '.jobs[] | .job_id' | \
    while read job_id; do
        databricks jobs list-runs --job-id $job_id --active-only | \
            jq -r '.runs[]? | .run_id' | \
            while read run_id; do
                databricks jobs cancel-run --run-id $run_id
            done
    done

# Terminate all clusters
databricks clusters list --output json | \
    jq -r '.clusters[] | select(.state=="RUNNING") | .cluster_id' | \
    while read cluster_id; do
        databricks clusters delete --cluster-id $cluster_id
    done
```