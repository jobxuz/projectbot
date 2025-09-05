from drf_spectacular.utils import extend_schema

from apps.application.models import Package
from .serializers import PackageListSerializer, PackageDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


@extend_schema(tags=["Package"])
class PackageListAPIView(ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['type']
    ordering_fields = ['order']

@extend_schema(tags=["Package"])
class PackageDetailAPIView(RetrieveAPIView):
    queryset = Package.objects.prefetch_related('package_items').all()
    serializer_class = PackageDetailSerializer
