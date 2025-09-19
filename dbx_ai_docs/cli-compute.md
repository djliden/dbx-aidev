# Compute Resources

## Command Groups
- `clusters` - Interactive clusters for notebooks and jobs
- `instance-pools` - Pre-configured compute instances
- `warehouses` - SQL compute warehouses

## Cluster Management (`clusters`)

### Basic Cluster Operations
```bash
# List clusters
databricks clusters list
databricks clusters list --output json

# Get cluster details
databricks clusters get --cluster-id <cluster-id>

# Start cluster
databricks clusters start --cluster-id <cluster-id>

# Restart cluster
databricks clusters restart --cluster-id <cluster-id>

# Terminate cluster
databricks clusters delete --cluster-id <cluster-id>
```

### Cluster Creation
```bash
# Create cluster from JSON config
databricks clusters create --json-file cluster-config.json

# Create cluster with inline JSON
databricks clusters create --json '{
  "cluster_name": "my-cluster",
  "spark_version": "12.2.x-scala2.12",
  "node_type_id": "i3.xlarge",
  "num_workers": 2
}'
```

### Example cluster-config.json
```json
{
  "cluster_name": "development-cluster",
  "spark_version": "12.2.x-scala2.12",
  "node_type_id": "i3.xlarge",
  "num_workers": 2,
  "autotermination_minutes": 60,
  "spark_conf": {
    "spark.sql.adaptive.enabled": "true"
  },
  "aws_attributes": {
    "availability": "SPOT_WITH_FALLBACK",
    "spot_bid_price_percent": 100
  }
}
```

## Instance Pools (`instance-pools`)

### Pool Management
```bash
# List instance pools
databricks instance-pools list

# Get pool details
databricks instance-pools get --instance-pool-id <pool-id>

# Create instance pool
databricks instance-pools create --json-file pool-config.json

# Delete instance pool
databricks instance-pools delete --instance-pool-id <pool-id>
```

## SQL Warehouses (`warehouses`)

### Warehouse Operations
```bash
# List SQL warehouses
databricks warehouses list

# Get warehouse details
databricks warehouses get --warehouse-id <warehouse-id>

# Start warehouse
databricks warehouses start --warehouse-id <warehouse-id>

# Stop warehouse
databricks warehouses stop --warehouse-id <warehouse-id>

# Create warehouse
databricks warehouses create --json-file warehouse-config.json
```

## Library Management (`libraries`)

### Install Libraries on Clusters
```bash
# Install PyPI package
databricks libraries install --cluster-id <cluster-id> --pypi-package pandas==1.5.0

# Install JAR
databricks libraries install --cluster-id <cluster-id> --jar dbfs:/path/to/library.jar

# Install wheel
databricks libraries install --cluster-id <cluster-id> --whl dbfs:/path/to/package.whl

# List installed libraries
databricks libraries list --cluster-id <cluster-id>

# Uninstall library
databricks libraries uninstall --cluster-id <cluster-id> --pypi-package pandas
```

## Common Patterns

### Development Cluster Setup
```bash
# 1. Create cluster
CLUSTER_ID=$(databricks clusters create --json-file dev-cluster.json | jq -r .cluster_id)

# 2. Wait for cluster to start
databricks clusters start --cluster-id $CLUSTER_ID

# 3. Install development libraries
databricks libraries install --cluster-id $CLUSTER_ID --pypi-package pandas
databricks libraries install --cluster-id $CLUSTER_ID --pypi-package scikit-learn

# 4. Check cluster status
databricks clusters get --cluster-id $CLUSTER_ID
```

### Cluster Cost Management
```bash
# List all running clusters
databricks clusters list --output json | jq '.clusters[] | select(.state=="RUNNING") | {cluster_name, cluster_id}'

# Terminate idle clusters (requires custom scripting)
databricks clusters list --output json | \
    jq -r '.clusters[] | select(.state=="RUNNING") | .cluster_id' | \
    while read cluster_id; do
        databricks clusters delete --cluster-id $cluster_id
    done
```

## Configuration Tips

### Cluster Sizing Guidelines
- **Development**: 1-2 workers, spot instances
- **Production**: 3+ workers, on-demand instances
- **ML Training**: GPU-enabled node types
- **Streaming**: Memory-optimized instances

### Spark Configuration
Common spark_conf settings:
```json
{
  "spark.sql.adaptive.enabled": "true",
  "spark.sql.adaptive.coalescePartitions.enabled": "true",
  "spark.serializer": "org.apache.spark.serializer.KryoSerializer"
}
```

## Help Commands
```bash
databricks clusters --help
databricks instance-pools --help
databricks warehouses --help
databricks libraries --help

# Get specific command help
databricks clusters create --help
databricks warehouses start --help
```