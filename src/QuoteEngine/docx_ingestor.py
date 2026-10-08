"""Read quotes from DOCX documents."""

import docx

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class DocxIngestor(IngestorInterface):
    """Ingestor for DOCX files containing quotes."""

    allowed_extensions = (".docx",)

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Parse a DOCX file and return a list of QuoteModel instances.

        :param path: The path to the DOCX file.
        :return: A list of QuoteModel instances.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest file with extension: {path}")

        quotes = []
        doc = docx.Document(path)
        for para in doc.paragraphs:
            line = para.text.strip()
            if line:
                body, author = line.rsplit(" - ", 1)
                body = body.strip()  # Remove any leading/trailing whitespace from body
                if len(body) >= 2 and body.startswith('"') and body.endswith('"'):
                    body = body[1:-1]  # Remove surrounding quotes if present
                author = (
                    author.strip()
                )  # Remove any leading/trailing whitespace from author
                quotes.append(QuoteModel(body, author))

        return quotes
