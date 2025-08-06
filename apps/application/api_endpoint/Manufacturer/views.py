from rest_framework import generics
from apps.application.models import Manufacturer
from .serializers import ManufacturerCreateSerializer



class ManufacturerCreateAPIView(generics.CreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerCreateSerializer