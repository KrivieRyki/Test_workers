from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DriverLogViewSet

router = DefaultRouter()
router.register(r'driver-logs', DriverLogViewSet, basename='driver-logs')

urlpatterns = [

    path('api/', include(router.urls)),
]