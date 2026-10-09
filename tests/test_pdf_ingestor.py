"""Test the pdf ingestor class."""

import pytest

from QuoteEngine import (
    IngestorError,
    PdfIngestor,
    QuoteModel,
    UnsupportedFileTypeError,
)


def test_parse_supplied_dog_quotes_pdf() -> None:
    """Test that PdfIngestor correctly parses a PDF file with quotes."""
    path = "src/_data/DogQuotes/DogQuotesPDF.pdf"

    quotes = PdfIngestor.parse(path)

    assert all(isinstance(quote, QuoteModel) for quote in quotes), (
        "All items should be instances of QuoteModel."
    )
    quotes_r = [
        (quote.body, quote.author)
        for quote in quotes
        if isinstance(quote, QuoteModel)
    ]
    assert quotes_r == [
        ("Treat yo self", "Fluffles"),
        ("Life is like a box of treats", "Forrest Pup"),
        ("It's the size of the fight in the dog", "Bark Twain"),
    ]


def test_parse_supplied_simple_lines_pdf() -> None:
    """Test that PdfIngestor correctly parses a pdf file with simple lines."""
    path = "src/_data/SimpleLines/SimpleLines.pdf"
    quotes = PdfIngestor.parse(path)
    assert all(isinstance(quote, QuoteModel) for quote in quotes), (
        "All items should be instances of QuoteModel."
    )
    quotes_r = [
        (quote.body, quote.author)
        for quote in quotes
        if isinstance(quote, QuoteModel)
    ]
    assert quotes_r == [
        ("Line 1", "Author 1"),
        ("Line 2", "Author 2"),
        ("Line 3", "Author 3"),
        ("Line 4", "Author 4"),
        ("Line 5", "Author 5"),
    ]


def test_parse_rejects_unsupported_file_extension() -> None:
    """Reject unsupported file extensions."""
    with pytest.raises(UnsupportedFileTypeError):
        PdfIngestor.parse("quotes.txt")


def test_parse_missing_pdf_raises_conversion_error() -> None:
    """Report conversion failure when the PDF does not exist."""
    with pytest.raises(IngestorError):
        PdfIngestor.parse("src/_data/DogQuotes/missing.pdf")
