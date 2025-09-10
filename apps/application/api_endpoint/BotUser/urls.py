from django.urls import path
from .views import BotUserRegisterAPIView, DeleteAccountAPIView

urlpatterns = [
    path("register/", BotUserRegisterAPIView.as_view()),
    path("delete-account/<int:user_id>/", DeleteAccountAPIView.as_view()),
]