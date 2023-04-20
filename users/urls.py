from django.conf.urls.static import static
from rest_framework import routers
from django.urls import path, include

from library_service import settings

urlpatterns = [ ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


app_name = "users"
