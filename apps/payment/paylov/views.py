from typing import Dict, Any, Callable, Union

from django.db import transaction as db_transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.models import ProviderChoices, Transaction
from apps.payment.paylov.auth import authentication as paylov_auth
from apps.payment.paylov.client import PaylovClient
from apps.payment.paylov.methods import PaylovMethods
from apps.payment.paylov.serializers import PaylovSerializer


class PaylovAPIView(APIView):
    """
    API view to handle Paylov transactions.

    This view provides methods to check and perform transactions through the Paylov payment service.
    """

    permission_classes = (AllowAny,)
    http_method_names = ("post",)
    authentication_classes = []
    # schema = None

    def __init__(self):
        """
        Initializes the PaylovAPIView with method mappings.
        """

        self.METHODS: Dict[str, Callable[[], Dict[str, Any]]] = {
            PaylovMethods.CHECK_TRANSACTION: self.check_transaction,
            PaylovMethods.PERFORM_TRANSACTION: self.perform_transaction,
        }
        self.params: Union[Dict[str, Any], None] = None
        super(APIView, self).__init__()

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handles POST requests to perform actions related to Paylov transactions.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """

        is_authenticated = paylov_auth(request)
        if not is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = PaylovSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        method = serializer.validated_data["method"]
        self.params = serializer.validated_data["params"]

        with db_transaction.atomic():
            response_data = self.METHODS[method]()

        if isinstance(response_data, dict):
            response_data.update({"jsonrpc": "2.0", "id": request.data.get("id", None)})

        return Response(response_data)

    def check_transaction(self) -> Dict[str, Any]:
        """
        Checks the status of a transaction.

        Returns:
            dict: A dictionary with the transaction status and status text.
        """

        error, code = PaylovClient(self.params).check_transaction()

        if error and code == PaylovClient.STATUS_CODES["ORDER_NOT_FOUND"]:
            return dict(result=dict(status=code, statusText=PaylovClient.STATUS_TEXT["ERROR"]))
        return dict(result=dict(status=code, statusText=PaylovClient.STATUS_TEXT["SUCCESS"]))

    def perform_transaction(self) -> Dict[str, Any]:
        """
        Performs a transaction.

        Returns:
            dict: A dictionary with the transaction status and status text.
        """
        error, code = PaylovClient(self.params).perform_transaction()

        if error and code == PaylovClient.STATUS_CODES["ORDER_NOT_FOUND"]:
            return dict(result=dict(status=code, statusText=PaylovClient.STATUS_TEXT["ERROR"]))

        transaction = Transaction.objects.get(
            id=self.params["account"]["order_id"],
            provider=ProviderChoices.PAYLOV
        )

        if error:
            transaction.status = Transaction.TransactionStatus.FAILED
            transaction.save(update_fields=["status"])
            return dict(result=dict(status=code, statusText=PaylovClient.STATUS_TEXT["ERROR"]))

        transaction.apply_transaction(provider=ProviderChoices.PAYLOV)
        return dict(result=dict(status=code, statusText=PaylovClient.STATUS_TEXT["SUCCESS"]))