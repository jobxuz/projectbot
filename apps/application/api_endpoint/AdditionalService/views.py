from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from apps.application.models import AdditionalService
from .serializers import AdditionalServiceSerializer


@extend_schema(tags=["Service"])
class AdditionalServiceListAPIView(generics.ListAPIView):
    queryset = AdditionalService.objects.filter(is_active=True)
    serializer_class = AdditionalServiceSerializer
    permission_classes = [permissions.AllowAny]
