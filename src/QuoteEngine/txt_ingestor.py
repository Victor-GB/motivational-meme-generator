"""Text file ingestor for quotes."""

from .exceptions import IngestorError, UnsupportedFileTypeError
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class TxtIngestor(IngestorInterface):
    """Ingestor for text files containing quotes."""

    allowed_extensions = (".txt",)

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Read valid quotes, skipping malformed or incomplete lines.

        Raise IngestorError when the file cannot be read or decoded.
        """
        if not cls.can_ingest(path):
            raise UnsupportedFileTypeError(
                f"TXT reader cannot ingest {path}; expected a .txt file"
            )

        quotes: list[QuoteModel] = []
        try:
            with open(path, encoding="utf-8-sig") as file:
                for line in file:
                    quote = cls._quote_from_line(line)
                    if quote is not None:
                        quotes.append(quote)
        except (OSError, UnicodeDecodeError) as exc:
            raise IngestorError(
                f"Could not read TXT quote file {path!r}: {exc}"
            ) from exc
        return quotes
