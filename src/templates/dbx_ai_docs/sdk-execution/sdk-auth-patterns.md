# SDK Authentication Patterns

Advanced authentication patterns for Databricks SDK execution, extending beyond basic CLI profile usage.

## Quick Reference

```python
from databricks.sdk import WorkspaceClient
from dbx_execution import create_workspace_client

# Use utility function for flexible authentication
client = create_workspace_client(profile="my-profile")

# Or create directly
client = WorkspaceClient(host="https://workspace.cloud.databricks.com", token="dapi...")
```

## Authentication Methods

### 1. CLI Profile Authentication (Recommended for Development)

**Default profile:**
```python
from databricks.sdk import WorkspaceClient

# Uses default profile from ~/.databrickscfg
client = WorkspaceClient()
```

**Specific profile:**
```python
# Uses named profile from ~/.databrickscfg
client = WorkspaceClient(profile="production")
client = WorkspaceClient(profile="development")
```

**Custom config file:**
```python
client = WorkspaceClient(
    profile="my-profile",
    config_file="/path/to/custom/databrickscfg"
)
```

### 2. Direct Token Authentication

**Personal Access Token:**
```python
client = WorkspaceClient(
    host="https://my-workspace.cloud.databricks.com",
    token="dapi1234567890abcdef"
)
```

**Environment variable token:**
```python
import os

client = WorkspaceClient(
    host=os.environ["DATABRICKS_HOST"],
    token=os.environ["DATABRICKS_TOKEN"]
)
```

### 3. Environment Variable Authentication

**Set environment variables:**
```bash
export DATABRICKS_HOST="https://my-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi1234567890abcdef"
```

```python
# Automatically picks up environment variables
client = WorkspaceClient()
```

**Complete environment setup:**
```bash
export DATABRICKS_HOST="https://workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_CLUSTER_ID="0123-456789-abcdef"  # Optional default cluster
export DATABRICKS_WAREHOUSE_ID="abc123def456"      # Optional default warehouse
```

### 4. Service Principal Authentication

**Azure Service Principal:**
```python
client = WorkspaceClient(
    host="https://adb-1234567890123456.7.azuredatabricks.net",
    azure_workspace_resource_id="/subscriptions/.../resourceGroups/.../providers/Microsoft.Databricks/workspaces/...",
    azure_client_id="your-app-id",
    azure_client_secret="your-app-secret",
    azure_tenant_id="your-tenant-id"
)
```

**AWS Service Principal (OAuth):**
```python
client = WorkspaceClient(
    host="https://workspace.cloud.databricks.com",
    client_id="your-oauth-client-id",
    client_secret="your-oauth-client-secret"
)
```

### 5. Notebook-Native Authentication

**Inside Databricks notebook:**
```python
# Automatically uses notebook context (no additional auth needed)
from databricks.sdk import WorkspaceClient

client = WorkspaceClient()

# This works seamlessly inside Databricks notebooks
# No tokens or authentication configuration required
```

## Authentication Utilities

### Flexible Client Creation

**Utility function for multiple auth methods:**
```python
from dbx_execution.utils import create_workspace_client

# Method 1: Use specific profile
client = create_workspace_client(profile="production")

# Method 2: Use direct credentials
client = create_workspace_client(
    host="https://workspace.cloud.databricks.com",
    token="dapi..."
)

# Method 3: Use environment variables (no parameters)
client = create_workspace_client()
```

### Authentication Testing

**Test authentication:**
```python
def test_authentication(client: WorkspaceClient) -> bool:
    """Test if authentication is working."""
    try:
        # Simple API call to test auth
        current_user = client.current_user.me()
        print(f"✅ Authenticated as: {current_user.user_name}")
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

# Test your client
client = WorkspaceClient()
if test_authentication(client):
    print("Ready to proceed with SDK operations")
```

**Comprehensive auth test:**
```python
def validate_auth_and_permissions(client: WorkspaceClient) -> Dict[str, bool]:
    """Test authentication and key permissions."""
    results = {}

    try:
        # Test basic auth
        user = client.current_user.me()
        results['authentication'] = True
        print(f"✅ Authenticated as: {user.user_name}")

        # Test workspace access
        try:
            client.workspace.list("/")
            results['workspace_access'] = True
            print("✅ Workspace access: OK")
        except:
            results['workspace_access'] = False
            print("❌ Workspace access: DENIED")

        # Test cluster access
        try:
            clusters = list(client.clusters.list())
            results['cluster_access'] = True
            print(f"✅ Cluster access: OK ({len(clusters)} clusters visible)")
        except:
            results['cluster_access'] = False
            print("❌ Cluster access: DENIED")

        # Test SQL warehouse access
        try:
            warehouses = list(client.warehouses.list())
            results['warehouse_access'] = True
            print(f"✅ Warehouse access: OK ({len(warehouses)} warehouses visible)")
        except:
            results['warehouse_access'] = False
            print("❌ Warehouse access: DENIED")

    except Exception as e:
        results['authentication'] = False
        print(f"❌ Authentication failed: {e}")

    return results
```

## Production Authentication Patterns

### 1. CI/CD Pipeline Authentication

**GitHub Actions example:**
```yaml
# .github/workflows/databricks.yml
env:
  DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
  DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}

jobs:
  execute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Execute notebook
        run: |
          python -c "
          from databricks.sdk import WorkspaceClient
          from dbx_execution import NotebookExecutor

          client = WorkspaceClient()  # Uses env vars
          executor = NotebookExecutor(client)
          result = executor.run_notebook('/path/to/notebook')
          print(f'Status: {result[\"status\"]}')
          "
```

### 2. Multi-Environment Configuration

**Environment-specific configs:**
```python
import os
from databricks.sdk import WorkspaceClient

def get_client_for_environment(env: str) -> WorkspaceClient:
    """Get client for specific environment."""
    if env == "development":
        return WorkspaceClient(profile="dev")
    elif env == "staging":
        return WorkspaceClient(profile="staging")
    elif env == "production":
        # Use service principal in production
        return WorkspaceClient(
            host=os.environ["PROD_DATABRICKS_HOST"],
            azure_client_id=os.environ["PROD_CLIENT_ID"],
            azure_client_secret=os.environ["PROD_CLIENT_SECRET"],
            azure_tenant_id=os.environ["PROD_TENANT_ID"],
            azure_workspace_resource_id=os.environ["PROD_WORKSPACE_RESOURCE_ID"]
        )
    else:
        raise ValueError(f"Unknown environment: {env}")

# Usage
env = os.environ.get("ENVIRONMENT", "development")
client = get_client_for_environment(env)
```

### 3. Credential Management

**Secure credential handling:**
```python
import os
import json
from pathlib import Path
from databricks.sdk import WorkspaceClient

def load_credentials_from_file(path: str) -> WorkspaceClient:
    """Load credentials from secure file."""
    cred_path = Path(path)
    if not cred_path.exists():
        raise FileNotFoundError(f"Credentials file not found: {path}")

    with open(cred_path) as f:
        creds = json.load(f)

    return WorkspaceClient(
        host=creds["host"],
        token=creds.get("token"),
        azure_client_id=creds.get("azure_client_id"),
        azure_client_secret=creds.get("azure_client_secret"),
        azure_tenant_id=creds.get("azure_tenant_id")
    )

# Usage
client = load_credentials_from_file("~/.databricks/prod_creds.json")
```

## Authentication Best Practices

### Security Guidelines

1. **Never hardcode credentials** in source code
2. **Use environment variables** for automated systems
3. **Use CLI profiles** for development
4. **Use service principals** for production
5. **Rotate tokens regularly**
6. **Use least-privilege access**
7. **Store credentials securely** (e.g., AWS Secrets Manager, Azure Key Vault)

### Development Workflow

**Local development setup:**
```bash
# Set up development profile
databricks auth login --host https://dev-workspace.cloud.databricks.com --profile dev

# Set up production profile (for testing prod access)
databricks auth login --host https://prod-workspace.cloud.databricks.com --profile prod
```

```python
# In your development scripts
def get_development_client():
    return WorkspaceClient(profile="dev")

def get_production_client():
    return WorkspaceClient(profile="prod")
```

### Error Handling

**Robust authentication with fallback:**
```python
def create_authenticated_client() -> WorkspaceClient:
    """Create authenticated client with multiple fallback methods."""
    auth_methods = [
        ("Environment variables", lambda: WorkspaceClient()),
        ("Default profile", lambda: WorkspaceClient(profile="default")),
        ("Development profile", lambda: WorkspaceClient(profile="dev")),
    ]

    for method_name, create_client in auth_methods:
        try:
            client = create_client()
            # Test the client
            client.current_user.me()
            print(f"✅ Authenticated using: {method_name}")
            return client
        except Exception as e:
            print(f"❌ {method_name} failed: {e}")
            continue

    raise Exception("❌ All authentication methods failed")

# Usage
client = create_authenticated_client()
```

## Common Authentication Issues

**Troubleshooting guide:**

1. **"Authentication failed" errors:**
   - Check token expiration
   - Verify workspace URL format
   - Ensure token has proper permissions

2. **"Profile not found" errors:**
   - Run `databricks auth describe` to list profiles
   - Check `~/.databrickscfg` file exists and has correct format

3. **"Permission denied" errors:**
   - Verify user has necessary workspace permissions
   - Check Unity Catalog permissions for data access

4. **"Host unreachable" errors:**
   - Verify workspace URL is correct
   - Check network connectivity
   - Ensure workspace is not suspended

**Debug authentication:**
```python
import logging
from databricks.sdk import WorkspaceClient

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

client = WorkspaceClient()
# This will show detailed authentication debug info
```