"""Provide quote models and readers for supported file formats."""

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel

__all__ = ["QuoteModel", "IngestorInterface"]
