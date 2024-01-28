from secrets import token_urlsafe

from django.db import models

from url_shortner.service import normalize_url, validate_url


class ShortenedURLManager(models.Manager):
    """
    Custom model manager for shortened URLs.
    Implements method for shortening an url
    (creating related model instance)
    """

    def generate_unique_url_code(self) -> str:
        """
        Calls code generator function.
        Checks if code already exists in DB
        and regenerates codes until one is unique.
        Returns the unique code.
        """

        url_code = None
        while (not url_code) or (self.filter(url_code=url_code).exists()):
            url_code = token_urlsafe(8)
        return url_code

    def create_shortened_url(
        self,
        original_url: str,
        redirect_code: int | None = None,
        enabled: bool | None = None,
    ) -> "ShortenedURL":
        """
        > Calls url normalization function
        > Calls url validation function
        > Calls code generator function
        > Creates url instance with the unique URL code
        > Sets redirect code and enabled-status if any passed
        > Saves instance to db and return it
        """

        normalized_url = normalize_url(original_url)
        validate_url(normalized_url)
        url_code = self.generate_unique_url_code()

        shortened_url = self.model(
            original_url=normalized_url,
            url_code=url_code,
        )
        if redirect_code:
            shortened_url.redirect_code = redirect_code
        if enabled is not None:
            shortened_url.enabled = enabled
        shortened_url.save()
        return shortened_url


class ShortenedURL(models.Model):
    """
    Model for storing information about shortened urls.
    """

    objects = ShortenedURLManager()

    original_url = models.TextField(
        verbose_name="Original URL",
        max_length=10000,
    )
    url_code = models.CharField(
        verbose_name="Coded URL",
        unique=True,
        editable=False,
        max_length=255,
    )

    class RedirectCodeChoices(models.IntegerChoices):
        MULTIPLE_CHOICES = 300, "300"
        MOVED_PERMANENTLY = 301, "301"
        FOUND = 302, "302"
        SEE_OTHER = 303, "303"
        NOT_MODIFIED = 304, "304"
        USE_PROXY = 305, "305"
        RESERVED = 306, "306"
        TEMPORARY_REDIRECT = 307, "307"
        PERMANENT_REDIRECT = 308, "308"

    redirect_code = models.IntegerField(
        choices=RedirectCodeChoices.choices,
        verbose_name="Redirect HTTP code",
        default=RedirectCodeChoices.FOUND,
    )

    enabled = models.BooleanField(default=True, verbose_name="Can be accessed")

    class Meta:
        verbose_name = "Shortened URL"
        verbose_name_plural = "Shortened URLs"

    def __str__(self) -> str:
        return f"Shortened: {self.original_url}"
