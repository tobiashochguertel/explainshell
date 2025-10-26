"""Unit tests for configuration management."""

import os
from pathlib import Path

import pytest

from manpage_manager.config import Settings


class TestSettings:
    """Test settings configuration."""

    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()
        assert settings.github_owner == "idank"
        assert settings.github_repo == "explainshell"
        assert settings.github_release_tag == "db-dump"
        assert settings.mongo_host == "localhost"
        assert settings.mongo_port == 27017
        assert settings.mongo_db == "explainshell"

    def test_github_api_url(self):
        """Test GitHub API URL construction."""
        settings = Settings()
        url = settings.github_api_url
        assert "api.github.com" in url
        assert "idank" in url
        assert "explainshell" in url
        assert "db-dump" in url

    def test_download_path(self):
        """Test download path construction."""
        settings = Settings()
        path = settings.download_path
        assert isinstance(path, Path)
        assert path.name == "dump.gz"

    def test_env_override(self, monkeypatch):
        """Test environment variable override."""
        monkeypatch.setenv("MANPAGE_MGR_GITHUB_OWNER", "test-owner")
        monkeypatch.setenv("MANPAGE_MGR_GITHUB_REPO", "test-repo")
        monkeypatch.setenv("MANPAGE_MGR_MONGO_PORT", "27018")

        settings = Settings()
        assert settings.github_owner == "test-owner"
        assert settings.github_repo == "test-repo"
        assert settings.mongo_port == 27018

    def test_custom_download_dir(self, monkeypatch, tmp_path):
        """Test custom download directory."""
        monkeypatch.setenv("MANPAGE_MGR_DOWNLOAD_DIR", str(tmp_path))
        settings = Settings()
        assert settings.download_dir == tmp_path

    def test_log_level_setting(self, monkeypatch):
        """Test log level configuration."""
        monkeypatch.setenv("MANPAGE_MGR_LOG_LEVEL", "DEBUG")
        settings = Settings()
        assert settings.log_level == "DEBUG"
