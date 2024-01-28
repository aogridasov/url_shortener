from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from url_shortner.models import ShortenedURL


class ShortenedURLTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.original_url = "https://example.com/somepath/a?user_id=22312"

    def test_create_short_url(self):
        input_data = {"original_url": self.original_url, "redirect_code": 302}
        response = self.client.post(
            reverse("shortened-urls-list"), input_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["original_url"], input_data["original_url"])

    def test_redirect_to_original_url(self):
        short_url = ShortenedURL.objects.create_shortened_url(
            original_url=self.original_url, redirect_code=307
        )
        response = self.client.get(reverse("redirect-view", args=[short_url.url_code]))
        self.assertEqual(response.status_code, status.HTTP_307_TEMPORARY_REDIRECT)
        self.assertEqual(response.url, self.original_url)

    def test_disabled_short_url_redirect(self):
        short_url = ShortenedURL.objects.create_shortened_url(
            original_url=self.original_url, redirect_code=307, enabled=False
        )
        response = self.client.get(reverse("redirect-view", args=[short_url.url_code]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_short_urls(self):
        response = self.client.get(reverse("shortened-urls-list"))
        self.assertEqual(len(response.data), 0)
        ShortenedURL.objects.create_shortened_url(
            original_url=self.original_url, redirect_code=307
        )
        response = self.client.get(reverse("shortened-urls-list"))
        self.assertEqual(len(response.data), 1)

    def test_edit_short_url_redirection(self):
        short_url = ShortenedURL.objects.create_shortened_url(
            original_url=self.original_url, redirect_code=307
        )
        new_url = "https://newexample.com"
        response = self.client.patch(
            reverse("shortened-urls-detail", args=[short_url.url_code]),
            {"original_url": new_url, "redirect_code": 301},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_url = ShortenedURL.objects.get(id=short_url.id)
        self.assertEqual(updated_url.original_url, new_url)
        self.assertEqual(updated_url.redirect_code, 301)
