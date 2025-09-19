#!/bin/bash

# CLI App Status Checker
# Checks the current status of the CLI application development

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Emoji indicators
CHECK_MARK="✅"
IN_PROGRESS="⏺️"
PENDING="⏸️"
ERROR="❌"

# Verbose mode flag
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [-v|--verbose] [-h|--help]"
            echo "Check the status of CLI application development"
            echo ""
            echo "Options:"
            echo "  -v, --verbose    Show detailed information"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🔍 CLI Application Status Check${NC}"
echo "================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "src/cli" ] || [ ! -f "app.py" ]; then
    echo -e "${ERROR} ${RED}Not in a dbx-aidev project directory${NC}"
    echo "Please run this script from the root of your CLI app project"
    echo "Expected files: pyproject.toml, app.py, src/cli/"
    exit 1
fi

# Step 1: Environment Setup
echo -e "\n${BLUE}Step 1: Environment Setup${NC}"
if command -v uv >/dev/null 2>&1 && [ -f "uv.lock" ]; then
    echo -e "${CHECK_MARK} ${GREEN}Environment detected, syncing dependencies...${NC}"
    
    # Run uv sync to ensure dependencies are installed
    if uv sync >/dev/null 2>&1; then
        echo -e "${CHECK_MARK} ${GREEN}Environment setup complete${NC}"
        STEP1_COMPLETE=true
    else
        echo -e "${ERROR} ${RED}Failed to sync dependencies${NC}"
        echo "  Try running: uv sync"
        STEP1_COMPLETE=false
    fi
    
    if [ "$VERBOSE" = true ]; then
        echo "  • uv version: $(uv --version)"
        echo "  • Python version: $(uv run python --version 2>/dev/null || echo 'Not available')"
        echo "  • Dependencies synced: $([ $STEP1_COMPLETE = true ] && echo "Yes" || echo "No")"
    fi
else
    echo -e "${IN_PROGRESS} ${YELLOW}Environment setup needed${NC}"
    echo "  Run: ./scripts/setup.sh"
    STEP1_COMPLETE=false
fi

# Step 2: Product Requirements
echo -e "\n${BLUE}Step 2: Product Requirements Document${NC}"
if [ -f "docs/product.md" ]; then
    # Check if it's been modified from template (simple heuristic: check file size and content)
    if [ -s "docs/product.md" ] && grep -q "CLI Application" "docs/product.md" 2>/dev/null; then
        echo -e "${CHECK_MARK} ${GREEN}Product requirements defined${NC}"
        STEP2_COMPLETE=true
        
        if [ "$VERBOSE" = true ]; then
            echo "  • File size: $(wc -c < docs/product.md) bytes"
            echo "  • Last modified: $(stat -f "%Sm" docs/product.md 2>/dev/null || stat -c "%y" docs/product.md 2>/dev/null || echo 'Unknown')"
        fi
    else
        echo -e "${IN_PROGRESS} ${YELLOW}Product requirements template exists but needs completion${NC}"
        STEP2_COMPLETE=false
    fi
else
    echo -e "${PENDING} ${YELLOW}Product requirements not started${NC}"
    echo "  Template will be created when you start Step 2"
    STEP2_COMPLETE=false
fi

# Step 3: Technical Architecture
echo -e "\n${BLUE}Step 3: Technical Architecture${NC}"
if [ -f "docs/design.md" ]; then
    if [ -s "docs/design.md" ] && grep -q "Technical Architecture" "docs/design.md" 2>/dev/null; then
        echo -e "${CHECK_MARK} ${GREEN}Technical architecture defined${NC}"
        STEP3_COMPLETE=true
        
        if [ "$VERBOSE" = true ]; then
            echo "  • File size: $(wc -c < docs/design.md) bytes"
            echo "  • Last modified: $(stat -f "%Sm" docs/design.md 2>/dev/null || stat -c "%y" docs/design.md 2>/dev/null || echo 'Unknown')"
        fi
    else
        echo -e "${IN_PROGRESS} ${YELLOW}Technical architecture template exists but needs completion${NC}"
        STEP3_COMPLETE=false
    fi
else
    echo -e "${PENDING} ${YELLOW}Technical architecture not started${NC}"
    echo "  Template will be created when you start Step 3"
    STEP3_COMPLETE=false
fi

# Step 4: Implementation
echo -e "\n${BLUE}Step 4: Implementation${NC}"
if [ -d "src/cli/commands" ]; then
    # Count custom command files
    CUSTOM_COMMANDS=$(find src/cli/commands -name "*.py" -not -name "__init__.py" 2>/dev/null | wc -l || echo 0)
    
    if [ "$CUSTOM_COMMANDS" -gt 0 ]; then
        echo -e "${CHECK_MARK} ${GREEN}Implementation in progress${NC}"
        STEP4_COMPLETE=true
        
        if [ "$VERBOSE" = true ]; then
            echo "  • Custom command modules: $CUSTOM_COMMANDS"
            echo "  • Total command modules: $(find src/cli/commands -name "*.py" -not -name "__init__.py" 2>/dev/null | wc -l || echo 0)"
        fi
    else
        echo -e "${PENDING} ${YELLOW}Implementation not started${NC}"
        STEP4_COMPLETE=false
    fi
else
    echo -e "${PENDING} ${YELLOW}Implementation not started${NC}"
    STEP4_COMPLETE=false
fi

# CLI Functionality Test
echo -e "\n${BLUE}CLI Functionality Test${NC}"
if $STEP1_COMPLETE; then
    if uv run python app.py --help >/dev/null 2>&1; then
        echo -e "${CHECK_MARK} ${GREEN}CLI is functional${NC}"
        
        if [ "$VERBOSE" = true ]; then
            echo "  • Available commands:"
            uv run python app.py --help | grep -E "^\s+[a-z]+" | sed 's/^/    /' 2>/dev/null || echo "    (unable to parse commands)"
        fi
    else
        echo -e "${ERROR} ${RED}CLI has issues${NC}"
        echo "  Run: uv run python app.py --help"
    fi
else
    echo -e "${PENDING} ${YELLOW}CLI not testable (environment not set up)${NC}"
fi

# Test Coverage Analysis
echo -e "\n${BLUE}Test Coverage${NC}"
if $STEP1_COMPLETE; then
    # Check for command files
    COMMAND_FILES=$(find src/cli/commands -name "*.py" -not -name "__init__.py" 2>/dev/null | wc -l || echo 0)
    TEST_FILES=$(find tests/ -name "test_*.py" 2>/dev/null | wc -l || echo 0)
    
    if [ "$COMMAND_FILES" -eq 0 ]; then
        echo -e "${PENDING} ${YELLOW}No command files found${NC}"
        echo "  Commands should be in src/cli/commands/"
    else
        # Check for missing test files
        MISSING_TESTS=()
        for cmd_file in src/cli/commands/*.py; do
            if [ -f "$cmd_file" ] && [ "$(basename "$cmd_file")" != "__init__.py" ]; then
                cmd_name=$(basename "$cmd_file" .py)
                test_file="tests/test_${cmd_name}.py"
                if [ ! -f "$test_file" ]; then
                    MISSING_TESTS+=("$cmd_name")
                fi
            fi
        done
        
        if [ ${#MISSING_TESTS[@]} -eq 0 ]; then
            echo -e "${CHECK_MARK} ${GREEN}All commands have test files${NC}"
        else
            echo -e "${IN_PROGRESS} ${YELLOW}Missing test files for: ${MISSING_TESTS[*]}${NC}"
        fi
        
        if [ "$VERBOSE" = true ]; then
            echo "  • Command files: $COMMAND_FILES"
            echo "  • Test files: $TEST_FILES"
            echo "  • Run tests with: ./scripts/test.sh"
        fi
    fi
else
    echo -e "${PENDING} ${YELLOW}Test analysis not available (environment not set up)${NC}"
fi

# Overall Status Summary
echo -e "\n${BLUE}Overall Progress${NC}"
echo "================="

if $STEP1_COMPLETE && $STEP2_COMPLETE && $STEP3_COMPLETE && $STEP4_COMPLETE; then
    echo -e "${CHECK_MARK} ${GREEN}All steps complete! Your CLI application is ready.${NC}"
elif $STEP1_COMPLETE && $STEP2_COMPLETE && $STEP3_COMPLETE; then
    echo -e "${IN_PROGRESS} ${YELLOW}Ready for implementation phase.${NC}"
elif $STEP1_COMPLETE && $STEP2_COMPLETE; then
    echo -e "${IN_PROGRESS} ${YELLOW}Ready for technical architecture design.${NC}"
elif $STEP1_COMPLETE; then
    echo -e "${IN_PROGRESS} ${YELLOW}Ready for product requirements definition.${NC}"
else
    echo -e "${IN_PROGRESS} ${YELLOW}Ready to start with environment setup.${NC}"
fi

# Exit with appropriate code
if $STEP1_COMPLETE; then
    exit 0
else
    exit 1
fi