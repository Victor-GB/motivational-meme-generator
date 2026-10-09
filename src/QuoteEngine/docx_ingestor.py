"""Read quotes from DOCX documents."""

from zipfile import BadZipFile

import docx
from docx.opc.exceptions import PackageNotFoundError

from .exceptions import IngestorError, UnsupportedFileTypeError
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class DocxIngestor(IngestorInterface):
    """Ingestor for DOCX files containing quotes."""

    allowed_extensions = (".docx",)

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Read valid quotes, skipping malformed or incomplete paragraphs.

        Raise IngestorError when the document cannot be opened or parsed.
        """
        if not cls.can_ingest(path):
            raise UnsupportedFileTypeError(
                f"Cannot ingest file with extension: {path!r}; "
                "expected a .docx file."
            )

        try:
            doc = docx.Document(path)
        except (
            OSError,
            PackageNotFoundError,
            BadZipFile,
            ValueError,
            KeyError,
            SyntaxError,
        ) as exc:
            raise IngestorError(
                f"Could not read DOCX quote file {path!r}: {exc}"
            ) from exc

        quotes: list[QuoteModel] = []
        for para in doc.paragraphs:
            quote = cls._quote_from_line(para.text)
            if quote is not None:
                quotes.append(quote)

        return quotes
