from django.urls import path

from apps.application.api_endpoint.AdditionalService.views import AdditionalServiceListAPIView
from apps.application.api_endpoint.ApplicationAdditionalService.views import ApplicationAdditionalServiceCreateAPIView
from .api_endpoint.Manufacturer.views import ManufacturerCreateAPIView
from .api_endpoint.Customer.views import CustomerCreateAPIView



urlpatterns = [
    path("application/manufactur-create/",ManufacturerCreateAPIView.as_view(), name="manufacturer"),
    path("application/customer-create/", CustomerCreateAPIView.as_view(), name="customer"),
    path("additional-services/list/", AdditionalServiceListAPIView.as_view(), name="additional-services-list"),
    path("application-additional-services/create/", ApplicationAdditionalServiceCreateAPIView.as_view(), name="application-additional-service-create"),
]