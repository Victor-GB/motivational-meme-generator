"""Select the appropriate reader for a quote file."""

from .csv_ingestor import CsvIngestor
from .docx_ingestor import DocxIngestor
from .exceptions import UnsupportedFileTypeError
from .ingestor_interface import IngestorInterface
from .pdf_ingestor import PdfIngestor
from .quote_model import QuoteModel
from .txt_ingestor import TxtIngestor


class Ingestor(IngestorInterface):
    """Select the appropriate reader for a quote file."""

    ingestors = (TxtIngestor, CsvIngestor, DocxIngestor, PdfIngestor)

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return whether any registered reader accepts the file."""
        return any(ingestor.can_ingest(path) for ingestor in cls.ingestors)

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Delegate parsing to the first reader that accepts the file."""
        for reader in cls.ingestors:
            if reader.can_ingest(path):
                return reader.parse(path)
        raise UnsupportedFileTypeError(f"No registered reader accepts {path}")
