from django.conf import settings
from rest_framework import serializers

from url_shortner.models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    redirect_code = serializers.ChoiceField(
        choices=ShortenedURL.RedirectCodeChoices.choices,
        initial=ShortenedURL.RedirectCodeChoices.FOUND,
    )
    url = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = [
            "id",
            "url",
            "original_url",
            "url_code",
            "redirect_code",
            "enabled",
        ]

    def create(self, validated_data):
        return ShortenedURL.objects.create_shortened_url(**validated_data)

    def get_url(self, obj):
        """
        Forms and returns shortened url for an url instance.
        Tries to fetch host from settings. If not present tries to
        get the host from request header.
        """

        host = settings.HOST
        if not host:
            request = self.context.get("request", {})
            host = request.headers.get("Host") or "localhost"
        return f"http://{host}/sh/{obj.url_code}"
