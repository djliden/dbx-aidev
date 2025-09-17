"""Hello command implementation."""

import typer
from rich.console import Console

console = Console()


def hello(name: str):
    """Say hello to NAME."""
    console.print(f'Hello {name}')