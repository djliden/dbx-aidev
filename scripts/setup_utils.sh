#!/bin/bash

# Shared utilities for setup scripts

# Function to get OS type
get_os() {
    case "$(uname -s)" in
        Darwin*) echo "macOS" ;;
        Linux*) echo "Linux" ;;
        CYGWIN*|MINGW*|MSYS*) echo "Windows" ;;
        *) echo "Unknown" ;;
    esac
}

# Function to check for uv
check_uv() {
    if command -v uv >/dev/null 2>&1; then
        echo "✅ uv is already installed"
        uv --version
        return 0
    fi

    echo ""
    echo "❌ uv is not installed"
    echo "📋 uv is required for this project to work properly."
    echo ""
    read -p "🤔 Would you like me to install uv for you? (y/N): " install_choice

    if [[ "$install_choice" =~ ^[Yy]$ ]]; then
        echo "🚀 Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source "$HOME/.cargo/env"

        if command -v uv >/dev/null 2>&1; then
            echo "✅ uv installed successfully!"
            uv --version
            return 0
        else
            echo "❌ Failed to install uv. Please install it manually."
            return 1
        fi
    else
        echo "⚠️  Skipping uv installation."
        return 1
    fi
}