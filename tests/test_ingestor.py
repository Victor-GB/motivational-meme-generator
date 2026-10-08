"""Test quote reader selection through the coordinating ingestor."""

from pytest import mark

from QuoteEngine import Ingestor, QuoteModel


@mark.parametrize("extension", ["txt", "csv", "docx", "pdf"])
def test_selects_matching_reader(extension: str) -> None:
    """Test that Ingestor correctly selects the matching reader for each file type."""
    path = f"src/_data/SimpleLines/SimpleLines.{extension}"
    quotes = Ingestor.parse(path)
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
