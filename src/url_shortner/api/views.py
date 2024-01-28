from django.http.response import HttpResponseRedirect
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from url_shortner.models import ShortenedURL

from .serializers import ShortenedURLSerializer


class ShortenedURLViewSet(ModelViewSet):
    """
    ViewSet for creating, viewing and editing shortened urls.
    """

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = "url_code"


class RedirectView(RetrieveAPIView):
    """
    View for catching shortened_url instance by its code
    and redirecting it to origin url.
    """

    queryset = ShortenedURL.objects.all()
    lookup_field = "url_code"

    def retrieve(self, request, *args, **kwargs):
        """
        > Gets the shortened url instance by code
        > Checks if its enabled (returns 404 otherwise)
        > Returns redirect response with original url
          and redirect code from the instance
        """

        shortened_url = self.get_object()
        if not shortened_url.enabled:
            raise NotFound

        response = HttpResponseRedirect(
            redirect_to=shortened_url.original_url,
        )
        response.status_code = int(shortened_url.redirect_code)
        return response
