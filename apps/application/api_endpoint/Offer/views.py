from drf_spectacular.utils import extend_schema

from apps.application.models import Offer
from .serializers import OfferListSerializer, OfferUpdateSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import UpdateAPIView


    
    
@extend_schema(tags=["Offer"])
class OfferListAPIView(ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['manufacturer' ,'status', 'service', 'application', 'customer']




class OfferUpdateAPIView(UpdateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferUpdateSerializer
    lookup_field = "id"