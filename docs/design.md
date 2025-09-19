# Technical Design Document
## Databricks AI Development Setup Tool (`dbx-aidev`)

### Architecture Overview

The `dbx-aidev` CLI tool follows a **minimal static scaffolding approach** that generates comprehensive Databricks documentation and AI command structures without any dynamic configuration or dependencies. The tool creates static files that enable AI tools to handle all dynamic setup and operations.

## Simplified Architecture

### Core Philosophy: Static Documentation + AI Commands

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLI Tool (`dbai`)                        │
│                      Zero Dependencies                          │
├─────────────────────────────────────────────────────────────────┤
│  File Generation Only                                          │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐  │
│  │ Static Docs     │ │  CLAUDE.md      │ │ AI Commands     │  │
│  │ Generator       │ │  Generator      │ │ Generator       │  │
│  │                 │ │                 │ │                 │  │
│  │ • CLI reference │ │ • Overview      │ │ • /dbx-setup    │  │
│  │ • SDK reference │ │ • Navigation    │ │   workflow      │  │
│  │ • Deployment    │ │ • Quick start   │ │ • Setup guide   │  │
│  │ • Safety docs   │ │ • Safety notes  │ │ • Safety config │  │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  Output: Static Files Only                                     │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐  │
│  │ dbx_ai_docs/    │ │   CLAUDE.md     │ │ .claude/        │  │
│  │                 │ │                 │ │   commands/     │  │
│  │ • Pre-written   │ │ • Navigation    │ │     dbx-setup.md│  │
│  │   documentation │ │   to docs       │ │                 │  │
│  │ • No dynamic    │ │ • Basic setup   │ │ • Complete      │  │
│  │   content       │ │   overview      │ │   setup flow    │  │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      AI Tools (Claude Code)                     │
│                    Handle All Dynamic Work                      │
├─────────────────────────────────────────────────────────────────┤
│  Dynamic Operations (using static docs as reference)           │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐  │
│  │ Authentication  │ │ Project Analysis│ │ Configuration   │  │
│  │                 │ │                 │ │                 │  │
│  │ • Install CLI   │ │ • Structure     │ │ • CLAUDE.md     │  │
│  │ • Configure     │ │   analysis      │ │   enhancement   │  │
│  │ • Test access   │ │ • Deployment    │ │ • Deployment    │  │
│  │ • Validate      │ │   strategy      │ │   setup         │  │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## File Structure Design

### Generated File Structure
```
project-root/
├── CLAUDE.md                    # Basic overview, points to dbx_ai_docs/
├── dbx_ai_docs/                 # Static Databricks reference (structure TBD)
│   ├── authentication.md       # Auth methods and patterns
│   ├── cli-reference.md         # CLI commands and examples
│   ├── sdk-reference.md         # SDK patterns and operations
│   ├── deployment-patterns.md   # Standalone vs asset bundle guidance
│   ├── databricks-features.md   # display(), dbutils, Unity Catalog
│   └── safety-guidelines.md     # Risk levels, opt-ins, confirmations
└── .claude/
    └── commands/
        └── dbx-setup.md         # Complete AI-driven setup workflow
```

### Documentation Structure Options (TBD)

**Option A: Many Small Files (per command group)**
```
dbx_ai_docs/
├── cli/
│   ├── workspace-commands.md
│   ├── cluster-commands.md
│   ├── job-commands.md
│   ├── data-commands.md
│   └── bundle-commands.md
├── sdk/
│   ├── workspace-client.md
│   ├── cluster-operations.md
│   ├── job-operations.md
│   └── data-operations.md
└── safety/
    ├── low-risk-ops.md
    ├── medium-risk-ops.md
    └── high-risk-ops.md
```

**Option B: Topic-Based Groupings**
```
dbx_ai_docs/
├── authentication.md           # All auth methods (CLI + SDK)
├── compute-management.md       # Clusters, serverless, etc.
├── data-operations.md          # Unity Catalog, data access
├── job-management.md           # Jobs, pipelines, scheduling
├── deployment-strategies.md    # Asset bundles vs standalone
└── safety-guidelines.md        # All safety patterns
```

**Option C: Mixed Approach**
```
dbx_ai_docs/
├── quick-reference/            # Token-efficient lookups
│   ├── cli-commands.md
│   └── sdk-patterns.md
├── comprehensive/              # Detailed guidance
│   ├── authentication.md
│   ├── deployment.md
│   └── data-operations.md
└── safety/
    └── risk-guidelines.md
```

## Core Components

### 1. Static Documentation Generator (`src/services/docs.py`)

**Single Responsibility:** Generate comprehensive static Databricks documentation

```python
class StaticDocsGenerator:
    """Generate static Databricks documentation for AI tools."""

    def generate_all_docs(self, output_dir: Path) -> DocsResult:
        """Generate complete documentation structure."""
        # Create dbx_ai_docs/ directory
        # Generate all static documentation files
        # No dynamic content or workspace-specific info

    def generate_claude_md(self, project_dir: Path) -> str:
        """Generate basic CLAUDE.md pointing to docs."""
        # Simple overview and navigation
        # Points to dbx_ai_docs/ for detailed reference
        # Mentions /dbx-setup command

    def generate_ai_commands(self, commands_dir: Path) -> CommandsResult:
        """Generate AI command specifications."""
        # Create .claude/commands/dbx-setup.md
        # Complete workflow specification for AI tools
        # No execution, just specification
```

### 2. AI Command Specification

**`.claude/commands/dbx-setup.md` Structure:**
```markdown
# Databricks Project Setup

Complete setup wizard for Databricks AI development.

## Overview
This command guides the user through comprehensive Databricks setup including authentication, project analysis, and configuration customization.

## Workflow Steps

### 1. Environment Setup
- Check if `databricks` CLI is available
- If not: `uv add databricks-cli`
- Verify installation: `databricks --version`

### 2. Authentication Setup
- Present authentication options:
  - OAuth (recommended for interactive use)
  - Personal Access Token
  - Existing CLI profile
- Guide through chosen method
- Test connectivity: `databricks workspace list` or similar

### 3. Project Analysis
- Analyze current directory structure
- Detect notebooks and Python files
- Identify dependencies and complexity
- Recommend deployment strategy:
  - **Standalone**: Simple notebooks, few dependencies
  - **Asset Bundle**: Complex projects, multiple files

### 4. CLAUDE.md Enhancement
- Add workspace-specific context to CLAUDE.md
- Include chosen deployment strategy
- Add project-specific patterns and examples
- Document safety settings for this project

### 5. Safety Configuration
- Review operations requiring opt-ins
- Configure confirmation patterns
- Set up appropriate guardrails for project type
- Document any project-specific safety considerations

## Safety Guidelines
- Always confirm before destructive operations
- Validate permissions before suggesting operations
- Use least-privilege access patterns
- Provide rollback guidance for risky operations

## Success Criteria
- Authentication working and tested
- Deployment strategy chosen and documented
- CLAUDE.md customized for project
- Safety settings configured appropriately
```

### 3. CLI Command Structure

**Minimal CLI Implementation:**
```python
# src/cli/commands/setup.py
@app.command()
def dbai(
    workspace_url: Optional[str] = typer.Option(None, "--workspace", "-w",
                                              help="Workspace URL (for docs customization only)"),
    docs_format: str = typer.Option("standard", "--format", "-f",
                                   help="Documentation format (standard|minimal|comprehensive)"),
    dry_run: bool = typer.Option(False, "--dry-run",
                                help="Show what would be created without creating files")
):
    """Create Databricks AI development documentation scaffolding."""

    if dry_run:
        # Show what would be created
        show_file_structure()
        return

    # Generate static documentation
    docs_generator = StaticDocsGenerator()
    docs_generator.generate_all_docs(Path("dbx_ai_docs"))
    docs_generator.generate_claude_md(Path("."))
    docs_generator.generate_ai_commands(Path(".claude/commands"))

    console.print("✅ Databricks AI documentation scaffolding created!")
    console.print("📚 Documentation: dbx_ai_docs/")
    console.print("🤖 Run `/dbx-setup` to complete project configuration")
```

## Documentation Content Strategy

### Token Efficiency Design
- **Target file size:** 1000-2000 tokens per file
- **Clear headers:** Enable efficient AI tool search
- **Example-driven:** Provide actionable code patterns
- **Cross-references:** Link related operations

### Content Coverage
**CLI Reference:**
- All major `databricks` CLI commands
- Common usage patterns and examples
- Parameter explanations and options
- Error handling and troubleshooting

**SDK Reference:**
- Key `WorkspaceClient` operations
- Authentication patterns
- Common workflows and examples
- Error handling and retry patterns

**Safety Guidelines:**
- Risk classification for operations
- Opt-in patterns and confirmation flows
- Permission validation approaches
- Rollback and recovery strategies

## Implementation Priorities

### Phase 1: Core Static Generation (Critical)
1. **Basic file structure generation** with static content
2. **CLI command implementation** for creating scaffolding
3. **AI command specification** with complete setup workflow
4. **Documentation experimentation** to determine optimal structure

### Phase 2: Content Refinement (High)
1. **Comprehensive CLI/SDK documentation** with examples
2. **Safety guidelines** and risk classification
3. **Deployment strategy guidance** with decision frameworks
4. **Testing with real AI tools** to validate approach

### Phase 3: Polish & Optimization (Medium)
1. **Documentation format options** based on usage patterns
2. **Enhanced AI command workflows** with advanced features
3. **Template customization** for different project types
4. **Community feedback integration** and documentation updates

## Key Design Decisions

### Static-Only Approach
- **No authentication** - AI tools handle this using provided guidance
- **No validation** - AI tools test and validate configurations
- **No dependencies** - Tool works without Databricks CLI/SDK installed
- **No workspace interaction** - Pure documentation generation

### Documentation Structure (Needs Experimentation)
- **Test multiple approaches** with actual AI tool usage
- **Measure token efficiency** and search effectiveness
- **Gather feedback** on which structures work best
- **Iterate based on real usage patterns**

This minimal design eliminates all complexity while providing comprehensive capabilities through AI-driven setup and static documentation.