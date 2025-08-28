from rest_framework import serializers
from apps.application.models import BotUser


class BotUserRegisterSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(required=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    language_code = serializers.CharField(max_length=10, required=False, allow_blank=True)
    is_bot = serializers.BooleanField(default=False, required=False)
    
    def validate_telegram_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Telegram ID noto'g'ri")
        return value
    
    def validate(self, data):
        if not data.get('first_name') and not data.get('last_name') and not data.get('username'):
            raise serializers.ValidationError("Kamida ism, familiya yoki username kiritilishi kerak")
        return data
    
    class Meta:
        model = BotUser
        fields = ['telegram_id', 'first_name', 'last_name', 'username', 'phone_number', 'language_code', 'is_bot']
