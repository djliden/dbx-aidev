# Databricks Project Setup Wizard

**Interactive setup wizard for Databricks AI development projects**

I will guide you through a comprehensive, step-by-step setup process to configure this project for effective Databricks development with AI assistance.

## 🎯 Setup Phases Overview

**Phase 1**: ⏺ Environment & CLI Setup
**Phase 2**: ⏺ Authentication Configuration
**Phase 3**: ⏺ Project Analysis & Strategy
**Phase 4**: ⏺ Documentation Enhancement
**Phase 5**: ⏺ Validation & Testing

---

## 📋 Phase 1: Environment & CLI Setup

### Step 1.1: Check Current Environment
Let me first understand your current setup:

```bash
# Check if databricks CLI is available
databricks --version
```

**Expected Output**: `databricks 0.x.x` or higher

**If command not found**:
```bash
# Install Databricks CLI
uv add databricks-cli

# Verify installation
databricks --version
```

### Step 1.2: Verify Project Structure
Let me check what's already in your project:

```bash
# List current directory contents
ls -la

# Check for existing notebooks/Python files
find . -name "*.py" -o -name "*.ipynb" | head -10
```

**✅ Phase 1 Complete When**:
- [ ] Databricks CLI is installed and working
- [ ] Project structure is understood

---

## 🔐 Phase 2: Authentication Configuration

### Step 2.1: Choose Authentication Method

I'll help you set up authentication. What's your preference?

**Option A: OAuth (Recommended for Interactive Development)**
```bash
# Configure OAuth authentication
databricks auth login
```
- Follow the browser OAuth flow
- Most secure for personal development
- No tokens to manage

**Option B: Personal Access Token**
```bash
# Configure with Personal Access Token
databricks auth token
```
- Enter your workspace URL when prompted
- Enter your PAT when prompted
- Good for automation/CI scenarios

**Option C: Use Existing Profile**
```bash
# List existing profiles
databricks auth profiles

# Test existing profile
databricks --profile YOUR_PROFILE workspace list
```

### Step 2.2: Set Workspace URL
What's your Databricks workspace URL?
- Format: `https://your-workspace.cloud.databricks.com`
- Or: `https://your-workspace.databricks.azure.com` (Azure)
- Or: `https://your-workspace.gcp.databricks.com` (GCP)

### Step 2.3: Test Authentication
Let's verify your connection works:

```bash
# Test basic connectivity
databricks auth describe

# Test workspace access
databricks workspace list /

# Test cluster access (if any)
databricks clusters list
```

**Expected Output**: Should see workspace contents without errors

**Common Issues & Solutions**:
- `Error 401`: Token expired or invalid → Re-authenticate
- `Error 403`: Insufficient permissions → Check workspace access
- `Error 404`: Wrong workspace URL → Verify URL format

### Step 2.4: Environment Variables (Optional)
For consistent authentication, I can help set up environment variables:

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..." # Only if using PAT
```

**✅ Phase 2 Complete When**:
- [ ] Authentication method chosen and configured
- [ ] `databricks auth describe` shows valid authentication
- [ ] `databricks workspace list` works without errors

---

## 📊 Phase 3: Project Analysis & Strategy

### Step 3.1: Analyze Current Project
Based on your project structure, let me recommend the best approach:

```bash
# Count Python files
find . -name "*.py" | wc -l

# Count notebooks
find . -name "*.ipynb" | wc -l

# Check for dependencies
ls pyproject.toml requirements.txt setup.py 2>/dev/null || echo "No dependency files found"
```

### Step 3.2: Recommend Deployment Strategy

**If project has**:
- 1-3 notebooks, minimal dependencies → **Standalone Deployment**
- Multiple Python files, complex structure → **Asset Bundle Deployment**

**Standalone Deployment Setup**:
```bash
# For simple projects - direct notebook upload/execution
# Notebooks run individually on Databricks clusters
# Good for: Analysis, prototyping, simple pipelines
```

**Asset Bundle Deployment Setup**:
```bash
# Initialize Databricks Asset Bundle
databricks bundle init

# This creates:
# - databricks.yml (bundle configuration)
# - resources/ (job definitions)
# - src/ (source code)
```

### Step 3.3: Choose Development Pattern
What's your primary development pattern?

**A. Notebook-First Development**
- Develop primarily in Databricks workspace
- Use sync for collaborative editing
- Good for: Data exploration, interactive analysis

**B. Local-First Development**
- Develop locally, deploy to Databricks
- Use version control for all changes
- Good for: Production pipelines, complex applications

**C. Hybrid Development**
- Local development + notebook prototyping
- Best of both worlds
- Good for: Most data science projects

**✅ Phase 3 Complete When**:
- [ ] Project complexity assessed
- [ ] Deployment strategy chosen
- [ ] Development pattern selected

---

## 📝 Phase 4: Documentation Enhancement

### Step 4.1: Update CLAUDE.md with Project Context
I'll now enhance your CLAUDE.md with workspace-specific information:

```markdown
# Your Project Name

## Databricks Configuration
- **Workspace**: https://your-workspace.cloud.databricks.com
- **Authentication**: [OAuth/PAT/Profile name]
- **Deployment Strategy**: [Standalone/Asset Bundle]
- **Development Pattern**: [Notebook-first/Local-first/Hybrid]

## Project Structure
[Based on analysis from Phase 3]

## Common Commands for This Project
```bash
# Development commands specific to your setup
```

## Safety Settings for This Project
[Specific considerations based on your workspace and project type]
```

### Step 4.2: Create .env.local Template (if needed)
```bash
# Create environment template
cat > .env.local.template << 'EOF'
# Databricks Configuration
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi...  # Optional - use OAuth instead

# Project-specific settings
DATABRICKS_CLUSTER_ID=your-cluster-id  # Optional
DATABRICKS_WAREHOUSE_ID=your-warehouse-id  # Optional
EOF

# Add to .gitignore
echo ".env.local" >> .gitignore
```

**✅ Phase 4 Complete When**:
- [ ] CLAUDE.md updated with workspace context
- [ ] Environment template created (if needed)
- [ ] Project-specific documentation added

---

## ✅ Phase 5: Validation & Testing

### Step 5.1: End-to-End Test
Let's verify everything works together:

```bash
# Test 1: Basic CLI functionality
databricks workspace list / | head -5

# Test 2: Upload a test file
echo "print('Hello from Databricks!')" > test_upload.py
databricks workspace upload test_upload.py /Workspace/Shared/test_claude_setup.py

# Test 3: Download it back
databricks workspace download /Workspace/Shared/test_claude_setup.py downloaded_test.py

# Test 4: Clean up
rm test_upload.py downloaded_test.py
databricks workspace delete /Workspace/Shared/test_claude_setup.py
```

### Step 5.2: Test Specific Deployment Pattern

**If Standalone**:
```bash
# Test notebook upload (if you have notebooks)
# databricks workspace upload your_notebook.ipynb /Users/your-email/test_notebook.ipynb --format JUPYTER
```

**If Asset Bundle**:
```bash
# Test bundle validation
databricks bundle validate

# Test bundle deployment (to dev environment)
# databricks bundle deploy --target dev
```

### Step 5.3: Verify AI Tool Integration
Test that AI tools can use your setup:

```bash
# Check that dbx_ai_docs is accessible
ls dbx_ai_docs/

# Verify AI commands are available
ls .claude/commands/
```

**✅ Phase 5 Complete When**:
- [ ] End-to-end test passes
- [ ] Deployment pattern validated
- [ ] AI tool integration confirmed

---

## 🎉 Setup Complete!

### Summary of Configuration
- **Databricks Workspace**: [Configured workspace URL]
- **Authentication**: [Method used]
- **Deployment Strategy**: [Standalone/Asset Bundle]
- **Development Pattern**: [Selected approach]

### Next Steps
1. Start developing with your chosen pattern
2. Use the comprehensive documentation in `dbx_ai_docs/`
3. Run `/docs <url>` to add documentation for additional libraries
4. Follow the safety guidelines in `dbx_ai_docs/safety-guidelines.md`

### Troubleshooting
If you encounter issues:
1. Run `databricks auth describe` to check authentication
2. Check `dbx_ai_docs/cli-auth.md` for authentication troubleshooting
3. Review `dbx_ai_docs/safety-guidelines.md` for operational guidance

### 🚨 Important Security Notes
- Never commit authentication tokens to version control
- Use `.env.local` for sensitive configuration
- Follow least-privilege access patterns
- Review operations in `dbx_ai_docs/safety-guidelines.md` before destructive actions