---
description: "Create and develop a new Typer CLI application"
---

# CLI Application Developer

I will help you create and develop a new Typer CLI application using an interactive, step-by-step approach. This process is designed to guide you from initial concept to a fully functional CLI application with proper testing and documentation.

Let me first check your current progress and then guide you through the appropriate next steps.

## Progress Check

```bash
./app_status.sh
```

Based on this status check, I'll determine where we are in the development process and guide you accordingly.

---

## Step 1: Environment Setup

**Check if completed:** Run `./app_status.sh` to see if uv is configured and dependencies are installed.

If this step shows as incomplete, I'll run the interactive setup:

```bash
./scripts/setup.sh
```

Then verify everything works:

```bash
uv run python app.py --help
```

**✅ Step 1 Complete** when the status check shows environment setup is done.

---

## Step 2: Product Requirements Document

**Check if in progress:** The status script checks if `docs/product.md` exists and has been modified from the template.

If you've started working on product requirements, I'll ask: *"I see you've started working on product requirements. Would you like to continue refining them or skip to technical design?"*

Otherwise, I'll guide you through defining your CLI application with these key questions:

### Product Discovery Questions

**Core Purpose:**
1. What is the primary goal of your CLI application? What specific problem does it solve?
2. What tasks or workflows will it help automate or simplify?

**Target Users:**
3. Who are the target users? (developers, sysadmins, analysts, etc.)
4. What's their typical workflow where they'd use your tool?

**Feature Definition:**
5. What are the key commands/features, in order of priority?
6. What are the primary inputs and outputs for each command?

**Competitive Analysis:**
7. What existing CLI tools are similar? How will yours be different?
8. What unique value does your application provide?

**Technical Requirements:**
9. Any specific technologies, APIs, or services to integrate with?
10. Performance, security, or compatibility requirements?

I'll update `docs/product.md` based on your answers.

**✅ Step 2 Complete** when your product vision is clearly defined.

---

## Step 3: Technical Architecture Planning

**Check if in progress:** The status script checks if `docs/design.md` exists and has been modified from the template.

If you've started working on technical design, I'll ask: *"I see you've started working on technical design. Would you like to continue refining it or skip to implementation?"*

Otherwise, I'll guide you through architecture decisions:

### Architecture Discovery

**CLI Structure:**
1. How should commands be organized? (single-level, nested groups, plugins)
2. What configuration approach? (config files, env vars, CLI options)

**Data & Storage:**
3. What data to store/cache? (temp files, persistent config, logs)
4. Output format support? (JSON, YAML, table, plain text)

**Integrations:**
5. External APIs, services, or tools to integrate with?
6. How to handle authentication and credentials?

**Error Handling & UX:**
7. Error handling and user feedback strategy?
8. Logging and debugging features needed?

I'll create a comprehensive technical design document based on our discussion.

**✅ Step 3 Complete** when architecture is well-defined.

---

## Step 4: Implementation Planning & Development

**Check if in progress:** The status script checks if custom commands (beyond the template examples) exist in `src/cli/commands/`.

Based on the product requirements and technical architecture from previous steps, I'll:

1. **Summarize the scope** - Review what we're building, key commands, and technical decisions
2. **Present the implementation plan** - Break development into logical phases with clear deliverables
3. **Confirm the plan** - Get your approval before writing any code

### Implementation Planning Process

**Phase 1: Scope Summary & Design Review**
- Review product requirements and technical architecture decisions
- Confirm command structure, data models, and integration points
- Identify any missing requirements or technical concerns

**Phase 2: Implementation Plan Presentation**
- Break development into logical phases with clear deliverables
- Define success criteria for each phase
- Estimate development order and dependencies

**Phase 3: Plan Approval**
- Present complete implementation roadmap
- Get your confirmation before proceeding
- Adjust plan based on your feedback

**Phase 4: Development Execution**
Once approved, development phases typically include:
1. **Core CLI Structure** - Basic command structure and argument parsing
2. **Configuration System** - Settings and preferences management  
3. **Primary Commands** - Main functionality implementation
4. **Integration Layer** - External service connections
5. **Advanced Features** - Secondary functionality
6. **Testing & Documentation** - Comprehensive testing and docs

### Development Workflow - One File Per Command

This template follows Typer's **one-file-per-command** approach for better organization:

**Project Architecture:**
```
src/
├── cli/              # CLI interface layer only
│   ├── cli.py        # Main CLI app and command registration
│   └── commands/     # Individual command implementations
│       ├── __init__.py
│       ├── hello.py  # Thin CLI wrapper - calls src.core functions
│       └── mycommand.py
├── core/             # Core business logic and application services
├── models/           # Data models, schemas, domain objects
├── services/         # Database management, external APIs, AI agents
└── utils/            # Shared utility functions

tests/
├── test_hello.py     # CLI command tests
├── test_mycommand.py
├── test_core/        # Core business logic tests
└── test_models/      # Data model tests
```

**Key Principle:** CLI commands should be **thin interface layers** that:
- Parse arguments and handle user interaction
- Call functions from `src.core`, `src.models`, `src.services`
- Format and display results
- Handle CLI-specific errors and help text

**Adding New Commands:**
1. Create `src/cli/commands/mycommand.py` with command function
2. Import and register in `src/cli/cli.py`
3. Create `tests/test_mycommand.py` with comprehensive tests
4. Run `./app_status.sh` to verify test coverage

### Development Commands

Throughout implementation:

```bash
# Add dependencies
uv add [package-name]

# Run the CLI
uv run python app.py [command] [options]

# Run all tests
./scripts/test.sh

# Run specific command tests
uv run pytest tests/test_mycommand.py -v

# Check status and test coverage
./app_status.sh

# Code quality
uv run ruff check src/
uv run ruff format src/
```

**Automated Testing Approach:**
- Each command file should have a corresponding test file
- Status script warns about missing test files (without running slow tests)
- Use `CliRunner` for testing CLI interactions
- Test both success cases and error handling

**✅ Step 4 Complete** when your CLI application is fully implemented and tested.

---

## Typer Reference Documentation

For detailed Typer patterns and syntax, refer to the comprehensive guides:
- `docs/typer-reference.md` - Complete quick reference with code examples
- `docs/typer-urls.md` - Documentation navigation and search strategies

**Quick Access URLs:**
- **Getting Started**: https://typer.tiangolo.com/tutorial/first-steps/
- **One File Per Command**: https://typer.tiangolo.com/tutorial/one-file-per-command/  
- **Testing**: https://typer.tiangolo.com/tutorial/testing/
- **Parameter Types**: https://typer.tiangolo.com/tutorial/parameter-types/

---

## Development Philosophy

I follow an **additive development approach**:

- ✅ Build upon the existing template structure
- ✅ Add functionality incrementally using uv for package management
- ✅ Test each component as we develop
- ✅ Maintain comprehensive documentation
- ✅ Focus on user experience and reliability

## Project Tracking

Progress is tracked through:
- `./app_status.sh` - Overall development status
- `docs/todos.md` - Task tracking
- `docs/work/` - Ongoing work documentation  
- `docs/done/` - Completed work archive

---

**Ready to start? Let me run the status check and guide you to the appropriate step!**