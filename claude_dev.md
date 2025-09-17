# Meta-Instructions for Developing the Claude CLI App Template

This file contains meta-instructions for developing the `claude-cli-app-template` project. The goal of this project is to create a template for building Typer CLI applications, with the help of Claude.

## Core Task

The primary task is to adapt the `claude-databricks-app-template` (https://github.com/databricks-solutions/claude-databricks-app-template) for Typer CLI app development. This means you should liberally search and draw inspiration from the original template, but with a strong focus on adapting it to the specific needs of a CLI application.

### Key Adaptations:

*   **Remove Web Components:** All frontend components (React, Vite, bun, etc.) and the FastAPI backend should be removed.
*   **Focus on Typer:** The template should be centered around the Typer framework for building CLI applications.
*   **Simplify:** The overall project structure and setup should be much simpler than the original template, as there are no deployment or web server concerns.

## Guiding Principles

*   **Follow the Original:** Adhere closely to the structure and style of the `claude-databricks-app-template` where it makes sense. For example, the use of a `scripts` directory for setup and a `.claude/commands` directory for interactive commands is a good pattern to follow.
*   **CLI-First:** Always think about the end-user experience of the CLI application. The template should make it easy to create new commands, add parameters, and manage the CLI application's lifecycle.
*   **Leverage Claude:** The template should be designed to be used with Claude. This means the `.claude/commands` should be well-documented and provide a guided experience for the user.

## File Guide

*   **`claude.md` (this file):** Meta-instructions for developing the template itself.
*   **`claude_template.md`:** The template for the `CLAUDE.md` file that will be included in the *generated* projects. This file should guide the end-user in developing their CLI application.
*   **`.claude/commands/cli.md`:** The main interactive command for creating and managing a new CLI application. This should be heavily inspired by the `dba.md` command from the original template.

Remember to frequently refer to the `claude-databricks-app-template` repository for inspiration and guidance.
