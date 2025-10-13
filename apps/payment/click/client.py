from payment.models import Transaction, Providers


class ClickUPClient:
    def __init__(self, data):
        self.data = data
        self.click_trans_id = self.data.get("click_trans_id", None)
        self.service_id = self.data.get("service_id", None)
        self.click_paydoc_id = self.data.get("click_paydoc_id", None)
        self.order_id = self.data.get("merchant_trans_id", None)
        self.amount = self.data.get("amount", None)
        self.action = self.data.get("action", None)
        self.error = self.data.get("error", None)
        self.error_note = self.data.get("error_note", None)
        self.sign_time = self.data.get("sign_time", None)
        self.sign_string = self.data.get("sign_string", None)
        self.merchant_prepare_id = self.data.get("merchant_prepare_id", None) if self.action == 1 else ""
        self.order = self.get_order()
        self.success_response = {"error": "0", "error_note": "Success"}
        self.transaction_found = False
        self.transaction = None

    def prepare(self):
        if self.action != 0:
            return {"error": "-3", "error_note": "Action not found"}

        if not self.order:
            return {"error": "-5", "error_note": "Order does not exist"}

        check_order, error_response = self.check_order()
        if not check_order:
            return error_response

        # check transaction exist and create if not exist
        can_prepare_transaction, error_response = self.can_prepare_transaction()
        if not can_prepare_transaction:
            return error_response

        # check amount when can_prepare_transaction is True
        is_valid_amount, error_response = self.is_valid_amount()
        if not is_valid_amount:
            return error_response

        return self.success_response

    def complete(self):
        if self.action != 1:
            return {"error": "-3", "error_note": "Action not found"}

        if not self.order:
            return {"error": "-5", "error_note": "Order does not exist"}

        check_order, error_response = self.check_order()
        if not check_order:
            return error_response

        can_complete_transaction, error_response = self.can_complete_transaction()
        if not can_complete_transaction:
            return error_response

        # check amount when can_prepare_transaction is True
        is_valid_amount, error_response = self.is_valid_amount()
        if not is_valid_amount:
            return error_response

        return self.success_response

    def can_complete_transaction(self):
        try:
            transaction = Transaction.objects.get(id=self.merchant_prepare_id)
            # set transaction and transaction_found if transaction exist
            self.transaction_found = True
            self.transaction = transaction
            if transaction.transaction_id != str(self.click_trans_id):
                return False, {"error": "-8", "error_note": "Transaction ID not match"}
        except Transaction.DoesNotExist:
            return False, {"error": "-7", "error_note": "Transaction not found"}

        is_valid_status, error_response = self.check_transaction_status()
        if not is_valid_status:
            return False, error_response

        return True, self.success_response

    def can_prepare_transaction(self):
        transaction = self.get_transaction()
        self.transaction_found = True
        self.transaction = transaction

        is_valid_status, error_response = self.check_transaction_status()
        if not is_valid_status:
            return False, error_response

        return True, self.success_response

    def check_transaction_status(self):
        if self.transaction.status == Transaction.TransactionStatus.SUCCESS:
            return False, {"error": "-4", "error_note": "Already paid"}
        elif self.transaction.status in [Transaction.TransactionStatus.CANCELLED, Transaction.TransactionStatus.FAILED]:
            return False, {"error": "-9", "error_note": "Transaction cancelled or failed"}
        return True, self.success_response

    def get_transaction(self):
        transaction, created = Transaction.objects.get_or_create(
            id=self.order_id,
            provider=Providers.ProviderChoices.CLICK,
            defaults={
                "amount": self.amount,
                "status": Transaction.TransactionStatus.WAITING,
            }
        )
        transaction.transaction_id = self.click_trans_id
        transaction.save(update_fields=['transaction_id'])
        return transaction

    @property
    def has_transaction(self):
        return self.transaction_found

    def is_valid_amount(self):
        transaction = Transaction.objects.get(id=self.order_id)
        if self.amount != transaction.amount:
            return False, {"error": "-2", "error_note": "Incorrect parameter amount"}

        return True, self.success_response

    def get_order(self):
        try:
            return Transaction.objects.get(id=self.order_id)
        except Transaction.DoesNotExist:
            return

    def check_order(self):
        if self.order.status == Transaction.TransactionStatus.SUCCESS:
            return False, {"error": "-4", "error_note": "Already paid"}
        return True, self.success_response

    @classmethod
    def create_payment_link(cls, transaction: Transaction):
        """
        Generates a payment link for a transaction.

        Args:
            transaction (Transaction): The transaction object.

        Returns:
            str: The generated payment link.
        """
        import urllib.parse
        from payment.click.credentials import get_credentials

        credentials = get_credentials()

        base_url = "https://my.click.uz/services/pay"

        merchant_id = credentials["CLICK_MERCHANT_ID"]
        service_id = credentials["CLICK_MERCHANT_SERVICE_ID"]
        redirect_url = credentials["CLICK_REDIRECT_URL"]

        query = (
            f"?service_id={service_id}&merchant_id={merchant_id}&amount={transaction.amount}&"
            f"transaction_param={transaction.id}"
        )
        if redirect_url:
            parsed_redirect_url = urllib.parse.quote(redirect_url + f"?transaction_id={transaction.id}", safe='')
            query += f"&{parsed_redirect_url}"

        return f"{base_url}/{query}"
