# Workspace & File Operations

## Command Groups
- `workspace` - Notebooks and folders
- `fs` - File system operations
- `repos` - Git repository management

## File System Operations (`fs`)

### Basic File Operations
```bash
# List files and directories
databricks fs ls /path/to/directory
databricks fs ls dbfs:/mnt/data/

# Copy files
databricks fs cp local-file.txt dbfs:/path/to/remote-file.txt
databricks fs cp dbfs:/path/file.txt ./local-file.txt

# Remove files/directories
databricks fs rm dbfs:/path/to/file.txt
databricks fs rm -r dbfs:/path/to/directory/  # recursive

# Create directory
databricks fs mkdir dbfs:/path/to/new/directory

# View file contents
databricks fs cat dbfs:/path/to/file.txt
```

### File System Patterns
- Use `dbfs:/` prefix for DBFS paths
- Use `/mnt/` for mounted storage
- Local paths work as expected (relative or absolute)

## Workspace Operations (`workspace`)

### Notebook Management
```bash
# List workspace contents
databricks workspace list /Users/user@company.com
databricks workspace list /Shared

# Import notebook (upload)
databricks workspace import notebook.py /Users/user@company.com/notebook.py --language PYTHON
databricks workspace import notebook.sql /Shared/queries/analysis.sql --language SQL

# Export notebook (download)
databricks workspace export /Users/user@company.com/notebook.py --format SOURCE
databricks workspace export /path/to/notebook --format DBC  # Databricks archive

# Delete notebook/folder
databricks workspace delete /Users/user@company.com/old-notebook.py
databricks workspace delete -r /Users/user@company.com/old-folder/  # recursive
```

### Workspace Formats
- `SOURCE` - Original source code format
- `HTML` - HTML export
- `JUPYTER` - Jupyter notebook format
- `DBC` - Databricks archive format

## Git Repository Management (`repos`)

### Repository Operations
```bash
# List repositories
databricks repos list

# Create repository
databricks repos create --url https://github.com/user/repo.git --path /Repos/user@company.com/repo-name

# Get repository info
databricks repos get --repo-id <repo-id>

# Update repository (pull changes)
databricks repos update --repo-id <repo-id> --branch main

# Delete repository
databricks repos delete --repo-id <repo-id>
```

## Common Workflows

### Upload Development Files
```bash
# Upload Python files
databricks workspace import my_module.py /Users/user@company.com/my_module.py --language PYTHON

# Upload entire directory (requires scripting)
for file in $(find ./src -name "*.py"); do
    databricks workspace import "$file" "/Users/user@company.com/src/$(basename $file)" --language PYTHON
done
```

### Download for Local Development
```bash
# Download notebook for editing
databricks workspace export /Users/user@company.com/analysis.py --format SOURCE -o analysis.py

# Download all notebooks in folder
databricks workspace list /Users/user@company.com --output json | \
    jq -r '.[] | select(.object_type=="NOTEBOOK") | .path' | \
    while read path; do
        filename=$(basename "$path")
        databricks workspace export "$path" --format SOURCE -o "$filename"
    done
```

## Help Commands
```bash
databricks fs --help
databricks workspace --help
databricks repos --help

# Get specific command help
databricks fs cp --help
databricks workspace import --help
```