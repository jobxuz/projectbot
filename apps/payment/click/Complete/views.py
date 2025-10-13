from django.db import transaction as db_transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.click.Complete.serializers import ClickCompleteSerializer
from payment.click.auth import authentication
from payment.click.client import ClickUPClient
from payment.models import Transaction, Providers


class ClickCompleteAPIView(APIView):
    TYPE = "complete"
    PROVIDER = Providers.ProviderChoices.CLICK
    permission_classes = []

    @swagger_auto_schema(request_body=ClickCompleteSerializer)
    def post(self, request, *args, **kwargs):
        check_auth = authentication(request)
        if not check_auth:
            return Response({"error": "-1", "error_note": "Authentication failed"})

        serializer = ClickCompleteSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)

        with db_transaction.atomic():
            click_provider = ClickUPClient(serializer.validated_data)
            response = click_provider.complete()

        response["fiscal_items"] = list()

        if click_provider.has_transaction:
            transaction = click_provider.transaction
        else:
            transaction = None

        response["click_trans_id"] = serializer.validated_data.get("click_trans_id", None)
        response["merchant_trans_id"] = serializer.validated_data.get("merchant_trans_id", None)
        response["merchant_prepare_id"] = serializer.validated_data.get("merchant_prepare_id", None)
        response["merchant_confirm_id"] = serializer.validated_data.get("merchant_prepare_id", None)

        if response["error"] == "0":
            transaction = click_provider.transaction

            with db_transaction.atomic():
                transaction.apply_transaction(
                    provider=Providers.ProviderChoices.CLICK
                )
            return Response(response)

        if transaction and transaction.status == Transaction.TransactionStatus.WAITING:
            transaction.status = Transaction.TransactionStatus.FAILED
            transaction.save(update_fields=["status"])

        return Response(response)


__all__ = ['ClickCompleteAPIView']
