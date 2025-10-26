"""Shared test fixtures for manpage-manager tests."""

import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_dump_path(temp_dir: Path) -> Path:
    """Create a sample dump file for testing."""
    dump_file = temp_dir / "test_dump.gz"
    # Create a minimal gzip file
    import gzip

    with gzip.open(dump_file, "wb") as f:
        f.write(b"test data")
    return dump_file


@pytest.fixture
def mock_github_release():
    """Mock GitHub release data."""
    return {
        "tag_name": "db-dump",
        "name": "Database dump",
        "published_at": "2023-02-13T16:57:17Z",
        "created_at": "2023-02-13T16:51:00Z",
        "html_url": "https://github.com/idank/explainshell/releases/tag/db-dump",
        "body": "Database dump for explainshell",
        "assets": [
            {
                "name": "dump.gz",
                "browser_download_url": "https://github.com/idank/explainshell/releases/download/db-dump/dump.gz",
                "size": 245678901,
                "content_type": "application/gzip",
                "created_at": "2023-02-13T16:51:00Z",
                "updated_at": "2023-02-13T16:57:17Z",
            }
        ],
    }


@pytest.fixture
def mock_dump_stats():
    """Mock dump statistics."""
    from manpage_manager.models import DumpStats

    return DumpStats(
        total_collections=3,
        manpages_count=29763,
        mappings_count=42069,
        classifier_count=517,
        total_documents=72349,
    )
