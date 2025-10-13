from rest_framework import serializers


class PaymeCallbackSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    method = serializers.CharField()
    params = serializers.JSONField()
