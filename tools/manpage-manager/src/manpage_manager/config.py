"""Configuration management for manpage-manager."""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_prefix="MANPAGE_MGR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # GitHub settings
    github_owner: str = Field(default="idank", description="GitHub repository owner")
    github_repo: str = Field(default="explainshell", description="GitHub repository name")
    github_release_tag: str = Field(default="db-dump", description="Release tag for dump")

    # Download settings
    download_dir: Path = Field(default=Path("/tmp"), description="Default download directory")
    dump_filename: str = Field(default="dump.gz", description="Dump file name")

    # MongoDB settings
    mongo_host: str = Field(default="localhost", description="MongoDB host")
    mongo_port: int = Field(default=27017, description="MongoDB port")
    mongo_db: str = Field(default="explainshell", description="Database name")

    # Docker settings
    docker_compose_file: Optional[Path] = Field(default=None, description="Path to docker-compose.yml")
    docker_service_name: str = Field(default="db", description="MongoDB service name in compose")

    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_file: Optional[Path] = Field(default=None, description="Log file path")

    @property
    def github_api_url(self) -> str:
        """Get GitHub API URL for releases."""
        return f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/releases/tags/{self.github_release_tag}"

    @property
    def download_path(self) -> Path:
        """Get full download path."""
        return self.download_dir / self.dump_filename


settings = Settings()
