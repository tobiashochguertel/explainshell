"""Unit tests for CLI interface."""

import pytest
from typer.testing import CliRunner

from manpage_manager.cli import app

runner = CliRunner()


class TestCLIBasics:
    """Test basic CLI functionality."""

    def test_version(self):
        """Test version command."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "manpage-manager version" in result.stdout

    def test_help(self):
        """Test help command."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "manpage-mgr" in result.stdout
        assert "database dump" in result.stdout.lower()

    def test_download_help(self):
        """Test download command help."""
        result = runner.invoke(app, ["download", "--help"])
        assert result.exit_code == 0
        assert "Download" in result.stdout

    def test_inspect_help(self):
        """Test inspect command help."""
        result = runner.invoke(app, ["inspect", "--help"])
        assert result.exit_code == 0
        assert "Inspect" in result.stdout

    def test_import_help(self):
        """Test import command help."""
        result = runner.invoke(app, ["import-dump", "--help"])
        assert result.exit_code == 0
        assert "Import" in result.stdout

    def test_check_update_help(self):
        """Test check-update command help."""
        result = runner.invoke(app, ["check-update", "--help"])
        assert result.exit_code == 0
        assert "Check" in result.stdout

    def test_info_help(self):
        """Test info command help."""
        result = runner.invoke(app, ["info", "--help"])
        assert result.exit_code == 0
        assert "information" in result.stdout.lower()


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_inspect_nonexistent_file(self):
        """Test inspect with non-existent file."""
        result = runner.invoke(app, ["inspect", "/nonexistent/file.gz"])
        assert result.exit_code == 1
        assert "not found" in result.stdout.lower()

    def test_import_nonexistent_file(self):
        """Test import with non-existent file."""
        result = runner.invoke(app, ["import-dump", "/nonexistent/file.gz", "--docker"])
        assert result.exit_code == 1
        assert "not found" in result.stdout.lower()

    def test_info_nonexistent_file(self):
        """Test info with non-existent file."""
        result = runner.invoke(app, ["info", "/nonexistent/file.gz"])
        assert result.exit_code == 1


class TestCLILogLevels:
    """Test CLI log level configuration."""

    def test_log_level_debug(self):
        """Test debug log level."""
        result = runner.invoke(app, ["--log-level", "DEBUG", "--help"])
        assert result.exit_code == 0

    def test_log_level_info(self):
        """Test info log level."""
        result = runner.invoke(app, ["--log-level", "INFO", "--help"])
        assert result.exit_code == 0

    def test_log_level_warning(self):
        """Test warning log level."""
        result = runner.invoke(app, ["--log-level", "WARNING", "--help"])
        assert result.exit_code == 0

    def test_log_level_error(self):
        """Test error log level."""
        result = runner.invoke(app, ["--log-level", "ERROR", "--help"])
        assert result.exit_code == 0
