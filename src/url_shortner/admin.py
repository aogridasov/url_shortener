from django.contrib import admin

from url_shortner.models import ShortenedURL


@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ["id", "original_url", "url_code", "redirect_code", "enabled"]
