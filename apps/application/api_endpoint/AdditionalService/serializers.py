from rest_framework import serializers
from apps.application.models import AdditionalService, UserApply



class AdditionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalService
        fields = "__all__"
        
        
class UserApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApply
        fields = "__all__"
