"""Provide quote models and readers for supported file formats."""

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from .txt_ingestor import TxtIngestor

__all__ = ["QuoteModel", "IngestorInterface", "TxtIngestor"]
