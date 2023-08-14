from rest_framework import viewsets
from .models import DriverLog
from .serializers import DriverLogSerializer


class DriverLogViewSet(viewsets.ModelViewSet):
    queryset = DriverLog.objects.all()
    serializer_class = DriverLogSerializer
