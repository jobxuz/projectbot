from rest_framework import serializers
from apps.application.models import Tender, TenderResponse
from apps.application.api_endpoint.Customer.serializers import CustomerSerializer
from apps.application.api_endpoint.Manufacturer.serializers import ManufacturerSerializer

class TenderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    responses_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Tender
        fields = [
            'id', 'lot_number', 'product_description', 'order_quantity',
            'delivery_date', 'special_requirements', 'budget', 'product_segment',
            'status', 'responses_count', 'customer', 'created_at', 'updated_at'
        ]
        read_only_fields = ['lot_number', 'responses_count', 'created_at', 'updated_at']

class TenderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = [
            'product_description', 'order_quantity', 'delivery_date',
            'special_requirements', 'budget', 'product_segment'
        ]

class TenderResponseSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    tender = TenderSerializer(read_only=True)
    
    class Meta:
        model = TenderResponse
        fields = [
            'id', 'tender', 'manufacturer', 'message', 'price_offer',
            'delivery_time', 'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']

class TenderResponseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenderResponse
        fields = ['message', 'price_offer', 'delivery_time']

class TenderDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    responses = TenderResponseSerializer(many=True, read_only=True)
    responses_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Tender
        fields = [
            'id', 'lot_number', 'product_description', 'order_quantity',
            'delivery_date', 'special_requirements', 'budget', 'product_segment',
            'status', 'responses_count', 'customer', 'responses', 'created_at', 'updated_at'
        ]
