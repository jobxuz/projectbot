from django.urls import path
from payment.payme.views import PaymeAPIView

# payme-payments-callback/

urlpatterns = [
    path("payme/", PaymeAPIView.as_view())
]
