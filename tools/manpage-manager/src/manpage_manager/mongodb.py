"""MongoDB import operations."""

import time
from pathlib import Path
from typing import Optional

import sh
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import settings
from .models import ImportResult

console = Console()


class MongoDBImporter:
    """Manager for MongoDB import operations."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 27017,
        database: str = "explainshell",
        use_docker: bool = False,
        docker_service: str = "db",
    ):
        """Initialize MongoDB importer.

        Args:
            host: MongoDB host
            port: MongoDB port
            database: Database name
            use_docker: Whether to use docker-compose exec
            docker_service: Docker service name
        """
        self.host = host
        self.port = port
        self.database = database
        self.use_docker = use_docker
        self.docker_service = docker_service

    def import_dump(self, dump_path: Path, drop_existing: bool = False) -> ImportResult:
        """Import dump into MongoDB.

        Args:
            dump_path: Path to dump.gz file
            drop_existing: Whether to drop existing collections

        Returns:
            ImportResult with import details
        """
        if not dump_path.exists():
            return ImportResult(
                success=False,
                message=f"Dump file not found: {dump_path}",
                errors=[f"File does not exist: {dump_path}"],
            )

        start_time = time.time()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"[cyan]Importing dump into MongoDB ({self.database})...", total=None)

            try:
                if self.use_docker:
                    result = self._import_docker(dump_path, drop_existing)
                else:
                    result = self._import_direct(dump_path, drop_existing)

                duration = time.time() - start_time

                # Parse mongorestore output for stats
                output = str(result)
                collections = output.count("restoring")
                docs = self._extract_document_count(output)

                progress.update(task, completed=True, description="✅ Import complete")

                return ImportResult(
                    success=True,
                    message="Database import completed successfully",
                    collections_imported=collections,
                    documents_imported=docs,
                    duration_seconds=duration,
                )

            except sh.ErrorReturnCode as e:
                duration = time.time() - start_time
                error_msg = str(e.stderr) if hasattr(e, "stderr") else str(e)

                progress.update(task, completed=True, description="❌ Import failed")

                return ImportResult(
                    success=False,
                    message="Database import failed",
                    duration_seconds=duration,
                    errors=[error_msg],
                )

    def _import_docker(self, dump_path: Path, drop: bool) -> str:
        """Import via docker-compose exec.

        Args:
            dump_path: Path to dump file
            drop: Whether to drop collections

        Returns:
            Command output
        """
        logger.info(f"Importing via Docker service '{self.docker_service}'")

        cmd_args = [
            "docker-compose",
            "exec",
            "-T",
            self.docker_service,
            "mongorestore",
            "--archive",
            "--gzip",
            f"--db={self.database}",
        ]

        if drop:
            cmd_args.append("--drop")

        # Read dump file and pipe to docker
        with open(dump_path, "rb") as f:
            result = sh.Command(cmd_args[0])(
                *cmd_args[1:],
                _in=f,
                _err_to_out=True,
            )

        return str(result)

    def _import_direct(self, dump_path: Path, drop: bool) -> str:
        """Import directly to MongoDB.

        Args:
            dump_path: Path to dump file
            drop: Whether to drop collections

        Returns:
            Command output
        """
        logger.info(f"Importing directly to {self.host}:{self.port}/{self.database}")

        cmd_args = [
            f"--host={self.host}",
            f"--port={self.port}",
            f"--db={self.database}",
            f"--archive={dump_path}",
            "--gzip",
        ]

        if drop:
            cmd_args.append("--drop")

        result = sh.mongorestore(*cmd_args, _err_to_out=True)
        return str(result)

    def _extract_document_count(self, output: str) -> int:
        """Extract document count from mongorestore output.

        Args:
            output: mongorestore output

        Returns:
            Number of documents imported
        """
        # Parse lines like "29763 document(s) restored successfully"
        import re

        pattern = r"(\d+)\s+document\(s\)\s+restored"
        matches = re.findall(pattern, output)

        if matches:
            return sum(int(m) for m in matches)

        return 0

    def test_connection(self) -> bool:
        """Test MongoDB connection.

        Returns:
            True if connection successful
        """
        try:
            if self.use_docker:
                sh.docker_compose("exec", "-T", self.docker_service, "mongo", "--version")
            else:
                sh.mongo(
                    f"--host={self.host}",
                    f"--port={self.port}",
                    "--eval",
                    "db.version()",
                )

            logger.success("MongoDB connection successful")
            return True

        except sh.ErrorReturnCode as e:
            logger.error(f"MongoDB connection failed: {e}")
            return False
