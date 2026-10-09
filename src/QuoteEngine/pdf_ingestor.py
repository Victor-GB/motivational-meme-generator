"""PDF Ingestor for parsing PDF files containing quotes."""

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from .exceptions import IngestorError, UnsupportedFileTypeError
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from .txt_ingestor import TxtIngestor


class PdfIngestor(IngestorInterface):
    """Ingestor for PDF files containing quotes."""

    allowed_extensions = (".pdf",)

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Read quotes form a PDF converted to text by Xpdf.

        Raise IngestorError when the conversion or text reading fails.
        """
        if not cls.can_ingest(path):
            raise UnsupportedFileTypeError(
                f"PDF reader cannot ingest {path!r}; expected a .pdf file"
            )

        try:
            with TemporaryDirectory() as temp_dir:
                tmp = str(Path(temp_dir) / "quotes.txt")
                subprocess.run(
                    ["pdftotext", "-layout", path, tmp],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                return TxtIngestor.parse(tmp)
        except subprocess.CalledProcessError as exc:
            reason = exc.stderr.strip() if exc.stderr else str(exc)
            raise IngestorError(
                f"Could not convert PDF quote file {path!r}: {reason}"
            ) from exc
        except (OSError, IngestorError) as exc:
            raise IngestorError(
                f"Could not read PDF quote file {path!r}: {exc}"
            ) from exc
