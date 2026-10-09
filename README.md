# Motivational Meme Generator

A Udacity Intermediate Python project that generates memes from images,
quote bodies and authors through a command-line interface or Flask web app.

## Components

- `QuoteEngine`: quote models and TXT, CSV, DOCX and PDF ingestion.
- `MemeEngine`: proportional image resizing, text rendering and JPEG output.
- `src/meme.py`: command-line interface.
- `src/app.py`: Flask interface for random memes and submitted image URLs.

The starter application, templates and sample resources were supplied by Udacity.

## Setup

Tested on Ubuntu ARM64 with Python 3.14.4.

Requirements:

- Python 3.14.
- Genuine Xpdf 4.06, with its `pdftotext` executable available on `PATH`.

From the project root:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The Python requirements install Flask, Pillow, pandas, python-docx and Requests.
They do not install Xpdf. PDF ingestion invokes Xpdf through subprocess;
the similarly named Poppler executable is not the converter used for this project.

### Xpdf on Ubuntu

The following source build was used on Ubuntu ARM64:

```bash
sudo apt-get update
sudo apt-get install build-essential cmake libfreetype-dev curl
xpdf_setup_dir="$(mktemp -d)"
curl --fail --location https://dl.xpdfreader.com/xpdf-4.06.tar.gz -o "$xpdf_setup_dir/xpdf.tar.gz"
printf '%s  %s\n' '1c38f527c46caee0f712386d42a885b96a31ed9ce11904e872559859894d137e' "$xpdf_setup_dir/xpdf.tar.gz" | sha256sum --check
tar -xzf "$xpdf_setup_dir/xpdf.tar.gz" -C "$xpdf_setup_dir"
cmake -S "$xpdf_setup_dir/xpdf-4.06" -B "$xpdf_setup_dir/build" -DCMAKE_BUILD_TYPE=Release
cmake --build "$xpdf_setup_dir/build" --target pdftotext -j2
sudo install -m 0755 "$xpdf_setup_dir/build/xpdf/pdftotext" /usr/local/bin/pdftotext
export PATH="/usr/local/bin:$PATH"
hash -r
command -v pdftotext
pdftotext -v || test "$?" -eq 99
```

Run commands in order and stop if one fails. The checksum must pass.
The final commands should identify `/usr/local/bin/pdftotext` and Xpdf 4.06.
A missing Qt warning is expected: the graphical viewer is not being built.

## Usage

Run these commands from the project root with `.venv` active.

### Command line

Generate a meme using a random supplied photo and quote:

```bash
python src/meme.py
```

Supply an image, quote and author:

```bash
python src/meme.py --path src/_data/photos/dog/xander_1.jpg --body "Treat yo self" --author "Fluffles"
```

All three options are optional. Omitting `--path` selects a random photo.
Omitting `--body` selects a random quote and its author.
When supplying `--body`, also supply `--author`.

The command prints the generated JPEG path. Output is saved in the project's
`tmp` directory. Relative user-supplied image paths are resolved from the
terminal's working directory.

### Web application

```bash
python -m flask --app src/app.py run
```

Open [the web app](http://127.0.0.1:5000) in a browser.

- `/` generates a random meme.
- `/create` displays a form for an image URL, quote body and author.

Use a direct image URL and complete all three form fields. Downloaded source
images are temporary; generated JPEGs are saved in `src/static`.
Submitting an already captioned image preserves its existing text.

For VS Code Remote SSH, forward port 5000 to open the Ubuntu application
from your local browser.

## Python package examples

From the project root, start Python with `src` on its import path:

```bash
PYTHONPATH=src python
```

Then:

```python
from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeEngine

quote = QuoteModel("Treat yo self", "Fluffles")
print(quote)

quotes = Ingestor.parse("src/_data/DogQuotes/DogQuotesTXT.txt")
print(quotes[0])

engine = MemeEngine("tmp")
output = engine.make_meme(
    "src/_data/photos/dog/xander_1.jpg",
    quote.body,
    quote.author,
    width=250,
)
print(output)
```

`Ingestor` asks its registered readers whether they support the file and
delegates parsing to the matching reader. TXT and DOCX readers skip malformed
or incomplete quote lines.

`MemeEngine` accepts JPEG and PNG images, preserves their proportions and
limits output width to 500 pixels. It places the quote and author at a random
position within the image bounds and returns the saved JPEG path.

## Error handling

Quote readers raise `IngestorError` for reading or parsing failures.
Unsupported formats raise `UnsupportedFileTypeError`.
`MemeEngineError` reports image-generation failures, including captions
that cannot fit within the image.

The CLI displays expected error messages and exits with a non-zero status.
Flask reports invalid submissions with HTTP 400 and application failures
with HTTP 500. Missing startup resources produce a clear startup message.

## Development checks

Install development dependencies with `.venv` active:

```bash
python -m pip install -r requirements-dev.txt
```

Run the complete quality check:

```bash
./scripts/check.sh
```

This checks formatting, linting, types, dependency vulnerabilities and tests.
CLI and web behaviour have also been checked manually.

Install local Git hooks on each clone:

```bash
python -m pre_commit install --hook-type pre-commit --hook-type pre-push
```

The commit hook performs quick checks; the push hook runs the full quality
script. Additional development tooling is described in `EXTENSIONS.md`.
