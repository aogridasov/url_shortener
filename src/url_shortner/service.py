from rest_framework.exceptions import ValidationError as DRFValidationError
from validators.url import url as url_validator


def normalize_url(url: str) -> str:
    """
    > Removes spaces
    > Appends 'http://' prefix if no suitable protocol is present on url
    """

    url = url.replace(" ", "")

    suitable_prefixes = ("http://", "https://", "ftp://")
    if not url.startswith(suitable_prefixes):
        return f"http://{url}"
    return url


def validate_url(url: str) -> None:
    """
    Validates if url string is a valid url.
    Raises DRF-compatible error if not.

    Does NOT check if url is reacheble.
    """
    if not url_validator(url):
        raise DRFValidationError("Incorrect URL")
