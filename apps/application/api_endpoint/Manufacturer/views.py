from rest_framework import generics
from apps.application.models import Manufacturer
from apps.application.tasks import send_manufacturer_to_bitrix
from .serializers import ManufacturerCreateSerializer, ManufacturerDetailSerializer, ManufacturerListSerializer
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
    filterset_fields = ["min_order_quantity", "product_segment"]
    search_fields = ["company_name", "full_name", "position", "min_order_quantity", "product_segment", "commercial_offer_text"]
    ordering_fields = ["created_at", "order"]

@extend_schema(tags=["Manufacturer"])
class ManufacturerDetailAPIView(generics.RetrieveAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerDetailSerializer
    lookup_field = "id" 