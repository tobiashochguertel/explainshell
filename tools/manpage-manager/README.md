# Manpage Manager

Modern CLI tool for managing explainshell manpage database dumps.

## Features

- 📥 Download latest database dump from GitHub releases
- 🔍 Inspect dump contents and statistics
- 📦 Extract and validate dumps
- 🗄️ Import dumps into MongoDB (Docker or local)
- 🔄 Check for updates and version information
- 🎨 Beautiful terminal UI with progress bars

## Installation

```bash
# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

## Usage

```bash
# Show help
manpage-mgr --help

# Download latest dump
manpage-mgr download

# Download to specific location
manpage-mgr download --output /custom/path/dump.gz

# Inspect dump contents
manpage-mgr inspect /tmp/dump.gz

# Import into Docker MongoDB
manpage-mgr import /tmp/dump.gz --docker

# Import into local MongoDB
manpage-mgr import /tmp/dump.gz --host localhost --port 27017

# Check for updates
manpage-mgr check-update

# Show current dump info
manpage-mgr info
```

## Development

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format .

# Lint
ruff check .
```

## Architecture

Built with modern Python tools:

- **typer**: Beautiful CLI interface with auto-completion
- **rich**: Rich terminal formatting and progress bars
- **loguru**: Simplified logging
- **httpx**: Modern async HTTP client
- **sh**: Pythonic shell command execution
- **pydantic**: Data validation and settings management
