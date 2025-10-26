#!/bin/bash
# Development environment preparation script for manpage-manager

set -e

echo "🔧 Manpage Manager - Development Environment Setup"
echo "===================================================="
echo ""

# Check if in correct directory
if [ ! -f "pyproject.toml" ]; then
  echo "❌ Error: Please run this script from the manpage-manager directory"
  echo "   cd tools/manpage-manager"
  exit 1
fi

# Check for uv
if ! command -v uv &>/dev/null; then
  echo "📦 Installing uv (fast Python package manager)..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  echo ""
  echo "✅ uv installed! Please restart your shell or run:"
  echo "   source $HOME/.cargo/env"
  echo ""
  echo "Then run this script again."
  exit 0
fi

echo "✅ uv found: $(which uv)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "🔨 Creating virtual environment..."
  uv venv
  echo "✅ Virtual environment created at .venv"
else
  echo "✅ Virtual environment already exists at .venv"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install the package in editable mode with dev dependencies
echo "📦 Installing manpage-manager with dev dependencies..."
uv pip install -e ".[dev]"

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "📚 Development Commands"
echo "======================="
echo ""
echo "Activate environment:"
echo "   source .venv/bin/activate"
echo ""
echo "Run tests:"
echo "   pytest"
echo "   pytest -v                    # Verbose"
echo "   pytest --cov                 # With coverage"
echo "   pytest tests/unit/           # Unit tests only"
echo "   pytest tests/integration/    # Integration tests only"
echo ""
echo "Code quality:"
echo "   ruff check .                 # Lint"
echo "   ruff format .                # Format"
echo "   make lint                    # Via Makefile"
echo "   make format                  # Via Makefile"
echo ""
echo "Use the tool:"
echo "   manpage-mgr --help"
echo "   manpage-mgr check-update"
echo "   manpage-mgr download"
echo ""
echo "🎉 Happy developing!"
