from rest_framework import serializers
from apps.application.models import Application



class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        

class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "manufacturer", "service", "status", "created_at"]
        read_only_fields = ["id", "created_at", "status"]