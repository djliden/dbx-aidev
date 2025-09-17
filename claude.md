# Claude CLI App Template

This is a template for building Typer CLI applications with the help of Claude.

> **Note for Claude:** For template development tasks (modifying this template itself), refer to `claude_dev.md` instead of this file.

## Implementation Guidance

When implementing features for projects using this template:
- **docs/product.md** - Contains product requirements, user stories, and feature specifications
- **docs/design.md** - Contains technical design decisions, architecture patterns, and implementation guidelines

Reference these documents for context on what to build and how to build it before implementing new features.

## Tech Stack

**Core Framework:**
- **Python 3.8+** - Modern Python with type hints
- **Typer** - CLI framework with automatic help generation
- **Pydantic v2** - Data validation, settings, and configuration management
- **Rich** - Rich text and beautiful formatting for CLI output
- **uv** - Fast Python package manager and project management

**Development Tools:**
- **Pytest** - Testing framework with CliRunner for CLI testing
- **Ruff** - Lightning-fast Python linter and formatter
- **Pre-commit** - Git hooks for code quality (optional)

**Common Integrations:**
- **httpx** - Modern async HTTP client for API integrations  
- **SQLite/PostgreSQL** - Database integration via `src/services/`
- **aiofiles** - Async file operations
- **structlog** - Structured logging for better debugging

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
./scripts/setup.sh                    # Interactive environment setup
uv sync                               # Sync dependencies

# CLI Development  
uv run python app.py --help           # Test CLI functionality
uv run python app.py [command]        # Run specific command
./app_status.sh                       # Check project status quickly
./app_status.sh -v                    # Verbose status with details

# Testing & Quality
./scripts/test.sh                     # Run full test suite
uv run pytest tests/test_hello.py -v  # Run specific command tests
uv run ruff check src/               # Lint code
uv run ruff format src/              # Format code

# Development Iteration
uv run python app.py [cmd] [args]     # Quick CLI testing
./app_status.sh                       # Fast status check (no slow tests)
```

### 🚨 CRITICAL: Development Rules
1. **CLI Testing**: Always test commands via `uv run python app.py` before committing
2. **Test Coverage**: Every command file MUST have a corresponding test file
3. **Status Checks**: Run `./app_status.sh` frequently to catch missing tests
4. **Dependencies**: Only add dependencies via `uv add` - never manual pyproject.toml edits
5. **Code Quality**: Format with `uv run ruff format` before committing

## CLI Structure

This template follows the **one-file-per-command** approach recommended by Typer:

**Project Architecture:**
```
src/
├── cli/              # CLI interface layer only
│   ├── cli.py        # Main CLI app and command registration
│   └── commands/     # Individual command implementations
│       ├── __init__.py
│       ├── hello.py  # Thin CLI wrapper - calls src.core functions
│       └── goodbye.py
├── core/             # Core business logic and application services
├── models/           # Data models, schemas, domain objects
├── services/         # Database management, external APIs, AI agents
└── utils/            # Shared utility functions

tests/
├── test_hello.py     # CLI command tests
├── test_goodbye.py
├── test_core/        # Core business logic tests
└── test_models/      # Data model tests
```

**Key Principle:** CLI commands should be **thin interface layers** that parse arguments and call core business logic.

**Adding New Commands:**
1. Create `src/cli/commands/mycommand.py` with command function
2. Import and register in `src/cli/cli.py`
3. Create `tests/test_mycommand.py` with tests
4. Run `./app_status.sh` to verify test coverage

### Testing Your CLI
This template includes a robust testing setup with **one test file per command**:

**Running Tests:**
```bash
./scripts/test.sh              # Run all tests
uv run pytest tests/ -v        # Run tests with verbose output
uv run pytest tests/test_hello.py  # Run tests for specific command
```

**Writing Tests:**
Each command should have a corresponding test file. Use `CliRunner` to test CLI commands:

```python
from typer.testing import CliRunner
from src.cli.cli import app

runner = CliRunner()

def test_my_command():
    result = runner.invoke(app, ['my-command', '--arg', 'value'])
    assert result.exit_code == 0
    assert 'expected output' in result.output
```

**Test Coverage Verification:**
- `./app_status.sh` checks that every command file has a corresponding test file
- Status warns about missing test files without running slow tests
- Run `./scripts/test.sh` when you want to actually execute tests

### Claude Natural Language Commands
Claude understands natural language commands for common development tasks:

**Development:**
- "add a new command called X that does Y" - Creates new command file and registers it
- "add a parameter --flag to the existing command"
- "run the cli with arguments: hello world"

**Testing (Automated):**
- Claude will automatically create test files when adding new commands
- "write tests for the new command" - Adds comprehensive test coverage
- "test that invalid arguments show an error"
- "run the test suite and fix any failures"

**Examples:**
- "I want to add a 'list' command that shows files in a directory"
  → Creates `src/cli/commands/list.py` and `tests/test_list.py`
- "Add a --verbose flag to the list command"
- "Test the list command with different directory arguments"

## Reference Documentation

For quick access to framework and library information, this project maintains focused reference docs in `/docs/`:

### Existing References
- `typer-reference.md` - Complete Typer CLI patterns and syntax  
- `typer-urls.md` - Official Typer documentation navigation

### Documentation Naming Convention
- `{library}-reference.md` - Claude's quick reference with essential concepts and code examples
- `{library}-urls.md` - Navigation guide with links to official docs and search strategies

### Adding New Documentation
Use the `/docs` command to create focused reference documentation:
```bash
/docs https://docs.pydantic.dev    # Creates pydantic-reference.md and pydantic-urls.md
/docs https://rich.readthedocs.io  # Creates rich-reference.md and rich-urls.md
```

The command analyzes documentation and creates Claude-friendly references tailored to this project's Python CLI development context.

## Modern Python CLI Development

### Modern Configuration with Pydantic
```python
# src/models/config.py
from pydantic import BaseModel, Field
from pathlib import Path

class AppConfig(BaseModel):
    """App config with validation and env var support."""
    data_dir: Path = Field(default_factory=lambda: Path.home() / ".myapp")
    api_key: str = Field(default="", env="MY_APP_API_KEY")
    debug: bool = Field(default=False, env="DEBUG")
    max_retries: int = Field(default=3, ge=0, le=10)
```

### Async Operations & Type Safety
```python
# Modern async CLI command with full type hints
from typing import Annotated
import asyncio
import httpx
from enum import Enum

class OutputFormat(str, Enum):
    json = "json"
    yaml = "yaml"

async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

def fetch_command(
    url: Annotated[str, typer.Argument(help="API URL to fetch")],
    format: OutputFormat = OutputFormat.json
):
    """Fetch data asynchronously with type safety."""
    result = asyncio.run(fetch_data(url))
    console.print(f"✅ Fetched data in {format.value} format")
```