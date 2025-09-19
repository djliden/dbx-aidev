# Job Management

## Command Groups
- `jobs` - Job lifecycle management and execution

## Job Operations (`jobs`)

### Basic Job Management
```bash
# List jobs
databricks jobs list
databricks jobs list --output json

# Get job details
databricks jobs get --job-id <job-id>

# Create job
databricks jobs create --json-file job-config.json

# Update job
databricks jobs update --job-id <job-id> --json-file updated-job-config.json

# Delete job
databricks jobs delete --job-id <job-id>
```

### Job Execution
```bash
# Run job immediately
databricks jobs run-now --job-id <job-id>

# Run job with parameters
databricks jobs run-now --job-id <job-id> --json '{
  "notebook_params": {
    "input_path": "/data/today",
    "output_path": "/results/analysis"
  }
}'

# Get run details
databricks jobs get-run --run-id <run-id>

# Cancel running job
databricks jobs cancel-run --run-id <run-id>

# List runs for a job
databricks jobs list-runs --job-id <job-id>
```

## Job Configuration Examples

### Notebook Job
```json
{
  "name": "Daily Data Processing",
  "tasks": [
    {
      "task_key": "process_data",
      "notebook_task": {
        "notebook_path": "/Users/user@company.com/data_processing",
        "base_parameters": {
          "input_date": "{{job.start_time.date}}"
        }
      },
      "new_cluster": {
        "spark_version": "12.2.x-scala2.12",
        "node_type_id": "i3.xlarge",
        "num_workers": 2,
        "spark_conf": {
          "spark.sql.adaptive.enabled": "true"
        }
      }
    }
  ],
  "schedule": {
    "quartz_cron_expression": "0 0 2 * * ?",
    "timezone_id": "UTC"
  },
  "email_notifications": {
    "on_failure": ["user@company.com"]
  }
}
```

### Python Wheel Job
```json
{
  "name": "ML Model Training",
  "tasks": [
    {
      "task_key": "train_model",
      "python_wheel_task": {
        "package_name": "my_ml_package",
        "entry_point": "train",
        "parameters": ["--data-path", "/data/training"]
      },
      "new_cluster": {
        "spark_version": "12.2.x-ml-scala2.12",
        "node_type_id": "i3.2xlarge",
        "num_workers": 4
      },
      "libraries": [
        {
          "whl": "dbfs:/packages/my_ml_package-1.0.0-py3-none-any.whl"
        },
        {
          "pypi": {
            "package": "scikit-learn==1.2.0"
          }
        }
      ]
    }
  ]
}
```

### Multi-Task Job with Dependencies
```json
{
  "name": "ETL Pipeline",
  "tasks": [
    {
      "task_key": "extract",
      "notebook_task": {
        "notebook_path": "/pipelines/extract"
      },
      "new_cluster": {
        "spark_version": "12.2.x-scala2.12",
        "node_type_id": "i3.large",
        "num_workers": 1
      }
    },
    {
      "task_key": "transform",
      "notebook_task": {
        "notebook_path": "/pipelines/transform"
      },
      "depends_on": [{"task_key": "extract"}],
      "existing_cluster_id": "shared-cluster-id"
    },
    {
      "task_key": "load",
      "notebook_task": {
        "notebook_path": "/pipelines/load"
      },
      "depends_on": [{"task_key": "transform"}],
      "existing_cluster_id": "shared-cluster-id"
    }
  ]
}
```

## Job Monitoring

### Check Job Status
```bash
# Get latest run for a job
databricks jobs list-runs --job-id <job-id> --limit 1

# Monitor running job
while true; do
  STATUS=$(databricks jobs get-run --run-id <run-id> | jq -r .state.life_cycle_state)
  echo "Job status: $STATUS"
  if [[ "$STATUS" == "TERMINATED" || "$STATUS" == "SKIPPED" || "$STATUS" == "INTERNAL_ERROR" ]]; then
    break
  fi
  sleep 30
done
```

### Get Job Logs
```bash
# Get run output
databricks jobs get-run-output --run-id <run-id>

# For notebook jobs, logs are in the notebook output
# For Python wheel jobs, logs are in cluster logs
```

## Common Patterns

### Development Workflow
```bash
# 1. Create job from config
JOB_ID=$(databricks jobs create --json-file job-config.json | jq -r .job_id)

# 2. Test run with parameters
RUN_ID=$(databricks jobs run-now --job-id $JOB_ID --json '{"notebook_params": {"debug": "true"}}' | jq -r .run_id)

# 3. Monitor execution
databricks jobs get-run --run-id $RUN_ID

# 4. Update job if needed
databricks jobs update --job-id $JOB_ID --json-file updated-config.json
```

### Production Deployment
```bash
# Deploy job with proper error handling
if ! databricks jobs create --json-file prod-job.json; then
  echo "Job creation failed"
  exit 1
fi

# Set up monitoring
databricks jobs run-now --job-id $JOB_ID
```

## Scheduling

### Cron Expressions
- `0 0 2 * * ?` - Daily at 2 AM UTC
- `0 0 2 * * MON` - Weekly on Monday at 2 AM UTC
- `0 0 2 1 * ?` - Monthly on 1st at 2 AM UTC
- `0 0/30 * * * ?` - Every 30 minutes

### Time Zones
Use timezone_id field with values like:
- `UTC`
- `America/New_York`
- `Europe/London`
- `Asia/Tokyo`

## Help Commands
```bash
databricks jobs --help

# Get specific command help
databricks jobs create --help
databricks jobs run-now --help
databricks jobs get-run --help
```