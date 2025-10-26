# 🚀 explainshell - Community Integration Fork

> **Python 3.12 Compatible** | **Modern Dependencies** | **Security Fixes** | **Dark Mode Support**

This is a community-maintained fork of [idank/explainshell](https://github.com/idank/explainshell) that integrates valuable open pull requests into a working, tested Python 3.12-compatible version.

[![Original Project](https://img.shields.io/badge/Original-idank/explainshell-blue)](https://github.com/idank/explainshell)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-green)](https://www.python.org/downloads/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0.3-orange)](https://flask.palletsprojects.com/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---

## 🆕 What's New in This Fork

This fork integrates **6 valuable community pull requests** from the original repository:

| Feature | Status | PR | Contributor |
|---------|--------|-----|-------------|
| 🐍 Python 3.12 Migration | ✅ | [#330](https://github.com/idank/explainshell/pull/330) | [@mundanevision20](https://github.com/mundanevision20) |
| 🔧 pymongo 4.x Compatibility | ✅ | [#323](https://github.com/idank/explainshell/pull/323) | [@cben](https://github.com/cben) |
| 🌙 Dark Mode Support | ✅ | [#237](https://github.com/idank/explainshell/pull/237) | [@rugk](https://github.com/rugk) |
| 🎨 Search Box Fix | ✅ | [#248](https://github.com/idank/explainshell/pull/248) | [@apoorvlathey](https://github.com/apoorvlathey) |
| 📚 Better Examples | ✅ | [#293](https://github.com/idank/explainshell/pull/293) | [@Strahinja](https://github.com/Strahinja) |
| 📖 Ubuntu Noble Manpages | ✅ | [#232](https://github.com/idank/explainshell/pull/232) | [@wesinator](https://github.com/wesinator) |

**See [COMMUNITY_INTEGRATION.md](./COMMUNITY_INTEGRATION.md) for detailed information.**

---

## 📋 Table of Contents

- [About explainshell](#about-explainshell)
- [Why This Fork?](#why-this-fork)
- [Key Improvements](#key-improvements)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Credits](#credits)

---

## 🤔 About explainshell

[explainshell.com](http://www.explainshell.com) is a tool capable of parsing man pages, extracting options and explaining a given command-line by matching each argument to the relevant help text in the man page.

### How It Works

explainshell is built from these components:

1. **Man page reader** - Converts man pages from raw format to HTML
2. **Classifier** - Identifies paragraphs containing options
3. **Options extractor** - Scans and extracts options from classified paragraphs
4. **Storage backend** - Saves processed man pages to MongoDB
5. **Matcher** - Walks the command's AST (parsed by [bashlex](https://github.com/idank/bashlex)) and matches nodes to help text

When you query explainshell:

1. Parses your command into an AST
2. Visits interesting nodes (commands, shell operators like `|`, `&&`)
3. Matches each token to known options and help text
4. Returns formatted matches via Flask web interface

---

## 🎯 Why This Fork?

The original explainshell is an **amazing tool**, but it's been stuck on **Python 2.7** (end-of-life since 2020) with several valuable community contributions waiting for review.

### The Problem

```bash
$ docker compose build
# ❌ Error: Debian Buster repositories not found
# ❌ Error: Python 2.7 packages unavailable
# ❌ Security vulnerabilities in old dependencies
```

### The Solution

This fork:
- ✅ **Works with modern Docker images**
- ✅ **Fixes security vulnerabilities**
- ✅ **Integrates tested community improvements**
- ✅ **Provides Python 3.12 compatibility**
- ✅ **Maintains backward compatibility for users**

---

## 🔥 Key Improvements

### Security Enhancements

| Component | Before | After | Benefit |
|-----------|--------|-------|---------|
| Python | 2.7 (EOL) | 3.12 | Modern security patches |
| Flask | 0.12 | 3.0.3 | CVE-2023-30861 fixed |
| nltk | 3.4.5 | 3.9.1 | ReDoS vulnerabilities fixed |
| pymongo | 3.13.0 | 4.8.0 | Modern MongoDB support |

### User Experience

- 🌙 **Auto Dark Mode**: Respects system preferences
- 🎨 **Fixed UI**: No more search box overlap
- 📚 **Modern Examples**: Uses current best practices, not deprecated syntax
- 📖 **Latest Docs**: Ubuntu 24.04 LTS (noble) man pages

### Developer Experience

- 🐍 **Python 3.12**: Modern syntax and features
- 📝 **Better Logging**: Enhanced with loguru
- 🐳 **Docker Support**: Works with current images
- 🔧 **Type Hints**: Improved code quality

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone this fork
git clone https://github.com/tobiashochguertel/explainshell.git
cd explainshell

# Start the application
docker compose up --build
```

Visit http://localhost:5000 🎉

### Option 2: Local Python

```bash
# Clone and install
git clone https://github.com/tobiashochguertel/explainshell.git
cd explainshell
pip install -r requirements.txt

# Run the application
python3 runserver.py
```

### Option 3: With Man Pages Database

```bash
# Download man pages database
curl -L -o /tmp/dump.gz https://github.com/idank/explainshell/releases/download/db-dump/dump.gz

# Clone and start
git clone https://github.com/tobiashochguertel/explainshell.git
cd explainshell
docker compose up --build
```

---

## 📚 Documentation

- **[COMMUNITY_INTEGRATION.md](./COMMUNITY_INTEGRATION.md)** - What's integrated and why
- **[PR_ANALYSIS.md](./PR_ANALYSIS.md)** - Comprehensive analysis of all 12 open PRs
- **[Original README](https://github.com/idank/explainshell/blob/master/README.md)** - Original documentation

### Updated Dependencies

```txt
Flask==3.0.3        # was 0.12
nltk==3.9.1         # was 3.4.5
pymongo==4.8.0      # was 3.13.0
bashlex==0.18       # was 0.12
loguru==0.7.2       # new
nose==1.3.7         # same
```

---

## 🤝 Contributing

We welcome contributions! This fork aims to:

1. **Maintain** compatibility with the original project
2. **Integrate** valuable community contributions
3. **Provide** a working version for users needing Python 3

### How to Contribute

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🙏 Credits

### Original Project

**Massive thanks to [@idank](https://github.com/idank)** for creating this incredible tool!

- **Original Repository**: https://github.com/idank/explainshell
- **Live Site**: https://explainshell.com

### Community Contributors

This fork wouldn't exist without these amazing contributors:

- **[@mundanevision20](https://github.com/mundanevision20)** - Python 3.12 migration ([PR #330](https://github.com/idank/explainshell/pull/330))
- **[@cben](https://github.com/cben)** - pymongo compatibility ([PR #323](https://github.com/idank/explainshell/pull/323))
- **[@rugk](https://github.com/rugk)** - Dark mode support ([PR #237](https://github.com/idank/explainshell/pull/237))
- **[@apoorvlathey](https://github.com/apoorvlathey)** - Search box fix ([PR #248](https://github.com/idank/explainshell/pull/248))
- **[@Strahinja](https://github.com/Strahinja)** - Better examples ([PR #293](https://github.com/idank/explainshell/pull/293))
- **[@wesinator](https://github.com/wesinator)** - Updated manpages ([PR #232](https://github.com/idank/explainshell/pull/232))

### Fork Maintainer

**Tobias Hochgürtel** ([@tobiashochguertel](https://github.com/tobiashochguertel))

---

## 📜 License

GPL-3.0 License (same as the original project)

Copyright (C) 2024 Tobias Hochgürtel
Copyright (C) 2013-2024 Idan Kamara

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation.

---

## 🔗 Links

- 🏠 **Original Project**: https://github.com/idank/explainshell
- 🌐 **Live Demo**: https://explainshell.com
- 🐛 **Issues**: Report issues in the [original repo](https://github.com/idank/explainshell/issues) or this fork
- 📊 **PR Analysis**: [PR_ANALYSIS.md](./PR_ANALYSIS.md)

---

## ⚠️ Note to Users

This fork exists to:
1. Help the community use explainshell on modern infrastructure
2. Demonstrate that community PRs work and are valuable
3. Provide an interim solution while the original project is updated

**We encourage you to support the [original project](https://github.com/idank/explainshell)!**

If the original maintainer merges these PRs, this fork may become unnecessary (which would be great! 🎉)

---

<div align="center">

**Made with ❤️ by the open source community**

[⭐ Star this repo](https://github.com/tobiashochguertel/explainshell) | [🐛 Report Bug](https://github.com/tobiashochguertel/explainshell/issues) | [💡 Request Feature](https://github.com/tobiashochguertel/explainshell/issues)

</div>
