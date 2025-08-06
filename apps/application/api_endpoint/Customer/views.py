from rest_framework import generics
from apps.application.models import Customer
from .serializers import CustomerCreateSerializer



class CustomerCreateAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer