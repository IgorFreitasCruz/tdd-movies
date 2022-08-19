from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MovieViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movies")

urlpatterns = [
    path("api/", include(router.urls)),
]
