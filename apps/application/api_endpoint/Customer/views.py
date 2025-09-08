from drf_spectacular.utils import extend_schema
from rest_framework import generics

from apps.application.models import Customer
from apps.application.tasks import send_customer_to_bitrix
from .serializers import CustomerCreateSerializer


@extend_schema(tags=["Customer"])
class CustomerCreateAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer

    def perform_create(self, serializer):
        customer = serializer.save()
        # Celery taskni backgroundda chaqiramiz
        send_customer_to_bitrix.delay(customer.id)
