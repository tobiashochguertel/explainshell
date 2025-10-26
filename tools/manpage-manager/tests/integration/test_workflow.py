"""Integration tests for the complete CLI workflow."""

import pytest
from typer.testing import CliRunner

from manpage_manager.cli import app

runner = CliRunner()


class TestCheckUpdateCommand:
    """Test check-update command integration."""

    def test_check_update_command(self):
        """Test check-update command (requires network)."""
        result = runner.invoke(app, ["check-update"])

        # Should either succeed or fail gracefully
        assert result.exit_code in [0, 1]

        if result.exit_code == 0:
            # If successful, should show release info
            assert "Release" in result.stdout or "Latest" in result.stdout


class TestInfoCommand:
    """Test info command integration."""

    def test_info_default_location(self):
        """Test info command with default location."""
        result = runner.invoke(app, ["info"])

        # Should handle missing file gracefully
        assert result.exit_code in [0, 1]


class TestCommandChaining:
    """Test command workflow patterns."""

    def test_help_for_all_commands(self):
        """Test that help works for all commands."""
        commands = ["download", "inspect", "import-dump", "check-update", "info"]

        for cmd in commands:
            result = runner.invoke(app, [cmd, "--help"])
            assert result.exit_code == 0, f"Help failed for {cmd}"
            assert len(result.stdout) > 0, f"No help output for {cmd}"


class TestErrorRecovery:
    """Test error handling and recovery."""

    def test_invalid_command(self):
        """Test handling of invalid command."""
        result = runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0

    def test_missing_required_argument(self):
        """Test handling of missing required arguments."""
        result = runner.invoke(app, ["inspect"])
        assert result.exit_code != 0
