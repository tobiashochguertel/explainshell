#!/usr/bin/env bash
# User installation script for manpage-manager (system-wide or user install)

set -e

echo "🚀 Manpage Manager - Installation & Quick Start"
echo "================================================"
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

# Install the package (system-wide with --system flag)
echo "📦 Installing manpage-manager..."
uv pip install --system -e .

echo ""
echo "✅ Installation complete!"
echo ""
echo "📚 Quick Start Guide"
echo "===================="
echo ""
echo "1. Check for updates:"
echo "   manpage-mgr check-update"
echo ""
echo "2. Download latest dump:"
echo "   manpage-mgr download"
echo ""
echo "3. Inspect the dump:"
echo "   manpage-mgr inspect /tmp/dump.gz"
echo ""
echo "4. Import into Docker MongoDB:"
echo "   manpage-mgr import /tmp/dump.gz --docker"
echo ""
echo "5. Or import into local MongoDB:"
echo "   manpage-mgr import /tmp/dump.gz --host localhost --port 27017"
echo ""
echo "🆘 Get help:"
echo "   manpage-mgr --help"
echo "   manpage-mgr download --help"
echo ""
echo "🎉 Happy managing!"
