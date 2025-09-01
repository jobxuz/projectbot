from rest_framework import serializers
from apps.application.models import AdditionalService, UserApply



class AdditionalServiceSerializer(serializers.ModelSerializer):
    is_apply = serializers.BooleanField(read_only=False)
    
    class Meta:
        model = AdditionalService
        fields = ["id", "name", "description", "price", "is_apply"]
        
        
class UserApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApply
        fields = ["id", "service", "user"]
