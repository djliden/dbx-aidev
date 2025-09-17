import typer

from .commands.hello import hello
from .commands.goodbye import goodbye

app = typer.Typer()

# Register commands
app.command()(hello)
app.command()(goodbye)

if __name__ == '__main__':
    app()