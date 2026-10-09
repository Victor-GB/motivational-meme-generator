"""tests the TxtIngestor class."""

import pytest

from QuoteEngine import QuoteModel, TxtIngestor, UnsupportedFileTypeError


def test_pars_supplied_dog_quotes() -> None:
    """Test that TxtIngestor correctly parses a text file with quotes."""
    path = "src/_data/DogQuotes/DogQuotesTXT.txt"

    quotes = TxtIngestor.parse(path)
    assert all(isinstance(quote, QuoteModel) for quote in quotes), (
        "All items should be instances of QuoteModel."
    )
    quotes_r = [
        (quote.body, quote.author)
        for quote in quotes
        if isinstance(quote, QuoteModel)
    ]

    assert quotes_r == [
        ("To bork or not to bork", "Bork"),
        ("He who smelt it...", "Stinky"),
    ]


def test_parse_supplied_simple_lines() -> None:
    """Test that TxtIngestor correctly parses a text file with simple lines."""
    path = "src/_data/SimpleLines/SimpleLines.txt"

    quotes = TxtIngestor.parse(path)
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
        TxtIngestor.parse("quotes.pdf")
