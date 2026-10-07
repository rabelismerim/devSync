from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, MeetingViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='User')
router.register(r'meetings', MeetingViewSet, basename='Meettings')


urlpatterns = [
    path('', include(router.urls)),
]
