from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DriverLogViewSet, DriverLogWeeklyViewSet

router = DefaultRouter()
router.register(r'driver-logs', DriverLogViewSet, basename='driver-logs')
router.register(r'driver-logs-weekly', DriverLogWeeklyViewSet, basename='driver-logs-weekly')


urlpatterns = [
    path('api/', include(router.urls)),
]
