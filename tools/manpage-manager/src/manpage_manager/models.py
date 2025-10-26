"""Data models for manpage-manager."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class GitHubAsset(BaseModel):
    """GitHub release asset."""

    name: str
    browser_download_url: HttpUrl
    size: int
    content_type: str
    created_at: datetime
    updated_at: datetime


class GitHubRelease(BaseModel):
    """GitHub release information."""

    tag_name: str
    name: str
    published_at: datetime
    created_at: datetime
    assets: list[GitHubAsset]
    html_url: HttpUrl
    body: Optional[str] = None


class DumpInfo(BaseModel):
    """Database dump information."""

    path: Path
    size_bytes: int
    created_at: Optional[datetime] = None
    source_url: Optional[str] = None
    version: Optional[str] = None

    @property
    def size_mb(self) -> float:
        """Get size in megabytes."""
        return self.size_bytes / (1024 * 1024)

    @property
    def size_human(self) -> str:
        """Get human-readable size."""
        size = self.size_bytes
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"


class DumpStats(BaseModel):
    """Statistics from database dump."""

    total_collections: int = Field(default=0, description="Number of collections")
    manpages_count: int = Field(default=0, description="Number of manpages")
    mappings_count: int = Field(default=0, description="Number of command mappings")
    classifier_count: int = Field(default=0, description="Number of classifier entries")
    total_documents: int = Field(default=0, description="Total documents")

    def __str__(self) -> str:
        """Human-readable statistics."""
        return f"""
Database Statistics:
  Collections: {self.total_collections}
  Manpages: {self.manpages_count:,}
  Mappings: {self.mappings_count:,}
  Classifier: {self.classifier_count:,}
  Total Documents: {self.total_documents:,}
"""


class ImportResult(BaseModel):
    """Result of database import operation."""

    success: bool
    message: str
    collections_imported: int = 0
    documents_imported: int = 0
    duration_seconds: float = 0.0
    errors: list[str] = Field(default_factory=list)
