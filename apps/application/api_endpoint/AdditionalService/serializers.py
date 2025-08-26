from rest_framework import serializers
from apps.application.models import AdditionalService



class AdditionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalService
        fields = ["id", "name", "description", "price"]
