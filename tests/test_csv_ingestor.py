"""Test the csv ingestor class."""

import pytest

from QuoteEngine import CsvIngestor, QuoteModel


def test_parse_supplied_dog_quotes_csv() -> None:
    """Test that CsvIngestor correctly parses a CSV file with quotes."""
    path = "src/_data/DogQuotes/DogQuotesCSV.csv"

    quotes = CsvIngestor.parse(path)
    assert all(isinstance(quote, QuoteModel) for quote in quotes), (
        "All items should be instances of QuoteModel."
    )
    quotes_r = [
        (quote.body, quote.author) for quote in quotes if isinstance(quote, QuoteModel)
    ]

    assert quotes_r == [
        ("Chase the mailman", "Skittle"),
        ("When in doubt, go shoe-shopping", "Mr. Paws"),
    ]


def test_parse_supplied_simple_lines_csv() -> None:
    """Test that CsvIngestor correctly parses a CSV file with simple lines."""
    path = "src/_data/SimpleLines/SimpleLines.csv"

    quotes = CsvIngestor.parse(path)
    assert all(isinstance(quote, QuoteModel) for quote in quotes), (
        "All items should be instances of QuoteModel."
    )
    quotes_r = [
        (quote.body, quote.author) for quote in quotes if isinstance(quote, QuoteModel)
    ]

    assert quotes_r == [
        ("Line 1", "Author 1"),
        ("Line 2", "Author 2"),
        ("Line 3", "Author 3"),
        ("Line 4", "Author 4"),
        ("Line 5", "Author 5"),
    ]


def test_parse_rejects_unsupported_file_extension() -> None:
    """Test that CsvIngestor raises a ValueError for unsupported file extensions."""
    with pytest.raises(ValueError):
        CsvIngestor.parse("quotes.pdf")
