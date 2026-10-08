"""Create meme images containing a quote and its author."""

from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Resizes images and renders quotes onto them."""

    def __init__(self, output_dir: str) -> None:
        """Prepare the directory for generated images."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """Create a meme and return the saved iamge path."""
        if width <= 0:
            raise ValueError("Width must be a positive integer.")
        with Image.open(img_path) as source:
            image = source.convert("RGB")

        target_width = min(width, 500, image.width)
        target_height = max(1, round(image.height * target_width / image.width))
        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default(size=20)
        draw.multiline_text(
            (10, 10),
            f"{text}\n- {author}",
            font=font,
            fill="white",
            stroke_width=2,
            stroke_fill="black",
            spacing=6,
        )

        output_path = self.output_dir / f"{uuid4().hex}.jpg"
        image.save(output_path)
        return str(output_path)
