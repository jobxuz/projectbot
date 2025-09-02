from rest_framework import generics
from apps.application.models import Manufacturer
from apps.application.tasks import notify_manufacturer_created
from .serializers import ManufacturerCreateSerializer, ManufacturerDetailSerializer, ManufacturerListSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Manufacturer"])
class ManufacturerCreateAPIView(generics.CreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerCreateSerializer

    def perform_create(self, serializer):
        manufacturer = serializer.save()
        # Celery taskni backgroundda chaqiramiz
        notify_manufacturer_created.delay(manufacturer.id)



class ManufacturerListAPIView(generics.ListAPIView):
    queryset = Manufacturer.objects.all().order_by("-created_at")
    serializer_class = ManufacturerListSerializer


class ManufacturerDetailAPIView(generics.RetrieveAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerDetailSerializer
    lookup_field = "id" 