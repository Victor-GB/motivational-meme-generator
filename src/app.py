"""Flask app for generating memes."""

import random
from pathlib import Path
from tempfile import TemporaryDirectory

import requests
from flask import Flask, abort, render_template, request, url_for

# @TODO Import your Ingestor and MemeEngine classes
from MemeEngine import MemeEngine, MemeEngineError
from QuoteEngine import Ingestor, IngestorError, QuoteModel

SRC_DIR = Path(__file__).resolve().parent

app = Flask(__name__)


def setup() -> tuple[list[QuoteModel], list[str]]:
    """Load all resources."""
    quote_files = [
        str(SRC_DIR / "_data" / "DogQuotes" / name)
        for name in (
            "DogQuotesTXT.txt",
            "DogQuotesDOCX.docx",
            "DogQuotesPDF.pdf",
            "DogQuotesCSV.csv",
        )
    ]

    quotes: list[QuoteModel] = []
    for path in quote_files:
        quotes.extend(Ingestor.parse(path))

    images_path = SRC_DIR / "_data" / "photos" / "dog"
    imgs = [str(path) for path in images_path.glob("*.jpg")]
    if not quotes:
        raise IngestorError("No valid quotes found in the quote files.")
    if not imgs:
        raise MemeEngineError(
            f"No sources images found in {str(images_path)!r}"
        )

    return quotes, imgs


try:
    meme = MemeEngine(str(SRC_DIR / "static"))
    quotes, imgs = setup()
except (IngestorError, MemeEngineError, OSError) as exc:
    raise SystemExit(f"Could not start the meme app: {exc}") from None


@app.route("/")
def meme_rand() -> str:
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    try:
        output_path = meme.make_meme(img, quote.body, quote.author)
    except MemeEngineError as exc:
        abort(500, description=f"Could not generate a meme: {exc}")
    image_url = url_for("static", filename=Path(output_path).name)

    return render_template("meme.html", path=image_url)


@app.route("/create", methods=["GET"])
def meme_form() -> str:
    """User input for meme information."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post() -> str:
    """Create a user defined meme."""
    image_url = request.form.get("image_url", "").strip()
    body = request.form.get("body", "").strip()
    author = request.form.get("author", "").strip()

    if not image_url or not body or not author:
        abort(400, description="Image URL, quote body and author are required")
    try:
        with requests.get(image_url, timeout=10) as response:
            response.raise_for_status()
            with TemporaryDirectory() as temp_dir:
                downloaded_image = Path(temp_dir) / "image"
                downloaded_image.write_bytes(response.content)
                output_path = meme.make_meme(
                    str(downloaded_image), body, author
                )
    except (requests.RequestException, MemeEngineError) as exc:
        abort(400, description=f"Could not create the supplied meme: {exc}")
    except OSError as exc:
        abort(500, description=f"Could not store the downloaded image: {exc}")

    image_url = url_for("static", filename=Path(output_path).name)
    return render_template("meme.html", path=image_url)


if __name__ == "__main__":
    app.run()
