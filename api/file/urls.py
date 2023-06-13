from django.urls import path, re_path
from rest_framework import routers

from file import views

router = routers.DefaultRouter()
router.register(prefix=r"file", viewset=views.FileViewSet, basename='file')

urlpatterns = router.urls
