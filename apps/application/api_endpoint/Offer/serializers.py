from rest_framework import serializers
from apps.application.api_endpoint.Manufacturer.serializers import ManufacturerListSerializer
from apps.application.models import Offer


class OfferListSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerListSerializer(read_only=True)
    
    class Meta:
        model = Offer
        fields = ["id", "manufacturer", "service", "status", "created_at"]
        



class OfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__" 
        
