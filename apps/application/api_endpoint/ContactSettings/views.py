from drf_spectacular.utils import extend_schema

from .serializers import ContactSettingsSerializer
from rest_framework.generics import  ListAPIView
from apps.application.models import ContactSettings



@extend_schema(tags=["ContactSettings"])
class ContactSettingsListAPIView(ListAPIView):
    queryset = ContactSettings.objects.all()
    serializer_class = ContactSettingsSerializer
