from django.db import transaction as db_transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.click.auth import authentication
from payment.click.client import ClickUPClient
from payment.models import Transaction, Providers
from payment.click.Prepare.serializers import ClickPrepareSerializer


class ClickPrepareAPIView(APIView):
    TYPE = "prepare"
    PROVIDER = Providers.ProviderChoices.CLICK
    permission_classes = []

    @swagger_auto_schema(request_body=ClickPrepareSerializer)
    def post(self, request, *args, **kwargs):
        is_authenticated = authentication(request)
        if not is_authenticated:
            return Response({"error": "-1", "error_note": "Authentication failed"})
        serializer = ClickPrepareSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)

        with db_transaction.atomic():
            click_up_client = ClickUPClient(serializer.validated_data)
            response = click_up_client.prepare()

        if click_up_client.has_transaction:
            transaction = click_up_client.transaction
        else:
            transaction = None

        response["click_trans_id"] = serializer.validated_data.get("click_trans_id", None)
        response["merchant_trans_id"] = serializer.validated_data.get("merchant_trans_id", None)

        if response["error"] == "0":
            transaction = click_up_client.transaction
            response["merchant_prepare_id"] = transaction.id
            return Response(response)

        if transaction and transaction.status == Transaction.TransactionStatus.WAITING:
            transaction.status = Transaction.TransactionStatus.FAILED
            transaction.save(update_fields=["status"])

        return Response(response)


__all__ = ['ClickPrepareAPIView']
