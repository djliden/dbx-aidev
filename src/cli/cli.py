"""Main CLI application for dbx-aidev tool."""

import typer

from .commands.dbai import dbai

app = typer.Typer()

# Register main command as the default function
app.callback(invoke_without_command=True)(dbai)

if __name__ == '__main__':
  app()
