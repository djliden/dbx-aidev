"""Main dbai command for setting up Databricks AI development scaffolding."""

import shutil
from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm

console = Console()


def dbai():
  """Create Databricks AI development documentation scaffolding.

  This command generates static documentation and AI command structures
  that enable AI tools like Claude Code to effectively work with Databricks
  CLI and SDK operations.
  """
  # Copy templates to create scaffolding
  _copy_templates()

  console.print('✅ [green]Databricks AI documentation scaffolding created![/green]')
  console.print('📚 [blue]Documentation:[/blue] dbx_ai_docs/')
  console.print('📝 [blue]Project overview:[/blue] CLAUDE.md')
  console.print('🤖 [blue]AI commands:[/blue] .claude/commands/')
  console.print()
  console.print('🚀 [yellow]Next step:[/yellow] Run `/dbx-setup` to complete project configuration')


def _copy_templates():
  """Copy template files to create project scaffolding."""
  # Get the template directory (relative to this module)
  # When installed as package: ../../../templates
  # When run locally: ../../../templates
  template_dir = Path(__file__).parent.parent.parent / 'templates'

  if not template_dir.exists():
    console.print(f'❌ [red]Template directory not found: {template_dir}[/red]')
    raise typer.Exit(1)

  console.print('📁 [yellow]Copying template files...[/yellow]')

  # Handle CLAUDE.md with append option
  claude_md_src = template_dir / 'CLAUDE.md'
  claude_md_dst = Path('CLAUDE.md')
  if claude_md_src.exists():
    if not claude_md_dst.exists():
      shutil.copy2(claude_md_src, claude_md_dst)
      console.print(f'  ✓ Created {claude_md_dst}')
    else:
      if Confirm.ask('📝 CLAUDE.md already exists. Add Databricks AI setup section to it?'):
        _append_to_claude_md(claude_md_src, claude_md_dst)
      else:
        console.print('📝 [yellow]CLAUDE.md already exists, skipping...[/yellow]')

  # Copy docs directory
  docs_src = template_dir / 'dbx_ai_docs'
  docs_dst = Path('dbx_ai_docs')
  if docs_src.exists():
    if not docs_dst.exists():
      shutil.copytree(docs_src, docs_dst)
      console.print(f'  ✓ Created {docs_dst}/')
    else:
      if Confirm.ask('📚 dbx_ai_docs/ already exists. Replace with latest documentation?'):
        shutil.rmtree(docs_dst)
        shutil.copytree(docs_src, docs_dst)
        console.print(f'  ✓ Replaced {docs_dst}/')
      else:
        console.print('📚 [yellow]dbx_ai_docs/ already exists, skipping...[/yellow]')

  # Handle .claude commands with merge option
  claude_commands_src = template_dir / '.claude' / 'commands'
  claude_commands_dst = Path('.claude/commands')
  if claude_commands_src.exists():
    claude_commands_dst.mkdir(parents=True, exist_ok=True)
    existing_commands = list(claude_commands_dst.glob('*.md'))

    if existing_commands:
      if Confirm.ask('🤖 .claude/commands/ already has files. Add new Databricks commands?'):
        _merge_claude_commands(claude_commands_src, claude_commands_dst)
      else:
        console.print('🤖 [yellow].claude/commands/ already exists, skipping...[/yellow]')
    else:
      _merge_claude_commands(claude_commands_src, claude_commands_dst)


def _append_to_claude_md(src_file: Path, dst_file: Path):
  """Append Databricks AI setup section to existing CLAUDE.md."""
  src_content = src_file.read_text()
  dst_content = dst_file.read_text()

  # Extract the Databricks section from the template
  databricks_section = _extract_databricks_section(src_content)

  # Check if Databricks content already exists
  if '# Databricks AI Development Setup Tool' in dst_content or 'dbx-aidev' in dst_content:
    console.print('📝 [yellow]Databricks AI setup section already exists in CLAUDE.md[/yellow]')
    return

  # Append the Databricks section
  updated_content = dst_content.rstrip() + '\n\n' + databricks_section
  dst_file.write_text(updated_content)
  console.print('  ✓ Added Databricks AI setup section to CLAUDE.md')


def _extract_databricks_section(content: str) -> str:
  """Extract the Databricks-specific section from template CLAUDE.md."""
  lines = content.split('\n')

  # Find the start of Databricks content (after the first heading)
  start_idx = 0
  for i, line in enumerate(lines):
    if line.startswith('# Databricks AI Development Setup Tool'):
      start_idx = i
      break

  return '\n'.join(lines[start_idx:])


def _merge_claude_commands(src_dir: Path, dst_dir: Path):
  """Merge .claude command files, avoiding duplicates."""
  for cmd_file in src_dir.glob('*.md'):
    dst_file = dst_dir / cmd_file.name
    if not dst_file.exists():
      shutil.copy2(cmd_file, dst_file)
      console.print(f'  ✓ Added {dst_file}')
    else:
      console.print(f'  📄 [yellow]{dst_file} already exists, skipping...[/yellow]')
