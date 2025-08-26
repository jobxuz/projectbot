from rest_framework import serializers
from apps.application.models import ApplicationAdditionalService



class ApplicationAdditionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationAdditionalService
        fields = ["id", "manufacturer", "service", "status", "created_at"]
        read_only_fields = ["id", "created_at", "status"] 
