from drf_spectacular.utils import extend_schema
from rest_framework import generics

from apps.application.models import Customer, Manufacturer
from .serializers import CustomerCreateSerializer


@extend_schema(tags=["Customer"])
class CustomerCreateAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer
