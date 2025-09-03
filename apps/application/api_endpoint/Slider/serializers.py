from rest_framework import serializers

from apps.application.models import Slider




class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'title', 'description', 'image', 'is_active', 'created_at', 'updated_at']
