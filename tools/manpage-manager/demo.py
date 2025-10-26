#!/usr/bin/env python3
"""
Quick demo script showing manpage-manager capabilities
Run this after installation to see the tool in action
"""

import asyncio
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
except ImportError:
    print("❌ Please install manpage-manager first:")
    print("   ./install.sh")
    sys.exit(1)

console = Console()


def show_demo():
    """Show interactive demo."""

    demo_md = """
# 🎯 Manpage Manager Demo

## What This Tool Does

The **manpage-manager** is a modern CLI tool that automates the management of explainshell's
database dumps. It replaces manual curl/mongorestore commands with a beautiful, Git-like interface.

## Key Features

### 📥 Download Management
- Automatic download from GitHub releases
- Progress bars and transfer speed indicators
- Smart file validation and checksum verification

### 🔍 Dump Inspection
- View file metadata and statistics
- Extract collection counts without full import
- Validate dump integrity before import

### 🗄️ MongoDB Import
- Support for both Docker and direct MongoDB connections
- Progress indicators during import
- Detailed import statistics and error reporting

### 🔄 Update Checking
- Check GitHub for newer dump versions
- Display release information and age warnings
- Compare with local dump versions

## Architecture

```
┌─────────────────┐
│   GitHub API    │  Fetch release info & download dumps
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DumpManager    │  Inspect, validate, extract metadata
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ MongoDBImporter │  Import via Docker or direct connection
└─────────────────┘
```

## Technologies Used

- **Typer**: Click-based CLI with automatic help generation
- **Rich**: Beautiful terminal formatting, tables, and progress bars
- **Loguru**: Simplified logging with automatic rotation
- **httpx**: Modern async HTTP client for downloads
- **sh**: Pythonic shell command execution
- **Pydantic**: Data validation and settings management

## Example Workflow

```bash
# 1. Check what's available
$ manpage-mgr check-update
📦 Latest Release Info
  Release:    Database dump
  Published:  2023-02-13
  Age:        ~3 years (OUTDATED)

# 2. Download the dump
$ manpage-mgr download
📥 Downloading dump.gz (234.5 MB)
[████████████████████████] 100% • 234.5 MB • 15.2 MB/s

# 3. Inspect before importing
$ manpage-mgr inspect /tmp/dump.gz
📊 Database Statistics:
  Collections:  3
  Manpages:     29,763
  Mappings:     42,069
  Classifier:   517
  Total Docs:   72,349

# 4. Import into MongoDB
$ manpage-mgr import /tmp/dump.gz --docker
✅ Connection successful
[████████████████████████] Importing...
✅ Import Results:
  Collections:  3
  Documents:    72,349
  Duration:     45.2 seconds
```

## Comparison with Manual Process

### Before (Manual):
```bash
# Download
curl -L -o /tmp/dump.gz https://github.com/.../dump.gz

# No validation
# No progress indicator
# No metadata inspection

# Import (blind)
docker-compose exec -T db mongorestore --archive --gzip < /tmp/dump.gz
# No progress
# No statistics
# No error handling
```

### After (manpage-manager):
```bash
# Download with progress & validation
manpage-mgr download

# Inspect metadata & stats
manpage-mgr inspect /tmp/dump.gz

# Import with progress & results
manpage-mgr import /tmp/dump.gz --docker
```

## Why This Matters

1. **User Experience**: Beautiful terminal UI makes operations clear and intuitive
2. **Reliability**: Validation and error handling prevent bad imports
3. **Visibility**: Progress bars and statistics show what's happening
4. **Automation**: Single commands replace multi-step manual processes
5. **Extensibility**: Easy to add new commands (e.g., backup, sync, diff)

## Future Enhancements

- [ ] Automated manpage scraping from Ubuntu repos
- [ ] Incremental updates (only fetch new/changed pages)
- [ ] Database backup before import
- [ ] Dump comparison and diffing
- [ ] Integration with CI/CD pipelines
- [ ] Support for multiple dump sources

---

**Ready to try it? Run:** `manpage-mgr --help`
"""

    console.print(
        Panel(
            Markdown(demo_md),
            title="[bold blue]Manpage Manager Demo[/bold blue]",
            border_style="blue",
            padding=(1, 2),
        )
    )


if __name__ == "__main__":
    show_demo()
