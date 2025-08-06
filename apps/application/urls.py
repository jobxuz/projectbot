from django.urls import path
from .api_endpoint.Manufacturer.views import ManufacturerCreateAPIView
from .api_endpoint.Customer.views import CustomerCreateAPIView



urlpatterns = [
    path("application/manufactur-create/",ManufacturerCreateAPIView.as_view(), name="manufacturer"),
    path("application/customer-create/", CustomerCreateAPIView.as_view(), name="customer"),
]