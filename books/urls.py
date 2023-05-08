from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from books.views import GenreViewSet, BookViewSet
from library_service import settings


router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


app_name = "books"
