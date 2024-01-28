# Generated by Django 5.0.1 on 2024-01-28 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ShortenedURL",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "original_url",
                    models.TextField(max_length=10000, verbose_name="Original URL"),
                ),
                (
                    "url_code",
                    models.CharField(
                        editable=False,
                        max_length=255,
                        unique=True,
                        verbose_name="Coded URL",
                    ),
                ),
                (
                    "redirect_code",
                    models.IntegerField(
                        choices=[
                            (300, "300"),
                            (301, "301"),
                            (302, "302"),
                            (303, "303"),
                            (304, "304"),
                            (305, "305"),
                            (306, "306"),
                            (307, "307"),
                            (308, "308"),
                        ],
                        default=302,
                        verbose_name="Redirect HTTP code",
                    ),
                ),
                (
                    "enabled",
                    models.BooleanField(default=True, verbose_name="Can be accessed"),
                ),
            ],
            options={
                "verbose_name": "Shortened URL",
                "verbose_name_plural": "Shortened URLs",
            },
        ),
    ]
