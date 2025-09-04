from rest_framework import serializers
from apps.application.models import Customer



class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


