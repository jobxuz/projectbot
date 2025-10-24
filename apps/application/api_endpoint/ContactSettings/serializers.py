from rest_framework import serializers

from apps.application.models import ContactSettings



class ContactSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSettings
        fields = ["id", "name", "phone_number"]
