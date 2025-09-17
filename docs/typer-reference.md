# Typer Quick Reference

This is a comprehensive reference for building CLI applications with Typer. Use this for quick lookup of patterns and syntax.

## Core Application Structure

### Basic App
```python
import typer

def main(name: str):
    print(f"Hello {name}")

if __name__ == "__main__":
    typer.run(main)
```

### Multi-Command App
```python
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    print(f"Creating {name}")

@app.command()  
def delete(name: str):
    print(f"Deleting {name}")

if __name__ == "__main__":
    app()
```

## Arguments vs Options

### Arguments (Positional, Required)
```python
def main(name: str):  # Required
    pass

def main(name: str = "World"):  # Optional with default
    pass

def main(name: Annotated[str, typer.Argument(help="Name to greet")] = "World"):
    pass
```

### Options (Flag-based, Optional)
```python
def main(name: str, lastname: str = ""):  # --lastname optional
    pass

def main(name: str, formal: bool = False):  # --formal flag
    pass

def main(name: str, count: int = typer.Option(1, "--count", "-c")):
    pass
```

## Type System & Validation

### Enums for Choices
```python
from enum import Enum

class OutputFormat(str, Enum):
    json = "json"
    yaml = "yaml" 
    table = "table"

def export(format: OutputFormat = OutputFormat.json):
    print(f"Exporting in {format.value} format")
```

### Path Validation
```python
from pathlib import Path

def process_file(
    file: Annotated[Path, typer.Argument(
        exists=True,          # File must exist
        file_okay=True,       # Allow files
        dir_okay=False,       # Disallow directories  
        readable=True,        # Must be readable
        resolve_path=True     # Convert to absolute path
    )]
):
    print(f"Processing {file}")
```

### DateTime Parameters
```python
from datetime import datetime

def schedule(
    when: Annotated[datetime, typer.Argument(
        formats=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y"]
    )]
):
    print(f"Scheduled for {when}")
```

## Advanced Parameter Patterns

### Required Options
```python
def main(name: str, token: Annotated[str, typer.Option()]):  # Required option
    pass

def main(name: str, token: str = typer.Option(...)):  # Required using Ellipsis
    pass
```

### Multiple Values
```python
def main(
    names: Annotated[list[str], typer.Option()] = None,  # --names value1 --names value2
    files: Annotated[list[Path], typer.Argument()] = None  # file1.txt file2.txt
):
    pass
```

### Environment Variables
```python
def main(
    token: Annotated[str, typer.Option(envvar="API_TOKEN")] = ""
):
    pass
```

## Command Organization

### One-File-Per-Command Pattern
```python
# src/cli/cli.py
import typer
from .commands.users import app as users_app
from .commands.files import app as files_app

app = typer.Typer()
app.add_typer(users_app, name="users")
app.add_typer(files_app, name="files")

# Or register individual commands
from .commands.hello import hello
app.command()(hello)
```

### Individual Command File
```python
# src/cli/commands/hello.py
import typer
from rich.console import Console

console = Console()

def hello(
    name: Annotated[str, typer.Argument(help="Name to greet")],
    formal: bool = typer.Option(False, "--formal", help="Use formal greeting")
):
    """Say hello to NAME."""
    if formal:
        console.print(f"Good day, {name}!")
    else:
        console.print(f"Hello {name}!")
```

### Subcommands
```python
# Creates nested commands like: mycli users create
users_app = typer.Typer()

@users_app.command()
def create(name: str):
    print(f"Creating user {name}")

@users_app.command()
def delete(name: str):
    print(f"Deleting user {name}")

# Add to main app
app.add_typer(users_app, name="users")
```

## Interactive Features

### Prompts
```python
def main():
    name = typer.prompt("What's your name?")
    password = typer.prompt("Password", hide_input=True)
    delete = typer.confirm("Are you sure?")
    
    if delete:
        typer.confirm("Really delete?", abort=True)  # Exits if no
```

### Progress Bars
```python
import time
from rich.progress import track

def process():
    # Rich progress (recommended)
    for item in track(range(100), description="Processing..."):
        time.sleep(0.01)
    
    # Typer progress
    with typer.progressbar(range(100), label="Processing") as progress:
        for item in progress:
            time.sleep(0.01)
```

## Output & User Experience

### Rich Integration
```python
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

def display_data(data):
    # Rich console
    console.print("Hello", style="bold red")
    
    # Rich print
    rprint("[bold red]Alert![/bold red]")
    
    # Tables
    table = Table()
    table.add_column("Name")
    table.add_column("Age")
    table.add_row("Alice", "25")
    console.print(table)
```

### Colors and Styling
```python
def main():
    # Typer styling
    typer.secho("Hello", fg=typer.colors.GREEN, bold=True)
    styled = typer.style("World", fg=typer.colors.BLUE)
    print(styled)
    
    # Rich styling (preferred)
    console.print("Hello [bold green]World[/bold green]!")
```

## Error Handling & Exit

### Clean Exits
```python
def main(name: str):
    if not name:
        typer.echo("Name is required", err=True)
        raise typer.Exit(1)
    
    if name == "forbidden":
        raise typer.Abort()  # Exit with code 1
    
    print(f"Hello {name}")
```

### Exception Handling
```python
# Pretty exceptions (with Rich installed)
app = typer.Typer(pretty_exceptions_enable=True)

# Security: hide local variables
app = typer.Typer(pretty_exceptions_show_locals=False)
```

## Configuration & Data

### App Directory
```python
from pathlib import Path

def get_config():
    app_dir = typer.get_app_dir("my-cli-app")
    config_path = Path(app_dir) / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    return config_path
```

### Opening Files/URLs
```python
def main():
    typer.launch("https://example.com")  # Opens in browser
    typer.launch("/path/to/file.txt", locate=True)  # Opens file location
```

## Testing Patterns

### Basic Test Structure
```python
from typer.testing import CliRunner
from src.cli.cli import app

runner = CliRunner()

def test_command():
    result = runner.invoke(app, ["hello", "World"])
    assert result.exit_code == 0
    assert "Hello World" in result.output

def test_command_with_options():
    result = runner.invoke(app, ["hello", "World", "--formal"])
    assert result.exit_code == 0
    assert "Good day" in result.output

def test_command_help():
    result = runner.invoke(app, ["hello", "--help"])
    assert result.exit_code == 0
    assert "Say hello" in result.output
```

### Testing Interactive Input
```python
def test_with_prompt():
    result = runner.invoke(app, ["create"], input="test-name\ny\n")
    assert result.exit_code == 0
    assert "Created test-name" in result.output
```

### Testing Functions Without App
```python
def test_function_directly():
    app = typer.Typer()
    app.command()(main_function)
    
    result = runner.invoke(app, ["arg1", "--option", "value"])
    assert result.exit_code == 0
```

## Common Patterns

### Version Command
```python
import typer
from . import __version__

def version_callback(value: bool):
    if value:
        typer.echo(f"My CLI Version: {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[bool, typer.Option("--version", callback=version_callback)] = False
):
    pass
```

### Context and Callbacks
```python
def name_callback(value: str):
    if value != value.lower():
        raise typer.BadParameter("Name must be lowercase")
    return value

def main(
    name: Annotated[str, typer.Option(callback=name_callback)]
):
    pass
```

### Help Panels (Rich)
```python
def main(
    debug: Annotated[bool, typer.Option(
        help="Enable debug mode",
        rich_help_panel="Developer Options"
    )] = False
):
    pass
```

## Modern Type Annotations

### With Annotated (Python 3.9+)
```python
from typing import Annotated

def main(
    name: Annotated[str, typer.Argument(help="Name to process")],
    count: Annotated[int, typer.Option("--count", "-c", help="Number of times")] = 1,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False
):
    pass
```

### Legacy Syntax (Python 3.8)
```python
def main(
    name: str = typer.Argument(..., help="Name to process"),
    count: int = typer.Option(1, "--count", "-c", help="Number of times"),
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    pass
```