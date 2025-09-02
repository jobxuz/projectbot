from django.urls import path

from apps.application.api_endpoint.AdditionalService.views import AdditionalServiceListAPIView, AdditionalServiceApplyAPIView
from apps.application.api_endpoint.ApplicationAdditionalService.views import ApplicationAdditionalServiceCreateAPIView
from .api_endpoint.Manufacturer.views import ManufacturerCreateAPIView, ManufacturerDetailAPIView, ManufacturerListAPIView
from .api_endpoint.Customer.views import CustomerCreateAPIView
from .api_endpoint.BotUser.views import BotUserRegisterAPIView
from .api_endpoint.BotUser.views import UserInfo


urlpatterns = [
    path("application/manufactur-create/",ManufacturerCreateAPIView.as_view(), name="manufacturer"),
    path("application/customer-create/", CustomerCreateAPIView.as_view(), name="customer"),
    path("additional-services/<str:telegram_id>/list/", AdditionalServiceListAPIView.as_view(), name="additional-services-list"),
    path("application-additional-services/create/", ApplicationAdditionalServiceCreateAPIView.as_view(), name="application-additional-service-create"),
    path("bot-user/register/", BotUserRegisterAPIView.as_view(), name="bot-user-register"),
    path("additional-services/apply/", AdditionalServiceApplyAPIView.as_view(), name="additional-services-apply"),
    path("bot-user/<str:telegram_id>/info/", UserInfo.as_view(), name="bot-user-info"),
    path("application/customer-create/", CustomerCreateAPIView.as_view(), name="customer"),
    path("application/manufacturer-list/", ManufacturerListAPIView.as_view(), name="manufacturer-list"),
    path("application/manufacturer-detail/<int:id>/", ManufacturerDetailAPIView.as_view(), name="manufacturer-detail"),

]