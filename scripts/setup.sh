#!/bin/bash

set -e

echo "🚀 Claude CLI App Template Setup"
echo "================================="

# Get the directory of this script
SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source shared utilities
source "$SETUP_DIR/setup_utils.sh"

# Check for required tools
echo ""
echo "🔧 Checking System Dependencies"
echo "================================"
echo ""

OS=$(get_os)
echo "🖥️  Detected OS: $OS"
echo ""

echo "📦 Checking uv (Python package manager)..."
if ! check_uv; then
    exit 1
fi

echo ""
echo "🎉 All required system dependencies are installed!"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
uv sync --dev

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run 'uv run python app.py --help' to test the CLI app"
echo ""