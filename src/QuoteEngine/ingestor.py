"""Select the appropriate reader for a quote file."""

from .csv_ingestor import CsvIngestor
from .docx_ingestor import DocxIngestor
from .ingestor_interface import IngestorInterface
from .pdf_ingestor import PdfIngestor
from .quote_model import QuoteModel
from .txt_ingestor import TxtIngestor


class Ingestor(IngestorInterface):
    """Select the appropriate reader for a quote file."""

    allowed_extensions = (".txt", ".csv", ".docx", ".pdf")

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Select the appropriate reader based on the file extension and parse the file.

        :param path: The path to the quote file.
        :return: A list of QuoteModel instances.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest file with extension: {path}")

        extension = path.split(".")[-1].lower()
        if extension == "txt":
            return TxtIngestor.parse(path)
        elif extension == "csv":
            return CsvIngestor.parse(path)
        elif extension == "docx":
            return DocxIngestor.parse(path)
        elif extension == "pdf":
            return PdfIngestor.parse(path)
        else:
            raise ValueError(f"Unsupported file extension: {extension}")
