"""Tests for the dbai command."""

import tempfile
from pathlib import Path

from typer.testing import CliRunner

from src.cli.cli import app

runner = CliRunner()


def test_dbai_command_creates_scaffolding():
    """Test that dbai command creates the expected file structure."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory for test
        original_cwd = Path.cwd()
        temp_path = Path(temp_dir)

        try:
            import os
            os.chdir(temp_path)

            # Run the main command
            result = runner.invoke(app, [])

            # Check command succeeded
            assert result.exit_code == 0
            assert 'Databricks AI documentation scaffolding created!' in result.output

            # Check that expected files were created
            assert (temp_path / 'CLAUDE.md').exists()
            assert (temp_path / 'dbx_ai_docs').is_dir()
            assert (temp_path / '.claude' / 'commands' / 'dbx-setup.md').exists()
            assert (temp_path / '.claude' / 'commands' / 'docs.md').exists()

            # Check some documentation files were created
            assert (temp_path / 'dbx_ai_docs' / 'cli-overview.md').exists()
            assert (temp_path / 'dbx_ai_docs' / 'cli-workspace.md').exists()
            assert (temp_path / 'dbx_ai_docs' / 'safety-guidelines.md').exists()

        finally:
            os.chdir(original_cwd)


def test_dbai_command_skips_existing_files():
    """Test that dbai command skips files that already exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = Path.cwd()
        temp_path = Path(temp_dir)

        try:
            import os
            os.chdir(temp_path)

            # Create a CLAUDE.md file that already exists
            (temp_path / 'CLAUDE.md').write_text('# Existing file')

            # Run the main command
            result = runner.invoke(app, [])

            # Check command succeeded
            assert result.exit_code == 0
            assert 'CLAUDE.md already exists, skipping...' in result.output

            # Check that existing file wasn't overwritten
            assert (temp_path / 'CLAUDE.md').read_text() == '# Existing file'

            # But other files should still be created
            assert (temp_path / 'dbx_ai_docs').is_dir()
            assert (temp_path / '.claude' / 'commands' / 'dbx-setup.md').exists()
            assert (temp_path / '.claude' / 'commands' / 'docs.md').exists()

        finally:
            os.chdir(original_cwd)


def test_dbai_command_output_messages():
    """Test that dbai command produces expected output messages."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = Path.cwd()
        temp_path = Path(temp_dir)

        try:
            import os
            os.chdir(temp_path)

            result = runner.invoke(app, [])

            # Check for expected output messages
            assert 'Copying template files...' in result.output
            assert 'Documentation: dbx_ai_docs/' in result.output
            assert 'Project overview: CLAUDE.md' in result.output
            assert 'AI commands: .claude/commands/' in result.output
            assert 'Next step: Run `/dbx-setup`' in result.output

        finally:
            os.chdir(original_cwd)


def test_dbai_command_help():
    """Test that dbai command help works."""
    result = runner.invoke(app, ['--help'])

    assert result.exit_code == 0
    assert 'Create Databricks AI development documentation scaffolding' in result.output
    assert 'This command generates static documentation' in result.output