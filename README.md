# Databricks AI Development Setup Tool (`dbx-aidev`)

A CLI tool that creates comprehensive Databricks development scaffolding optimized for AI tools like Claude Code. Generates static documentation, AI commands, and safety guidelines to enable effective Databricks CLI and SDK operations.

## 🚀 Quick Start

### Installation

**Option 1: Install with uv (Recommended)**
```bash
# Install directly from GitHub
uv tool install git+https://github.com/djliden/dbx-aidev.git

# Use the tool
dbai
```

**Option 2: Clone and Install Locally**
```bash
# Clone repository
git clone https://github.com/djliden/dbx-aidev.git
cd dbx-aidev

# Install with uv
uv tool install .

# Use the tool
dbai
```

**Option 3: Development Installation**
```bash
# Clone repository
git clone https://github.com/djliden/dbx-aidev.git
cd dbx-aidev

# Install dependencies
uv sync

# Run directly
uv run python app.py dbai
```

### Basic Usage

```bash
# Navigate to any directory (existing project or new folder)
cd my-databricks-project/

# Generate Databricks AI development scaffolding
dbai

# Files created:
# ├── CLAUDE.md                    # Project overview
# ├── dbx_ai_docs/                 # Comprehensive Databricks docs
# │   ├── cli-overview.md          # Entry point for AI tools
# │   ├── cli-workspace.md         # File operations
# │   ├── cli-compute.md           # Clusters and warehouses
# │   ├── cli-jobs.md              # Job management
# │   ├── cli-auth.md              # Authentication
# │   ├── cli-dev-tools.md         # Asset bundles and sync
# │   ├── authentication.md       # SDK patterns
# │   └── safety-guidelines.md     # Security best practices
# └── .claude/commands/
#     ├── dbx-setup.md             # Interactive setup wizard
#     └── docs.md                  # Documentation generator
```

## 🎯 What This Tool Does

**Primary Purpose**: Enable AI tools like Claude Code to effectively work with Databricks by providing:

1. **Comprehensive CLI Documentation**: Modular, token-efficient docs covering all major Databricks CLI command groups
2. **AI Setup Workflows**: Step-by-step interactive commands for authentication and project configuration
3. **Safety Guidelines**: Risk classification and best practices for Databricks operations
4. **SDK Integration Patterns**: Authentication and common usage patterns for the Databricks SDK

## 🤖 AI Tool Integration

After running `dbai`, AI tools gain access to:

### Core AI Commands
- **`/dbx-setup`**: Interactive 5-phase setup wizard covering:
  - Environment & CLI setup
  - Authentication configuration (OAuth/PAT/profiles)
  - Project analysis & deployment strategy
  - Documentation enhancement
  - End-to-end validation & testing

- **`/docs <url>`**: Generate focused documentation for additional libraries:
  ```bash
  /docs https://docs.langchain.com      # Add LangChain reference
  /docs https://docs.pydantic.dev       # Add Pydantic patterns
  /docs https://huggingface.co/docs     # Add HuggingFace integration
  ```

### Documentation Structure
- **`cli-overview.md`**: Entry point explaining CLI structure and help patterns
- **Command group docs**: Focused files for workspace, compute, jobs, auth, etc.
- **Safety guidelines**: Risk classification with confirmation patterns
- **SDK patterns**: Authentication and common operations

## 🔧 Features

### Static Scaffolding Approach
- **Zero dependencies**: No Databricks CLI or workspace access required to run
- **Pure documentation generation**: AI tools handle all dynamic operations
- **Template-based**: Consistent, maintainable file generation
- **Modular structure**: Token-efficient organization for AI tool consumption

### Comprehensive Coverage
- **All major CLI command groups**: workspace, clusters, jobs, auth, dev tools
- **Safety classifications**: Low/medium/high risk operation guidelines
- **Multiple deployment strategies**: Standalone notebooks vs Asset Bundles
- **Authentication methods**: OAuth, PAT, profiles, environment variables

### AI-Optimized Design
- **Clear entry points**: AI tools know where to start (`cli-overview.md`)
- **Token efficiency**: Files sized for optimal AI tool processing
- **Cross-references**: Linked documentation for related operations
- **Example-driven**: Actionable code patterns throughout

## 📋 Use Cases

- **Data Scientists**: AI-assisted notebook development with Databricks deployment
- **ML Engineers**: Pipeline development with comprehensive CLI and SDK coverage
- **Analytics Engineers**: Data transformation workflows with safety guidelines
- **Teams**: Consistent Databricks development patterns across projects

## 🛡️ Safety & Security

The tool emphasizes safe Databricks operations:
- **Risk classification**: Clear guidance on low/medium/high risk operations
- **Confirmation patterns**: Templates for destructive operation safeguards
- **Permission validation**: Approaches for checking access before operations
- **Least privilege**: Guidelines for minimal permission access patterns

## 🔄 Development Workflow

1. **Setup**: Run `dbai` to create scaffolding
2. **Configure**: Use `/dbx-setup` for workspace-specific configuration
3. **Extend**: Use `/docs` to add documentation for additional libraries
4. **Develop**: AI tools leverage comprehensive documentation for effective Databricks operations

## 📊 Project Structure

```
dbx-aidev/
├── src/cli/                     # CLI implementation
│   ├── cli.py                   # Main CLI app
│   └── commands/dbai.py         # Core scaffolding command
├── templates/                   # Static template files
│   ├── CLAUDE.md                # Project overview template
│   ├── dbx_ai_docs/             # Databricks documentation
│   └── .claude/commands/        # AI command specifications
├── tests/                       # Test suite
└── docs/                        # Project documentation
```

## 🏗️ Future Enhancements

- **Multiple templates**: Minimal, ML-focused, enterprise variants
- **Template combinations**: Mix and match documentation modules
- **Custom templates**: Support for organization-specific patterns
- **Enhanced validation**: More comprehensive setup testing

---

Built for seamless integration with AI development tools and inspired by the [Databricks App Template](https://github.com/databricks-solutions/claude-databricks-app-template) approach.
