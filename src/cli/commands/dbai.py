"""Main dbai command for setting up Databricks AI development scaffolding."""

from pathlib import Path
import shutil

import typer
from rich.console import Console

console = Console()


def dbai():
    """Create Databricks AI development documentation scaffolding.

    This command generates static documentation and AI command structures
    that enable AI tools like Claude Code to effectively work with Databricks
    CLI and SDK operations.
    """
    # Copy templates to create scaffolding
    _copy_templates()

    console.print("✅ [green]Databricks AI documentation scaffolding created![/green]")
    console.print("📚 [blue]Documentation:[/blue] dbx_ai_docs/")
    console.print("📝 [blue]Project overview:[/blue] CLAUDE.md")
    console.print("🤖 [blue]AI commands:[/blue] .claude/commands/")
    console.print()
    console.print("🚀 [yellow]Next step:[/yellow] Run `/dbx-setup` to complete project configuration")


def _copy_templates():
    """Copy template files to create project scaffolding."""
    # Get the template directory (relative to this module)
    # When installed as package: ../../../templates
    # When run locally: ../../../templates
    template_dir = Path(__file__).parent.parent.parent / "templates"

    if not template_dir.exists():
        console.print(f"❌ [red]Template directory not found: {template_dir}[/red]")
        raise typer.Exit(1)

    console.print("📁 [yellow]Copying template files...[/yellow]")

    # Copy CLAUDE.md if it doesn't exist
    claude_md_src = template_dir / "CLAUDE.md"
    claude_md_dst = Path("CLAUDE.md")
    if claude_md_src.exists() and not claude_md_dst.exists():
        shutil.copy2(claude_md_src, claude_md_dst)
        console.print(f"  ✓ Created {claude_md_dst}")
    elif claude_md_dst.exists():
        console.print("📝 [yellow]CLAUDE.md already exists, skipping...[/yellow]")

    # Copy docs directory
    docs_src = template_dir / "dbx_ai_docs"
    docs_dst = Path("dbx_ai_docs")
    if docs_src.exists():
        if not docs_dst.exists():
            shutil.copytree(docs_src, docs_dst)
            console.print(f"  ✓ Created {docs_dst}/")
        else:
            console.print("📚 [yellow]dbx_ai_docs/ already exists, skipping...[/yellow]")

    # Copy .claude commands
    claude_commands_src = template_dir / ".claude" / "commands"
    claude_commands_dst = Path(".claude/commands")
    if claude_commands_src.exists():
        claude_commands_dst.mkdir(parents=True, exist_ok=True)
        for cmd_file in claude_commands_src.glob("*.md"):
            dst_file = claude_commands_dst / cmd_file.name
            if not dst_file.exists():
                shutil.copy2(cmd_file, dst_file)
                console.print(f"  ✓ Created {dst_file}")
            else:
                console.print(f"🤖 [yellow]{dst_file} already exists, skipping...[/yellow]")