from datetime import datetime
from typing import Any, Callable, Dict, Optional, Union

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.models import Transaction, Providers
from payment.payme import errors
from payment.payme.auth import authentication as payme_auth
from payment.payme.credentials import get_credentials
from payment.payme.serializers import PaymeCallbackSerializer


class PaymeAPIView(APIView):
    """
    API view to handle Payme transactions.

    This view provides methods to perform transactions through the Payme payment service.
    """

    permission_classes = (AllowAny,)
    http_method_names = ("post",)
    authentication_classes = []

    # schema = None

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the PaymeAPIView with method mappings and credentials.
        """
        super().__init__(**kwargs)
        self.METHOD_MAPPING: Dict[str, Optional[Callable]] = {
            "CreateTransaction": self.create_transaction,
            "CheckPerformTransaction": self.check_perform_transaction,
            "PerformTransaction": self.perform_transaction,
            "CheckTransaction": self.check_transaction,
            "CancelTransaction": self.cancel_transaction,
            "GetStatement": self.get_statement,
            "SetFiscalData": None
        }

        credentials = get_credentials()
        self.PAYME_FIELD_NAME_FOR_ID: str = credentials['PAYME_FIELD_NAME_FOR_ID']

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST requests for Payme transactions.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with the result of the Payme transaction.
        """

        if not payme_auth(request):
            return Response(errors.AUTH_MESSAGE)

        serializer = PaymeCallbackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors.PARSING_JSON_MESSAGE)

        method = serializer.validated_data["method"]
        if method not in self.METHOD_MAPPING:
            return Response(errors.RPC_METHOD_NOT_FOUND_MESSAGE)

        method_callback_function = self.METHOD_MAPPING.get(method)
        if not callable(method_callback_function):
            return Response(errors.RPC_METHOD_NOT_IMPLEMENT_MESSAGE)

        pre_response = method_callback_function(
            params=serializer.validated_data["params"],
            field_name_for_id=self.PAYME_FIELD_NAME_FOR_ID
        )

        return Response(pre_response, status=status.HTTP_200_OK)

    @classmethod
    def check_perform_transaction(cls, params: Dict[str, Any], field_name_for_id: str) -> Union[str, Dict[str, Any]]:
        """
        Check if a transaction can be performed.

        Args:
            params: The parameters of the transaction.
            field_name_for_id: The field name used for identifying the transaction.

        Returns:
            A message indicating the result of the check or a response dict.
        """
        transaction_id = int(params.get("account", {}).get(field_name_for_id, 0))
        amount = int(params.get("amount")) / 100

        transaction = cls.get_transaction(pk=transaction_id)

        if transaction is None:
            return errors.ORDER_NOT_FOUND_MESSAGE

        if transaction.amount != amount:
            return errors.INVALID_AMOUNT_MESSAGE

        if transaction.status == Transaction.TransactionStatus.SUCCESS:
            return errors.ORDER_ALREADY_PAID_MESSAGE

        if transaction.status != Transaction.TransactionStatus.WAITING:
            return errors.TRANSACTION_NOT_FOUND_MESSAGE

        return {
            "result": {
                "allow": True,
                "additional": {"user_id": transaction.order.user.get_uuid()}
            },
        }

    @classmethod
    def create_transaction(cls, params: Dict[str, Any], field_name_for_id: str) -> Union[str, Dict[str, Any]]:
        """
        Create a new transaction.

        Args:
            params: The parameters of the transaction.
            field_name_for_id: The field name used for identifying the transaction.

        Returns:
            A message indicating the result of the transaction creation or a response dict.
        """
        provider_transaction_id = params.get("id", 0)
        transaction_id = int(params.get("account", {}).get(field_name_for_id, 0))
        amount = int(params.get("amount")) / 100

        transaction = cls.get_transaction(pk=transaction_id)

        if transaction is None:
            return errors.ORDER_NOT_FOUND_MESSAGE

        if transaction.amount != amount:
            return errors.INVALID_AMOUNT_MESSAGE

        if not transaction.transaction_id:
            transaction.transaction_id = provider_transaction_id
            transaction.save(update_fields=["transaction_id"])

        if transaction.transaction_id != provider_transaction_id:
            return errors.ORDER_NOT_FOUND_MESSAGE

        if transaction.status != Transaction.TransactionStatus.WAITING:
            return errors.ORDER_NOT_FOUND_MESSAGE

        return {
            "result": {
                "create_time": int(transaction.created_at.timestamp() * 1000),
                "transaction": transaction.transaction_id,
                "state": cls.get_transaction_state(transaction)
            }
        }

    @classmethod
    def perform_transaction(cls, params: Dict[str, Any], **kwargs: Any) -> Union[str, Dict[str, Any]]:
        """
        Perform a transaction.

        Args:
            params: The parameters of the transaction.

        Returns:
            A message indicating the result of the transaction performance or a response dict.
        """
        transaction_id = params.get("id")
        print(transaction_id, "in perform_transaction")
        transaction = cls.get_transaction(transaction_id=transaction_id)
        if transaction is None:
            print(transaction_id, "in perform_transaction", "none")
            return errors.TRANSACTION_NOT_FOUND_MESSAGE

        if transaction.status == Transaction.TransactionStatus.SUCCESS:
            return {
                "result": {
                    "transaction": str(transaction.transaction_id),
                    "perform_time": int(transaction.paid_at.timestamp() * 1000) if transaction.paid_at else 0,
                    "state": errors.TransactionStates.CLOSED
                }
            }

        if transaction.status == Transaction.TransactionStatus.FAILED:
            return errors.UNABLE_TO_PERFORM_OPERATION_MESSAGE

        transaction.apply_transaction(Providers.ProviderChoices.PAYME, transaction.transaction_id)
        return {
            "result": {
                "transaction": str(transaction.transaction_id),
                "perform_time": int(transaction.paid_at.timestamp() * 1000),
                "state": errors.TransactionStates.CLOSED
            }
        }

    @classmethod
    def check_transaction(cls, params: Dict[str, Any], **kwargs: Any) -> Union[str, Dict[str, Any]]:
        """
        Check the status of a transaction.

        Args:
            params: The parameters of the transaction.

        Returns:
            A message indicating the result of the transaction check or a response dict.
        """
        transaction_id = params.get('id')
        transaction = cls.get_transaction(transaction_id=transaction_id)
        if not transaction:
            return errors.TRANSACTION_NOT_FOUND_MESSAGE

        return {
            "result": {
                "create_time": int(transaction.created_at.timestamp() * 1000),
                "perform_time": int(transaction.paid_at.timestamp() * 1000) if transaction.paid_at else 0,
                "cancel_time": int(transaction.cancelled_at.timestamp() * 1000) if transaction.cancelled_at else 0,
                "transaction": transaction.transaction_id,
                "state": cls.get_transaction_state(transaction),
                "reason": transaction.extra.get("payme_cancel_reason") if transaction.extra else None
            }
        }

    @classmethod
    def cancel_transaction(cls, params: Dict[str, Any], **kwargs: Any) -> Union[str, Dict[str, Any]]:
        """
        Cancel a transaction.

        Args:
            params: The parameters of the transaction.

        Returns:
            A message indicating the result of the transaction cancellation or a response dict.
        """
        transaction_id = params.get('id', 0)
        reason = params.get('reason')
        transaction = cls.get_transaction(transaction_id=transaction_id)
        if not transaction:
            return errors.TRANSACTION_NOT_FOUND_MESSAGE

        if transaction.status == Transaction.TransactionStatus.CANCELLED:
            return {
                "result": {
                    "transaction": transaction.transaction_id,
                    "cancel_time": int(transaction.cancelled_at.timestamp() * 1000) if transaction.cancelled_at else 0,
                    "state": cls.get_transaction_state(transaction)
                }
            }

        transaction = transaction.cancel_transaction(reason)

        return {
            "result": {
                "transaction": transaction.transaction_id,
                "cancel_time": int(transaction.cancelled_at.timestamp() * 1000) if transaction.cancelled_at else 0,
                "state": cls.get_transaction_state(transaction)
            }
        }

    @classmethod
    def get_statement(cls, params: Dict[str, Any], field_name_for_id: str) -> Dict[str, Any]:
        """
        Retrieve a statement of transactions within a specified period.

        Args:
            params: The parameters including the time range for the statement.
            field_name_for_id: The field name used for identifying transactions.

        Returns:
            A dictionary containing the list of transactions within the specified period.
        """
        params_from_datetime = datetime.fromtimestamp(params["from"] // 1000)
        params_to_datetime = datetime.fromtimestamp(params["to"] // 1000)

        queryset = Transaction.objects.filter(
            created_at__gte=params_from_datetime, created_at__lte=params_to_datetime,
            provider=Providers.ProviderChoices.PAYME,
            transaction_id__isnull=False
        )

        transaction_list = [
            {
                "id": transaction.transaction_id,
                "amount": transaction.amount,
                "account": {
                    "order_id": transaction.id
                },
                "create_time": int(transaction.created_at.timestamp() * 1000) if transaction.created_at else 0,
                "perform_time": int(transaction.paid_at.timestamp() * 1000) if transaction.paid_at else 0,
                "cancel_time": int(transaction.cancelled_at.timestamp() * 1000) if transaction.cancelled_at else 0,
                "state": cls.get_transaction_state(transaction),
                "reason": transaction.extra.get("payme_cancel_reason") if transaction.extra else None
            }
            for transaction in queryset
        ]

        return {"result": {"transactions": transaction_list}}

    @staticmethod
    def get_transaction(**kwargs) -> Optional[Transaction]:
        """
        Retrieve a transaction by primary key or transaction ID.

        Returns:
            The transaction object if found, None otherwise.
        """
        transaction = Transaction.objects.filter(
            provider=Providers.ProviderChoices.PAYME,
            **kwargs
        ).last()

        return transaction

    @classmethod
    def get_transaction_state(cls, transaction):
        """
        Get the state of a transaction.

        Args:
            transaction: The transaction object.

        Returns:
            The state of the transaction as an integer.
        """
        transaction_mapping = {
            Transaction.TransactionStatus.SUCCESS: errors.TransactionStates.CLOSED,
            Transaction.TransactionStatus.WAITING: errors.TransactionStates.CREATED,
            Transaction.TransactionStatus.CANCELLED: errors.TransactionStates.CANCELED_CREATED
        }

        state = transaction_mapping.get(transaction.status)

        if state == errors.TransactionStates.CANCELED_CREATED and transaction.paid_at:
            state = errors.TransactionStates.CANCELED_CLOSED

        return state