from django.urls import path
from .views import BotUserRegisterAPIView

urlpatterns = [
    path("register/", BotUserRegisterAPIView.as_view())
]