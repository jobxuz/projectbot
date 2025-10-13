from django.urls import path
from payment.paylov.views import PaylovAPIView

urlpatterns = [
    path('paylov/', PaylovAPIView.as_view()),
]
