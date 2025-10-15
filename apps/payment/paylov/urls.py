from django.urls import path
from apps.payment.paylov.views import PaylovAPIView

urlpatterns = [
    path('paylov/', PaylovAPIView.as_view()),
]
