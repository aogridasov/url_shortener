from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from .views import RedirectView, ShortenedURLViewSet

router = routers.DefaultRouter()
router.register(r"shortened_urls", ShortenedURLViewSet, basename="shortened-urls")

urlpatterns = [
    path("api/", include(router.urls)),
    path("<str:url_code>", RedirectView.as_view(), name="redirect-view"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
