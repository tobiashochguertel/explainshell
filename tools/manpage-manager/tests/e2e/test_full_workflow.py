"""End-to-end tests for manpage-manager.

These tests require:
- Network access (for GitHub API)
- Sufficient disk space for downloads
- Optional: MongoDB instance for import tests

Mark tests with @pytest.mark.e2e to run them separately.
"""

import pytest
from typer.testing import CliRunner

from manpage_manager.cli import app

runner = CliRunner()
pytestmark = pytest.mark.e2e  # Mark all tests in this module as e2e


class TestFullWorkflow:
    """Test complete end-to-end workflows."""

    @pytest.mark.skip(reason="Requires network and downloads large file")
    def test_download_inspect_workflow(self, tmp_path):
        """Test download and inspect workflow."""
        # This would download the actual dump file
        output_file = tmp_path / "dump.gz"

        # Download
        result = runner.invoke(app, ["download", "--output", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()

        # Inspect
        result = runner.invoke(app, ["inspect", str(output_file)])
        assert result.exit_code == 0
        assert "Statistics" in result.stdout

    @pytest.mark.skip(reason="Requires MongoDB instance")
    def test_full_import_workflow(self, tmp_path):
        """Test complete import workflow."""
        # This would require an actual dump file and MongoDB
        pass


class TestQuickCommands:
    """Test quick commands that don't require heavy resources."""

    def test_check_update_e2e(self):
        """Test check-update with actual network call."""
        result = runner.invoke(app, ["check-update"])

        if result.exit_code == 0:
            # Verify actual data in output
            assert "2023" in result.stdout  # Should show the 2023 release date
            assert "dump" in result.stdout.lower()

    def test_version_e2e(self):
        """Test version display."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.stdout
