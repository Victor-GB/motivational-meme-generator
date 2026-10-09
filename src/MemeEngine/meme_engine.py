"""Create meme images containing a quote and its author."""

import random
from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont

from .exceptions import MemeEngineError


class MemeEngine:
    """Resizes images and renders quotes onto them."""

    def __init__(self, output_dir: str) -> None:
        """Prepare the directory for generated images."""
        self.output_dir = Path(output_dir)
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise MemeEngineError(
                f"Could not create output directory {output_dir!r}: {exc}"
            ) from exc

    def make_meme(
        self, img_path: str, text: str, author: str, width: int = 500
    ) -> str:
        """Create a meme and return the saved image path."""
        if width <= 0:
            raise MemeEngineError("Width must be a positive integer.")
        try:
            with Image.open(img_path) as source:
                image = source.convert("RGB")
        except OSError as exc:
            raise MemeEngineError(
                f"Could not read image {img_path!r}: {exc}"
            ) from exc

        target_width = min(width, 500, image.width)
        target_height = max(
            1, round(image.height * target_width / image.width)
        )
        image = image.resize(
            (target_width, target_height), Image.Resampling.LANCZOS
        )

        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default(size=20)
        caption = f"{text}\n- {author}"
        left, top, right, bottom = draw.multiline_textbbox(
            (0, 0),
            caption,
            font=font,
            stroke_width=2,
            spacing=6,
        )
        margin = 10
        max_x = int(image.width - (right - left) - margin)
        max_y = int(image.height - (bottom - top) - margin)
        if max_x < margin or max_y < margin:
            raise MemeEngineError(
                f"Caption does not fit within image {img_path!r}"
            )

        x = random.randint(margin, max_x)
        y = random.randint(margin, max_y)
        draw.multiline_text(
            (x - left, y - top),
            caption,
            font=font,
            fill="white",
            stroke_width=2,
            stroke_fill="black",
            spacing=6,
        )
        output_path = self.output_dir / f"{uuid4().hex}.jpg"
        try:
            image.save(output_path)
        except OSError as exc:
            raise MemeEngineError(
                f"Could not save meme image {str(output_path)!r}: {exc}"
            ) from exc

        return str(output_path)
