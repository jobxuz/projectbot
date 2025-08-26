from rest_framework import generics, permissions
from apps.application.models import ApplicationAdditionalService
from .serializers import ApplicationAdditionalServiceSerializer



class ApplicationAdditionalServiceCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationAdditionalService.objects.all()
    serializer_class = ApplicationAdditionalServiceSerializer
    permission_classes = [permissions.AllowAny]