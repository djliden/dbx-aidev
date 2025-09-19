# Development Tools

## Command Groups
- `bundle` - Databricks Asset Bundles for project deployment
- `sync` - Local directory synchronization

## Asset Bundles (`bundle`)

Asset Bundles provide Infrastructure-as-Code for Databricks, enabling version-controlled deployment of jobs, clusters, and other resources.

### Bundle Lifecycle
```bash
# Initialize new bundle
databricks bundle init

# Validate bundle configuration
databricks bundle validate

# Deploy bundle to target environment
databricks bundle deploy --target dev

# Run bundle resources
databricks bundle run my_job --target dev

# Destroy bundle resources
databricks bundle destroy --target dev
```

### Bundle Structure
```
my_project/
├── databricks.yml          # Bundle configuration
├── src/                    # Source code
├── resources/              # Job/cluster definitions
└── targets/                # Environment-specific configs
    ├── dev.yml
    └── prod.yml
```

### Basic databricks.yml
```yaml
bundle:
  name: my_project

variables:
  warehouse_id:
    description: SQL Warehouse ID
    default: "abc123"

resources:
  jobs:
    my_job:
      name: "${bundle.name}_job"
      tasks:
        - task_key: main
          notebook_task:
            notebook_path: ./src/main_notebook.py
          new_cluster:
            spark_version: "12.2.x-scala2.12"
            node_type_id: "i3.xlarge"
            num_workers: 2

targets:
  dev:
    workspace:
      host: https://dev-workspace.cloud.databricks.com
    variables:
      warehouse_id: "dev-warehouse-id"

  prod:
    workspace:
      host: https://prod-workspace.cloud.databricks.com
    variables:
      warehouse_id: "prod-warehouse-id"
```

### Bundle Commands
```bash
# Generate bundle template
databricks bundle init --template python-wheel

# Validate before deployment
databricks bundle validate --target dev

# Deploy with specific target
databricks bundle deploy --target dev

# Run specific job from bundle
databricks bundle run analytics_job --target dev

# Check deployment status
databricks bundle summary --target dev

# Clean up resources
databricks bundle destroy --target dev
```

## Directory Synchronization (`sync`)

Sync enables real-time synchronization between local directories and Databricks workspace.

### Basic Sync Operations
```bash
# Start sync from local to workspace
databricks sync ./local-folder /Workspace/Users/user@company.com/remote-folder

# Sync with specific patterns
databricks sync ./src /Workspace/Users/user@company.com/src --include "*.py" --exclude "*.pyc"

# One-time sync (no watching)
databricks sync ./local-folder /Workspace/remote-folder --watch=false
```

### Sync Configuration
```bash
# Include specific file types
databricks sync ./src /Workspace/src --include "*.py,*.sql,*.md"

# Exclude patterns
databricks sync ./project /Workspace/project --exclude "*.pyc,__pycache__,*.log"

# Bi-directional sync
databricks sync ./local /Workspace/remote --full-sync
```

## Development Workflows

### Bundle-Based Development
```bash
# 1. Initialize project
databricks bundle init --template python-wheel
cd my_project

# 2. Develop locally
# Edit src/main.py, add dependencies, etc.

# 3. Validate configuration
databricks bundle validate --target dev

# 4. Deploy to dev environment
databricks bundle deploy --target dev

# 5. Test deployment
databricks bundle run my_job --target dev

# 6. Deploy to production
databricks bundle deploy --target prod
```

### Sync-Based Development
```bash
# 1. Start sync process
databricks sync ./notebooks /Workspace/Users/user@company.com/development &

# 2. Develop locally with real-time sync
# Files automatically sync to workspace

# 3. Test in Databricks UI
# Open synced notebooks in workspace

# 4. Changes sync both ways
# Modifications in workspace sync back to local
```

### Hybrid Approach
```bash
# Use sync for active development
databricks sync ./src /Workspace/development

# Use bundles for deployment
databricks bundle deploy --target prod
```

## Bundle Templates

### Available Templates
```bash
# List available templates
databricks bundle init --help

# Common templates:
databricks bundle init --template default-python
databricks bundle init --template python-wheel
databricks bundle init --template dbt
```

### Custom Bundle Structure
```yaml
# databricks.yml for complex project
bundle:
  name: data_pipeline

variables:
  catalog:
    description: Unity Catalog name
  schema:
    description: Schema name

resources:
  jobs:
    etl_pipeline:
      name: "${bundle.name}_etl_${var.environment}"
      tasks:
        - task_key: extract
          notebook_task:
            notebook_path: ./notebooks/extract.py
        - task_key: transform
          depends_on:
            - task_key: extract
          python_wheel_task:
            package_name: data_transformations
            entry_point: transform
        - task_key: load
          depends_on:
            - task_key: transform
          sql_task:
            warehouse_id: "${var.warehouse_id}"
            query:
              query_path: ./sql/load_data.sql

  clusters:
    shared_cluster:
      cluster_name: "${bundle.name}_cluster"
      spark_version: "12.2.x-scala2.12"
      node_type_id: "i3.xlarge"
      num_workers: 2
```

## Environment Management

### Target-Specific Configurations
```yaml
# targets/dev.yml
variables:
  environment: "dev"
  catalog: "dev_catalog"
  warehouse_id: "dev-warehouse"

workspace:
  host: https://dev-workspace.cloud.databricks.com
  profile: dev

# targets/prod.yml
variables:
  environment: "prod"
  catalog: "prod_catalog"
  warehouse_id: "prod-warehouse"

workspace:
  host: https://prod-workspace.cloud.databricks.com
  profile: prod
```

### Deployment Strategies
```bash
# Development deployment
databricks bundle deploy --target dev

# Staging deployment with validation
databricks bundle validate --target staging
databricks bundle deploy --target staging

# Production deployment
databricks bundle deploy --target prod --auto-approve
```

## Help Commands
```bash
databricks bundle --help
databricks sync --help

# Get specific command help
databricks bundle init --help
databricks bundle deploy --help
databricks sync --help
```