"""Tests for goodbye command."""

from typer.testing import CliRunner

from src.cli.cli import app

runner = CliRunner()


def test_goodbye_command():
    """Test the goodbye command."""
    result = runner.invoke(app, ['goodbye', 'World'])
    assert result.exit_code == 0
    assert 'Bye World!' in result.output


def test_goodbye_formal():
    """Test the goodbye command with formal flag."""
    result = runner.invoke(app, ['goodbye', 'World', '--formal'])
    assert result.exit_code == 0
    assert 'Goodbye World. It was a pleasure.' in result.output


def test_goodbye_help():
    """Test the goodbye command help."""
    result = runner.invoke(app, ['goodbye', '--help'])
    assert result.exit_code == 0
    assert 'Say goodbye to NAME' in result.output