"""GitHub API interactions."""

import httpx
from loguru import logger
from rich.console import Console

from .config import settings
from .models import GitHubAsset, GitHubRelease

console = Console()


class GitHubClient:
    """Client for GitHub API operations."""

    def __init__(self, timeout: float = 30.0):
        """Initialize GitHub client.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "manpage-manager/0.1.0",
        }

    async def get_release(self) -> GitHubRelease:
        """Fetch release information from GitHub.

        Returns:
            GitHubRelease object with release details

        Raises:
            httpx.HTTPError: If request fails
        """
        url = settings.github_api_url
        logger.info(f"Fetching release info from {url}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers=self.headers, follow_redirects=True)
            response.raise_for_status()
            data = response.json()

        release = GitHubRelease(**data)
        logger.info(f"Found release '{release.name}' published at {release.published_at.isoformat()}")
        return release

    async def download_asset(self, asset: GitHubAsset, output_path: str | Path) -> Path:
        """Download a release asset.

        Args:
            asset: GitHubAsset to download
            output_path: Where to save the file

        Returns:
            Path to downloaded file

        Raises:
            httpx.HTTPError: If download fails
        """
        from pathlib import Path

        from rich.progress import (
            BarColumn,
            DownloadColumn,
            Progress,
            TextColumn,
            TimeRemainingColumn,
            TransferSpeedColumn,
        )

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Downloading {asset.name} ({asset.size / (1024**2):.2f} MB)")

        async with httpx.AsyncClient(timeout=300.0, follow_redirects=True) as client:
            async with client.stream("GET", str(asset.browser_download_url)) as response:
                response.raise_for_status()

                total = int(response.headers.get("content-length", 0))

                with Progress(
                    TextColumn("[bold blue]{task.description}"),
                    BarColumn(bar_width=None),
                    "[progress.percentage]{task.percentage:>3.1f}%",
                    "•",
                    DownloadColumn(),
                    "•",
                    TransferSpeedColumn(),
                    "•",
                    TimeRemainingColumn(),
                    console=console,
                ) as progress:
                    task = progress.add_task(f"Downloading {asset.name}", total=total)

                    with output.open("wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=8192):
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))

        logger.success(f"Downloaded to {output}")
        return output

    async def get_dump_asset(self) -> GitHubAsset:
        """Get the dump.gz asset from the release.

        Returns:
            GitHubAsset for dump.gz

        Raises:
            ValueError: If dump.gz not found in release
        """
        release = await self.get_release()

        for asset in release.assets:
            if asset.name == "dump.gz":
                return asset

        raise ValueError("dump.gz asset not found in release")
