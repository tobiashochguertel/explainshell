"""Unit tests for data models."""

from datetime import datetime
from pathlib import Path

import pytest
from pydantic import HttpUrl, ValidationError

from manpage_manager.models import (
    DumpInfo,
    DumpStats,
    GitHubAsset,
    GitHubRelease,
    ImportResult,
)


class TestDumpInfo:
    """Test DumpInfo model."""

    def test_create_dump_info(self, tmp_path):
        """Test creating dump info."""
        dump_file = tmp_path / "test.gz"
        dump_file.write_bytes(b"test data" * 1000)

        info = DumpInfo(
            path=dump_file,
            size_bytes=9000,
            created_at=datetime.now(),
            source_url="https://example.com/dump.gz",
        )

        assert info.path == dump_file
        assert info.size_bytes == 9000
        assert info.size_mb == pytest.approx(9000 / (1024 * 1024))

    def test_size_human_readable(self, tmp_path):
        """Test human-readable size formatting."""
        dump_file = tmp_path / "test.gz"

        # Test bytes
        info = DumpInfo(path=dump_file, size_bytes=512)
        assert "B" in info.size_human

        # Test KB
        info = DumpInfo(path=dump_file, size_bytes=2048)
        assert "KB" in info.size_human

        # Test MB
        info = DumpInfo(path=dump_file, size_bytes=2 * 1024 * 1024)
        assert "MB" in info.size_human

        # Test GB
        info = DumpInfo(path=dump_file, size_bytes=3 * 1024 * 1024 * 1024)
        assert "GB" in info.size_human


class TestDumpStats:
    """Test DumpStats model."""

    def test_create_dump_stats(self):
        """Test creating dump statistics."""
        stats = DumpStats(
            total_collections=3,
            manpages_count=29763,
            mappings_count=42069,
            classifier_count=517,
            total_documents=72349,
        )

        assert stats.total_collections == 3
        assert stats.manpages_count == 29763
        assert stats.total_documents == 72349

    def test_dump_stats_string_representation(self):
        """Test string representation of stats."""
        stats = DumpStats(
            total_collections=3,
            manpages_count=100,
            mappings_count=200,
            classifier_count=50,
            total_documents=350,
        )

        str_repr = str(stats)
        assert "Collections: 3" in str_repr
        assert "Manpages: 100" in str_repr
        assert "Total Documents: 350" in str_repr


class TestGitHubModels:
    """Test GitHub-related models."""

    def test_github_asset(self):
        """Test GitHubAsset model."""
        asset = GitHubAsset(
            name="dump.gz",
            browser_download_url="https://github.com/test/dump.gz",
            size=1000000,
            content_type="application/gzip",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert asset.name == "dump.gz"
        assert asset.size == 1000000
        assert "github.com" in str(asset.browser_download_url)

    def test_github_release(self):
        """Test GitHubRelease model."""
        now = datetime.now()
        release = GitHubRelease(
            tag_name="v1.0.0",
            name="Release 1.0.0",
            published_at=now,
            created_at=now,
            assets=[],
            html_url="https://github.com/test/releases/tag/v1.0.0",
        )

        assert release.tag_name == "v1.0.0"
        assert release.name == "Release 1.0.0"
        assert len(release.assets) == 0


class TestImportResult:
    """Test ImportResult model."""

    def test_successful_import(self):
        """Test successful import result."""
        result = ImportResult(
            success=True,
            message="Import completed",
            collections_imported=3,
            documents_imported=72349,
            duration_seconds=45.2,
        )

        assert result.success is True
        assert result.collections_imported == 3
        assert result.documents_imported == 72349
        assert result.duration_seconds == pytest.approx(45.2)
        assert len(result.errors) == 0

    def test_failed_import(self):
        """Test failed import result."""
        result = ImportResult(
            success=False,
            message="Import failed",
            duration_seconds=10.5,
            errors=["Connection error", "Timeout"],
        )

        assert result.success is False
        assert len(result.errors) == 2
        assert "Connection error" in result.errors
