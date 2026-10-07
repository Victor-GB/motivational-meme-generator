"""CSV file ingestor for quotes."""

import csv

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class CsvIngestor(IngestorInterface):
    """Ingestor for CSV files containing quotes."""

    allowed_extensions = (".csv",)

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Parse a CSV file and return a list of QuoteModel instances.

        :param path: The path to the CSV file.
        :return: A list of QuoteModel instances.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest file with extension: {path}")

        quotes = []
        with open(path, encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                body = row["body"].strip()
                author = row["author"].strip()
                if body and author:
                    quotes.append(QuoteModel(body, author))
        return quotes
