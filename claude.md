# Databricks AI Development Setup Tool (`dbx-aidev`)

This project provides the `dbai` command for setting up Databricks AI development scaffolding that enables AI tools like Claude Code to effectively work with Databricks CLI and SDK operations.

## Project Overview

**Package:** `dbx-aidev`
**Command:** `dbai`
**Purpose:** Generate static documentation and AI command structures for Databricks development

## Implementation Guidance

For understanding the project architecture and requirements:
- **docs/product.md** - Product requirements and user workflows
- **docs/design.md** - Technical architecture and minimal scaffolding approach
- **PROJECT_SPEC.md** - Original project specification

The tool follows a **minimal static scaffolding** approach - generating comprehensive documentation without performing dynamic operations.

## Tech Stack

**Core Framework:**
- **Python 3.11+** - Modern Python with type hints
- **Typer** - CLI framework with automatic help generation
- **Rich** - Rich text and beautiful formatting for CLI output
- **uv** - Fast Python package manager and project management

**Development Tools:**
- **Pytest** - Testing framework with CliRunner for CLI testing
- **Ruff** - Lightning-fast Python linter and formatter

**Target Integration:**
- **Databricks CLI** - Comprehensive command reference documentation
- **Databricks SDK** - Python SDK patterns and authentication
- **Claude Code** - AI tool integration through static documentation

## Development Workflow

### Package Management
**🚨 CRITICAL: Always use `uv` for dependency management**
- `uv add package-name` - Add production dependency
- `uv add --dev package-name` - Add development dependency  
- `uv remove package-name` - Remove dependency
- `uv sync` - Install all dependencies from lock file
- **NEVER** manually edit `pyproject.toml` dependencies - always use `uv add`

### Core Development Commands
```bash
# Environment Setup
uv sync                               # Sync dependencies

# CLI Development
uv run python app.py --help           # Test CLI functionality
uv run python app.py dbai             # Run the main dbai command
./app_status.sh                       # Check project status quickly

# Testing & Quality
./scripts/test.sh                     # Run full test suite
uv run pytest tests/test_dbai.py -v   # Run dbai command tests
uv run ruff check src/               # Lint code
uv run ruff format src/              # Format code

# Development Iteration
uv run python app.py dbai             # Test scaffolding generation
./app_status.sh                       # Fast status check
```

### 🚨 CRITICAL: Development Rules
1. **CLI Testing**: Always test commands via `uv run python app.py dbai` before committing
2. **Template Testing**: Verify generated documentation structure and content
3. **Status Checks**: Run `./app_status.sh` to catch missing tests
4. **Dependencies**: Only add dependencies via `uv add` - never manual pyproject.toml edits
5. **Code Quality**: Format with `uv run ruff format` before committing

## CLI Structure

The project implements a single main command `dbai` for scaffolding generation:

**Project Architecture:**
```
src/
├── cli/              # CLI interface layer
│   ├── cli.py        # Main CLI app and command registration
│   └── commands/     # Command implementations
│       ├── __init__.py
│       └── dbai.py   # Main scaffolding command

templates/            # Static template files
├── CLAUDE.md         # Generated project CLAUDE.md template
├── dbx_ai_docs/      # Databricks documentation templates
│   ├── cli-overview.md
│   ├── cli-workspace.md
│   ├── cli-compute.md
│   ├── cli-jobs.md
│   ├── cli-auth.md
│   ├── cli-dev-tools.md
│   ├── authentication.md
│   └── safety-guidelines.md
└── .claude/
    └── commands/
        ├── dbx-setup.md  # AI setup workflow
        └── docs.md       # Documentation generator

tests/
└── test_dbai.py      # Main command tests
```

**Key Principle:** Simple template-based file copying for static scaffolding generation.

**Generated Structure:**
When `dbai` runs, it creates:
- `CLAUDE.md` - Project overview pointing to documentation
- `dbx_ai_docs/` - Comprehensive Databricks CLI/SDK documentation
- `.claude/commands/dbx-setup.md` - AI-driven setup workflow

### Testing the CLI

The project includes testing for the main `dbai` scaffolding command:

**Running Tests:**
```bash
./scripts/test.sh              # Run all tests
uv run pytest tests/ -v        # Run tests with verbose output
uv run pytest tests/test_dbai.py  # Run tests for dbai command
```

**Test Structure:**
Tests verify the scaffolding generation functionality:

```python
from typer.testing import CliRunner
from src.cli.cli import app

runner = CliRunner()

def test_dbai_command():
    result = runner.invoke(app, ['dbai'])
    assert result.exit_code == 0
    assert 'Databricks AI documentation scaffolding created!' in result.output
```

**Testing Strategy:**
- **Unit Tests**: File creation and template copying logic
- **Integration Tests**: Verify complete scaffolding generation
- **Manual Testing**: AI tool integration with generated documentation

### AI Tool Integration

This project is designed to work seamlessly with AI development tools:

**Generated Documentation:**
- **`dbx_ai_docs/`**: Modular Databricks CLI and SDK documentation optimized for AI tool consumption
- **Token-efficient structure**: Files sized for optimal AI tool processing
- **Clear entry points**: `cli-overview.md` provides navigation for AI tools
- **Comprehensive coverage**: All major Databricks CLI command groups documented

**AI Commands:**
- **`/dbx-setup`**: Complete setup workflow for AI tools to guide users through authentication and configuration
- **`/docs`**: Generate focused reference documentation for additional libraries (e.g., LangChain, custom packages)
- **Safety guidelines**: Built-in risk classification and confirmation patterns
- **Deployment strategies**: Clear guidance on standalone vs asset bundle approaches

**Development Workflow:**
1. Run `dbai` in any directory to create scaffolding
2. AI tools gain immediate access to comprehensive Databricks documentation
3. Use `/dbx-setup` to complete project-specific configuration
4. Use `/docs <url>` to add documentation for additional libraries as needed
5. AI tools can effectively use Databricks CLI and SDK operations

## Template System

The tool uses a static template approach for modularity:

**Current Templates:**
- **Standard**: Comprehensive Databricks CLI/SDK documentation (default)
- **Templates directory**: `templates/` contains all static files

**Future Modularity:**
- Multiple template options (`--template minimal`, `--template ml-focused`)
- Extensible template system for different use cases
- Custom organization patterns based on team preferences

## Usage Examples

### Basic Usage
```bash
# Install the tool
pip install dbx-aidev

# Navigate to any directory
cd my-project/

# Generate Databricks AI development scaffolding
dbai

# Files created:
# ├── CLAUDE.md                    # Project overview
# ├── dbx_ai_docs/                 # Comprehensive Databricks docs
# └── .claude/commands/dbx-setup.md # AI setup workflow
```

### AI Tool Workflow
```bash
# After running dbai, AI tools can:
# 1. Read comprehensive Databricks CLI documentation from dbx_ai_docs/
# 2. Use /dbx-setup command to guide user through configuration
# 3. Effectively use Databricks CLI and SDK operations with safety guidelines
```

### Development Workflow
```bash
# For contributors to this tool:
uv sync                           # Install dependencies
uv run python app.py dbai         # Test the command
./app_status.sh                   # Check project status
uv run ruff format src/           # Format code
```