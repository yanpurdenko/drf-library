from django.conf.urls.static import static
from rest_framework import routers
from django.urls import path, include

from borrowings.views import BorrowingsViewSet
from library_service import settings


router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet)

urlpatterns = [
    path("", include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


app_name = "borrowings"
