"""Tests for the IngestorInterface class."""

import pytest

from QuoteEngine import IngestorInterface


class _TextReader(IngestorInterface):
    """Declare a supported extension for interface tests."""

    allowed_extensions = (".txt",)


def test_ingestor_interface_cannot_be_instantiated() -> None:
    """Test that IngestorInterface cannot be instantiated directly."""
    with pytest.raises(TypeError):
        IngestorInterface()


@pytest.mark.parametrize(
    "file_path, expected",
    [
        ("quotes.txt", True),
        ("quotes.TXT", True),
        ("quotes.pdf", False),
        ("quotes.PDF", False),
        ("quotes", False),
    ],
)
def test_can_ingest_accepts_supported_extensions(
    file_path: str, expected: bool
) -> None:
    """Test that can_ingest returns True for supported extensions."""
    assert _TextReader.can_ingest(file_path) == expected
