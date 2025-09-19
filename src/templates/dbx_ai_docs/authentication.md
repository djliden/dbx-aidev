# Authentication Quick Reference

This file provides a quick authentication reference. For comprehensive CLI authentication commands, see `cli-auth.md`. For advanced SDK authentication patterns, see `sdk-execution/sdk-auth-patterns.md`.

## SDK Authentication Patterns

### From CLI Profile
```python
from databricks.sdk import WorkspaceClient

# Uses default profile
w = WorkspaceClient()

# Use specific profile
w = WorkspaceClient(profile="my-profile")
```

### Direct Configuration
```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient(
    host="https://my-workspace.cloud.databricks.com",
    token="dapi..."
)
```

### Environment Variables
```python
import os
from databricks.sdk import WorkspaceClient

# Set environment variables
os.environ["DATABRICKS_HOST"] = "https://workspace-url"
os.environ["DATABRICKS_TOKEN"] = "dapi..."

w = WorkspaceClient()
```

## CLI Setup Quick Commands
```bash
# Interactive OAuth setup
databricks auth login --host https://workspace-url

# Token-based setup
databricks auth token --host https://workspace-url

# Test authentication
databricks auth describe
```

## Execution Utilities
For programmatic execution capabilities that complement CLI workflows:
- **Notebook execution**: See `sdk-execution/notebook-execution.md`
- **SQL execution**: See `sdk-execution/sql-execution.md`
- **Advanced authentication**: See `sdk-execution/sdk-auth-patterns.md`

## Safety Notes
- Store tokens securely, never commit to version control
- Use OAuth for interactive development
- Use service principals for production automation
- See `cli-auth.md` for comprehensive CLI authentication commands