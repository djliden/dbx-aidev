# Claude CLI App Template

A minimal template for building Python CLI apps with Typer and Claude.

## Quick Start

1. **Use this template:**
   - Click "Use this template" on GitHub to create your new repo
   - Clone your new repo locally

2. **Start development with Claude:**
   ```bash
   # In Claude Code
   /cli
   ```

The `/cli` command handles setup and provides an interactive walkthrough to scope and build your CLI application.

## For Claude: Reference Documentation

When developing with this template, refer to the comprehensive guides in the `docs/` directory:
- **`docs/typer-reference.md`**: Complete Typer patterns and syntax reference
- **`docs/typer-urls.md`**: Documentation navigation and search strategies
- **`CLAUDE.md`**: Project context and development workflow

### Adding New Documentation

Use the `/docs` command to create focused reference documentation for new libraries:
```bash
/docs https://docs.pydantic.dev    # Creates pydantic-reference.md and pydantic-urls.md
/docs https://rich.readthedocs.io  # Creates rich-reference.md and rich-urls.md

# Add specific instructions for focused documentation
/docs https://mlflow.org/docs/latest please focus on mlflow tracing
/docs https://docs.pydantic.dev I need validators and custom field types
```

This creates Claude-friendly references following the naming convention:
- `{library}-reference.md`: Essential concepts and code examples
- `{library}-urls.md`: Navigation guide for official documentation

## What's included

- 🔧 **Typer**: Modern CLI framework
- 🎨 **Rich**: Beautiful terminal output
- ⚡ **uv**: Fast Python package management
- 📁 **Project structure**: Organized and ready to extend
- 🛠️ **Development tools**: Linting, formatting with Ruff

Built with inspiration from [claude-databricks-app-template](https://github.com/databricks-solutions/claude-databricks-app-template).
