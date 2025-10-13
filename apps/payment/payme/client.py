from payment.models import Transaction
from payment.payme.credentials import get_credentials
import base64


class PaymeClient:
    """
    Payme client
    """
    CHECKOUT_BASE_URL = "https://checkout.paycom.uz/"
    # CHECKOUT_BASE_URL = "https://test.paycom.uz/"

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

        credentials = get_credentials()
        merchant_id = credentials["PAYME_KASSA_ID"]
        redirect_url = credentials["PAYME_REDIRECT_URL"]
        field_name_for_id = credentials["PAYME_FIELD_NAME_FOR_ID"]

        query = f"m={merchant_id};ac.order_id={transaction.id};a={transaction.amount * 100};"

        if redirect_url:
            parsed_url = urllib.parse.quote(redirect_url + f"?{field_name_for_id}={transaction.id}", safe='')
            query = f"m={merchant_id};ac.order_id={transaction.id};a={transaction.amount * 100};c={parsed_url}"

        encode_params = base64.b64encode(query.encode("utf-8"))
        encode_params = str(encode_params, "utf-8")

        return f"{cls.CHECKOUT_BASE_URL}{encode_params}"
