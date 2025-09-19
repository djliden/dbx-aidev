"""Tests for the dbai command."""

import tempfile
from pathlib import Path
from unittest.mock import patch

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


def test_dbai_command_interactive_prompts_decline_all():
  """Test that dbai command handles declining all interactive prompts."""
  with tempfile.TemporaryDirectory() as temp_dir:
    original_cwd = Path.cwd()
    temp_path = Path(temp_dir)

    try:
      import os

      os.chdir(temp_path)

      # Create existing files
      (temp_path / 'CLAUDE.md').write_text('# Existing file')
      (temp_path / 'dbx_ai_docs').mkdir()
      (temp_path / '.claude' / 'commands').mkdir(parents=True)
      (temp_path / '.claude' / 'commands' / 'custom.md').write_text('# Custom command')

      # Mock all prompts to return False
      with patch('src.cli.commands.dbai.Confirm.ask') as mock_confirm:
        mock_confirm.return_value = False

        result = runner.invoke(app, [])

        # Check command succeeded
        assert result.exit_code == 0
        assert 'CLAUDE.md already exists, skipping...' in result.output
        assert 'dbx_ai_docs/ already exists, skipping...' in result.output
        assert '.claude/commands/ already exists, skipping...' in result.output

        # Check that existing files weren't modified
        assert (temp_path / 'CLAUDE.md').read_text() == '# Existing file'
        assert not (temp_path / 'dbx_ai_docs' / 'cli-overview.md').exists()
        assert not (temp_path / '.claude' / 'commands' / 'dbx-setup.md').exists()
        assert (temp_path / '.claude' / 'commands' / 'custom.md').read_text() == '# Custom command'

    finally:
      os.chdir(original_cwd)


def test_dbai_command_claude_md_append():
  """Test that dbai command appends to existing CLAUDE.md when accepted."""
  with tempfile.TemporaryDirectory() as temp_dir:
    original_cwd = Path.cwd()
    temp_path = Path(temp_dir)

    try:
      import os

      os.chdir(temp_path)

      # Create existing CLAUDE.md without Databricks content
      original_content = '# My Project\n\nThis is my existing project.'
      (temp_path / 'CLAUDE.md').write_text(original_content)

      # Mock the Confirm.ask to return True for CLAUDE.md, False for others
      with patch('src.cli.commands.dbai.Confirm.ask') as mock_confirm:
        mock_confirm.side_effect = [True, False]  # True for CLAUDE.md, False for docs

        result = runner.invoke(app, [])

        # Check command succeeded
        assert result.exit_code == 0
        assert 'Added Databricks AI setup section to CLAUDE.md' in result.output

        # Check that content was appended
        final_content = (temp_path / 'CLAUDE.md').read_text()
        assert original_content in final_content
        assert 'Databricks AI Development Project' in final_content
        assert final_content.startswith(original_content)

    finally:
      os.chdir(original_cwd)


def test_dbai_command_claude_md_already_has_databricks():
  """Test handling when CLAUDE.md already has Databricks content."""
  with tempfile.TemporaryDirectory() as temp_dir:
    original_cwd = Path.cwd()
    temp_path = Path(temp_dir)

    try:
      import os

      os.chdir(temp_path)

      # Create CLAUDE.md that already has Databricks content
      content_with_dbx = '# My Project\n\n# Databricks AI Development Setup Tool\n\nAlready exists.'
      (temp_path / 'CLAUDE.md').write_text(content_with_dbx)

      # Mock the Confirm.ask to return True for CLAUDE.md
      with patch('src.cli.commands.dbai.Confirm.ask') as mock_confirm:
        mock_confirm.side_effect = [True, False]  # True for CLAUDE.md, False for docs

        result = runner.invoke(app, [])

        # Check that it detected existing content
        assert 'Databricks AI setup section already exists in CLAUDE.md' in result.output

        # Check that content wasn't duplicated
        final_content = (temp_path / 'CLAUDE.md').read_text()
        assert final_content == content_with_dbx

    finally:
      os.chdir(original_cwd)


def test_dbai_command_merge_claude_commands():
  """Test that dbai command merges commands when accepted."""
  with tempfile.TemporaryDirectory() as temp_dir:
    original_cwd = Path.cwd()
    temp_path = Path(temp_dir)

    try:
      import os

      os.chdir(temp_path)

      # Create existing command
      (temp_path / '.claude' / 'commands').mkdir(parents=True)
      (temp_path / '.claude' / 'commands' / 'custom.md').write_text('# Custom command')

      # Mock the Confirm.ask to return True for commands prompt
      with patch('src.cli.commands.dbai.Confirm.ask') as mock_confirm:
        # Return False for CLAUDE.md, False for docs, True for commands
        mock_confirm.side_effect = [False, False, True]

        result = runner.invoke(app, [])

        # Check command succeeded
        assert result.exit_code == 0
        assert 'Added .claude/commands/dbx-setup.md' in result.output
        assert 'Added .claude/commands/docs.md' in result.output

        # Check that both old and new commands exist
        assert (temp_path / '.claude' / 'commands' / 'custom.md').exists()
        assert (temp_path / '.claude' / 'commands' / 'dbx-setup.md').exists()
        assert (temp_path / '.claude' / 'commands' / 'docs.md').exists()

        # Check original command wasn't modified
        assert (temp_path / '.claude' / 'commands' / 'custom.md').read_text() == '# Custom command'

    finally:
      os.chdir(original_cwd)


def test_dbai_command_replace_docs_directory():
  """Test that dbai command replaces docs directory when accepted."""
  with tempfile.TemporaryDirectory() as temp_dir:
    original_cwd = Path.cwd()
    temp_path = Path(temp_dir)

    try:
      import os

      os.chdir(temp_path)

      # Create existing docs directory with custom file
      (temp_path / 'dbx_ai_docs').mkdir()
      (temp_path / 'dbx_ai_docs' / 'custom.md').write_text('# Custom doc')

      # Mock the Confirm.ask to return True for docs prompt
      with patch('src.cli.commands.dbai.Confirm.ask') as mock_confirm:
        # Return False for CLAUDE.md, True for docs, False for commands (no commands yet)
        mock_confirm.side_effect = [False, True]

        result = runner.invoke(app, [])

        # Check command succeeded
        assert result.exit_code == 0
        assert 'Replaced dbx_ai_docs/' in result.output

        # Check that docs were replaced with standard ones
        assert (temp_path / 'dbx_ai_docs' / 'cli-overview.md').exists()
        assert not (temp_path / 'dbx_ai_docs' / 'custom.md').exists()

    finally:
      os.chdir(original_cwd)


def test_dbai_command_accept_all_prompts():
  """Test that dbai command handles accepting all interactive prompts."""
  with tempfile.TemporaryDirectory() as temp_dir:
    original_cwd = Path.cwd()
    temp_path = Path(temp_dir)

    try:
      import os

      os.chdir(temp_path)

      # Create existing files
      original_claude = '# My Project\n\nExisting content.'
      (temp_path / 'CLAUDE.md').write_text(original_claude)
      (temp_path / 'dbx_ai_docs').mkdir()
      (temp_path / 'dbx_ai_docs' / 'old.md').write_text('# Old doc')
      (temp_path / '.claude' / 'commands').mkdir(parents=True)
      (temp_path / '.claude' / 'commands' / 'custom.md').write_text('# Custom')

      # Mock all prompts to return True
      with patch('src.cli.commands.dbai.Confirm.ask') as mock_confirm:
        mock_confirm.return_value = True

        result = runner.invoke(app, [])

        # Check command succeeded
        assert result.exit_code == 0

        # Check CLAUDE.md was appended
        claude_content = (temp_path / 'CLAUDE.md').read_text()
        assert original_claude in claude_content
        assert 'Databricks AI Development Project' in claude_content

        # Check docs were replaced
        assert (temp_path / 'dbx_ai_docs' / 'cli-overview.md').exists()
        assert not (temp_path / 'dbx_ai_docs' / 'old.md').exists()

        # Check commands were merged
        assert (temp_path / '.claude' / 'commands' / 'custom.md').exists()
        assert (temp_path / '.claude' / 'commands' / 'dbx-setup.md').exists()

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


def test_dbai_command_claude_commands_duplicate_files():
  """Test handling when trying to add commands that already exist."""
  with tempfile.TemporaryDirectory() as temp_dir:
    original_cwd = Path.cwd()
    temp_path = Path(temp_dir)

    try:
      import os

      os.chdir(temp_path)

      # Create existing commands with same names as template commands
      (temp_path / '.claude' / 'commands').mkdir(parents=True)
      (temp_path / '.claude' / 'commands' / 'dbx-setup.md').write_text('# Existing dbx-setup')
      (temp_path / '.claude' / 'commands' / 'docs.md').write_text('# Existing docs')

      # Mock the Confirm.ask to return True for commands prompt
      with patch('src.cli.commands.dbai.Confirm.ask') as mock_confirm:
        # Return False for CLAUDE.md, False for docs, True for commands
        mock_confirm.side_effect = [False, False, True]

        result = runner.invoke(app, [])

        # Check command succeeded
        assert result.exit_code == 0
        assert 'dbx-setup.md already exists, skipping...' in result.output
        assert 'docs.md already exists, skipping...' in result.output

        # Check that existing files weren't overwritten
        assert (
          temp_path / '.claude' / 'commands' / 'dbx-setup.md'
        ).read_text() == '# Existing dbx-setup'
        assert (temp_path / '.claude' / 'commands' / 'docs.md').read_text() == '# Existing docs'

    finally:
      os.chdir(original_cwd)


def test_dbai_command_empty_claude_commands_directory():
  """Test handling when .claude/commands exists but is empty."""
  with tempfile.TemporaryDirectory() as temp_dir:
    original_cwd = Path.cwd()
    temp_path = Path(temp_dir)

    try:
      import os

      os.chdir(temp_path)

      # Create empty commands directory
      (temp_path / '.claude' / 'commands').mkdir(parents=True)

      # Run command - should not prompt for commands since directory is empty
      result = runner.invoke(app, [], input='n\nn\n')

      # Check command succeeded and added commands without prompting
      assert result.exit_code == 0
      assert 'Added .claude/commands/dbx-setup.md' in result.output
      assert 'Added .claude/commands/docs.md' in result.output

      # Check that commands were created
      assert (temp_path / '.claude' / 'commands' / 'dbx-setup.md').exists()
      assert (temp_path / '.claude' / 'commands' / 'docs.md').exists()

    finally:
      os.chdir(original_cwd)


def test_dbai_extract_databricks_section():
  """Test the helper function that extracts Databricks section from template."""
  from src.cli.commands.dbai import _extract_databricks_section

  sample_content = """# Unrelated Header

Some content

# Databricks AI Development Setup Tool

This is the databricks content
that should be extracted.

## More Databricks Content

Additional sections."""

  result = _extract_databricks_section(sample_content)

  assert result.startswith('# Databricks AI Development Setup Tool')
  assert 'This is the databricks content' in result
  assert 'Additional sections.' in result
  assert '# Unrelated Header' not in result


def test_dbai_command_help():
  """Test that dbai command help works."""
  result = runner.invoke(app, ['--help'])

  assert result.exit_code == 0
  assert 'Create Databricks AI development documentation scaffolding' in result.output
  assert 'This command generates static documentation' in result.output
