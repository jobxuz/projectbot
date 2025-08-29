from django.urls import path, include
from apps.application.api_endpoint.BotUser.views import BotUserRegisterAPIView
from apps.application.api_endpoint.Manufacturer.views import ManufacturerCreateAPIView
from apps.application.api_endpoint.Customer.views import CustomerCreateAPIView
from apps.application.api_endpoint.AdditionalService.views import AdditionalServiceListAPIView
from apps.application.api_endpoint.Tender.views import (
    TenderListCreateAPIView, TenderDetailAPIView, TenderResponseCreateAPIView,
    TenderSearchAPIView, MyTendersAPIView
)
from apps.application.api_endpoint.Payment.views import (
    PaymentListCreateAPIView, PaymentDetailAPIView, payment_webhook,
    create_subscription_payment, create_catalog_access_payment
)

app_name = 'application'

urlpatterns = [
    # Bot User
    path('api/bot-user/register/', BotUserRegisterAPIView.as_view(), name='bot_user_register'),
    
    # Manufacturer
    path('api/manufacturer/create/', ManufacturerCreateAPIView.as_view(), name='manufacturer_create'),
    
    # Customer
    path('api/customer/create/', CustomerCreateAPIView.as_view(), name='customer_create'),
    
    # Additional Service
    path('api/additional-service/list/', AdditionalServiceListAPIView.as_view(), name='additional_service_list'),
    
    # Tender
    path('api/tender/', TenderListCreateAPIView.as_view(), name='tender_list_create'),
    path('api/tender/search/', TenderSearchAPIView.as_view(), name='tender_search'),
    path('api/tender/my/', MyTendersAPIView.as_view(), name='my_tenders'),
    path('api/tender/<str:lot_number>/', TenderDetailAPIView.as_view(), name='tender_detail'),
    path('api/tender/<int:tender_id>/response/', TenderResponseCreateAPIView.as_view(), name='tender_response_create'),
    
    # Payment
    path('api/payment/', PaymentListCreateAPIView.as_view(), name='payment_list_create'),
    path('api/payment/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment_detail'),
    path('api/payment/webhook/<str:provider>/', payment_webhook, name='payment_webhook'),
    path('api/payment/subscription/', create_subscription_payment, name='create_subscription_payment'),
    path('api/payment/catalog-access/', create_catalog_access_payment, name='create_catalog_access_payment'),
]