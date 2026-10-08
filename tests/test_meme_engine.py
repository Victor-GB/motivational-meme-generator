"""Testing generated meme images."""

from pathlib import Path

from PIL import Image

from MemeEngine import MemeEngine


def test_make_memes_saves_resized_jpeg(tmp_path: Path) -> None:
    """Save a square sample image at requested width."""
    engine = MemeEngine(str(tmp_path))
    output = engine.make_meme(
        "src/_data/photos/dog/xander_1.jpg",
        "Treat yo self",
        "Fluffles",
        width=250,
    )
    with Image.open(output) as image:
        assert image.size == (250, 250)
        assert image.format == "JPEG"
