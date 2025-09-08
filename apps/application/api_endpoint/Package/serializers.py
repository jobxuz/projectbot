from rest_framework import serializers
from apps.application.models import Package, PackageItem
        

class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ["id", "name", "banner", "description", 'order']
        
        
class PackageItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageItem
        fields = ["id", "name", "order"]
        
        
class PackageDetailSerializer(serializers.ModelSerializer):
    items = PackageItemListSerializer(many=True)
    
    class Meta:
        model = Package
        fields = ["id", "name", "banner", "description", 'order', 'items']