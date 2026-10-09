"""Test the docx ingestor class."""

import pytest

from QuoteEngine import DocxIngestor, QuoteModel, UnsupportedFileTypeError


def test_parse_supplied_dog_quotes_docx() -> None:
    """Test that DocxIngestor correctly parses a DOCX file with quotes."""
    path = "src/_data/DogQuotes/DogQuotesDOCX.docx"

    quotes = DocxIngestor.parse(path)
    assert all(isinstance(quote, QuoteModel) for quote in quotes), (
        "All items should be instances of QuoteModel."
    )
    quotes_r = [
        (quote.body, quote.author)
        for quote in quotes
        if isinstance(quote, QuoteModel)
    ]

    assert quotes_r == [
        ("Bark like no one’s listening", "Rex"),
        ("RAWRGWAWGGR", "Chewy"),
        ("Life is like peanut butter: crunchy", "Peanut"),
        ("Channel your inner husky", "Tiny"),
    ]


def test_parse_supplied_simple_lines_docx() -> None:
    """Test ßDocxIngestor correctly parses a docx file with simple lines."""
    path = "src/_data/SimpleLines/SimpleLines.docx"

    quotes = DocxIngestor.parse(path)
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
    """Tests rejects unsupported file extensions."""
    with pytest.raises(UnsupportedFileTypeError):
        DocxIngestor.parse("quotes.pdf")
