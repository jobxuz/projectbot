from django.urls import path
from .views import ContactSettingsListAPIView

urlpatterns = [
    path("contact-settings/", ContactSettingsListAPIView.as_view(), name="contact-settings-list"),
]
