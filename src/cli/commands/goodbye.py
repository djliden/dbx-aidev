"""Goodbye command implementation."""

import typer
from rich.console import Console

console = Console()


def goodbye(name: str, formal: bool = False):
    """Say goodbye to NAME."""
    if formal:
        console.print(f'Goodbye {name}. It was a pleasure.')
    else:
        console.print(f'Bye {name}!')