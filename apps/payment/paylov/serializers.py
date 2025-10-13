from rest_framework import serializers
from payment.paylov.methods import PaylovMethods


class PaylovSerializer(serializers.Serializer):
    """
    Serializer for handling Paylov transaction data.

    This serializer validates the data required for initiating and handling transactions with the Paylov service.
    """

    id: serializers.IntegerField = serializers.IntegerField()
    method: serializers.ChoiceField = serializers.ChoiceField(choices=PaylovMethods.choices())
    params: serializers.JSONField = serializers.JSONField()
