"""Text file ingestor for quotes."""

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class TxtIngestor(IngestorInterface):
    """Ingestor for text files containing quotes."""

    allowed_extensions = (".txt",)

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Parse a text file and return a list of QuoteModel instances.

        :param path: The path to the text file.
        :return: A list of QuoteModel instances.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest file with extension: {path}")

        quotes = []
        with open(path, encoding="utf-8-sig") as file:
            for line in file:
                line = line.strip()
                if line:
                    body, author = line.rsplit(" - ", 1)
                    body = (
                        body.strip()
                    )  # Remove any leading/trailing whitespace from body
                    if len(body) >= 2 and body.startswith('"') and body.endswith('"'):
                        body = body[1:-1]  # Remove surrounding quotes if present
                    author = (
                        author.strip()
                    )  # Remove any leading/trailing whitespace from author
                    quotes.append(QuoteModel(body, author))
        return quotes
