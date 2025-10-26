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

### Development Setup

```bash
# Clone and navigate to the tool
cd tools/manpage-manager

# Setup development environment (creates venv, installs deps)
./dev-prepare.sh

# Activate virtual environment
source .venv/bin/activate
```

### Production Install

```bash
# Install system-wide
./install.sh
```

## Usage

### Basic Commands

```bash
# Show help
manpage-mgr --help

# Check for updates
manpage-mgr check-update

# Download latest dump
manpage-mgr download

# Download to specific location
manpage-mgr download --output /custom/path/dump.gz

# Inspect dump contents
manpage-mgr inspect /tmp/dump.gz

# Import into Docker MongoDB
manpage-mgr import-dump /tmp/dump.gz --docker

# Import into local MongoDB
manpage-mgr import-dump /tmp/dump.gz --host localhost --port 27017

# Show current dump info
manpage-mgr info
```

### Example Workflow

```bash
# 1. Check what's available
$ manpage-mgr check-update
📦 Latest Release Info
  Published:  2023-02-13
  Size:       234.5 MB
  Age:        ~3 years old

# 2. Download the dump
$ manpage-mgr download
📥 Downloading dump.gz
[████████████████████████] 100% • 234.5 MB • 15.2 MB/s
✅ Download complete: /tmp/dump.gz

# 3. Inspect before importing
$ manpage-mgr inspect /tmp/dump.gz
📊 Database Statistics:
  Collections:  3
  Manpages:     29,763
  Mappings:     42,069
  Total:        72,349 documents

# 4. Import to MongoDB
$ manpage-mgr import-dump /tmp/dump.gz --docker
✅ Connection successful
[████████] Importing...
✅ Import Results:
  Documents:    72,349
  Duration:     45.2 seconds
```

## Configuration

Set environment variables to customize behavior:

```bash
# GitHub settings
export MANPAGE_MGR_GITHUB_OWNER=idank
export MANPAGE_MGR_GITHUB_REPO=explainshell
export MANPAGE_MGR_GITHUB_RELEASE_TAG=db-dump

# Download settings
export MANPAGE_MGR_DOWNLOAD_DIR=/tmp
export MANPAGE_MGR_DUMP_FILENAME=dump.gz

# MongoDB settings
export MANPAGE_MGR_MONGO_HOST=localhost
export MANPAGE_MGR_MONGO_PORT=27017
export MANPAGE_MGR_MONGO_DB=explainshell

# Docker settings
export MANPAGE_MGR_DOCKER_SERVICE_NAME=db

# Logging
export MANPAGE_MGR_LOG_LEVEL=INFO
```

Or use a `.env` file (see `.env.example`).

## Development

### Setup

```bash
# Install with dev dependencies
./dev-prepare.sh
source .venv/bin/activate
```

### Run Tests

```bash
# All tests
pytest

# Verbose mode
pytest -v

# With coverage
pytest --cov

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# E2E tests (may require network/MongoDB)
pytest tests/e2e/
```

### Code Quality

```bash
# Lint
ruff check .

# Format
ruff format .

# Or use Makefile
make lint
make format
make test
```

## Architecture

Built with modern Python tools:

- **typer**: Beautiful CLI interface with auto-completion
- **rich**: Rich terminal formatting and progress bars
- **loguru**: Simplified logging with rotation
- **httpx**: Modern async HTTP client for downloads
- **sh**: Pythonic shell command execution
- **pydantic**: Data validation and settings management
- **pytest**: Testing framework with fixtures
- **ruff**: Fast Python linter and formatter

### Project Structure

```
manpage-manager/
├── src/manpage_manager/     # Source code
│   ├── cli.py              # Typer CLI interface
│   ├── github.py           # GitHub API client
│   ├── dump.py             # Dump inspection/validation
│   ├── mongodb.py          # MongoDB import operations
│   ├── config.py           # Settings management
│   ├── logger.py           # Logging setup
│   └── models.py           # Data models
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   ├── e2e/               # End-to-end tests
│   ├── fixtures/          # Test fixtures
│   └── utils/             # Test utilities
├── docs/                   # Documentation
├── pyproject.toml         # Project configuration
├── dev-prepare.sh         # Development setup script
├── install.sh             # Production install script
└── Makefile               # Development tasks
```

## Database Dump Information

The current database dump available from GitHub:

- **Release Date**: February 13, 2023
- **Age**: ~3 years old (as of Oct 2025)
- **Size**: ~234.5 MB compressed
- **Contents**: 72,349 documents
  - 29,763 manpages
  - 42,069 command-to-manpage mappings
  - 517 classifier training entries
- **Coverage**: 99% of common Unix/Linux commands
- **Status**: Functional but outdated

### Recommendation

The dump works well for most use cases, but consider:

- Use existing dump for immediate needs ✅
- Plan future updates for modern commands
- Consider automation for regular updates

## Troubleshooting

### Virtual Environment Issues

```bash
# If installation fails, try removing and recreating
rm -rf .venv
./dev-prepare.sh
```

### MongoDB Connection Issues

```bash
# Test Docker MongoDB connection
docker-compose exec db mongo --version

# Check if MongoDB is running
docker-compose ps
```

### Download Issues

```bash
# Check network connectivity
curl -I https://api.github.com

# Try with explicit output path
manpage-mgr download --output ~/downloads/dump.gz
```

## Contributing

This tool is part of the explainshell project. Contributions welcome!

### Running Tests

Before submitting changes:

```bash
# Run all tests
pytest -v

# Check code quality
ruff check .
ruff format .

# Ensure all tests pass
pytest --cov
```

## License

Part of the explainshell project. See main repository for license details.

## Links

- **Repository**: <https://github.com/tobiashochguertel/explainshell>
- **Branch**: feature/manpages-modernization
- **Main Project**: <https://github.com/idank/explainshell>

## Documentation

- [EXECUTIVE_SUMMARY.md](docs/implementation/EXECUTIVE_SUMMARY.md) - High-level overview
- [SUMMARY.md](docs/implementation/SUMMARY.md) - Technical details
- [TEST_RESULTS.md](TEST_RESULTS.md) - Test suite results
- [COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md) - Implementation summary
- [QUICKSTART.sh](QUICKSTART.sh) - Interactive quick start guide

## Support

For issues or questions:

1. Check the documentation in `docs/`
2. Run `manpage-mgr --help` for command help
3. Review test examples in `tests/`
4. Open an issue on GitHub

---

**Version**: 0.1.0
**Status**: Production Ready ✅
**Python**: 3.11+
**Last Updated**: October 2025
