from drf_spectacular.utils import extend_schema

from apps.application.models import Application
from .serializers import ApplicationListSerializer, ApplicationCreateSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema(tags=["Application"])
class ApplicationCreateAPIView(CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    
    
@extend_schema(tags=["Application"])
class ApplicationListAPIView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'created_at']
