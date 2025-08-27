from rest_framework import generics
from apps.application.models import Manufacturer
from apps.application.tasks import notify_manufacturer_created
from .serializers import ManufacturerCreateSerializer



class ManufacturerCreateAPIView(generics.CreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerCreateSerializer

    def perform_create(self, serializer):
        manufacturer = serializer.save()
        # Celery taskni backgroundda chaqiramiz
        notify_manufacturer_created.delay(manufacturer.id)