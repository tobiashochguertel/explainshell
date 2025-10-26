"""Test utilities and helper functions."""


def create_mock_bson_dump(path, num_docs=100):
    """Create a mock BSON dump file for testing.

    Args:
        path: Path to create the dump file
        num_docs: Number of mock documents to include
    """
    import gzip

    # Create a simple gzip file with mock data
    with gzip.open(path, "wb") as f:
        for i in range(num_docs):
            # Write some mock BSON-like data
            mock_doc = f"document_{i}".encode()
            f.write(mock_doc + b"\n")


def assert_valid_download_output(output: str):
    """Assert that download output contains expected elements.

    Args:
        output: The stdout from download command
    """
    # Should show progress or completion
    assert any(keyword in output.lower() for keyword in ["download", "complete", "success", "%"])


def assert_valid_inspect_output(output: str):
    """Assert that inspect output contains expected elements.

    Args:
        output: The stdout from inspect command
    """
    # Should show statistics or file info
    assert any(keyword in output.lower() for keyword in ["statistics", "size", "collections", "documents"])
