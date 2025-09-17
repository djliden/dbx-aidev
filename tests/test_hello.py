"""Tests for hello command."""

from typer.testing import CliRunner

from src.cli.cli import app

runner = CliRunner()


def test_hello_command():
    """Test the hello command."""
    result = runner.invoke(app, ['hello', 'World'])
    assert result.exit_code == 0
    assert 'Hello World' in result.output


def test_hello_help():
    """Test the hello command help."""
    result = runner.invoke(app, ['hello', '--help'])
    assert result.exit_code == 0
    assert 'Say hello to NAME' in result.output