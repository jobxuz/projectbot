from django.db.models import Prefetch
from rest_framework import generics
from apps.application.models import Manufacturer, ManufacturerSertificate
from apps.application.tasks import send_manufacturer_to_bitrix
from .serializers import ManufacturerCreateSerializer, ManufacturerDetailSerializer, ManufacturerListSerializer, ManufacturerCertificateSerializer
from .filters import ManufacturerFilterSet
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



@extend_schema(tags=["Manufacturer"])
class ManufacturerCreateAPIView(generics.CreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerCreateSerializer

    def perform_create(self, serializer):
        manufacturer = serializer.save()
        send_manufacturer_to_bitrix.delay(manufacturer.id)


@extend_schema(tags=["Manufacturer"])
class ManufacturerListAPIView(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerListSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = ManufacturerFilterSet
    search_fields = ["company_name", "full_name", "position", "commercial_offer_text"]
    ordering_fields = ["created_at", "order"]


@extend_schema(tags=["Manufacturer"])
class ManufacturerDetailAPIView(generics.RetrieveAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerDetailSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related(
            'product_segment',
            Prefetch(
                lookup='sertificates',
                queryset=ManufacturerSertificate.objects.all(),
                to_attr='certificates_list'
            )
        )

    
@extend_schema(tags=["Manufacturer"])
class ManufacturerCertificateAPIView(generics.CreateAPIView):
    queryset = ManufacturerSertificate.objects.all()
    serializer_class = ManufacturerCertificateSerializer