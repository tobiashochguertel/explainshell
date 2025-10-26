.PHONY: help install install-dev test lint format clean run-download run-inspect

help:  ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install:  ## Install package with uv
	uv pip install -e .

install-dev:  ## Install with development dependencies
	uv pip install -e ".[dev]"

test:  ## Run tests
	pytest -v

lint:  ## Run linter
	ruff check .

format:  ## Format code
	ruff format .

clean:  ## Clean build artifacts
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run-download:  ## Download latest dump
	manpage-mgr download

run-inspect:  ## Inspect downloaded dump
	manpage-mgr inspect /tmp/dump.gz

run-import-docker:  ## Import dump using docker
	manpage-mgr import /tmp/dump.gz --docker

run-check:  ## Check for updates
	manpage-mgr check-update
