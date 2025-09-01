from rest_framework import serializers
from apps.application.models import BotUser, Customer, Manufacturer


class BotUserRegisterSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(required=True)
    
    def validate_telegram_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Telegram ID noto'g'ri")
        return value
    
    class Meta:
        model = BotUser
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id'
        ]


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = [
            'id'
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(source='customers', read_only=True)
    manufacturer = ManufacturerSerializer(source='manufacturers', read_only=True)
    
    class Meta:
        model = BotUser
        fields = [
            'telegram_id', 'first_name', 'last_name', 'username', 
            'phone_number', 'language_code', 'is_bot',
            'customer', 'manufacturer'
        ]
