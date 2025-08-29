from rest_framework import serializers
from apps.application.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'payment_type', 'payment_type_display', 'amount', 'currency',
            'payment_method', 'payment_method_display', 'status', 'status_display',
            'transaction_id', 'created_at', 'completed_at'
        ]
        read_only_fields = ['status', 'transaction_id', 'created_at', 'completed_at']

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_type', 'amount', 'currency', 'payment_method']

class PaymentWebhookSerializer(serializers.Serializer):
    transaction_id = serializers.CharField()
    status = serializers.CharField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    payment_data = serializers.JSONField(required=False)
