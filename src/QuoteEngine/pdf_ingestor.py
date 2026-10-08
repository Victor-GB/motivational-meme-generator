"""PDF Ingestor for parsing PDF files containing quotes."""

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from .txt_ingestor import TxtIngestor


class PdfIngestor(IngestorInterface):
    """Ingestor for PDF files containing quotes."""

    allowed_extensions = (".pdf",)

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Parse a PDF file and return a list of QuoteModel instances.

        :param path: The path to the PDF file.
        :return: A list of QuoteModel instances.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest file with extension: {path}")

        with TemporaryDirectory() as temp_dir:
            tmp = str(Path(temp_dir) / "quotes.txt")
            subprocess.run(["pdftotext", "-layout", path, tmp], check=True)
            return TxtIngestor.parse(tmp)
