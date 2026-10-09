"""Generate a meme given an path and a quote."""

import os
import random
from argparse import ArgumentParser
from pathlib import Path

from MemeEngine import MemeEngine, MemeEngineError
from QuoteEngine import Ingestor, IngestorError, QuoteModel

SRC_DIR = Path(__file__).resolve().parent


def generate_meme(
    path: str | None = None,
    body: str | None = None,
    author: str | None = None,
) -> str:
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        images = SRC_DIR / "_data" / "photos" / "dog/"
        imgs = []
        for root, _, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        if not imgs:
            raise MemeEngineError(
                f"No source images found in {str(images)!r}."
            )
        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = [
            str(SRC_DIR / "_data" / "DogQuotes" / name)
            for name in (
                "DogQuotesTXT.txt",
                "DogQuotesDOCX.docx",
                "DogQuotesPDF.pdf",
                "DogQuotesCSV.csv",
            )
        ]
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))
        if not quotes:
            raise IngestorError("No valid quotes found in the quote files.")
        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError("Author is required when body is supplied.")
        quote = QuoteModel(body, author)

    meme = MemeEngine(str(SRC_DIR.parent / "tmp"))
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Generate a meme from an image and quote."
    )
    parser.add_argument("--path", help="Path to an image file.")
    parser.add_argument("--body", help="Quote text.")
    parser.add_argument("--author", help="Quote author.")
    args = parser.parse_args()
    if args.body is not None and args.author is None:
        parser.error("--author is required when --body is supplied.")

    try:
        output_path = generate_meme(args.path, args.body, args.author)
    except (IngestorError, MemeEngineError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
    print(output_path)
