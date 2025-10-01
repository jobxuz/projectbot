from rest_framework import serializers
from apps.application.models import Package, PackageItem
        

class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"
        
        
class PackageItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageItem
        fields = ["id", "name", "order"]
        
        
class PackageDetailSerializer(serializers.ModelSerializer):
    items = PackageItemListSerializer(many=True)
    
    class Meta:
        model = Package
        fields = "__all__"