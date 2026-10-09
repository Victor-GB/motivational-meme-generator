"""Define exceptions raised while loading quote files."""


class IngestorError(Exception):
    """Report a failure to read or parse a quote file."""


class UnsupportedFileTypeError(IngestorError):
    """Report a quote file whose format has no matching reader."""
