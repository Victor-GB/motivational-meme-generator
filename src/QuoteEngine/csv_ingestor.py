"""CSV file ingestor for quotes."""

import pandas as pd

from .exceptions import IngestorError, UnsupportedFileTypeError
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
            raise UnsupportedFileTypeError(
                f"CSV reader cannot ingest {path!r}; expected a .csv file"
            )
        try:
            data = pd.read_csv(
                path, encoding="utf-8-sig", dtype=str, keep_default_na=False
            )

        except (
            OSError,
            UnicodeDecodeError,
            pd.errors.ParserError,
            pd.errors.EmptyDataError,
        ) as exc:
            raise IngestorError(
                f"Could not read CSV quote file {path!r}: {exc}"
            ) from exc
        if not {"body", "author"}.issubset(data.columns):
            raise IngestorError(
                f"CSV quote file {path!r} requires body and author columns."
            )

        quotes: list[QuoteModel] = []
        for _, row in data.iterrows():
            body = str(row["body"]).strip()
            author = str(row["author"]).strip()
            if body and author:
                quotes.append(QuoteModel(body, author))
        return quotes
