#!/bin/bash

set -e

echo "🧪 Running CLI Tests"
echo "==================="
echo ""

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Run tests
echo "📋 Running pytest..."
uv run pytest tests/ -v

echo ""
echo "✅ All tests passed!"
echo ""