"""Unit tests for dump management."""

import gzip
from pathlib import Path

import pytest

from manpage_manager.dump import DumpManager
from manpage_manager.models import DumpInfo


class TestDumpManager:
    """Test DumpManager class."""

    @pytest.fixture
    def manager(self):
        """Create a DumpManager instance."""
        return DumpManager()

    @pytest.fixture
    def valid_dump(self, tmp_path):
        """Create a valid gzip dump file."""
        dump_file = tmp_path / "valid_dump.gz"
        with gzip.open(dump_file, "wb") as f:
            f.write(b"test data for dump file" * 100)
        return dump_file

    def test_get_info(self, manager, valid_dump):
        """Test getting dump information."""
        info = manager.get_info(valid_dump)

        assert isinstance(info, DumpInfo)
        assert info.path == valid_dump
        assert info.size_bytes > 0

    def test_get_info_nonexistent_file(self, manager, tmp_path):
        """Test getting info for non-existent file."""
        nonexistent = tmp_path / "nonexistent.gz"

        with pytest.raises(FileNotFoundError):
            manager.get_info(nonexistent)

    def test_validate_valid_dump(self, manager, valid_dump):
        """Test validating a valid dump file."""
        is_valid = manager.validate(valid_dump)
        assert is_valid is True

    def test_validate_invalid_dump(self, manager, tmp_path):
        """Test validating an invalid dump file."""
        invalid_dump = tmp_path / "invalid.gz"
        # Write non-gzip data
        invalid_dump.write_bytes(b"not a gzip file")

        is_valid = manager.validate(invalid_dump)
        assert is_valid is False

    def test_validate_nonexistent_file(self, manager, tmp_path):
        """Test validating non-existent file."""
        nonexistent = tmp_path / "nonexistent.gz"

        is_valid = manager.validate(nonexistent)
        assert is_valid is False

    def test_display_info_no_crash(self, manager, valid_dump, capsys):
        """Test that display_info doesn't crash."""
        # This should not raise an exception
        manager.display_info(valid_dump)

        # Check that something was printed
        captured = capsys.readouterr()
        assert len(captured.out) > 0
