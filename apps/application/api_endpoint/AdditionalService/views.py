from rest_framework import generics, permissions
from apps.application.models import AdditionalService
from .serializers import AdditionalServiceSerializer



class AdditionalServiceListAPIView(generics.ListAPIView):
    queryset = AdditionalService.objects.filter(is_active=True)
    serializer_class = AdditionalServiceSerializer
    permission_classes = [permissions.AllowAny]