# Databricks CLI Overview

## Quick Start for AI Tools

The Databricks CLI is organized into **command groups** with consistent patterns. This is your entry point for understanding how to work with the CLI effectively.

For execution capabilities the CLI lacks, see the SDK execution modules: `sdk-execution/notebook-execution.md` and `sdk-execution/sql-execution.md`.

## Basic Structure
```bash
databricks <command-group> <command> [options]
```

## Essential Help Commands
```bash
# List all available command groups
databricks --help

# Get help for a command group
databricks <command-group> --help
databricks clusters --help

# Get help for a specific command
databricks <command-group> <command> --help
databricks clusters create --help
```

## Global Options (Available on All Commands)
- `--debug` - Enable debug logging
- `--help` / `-h` - Show help
- `--output json` / `-o json` - Output as JSON instead of table
- `--profile <name>` / `-p <name>` - Use specific auth profile

## Command Group Categories

### Workspace & Files
- `workspace` - Notebooks and folder management
- `fs` - File system operations
- `repos` - Git repository management

### Compute Resources
- `clusters` - Interactive clusters
- `instance-pools` - Pre-configured compute instances
- `warehouses` - SQL compute warehouses

### Jobs & Workflows
- `jobs` - Job management and execution

### Data & Catalogs
- `catalogs` - Unity Catalog management
- `schemas` - Schema operations
- `tables` - Table management
- `volumes` - File storage volumes

### ML & Experiments
- `experiments` - MLflow experiment tracking
- `model-registry` - ML model lifecycle

### Access & Security
- `auth` - Authentication setup
- `users` - User management
- `service-principals` - Service account management
- `account` - Account-level settings

### Development Tools
- `bundle` - Asset bundle deployment
- `sync` - Local file synchronization

## Discovery Pattern for AI Tools

1. **Start with help**: `databricks --help` to see all command groups
2. **Explore groups**: `databricks <group> --help` to see available commands
3. **Get command details**: `databricks <group> <command> --help` for parameters
4. **Check examples**: Most help includes usage examples

## Common Patterns

### Listing Resources
```bash
databricks clusters list
databricks jobs list
databricks workspace list /path
```

### Creating Resources
```bash
databricks clusters create --json-file cluster-config.json
databricks jobs create --json-file job-config.json
```

### Getting Resource Details
```bash
databricks clusters get --cluster-id <id>
databricks jobs get --job-id <id>
```

## Next Steps
Refer to specific command group documentation files:
- `cli-workspace.md` - Workspace and file operations
- `cli-compute.md` - Clusters and compute resources
- `cli-jobs.md` - Job management
- `cli-data.md` - Unity Catalog and data operations
- `cli-ml.md` - ML experiments and models
- `cli-access.md` - Authentication and user management
- `cli-dev-tools.md` - Asset bundles and development tools