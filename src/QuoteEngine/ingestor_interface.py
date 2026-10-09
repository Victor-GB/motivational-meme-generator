"""Define the common interface for quote-file readers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar

from .quote_model import QuoteModel


class IngestorInterface(ABC):
    """Specify the operations supported by quote-file readers."""

    allowed_extensions: ClassVar[tuple[str, ...]] = ()

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the given file path can be ingested by this reader.

        :param path: The file path to check.
        :return: True if the file extension is allowed, False otherwise.
        """
        ext = Path(path).suffix.lower()
        return ext in cls.allowed_extensions

    @staticmethod
    def _quote_from_line(line: str) -> QuoteModel | None:
        """Build a quote from a valid line, or return None."""
        line = line.strip()
        if " - " not in line:
            return None
        body, author = line.rsplit(" - ", 1)
        body = body.strip()
        author = author.strip()

        if len(body) >= 2 and body.startswith('"') and body.endswith('"'):
            body = body[1:-1].strip()

        if not body or not author:
            return None

        return QuoteModel(body, author)

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Parse the given file and return a list of QuoteModel instances.

        :param path: The file path to parse.
        :return: A list of QuoteModel instances.
        """
        raise NotImplementedError(
            "Subclasses must implement the parse method."
        )
