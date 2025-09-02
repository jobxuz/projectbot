from rest_framework import serializers
from apps.application.models import Manufacturer



class ManufacturerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class ManufacturerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class ManufacturerDetailSerializer(serializers.ModelSerializer):
    user_telegram_id = serializers.CharField(source="user.telegram_id", read_only=True)

    class Meta:
        model = Manufacturer
        fields = "__all__"