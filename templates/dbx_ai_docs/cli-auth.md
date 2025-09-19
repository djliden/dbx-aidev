# Authentication & Access Management

## Command Groups
- `auth` - Authentication setup and management
- `users` - User identity management
- `service-principals` - Service account management
- `account` - Account-level settings

## Authentication Setup (`auth`)

### Configure Authentication
```bash
# Interactive OAuth setup (recommended)
databricks auth login --host https://my-workspace.cloud.databricks.com

# Token-based authentication
databricks auth token --host https://my-workspace.cloud.databricks.com

# Environment variable setup
databricks auth env --host https://my-workspace.cloud.databricks.com
```

### Profile Management
```bash
# List authentication profiles
databricks auth profiles

# Test current authentication
databricks auth describe

# Use specific profile
databricks --profile my-profile workspace list
```

## User Management (`users`)

### User Operations
```bash
# List users
databricks users list

# Get user details
databricks users get --user-name user@company.com

# Create user
databricks users create --user-name newuser@company.com --display-name "New User"

# Update user
databricks users update --user-name user@company.com --display-name "Updated Name"

# Delete user
databricks users delete --user-name user@company.com
```

## Service Principals (`service-principals`)

### Service Principal Management
```bash
# List service principals
databricks service-principals list

# Create service principal
databricks service-principals create --display-name "CI/CD Pipeline"

# Get service principal details
databricks service-principals get --service-principal-id <sp-id>

# Generate token for service principal
databricks service-principals create-token --service-principal-id <sp-id> --comment "Production deployment"
```

## Account-Level Operations (`account`)

### Account Management
```bash
# List account users
databricks account users list --account-id <account-id>

# List workspaces
databricks account workspaces list --account-id <account-id>

# Manage account-level service principals
databricks account service-principals list --account-id <account-id>
```

## Authentication Methods

### 1. OAuth (Interactive Development)
```bash
# Setup OAuth
databricks auth login --host https://workspace-url

# This opens browser for authentication
# Token is stored securely in profile
```

### 2. Personal Access Token
```bash
# Generate token in Databricks UI: User Settings > Developer > Access Tokens
# Then configure:
databricks auth token --host https://workspace-url
# Enter token when prompted
```

### 3. Environment Variables
```bash
export DATABRICKS_HOST="https://workspace-url"
export DATABRICKS_TOKEN="dapi..."

# Test configuration
databricks auth describe
```

### 4. Service Principal (Production)
```bash
# Create service principal
SP_ID=$(databricks service-principals create --display-name "Production App" | jq -r .id)

# Generate token
TOKEN=$(databricks service-principals create-token --service-principal-id $SP_ID --comment "Prod token" | jq -r .token_value)

# Use in environment
export DATABRICKS_HOST="https://workspace-url"
export DATABRICKS_TOKEN="$TOKEN"
```

## Profile Configuration

### Multiple Workspaces
```bash
# Configure different profiles
databricks auth login --host https://dev-workspace.cloud.databricks.com --profile dev
databricks auth login --host https://prod-workspace.cloud.databricks.com --profile prod

# Use specific profile
databricks --profile dev clusters list
databricks --profile prod jobs list
```

### Profile Location
Profiles are stored in:
- `~/.databrickscfg` (default)
- Custom location with `DATABRICKS_CONFIG_FILE` environment variable

### Profile Format
```ini
[DEFAULT]
host = https://workspace-url
token = dapi...

[dev]
host = https://dev-workspace.cloud.databricks.com
token = dapi...

[prod]
host = https://prod-workspace.cloud.databricks.com
token = dapi...
```

## Security Best Practices

### Token Management
- Generate tokens with minimal required permissions
- Set expiration dates on tokens
- Regularly rotate tokens
- Never commit tokens to version control
- Use service principals for automation

### Access Control
- Use service principals for CI/CD and automation
- Implement least-privilege access
- Regular audit of user permissions
- Use Unity Catalog for fine-grained data access control

### Environment Isolation
```bash
# Separate profiles for environments
databricks --profile dev workspace list    # Development
databricks --profile staging jobs list     # Staging
databricks --profile prod clusters list    # Production
```

## Troubleshooting Authentication

### Common Issues
```bash
# Check current authentication
databricks auth describe

# Test connectivity
databricks workspace list

# Debug authentication issues
databricks --debug workspace list

# Clear cached credentials
rm ~/.databrickscfg
```

### Error Messages
- `Error 401: Unauthorized` - Invalid or expired token
- `Error 403: Forbidden` - Insufficient permissions
- `Error 404: Not Found` - Incorrect workspace URL

## Help Commands
```bash
databricks auth --help
databricks users --help
databricks service-principals --help

# Get specific command help
databricks auth login --help
databricks service-principals create --help
```