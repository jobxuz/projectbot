from rest_framework import serializers
from apps.application.models import Manufacturer


class ManufacturerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class ManufacturerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'company_name', 'full_name', 'product_segment']


class ManufacturerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'company_name', 'full_name', 'min_order_quantity', 'office_address', 'website', 'has_crm', 'employee_count']