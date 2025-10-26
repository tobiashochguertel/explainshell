"""CLI interface using Typer."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .config import settings
from .dump import DumpManager
from .github import GitHubClient
from .logger import setup_logging
from .mongodb import MongoDBImporter

app = typer.Typer(
    name="manpage-mgr",
    help="Modern CLI tool for managing explainshell manpage database dumps",
    add_completion=True,
)

console = Console()


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        console.print(f"manpage-manager version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        "-l",
        help="Set log level (DEBUG, INFO, WARNING, ERROR)",
    ),
):
    """Manpage Manager - Database dump management for explainshell."""
    setup_logging(level=log_level)


@app.command()
def download(
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output path for downloaded dump (default: /tmp/dump.gz)",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing file",
    ),
):
    """Download the latest database dump from GitHub releases."""
    output_path = output or settings.download_path

    if output_path.exists() and not force:
        console.print(f"[yellow]File already exists: {output_path}[/yellow]")
        console.print("[yellow]Use --force to overwrite[/yellow]")
        raise typer.Exit(1)

    async def _download():
        client = GitHubClient()
        asset = await client.get_dump_asset()

        console.print(
            Panel(
                f"[bold]Downloading dump.gz[/bold]\n\n" f"Size: {asset.size / (1024**2):.2f} MB\n" f"Created: {asset.created_at.isoformat()}\n" f"URL: {asset.browser_download_url}",
                title="📥 Download Info",
                border_style="blue",
            )
        )

        downloaded_path = await client.download_asset(asset, output_path)

        console.print(f"\n✅ [green]Download complete: {downloaded_path}[/green]")
        console.print(f"\n💡 Next step: [cyan]manpage-mgr inspect {downloaded_path}[/cyan]")

    try:
        asyncio.run(_download())
    except Exception as e:
        logger.error(f"Download failed: {e}")
        console.print(f"[red]❌ Download failed: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def inspect(
    dump_path: Path = typer.Argument(..., help="Path to dump.gz file"),
):
    """Inspect dump file contents and show statistics."""
    if not dump_path.exists():
        console.print(f"[red]❌ File not found: {dump_path}[/red]")
        raise typer.Exit(1)

    manager = DumpManager()

    # Show file info
    manager.display_info(dump_path)

    # Show statistics
    try:
        console.print("\n[cyan]Analyzing dump contents...[/cyan]")
        stats = manager.inspect(dump_path)

        console.print(
            Panel(
                str(stats),
                title="📊 Database Statistics",
                border_style="green",
            )
        )

        console.print(f"\n💡 Next step: [cyan]manpage-mgr import {dump_path} --docker[/cyan]")

    except Exception as e:
        logger.warning(f"Could not extract statistics: {e}")
        console.print(f"[yellow]⚠️  Could not extract full statistics: {e}[/yellow]")


@app.command()
def import_dump(
    dump_path: Path = typer.Argument(..., help="Path to dump.gz file"),
    docker: bool = typer.Option(
        False,
        "--docker",
        "-d",
        help="Use docker-compose exec for import",
    ),
    host: str = typer.Option(
        "localhost",
        "--host",
        "-h",
        help="MongoDB host (ignored if --docker is used)",
    ),
    port: int = typer.Option(
        27017,
        "--port",
        "-p",
        help="MongoDB port (ignored if --docker is used)",
    ),
    database: str = typer.Option(
        "explainshell",
        "--database",
        "--db",
        help="Database name",
    ),
    drop: bool = typer.Option(
        False,
        "--drop",
        help="Drop existing collections before import",
    ),
    service: str = typer.Option(
        "db",
        "--service",
        "-s",
        help="Docker service name (only with --docker)",
    ),
):
    """Import dump file into MongoDB."""
    if not dump_path.exists():
        console.print(f"[red]❌ File not found: {dump_path}[/red]")
        raise typer.Exit(1)

    importer = MongoDBImporter(
        host=host,
        port=port,
        database=database,
        use_docker=docker,
        docker_service=service,
    )

    # Test connection first
    console.print("[cyan]Testing MongoDB connection...[/cyan]")
    if not importer.test_connection():
        console.print("[red]❌ MongoDB connection failed[/red]")
        raise typer.Exit(1)

    console.print("[green]✅ Connection successful[/green]\n")

    # Perform import
    result = importer.import_dump(dump_path, drop_existing=drop)

    if result.success:
        table = Table(title="✅ Import Results", show_header=True, header_style="bold green")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Collections Imported", str(result.collections_imported))
        table.add_row("Documents Imported", f"{result.documents_imported:,}")
        table.add_row("Duration", f"{result.duration_seconds:.2f} seconds")

        console.print(table)

        console.print(f"\n💡 [green]Database '{database}' is now ready![/green]")
    else:
        console.print(
            Panel(
                f"[bold red]Import Failed[/bold red]\n\n" f"{result.message}\n\n" f"Errors:\n" + "\n".join(f"  • {e}" for e in result.errors),
                title="❌ Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)


@app.command()
def check_update():
    """Check for database dump updates on GitHub."""

    async def _check():
        client = GitHubClient()
        release = await client.get_release()

        table = Table(title="📦 Latest Release Info", show_header=True, header_style="bold blue")
        table.add_column("Property", style="cyan", width=20)
        table.add_column("Value", style="green")

        table.add_row("Release", release.name)
        table.add_row("Tag", release.tag_name)
        table.add_row("Published", release.published_at.strftime("%Y-%m-%d %H:%M:%S UTC"))
        table.add_row("Created", release.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"))
        table.add_row("URL", str(release.html_url))

        console.print(table)

        # Show assets
        if release.assets:
            asset_table = Table(title="📎 Assets", show_header=True)
            asset_table.add_column("Name", style="cyan")
            asset_table.add_column("Size", style="green")
            asset_table.add_column("Content Type", style="yellow")

            for asset in release.assets:
                asset_table.add_row(
                    asset.name,
                    f"{asset.size / (1024**2):.2f} MB",
                    asset.content_type,
                )

            console.print("\n")
            console.print(asset_table)

        # Check age
        import datetime

        age_days = (datetime.datetime.now(datetime.UTC) - release.published_at).days

        if age_days > 365:
            console.print(f"\n[yellow]⚠️  Warning: Dump is {age_days} days old (>1 year)[/yellow]")
        elif age_days > 180:
            console.print(f"\n[yellow]⚠️  Notice: Dump is {age_days} days old (>6 months)[/yellow]")
        else:
            console.print(f"\n[green]✅ Dump is relatively fresh ({age_days} days old)[/green]")

        console.print(f"\n💡 Download with: [cyan]manpage-mgr download[/cyan]")

    try:
        asyncio.run(_check())
    except Exception as e:
        logger.error(f"Failed to check updates: {e}")
        console.print(f"[red]❌ Failed to check updates: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def info(
    dump_path: Optional[Path] = typer.Argument(
        None,
        help="Path to dump file (default: check default location)",
    ),
):
    """Show information about local or default dump file."""
    target = dump_path or settings.download_path

    if not target.exists():
        console.print(f"[yellow]No dump file found at: {target}[/yellow]")
        console.print(f"\n💡 Download with: [cyan]manpage-mgr download[/cyan]")
        raise typer.Exit(1)

    manager = DumpManager()
    manager.display_info(target)


if __name__ == "__main__":
    app()
