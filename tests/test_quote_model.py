"""Test quote storage and string representation."""

from QuoteEngine import QuoteModel


def test_quote_model_stores_body_and_author() -> None:
    """Test that QuoteModel correctly stores the body and author."""
    body = "Life is what happens when you're busy making other plans."
    author = "John Lennon"
    quote = QuoteModel(body, author)

    assert quote.body == body
    assert quote.author == author


def test_quote_model_str_representation() -> None:
    """Test the string representation of QuoteModel."""
    body = "Be yourself; everyone else is already taken."
    author = "Oscar Wilde"
    quote = QuoteModel(body, author)

    assert (
        str(quote)
        == '"Be yourself; everyone else is already taken." - Oscar Wilde'
    )
