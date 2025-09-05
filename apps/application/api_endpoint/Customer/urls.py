from django.urls import path
from .views import CustomerCreateAPIView

urlpatterns = [
    path("create/", CustomerCreateAPIView.as_view()),
]