"""Represent quotes with their bodies and authors."""


class QuoteModel:
    """A simple QuoteModel class to represent a quote with its body and author."""

    def __init__(self, body: str, author: str) -> None:
        """
        Initialize a QuoteModel instance.

        :param body: The text of the quote.
        :param author: The author of the quote.
        """
        self.body = body
        self.author = author

    def __str__(self) -> str:
        """
        Return a string representation of the QuoteModel instance.

        :return: A string in the format '"<body>" - <author>'.
        """
        return f'"{self.body}" - {self.author}'
