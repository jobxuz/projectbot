from datetime import date
from rest_framework.exceptions import NotFound, APIException
import requests
import base64
from typing import Tuple, Dict, Union, Optional, Any

from django.contrib.auth import get_user_model
from django.core.cache import cache

from book.models import Book
from payment.paylov.credentials import get_credentials
from payment.paylov.errors import error_codes
from payment.models import Transaction, Order, UserCard, Providers
from study.models import Course, Discount, PromoCode
from payment.utils import calculate_amount_with_discount_promocode
import json

User = get_user_model()


class PaylovClient:
    """
    A client for interacting with the Paylov API.

    This class provides methods to handle various operations related to user cards, receipts, and transactions
    for the Paylov payment service.
    """

    SUBSCRIPTION_BASE_URL = "https://gw.paylov.uz/merchant/"
    CHECKOUT_BASE_URL = "https://my.paylov.uz/checkout/create/"

    API_ENDPOINTS = {
        # Card actions
        "CREATE_CARD": ("userCard/createUserCard/", "POST"),
        "CONFIRM_CARD": ("userCard/confirmUserCardCreate/", "POST"),
        "GET_CARDS": ("userCard/getAllUserCards/", "GET"),
        "DELETE_CARD": ("userCard/deleteUserCard/", "DELETE"),
        # Receipt actions
        "CREATE_RECEIPT": ("receipts/create/", "POST"),
        "PAY_RECEIPT": ("receipts/pay/", "POST")
    }

    STATUS_CODES = {
        "ORDER_NOT_FOUND": "303",
        "ORDER_ALREADY_PAID": "201",
        "INVALID_AMOUNT": "5",
        "SERVER_ERROR": "3",
        "SUCCESS": "0"
    }

    STATUS_TEXT = {
        "SUCCESS": "OK",
        "ERROR": "ERROR"
    }

    def __init__(self, params: Optional[Dict] = None) -> None:
        """
        Initializes the PaylovClient with API cqyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyMDAyNjkyLCJpYXQiOjE3MjE5MTYyOTIsImp0aSI6IjkxZTJkZTA4ZmIzYzQ3NDdhODdkNGM1NDRkNTcwNjc4IiwidXNlcl9pZCI6ImU3OTc1YjIxLWE0YTAtNGI2NS1hN2Q3LWJhYTg0MDhlYWQ1OSJ9.pY3maHPiIE7KsP-GfK5FsssRcsdH6-6M-0U3BFynrecredentials and optional parameters.

        Args:
            params (dict, optional): Parameters for initializing the client. Defaults to None.
        """

        # Setup credentials
        credentials = get_credentials()
        self.MERCHANT_KEY = credentials['PAYLOV_API_KEY']
        self.USERNAME = credentials['PAYLOV_USERNAME']
        self.PASSWORD = credentials['PAYLOV_PASSWORD']
        self.SUBSCRIPTION_KEY = credentials['PAYLOV_SUBSCRIPTION_KEY']

        # Provider attrs
        self.merchant_headers = {"api-key": self.MERCHANT_KEY}
        self.subscription_headers = {"api-key": self.SUBSCRIPTION_KEY}
        self.params = params
        self.error = False
        self.code = self.STATUS_CODES["SUCCESS"]
        self.transaction = self.get_transaction()

    def api_request(self, endpoint_key: str, payload: Optional[Dict] = None, params: Optional[Dict] = None) -> Tuple[
        bool, Dict]:
        """
        Sends an API request to the Paylov service.

        Args:
            endpoint_key (str): The key for the API endpoint.
            payload (dict, optional): The payload for POST requests. Defaults to None.
            params (dict, optional): The query parameters for GET and DELETE requests. Defaults to None.

        Returns:
            tuple: A tuple containing the success response data and the response data.
        """

        endpoint, method = self.API_ENDPOINTS[endpoint_key]
        url = self.SUBSCRIPTION_BASE_URL + str(endpoint)
        headers = self.subscription_headers

        method_map = {
            "POST": requests.post,
            "GET": requests.get,
            "DELETE": requests.delete
        }

        if method not in method_map:
            raise ValueError("Unsupported HTTP method")

        response = method_map[method](url, json=payload, headers=headers, params=params)
        return response.ok, response.json()

    @staticmethod
    def get_error_response(error_code: str) -> (bool, dict):
        error_details = error_codes[str(error_code).upper()]

        error_response = {
            "detail": error_details[1],
            "code": error_details[0]
        }
        return False, error_response

    def create_user_card(self, user: object, card_number: str, expire_date: str) -> Tuple[bool, Dict]:
        """
        Creates a new user card for subscription.

        Args:
            user_uuid (str): The UUID of the user.
            card_number (str): The card number.
            expire_date (str): The expiration date of the card.

        Returns:
            tuple: A tuple containing a boolean indicating success and a dictionary with the response data.
            @param expire_date:
            @param card_number:
            @param user:
        """

        expire_date_parts = str(expire_date).split("/")
        expire_date = expire_date_parts[1] + expire_date_parts[0]

        payload = {
            "userId": str(user.get_uuid()),
            "cardNumber": str(card_number),
            "expireDate": str(expire_date)
        }

        user_card = UserCard.objects.filter(card_number=card_number, user=user, confirmed=True, expire_date=expire_date)

        if user_card.exists():
            return self.get_error_response("card_exists")

        success, response_data = self.api_request("CREATE_CARD", payload=payload)

        if success:
            otp_sent_phone = response_data["result"]["otpSentPhone"]
            card_id = response_data["result"]["cid"]
            user_card, _ = UserCard.objects.update_or_create(
                user=user,
                card_number=card_number,
                expire_date=expire_date,
                defaults={
                    "card_id": card_id,
                    "provider": Providers.ProviderChoices.PAYLOV
                }
            )
            cache_key = f"otp_sent_phone_{user_card.id}"
            cache.set(cache_key, True, timeout=60)

            return success, {"otp_sent_phone": otp_sent_phone, "card_id": user_card.id}

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def confirm_user_card(self, user: User, card_id: int, otp: str) -> Tuple[bool, Dict]:
        """
        Confirms a user card.

        Args:
            user (User): The user object.
            card_id (str): The card ID.
            card_number (str): The card number.
            otp (int): The OTP code.

        Returns:
            tuple: A tuple containing a boolean indicating success and a dictionary with the response data.
        """

        try:
            card = UserCard.objects.get(user=user, id=card_id)
        except UserCard.DoesNotExist:
            return self.get_error_response("card_not_found")

        if card.confirmed:
            return self.get_error_response("card_is_already_activated")

        cache_key = f"otp_sent_phone_{card_id}"
        if not cache.get(cache_key):
            return self.get_error_response("invalid_otp")

        payload = {
            "cardId": card.card_id,
            "otp": otp,
            "card_name": user.full_name
        }

        success, response_data = self.api_request("CONFIRM_CARD", payload=payload)

        if success or response_data['error']['code'] == "card_is_already_activated":
            card.confirmed = True
            card.save(update_fields=["confirmed"])
            return True, {"card_id": card.id, "confirmed": True}

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def get_user_cards(self, user_uuid: str) -> Tuple[bool, Dict]:
        """
        Retrieves all cards for a user.

        Args:
            user_uuid (str): The UUID of the user.

        Returns:
            tuple: A tuple containing a boolean indicating success and a dictionary with the response data.
        """

        query_params = {"userId": str(user_uuid)}
        success, response_data = self.api_request("GET_CARDS", params=query_params)

        if success:
            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def delete_user_card(self, user: User, card_id: str) -> (bool, dict):

        """
        Deletes a user card.

        Args:
            user: User object
            card_id (str): The ID of the user card.

        Returns:
            tuple: A tuple containing a boolean indicating success and a dictionary with the response data.
        """
        card = UserCard.objects.filter(id=int(card_id)).first()

        if not card:
            raise NotFound("User card not found", code="card_not_found")

        card_id = card.card_id

        query_param = {"userCardId": card_id}
        success, response_data = self.api_request("DELETE_CARD", params=query_param)

        if success:
            cards = UserCard.objects.filter(user_id=user.id, card_id=card_id)
            for card in cards:
                card.soft_delete()
            response_data = {
                "detail": "User card is deleted successfully",
                "code": 204
            }
            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def create_receipt(self, user: object, card_id: int, amount: int, course_id: int, book_id: int, promo_code: str) -> Tuple[bool, Dict]:
        """
        Creates a receipt for a payment.

        Args:
            transaction (Transaction): The transaction object.
            user (object): User object

        Returns:
            tuple: A tuple containing a boolean indicating success and a dictionary with the response data.
            @param user:
            @param amount:
            @param card_id:
            @param course_id:
            @param book_id:
            @param promo_code:
        """
        try:
            user_card = UserCard.objects.get(pk=card_id)
        except UserCard.DoesNotExist:
            return self.get_error_response("card_not_found")

        if not user_card.confirmed:
            return self.get_error_response("card_is_not_activated")

        today = date.today()

        book = Book.objects.filter(id=book_id).first() if book_id else None
        course = Course.objects.filter(id=course_id).first() if course_id else None

        if book_id and not book:
            raise NotFound("Book not found")
        if course_id and not course:
            raise NotFound("Course not found")

        is_book = True if book else False

        if is_book:
            discount = Discount.objects.filter(book_id=book_id, start_date__lte=today, end_date__gte=today).first()
        else:
            discount = Discount.objects.filter(course__id=course_id, start_date__lte=today, end_date__gte=today).first()

        promo_code = PromoCode.objects.filter(code=promo_code, start_date__lte=today, end_date__gte=today).first()
        amount = calculate_amount_with_discount_promocode(discount, promo_code, amount, user)

        order = Order.objects.create(
            user=user,
            amount=amount,
            orginal_price=book.price if book else course.price,
            promo_code=promo_code,
            discount=discount,
            course=course,
            book=book,
        )

        transaction = Transaction.objects.create(
            order=order,
            provider=Providers.ProviderChoices.PAYLOV,
            amount=amount
        )

        payload = {
            "userId": str(transaction.user.get_uuid()),
            "amount": int(transaction.amount),
            "account": {
                "order_id": transaction.id
            }
        }

        success, response_data = self.api_request("CREATE_RECEIPT", payload=payload)

        if success:
            transaction.reference = response_data["result"]["transactionId"]
            transaction.provider = Providers.ProviderChoices.PAYLOV
            transaction.save(update_fields=["reference", "provider"])

            response_data["transaction"] = transaction
            response_data["user_card"] = user_card

            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def pay_receipt(self, transaction: Transaction, card: UserCard) -> Tuple[bool, Dict]:
        """
        Pays for a created receipt.

        Args:
            transaction (Transaction): The transaction object.
            card (UserCard): The user card object.

        Returns:
            tuple: A tuple containing a boolean indicating success, a dictionary with the response data, and the transaction object.
        """

        payload = {
            "transactionId": transaction.reference,
            "cardId": card.card_id
        }
        success, response_data = self.api_request("PAY_RECEIPT", payload=payload)

        if success:
            transaction_id = response_data["result"]["transactionId"]

            transaction.apply_transaction(
                provider=Providers.ProviderChoices.PAYLOV,
                transaction_id=transaction_id,
                is_paid_with_card=True,
                card=card
            )

            response_data = {
                "detail": "Payment is applied successfully",
                "code": "payment_success",
                "status": 200
            }

            return success, response_data

        error_code = response_data.get("error", {"code": "unknown_error"})["code"]
        return self.get_error_response(error_code)

    def get_transaction(self) -> Optional[Transaction]:
        """
        Retrieves the transaction based on provided parameters.

        Returns:
            Optional[Transaction]: The transaction object if found, otherwise None.
        """

        if not self.params or not self.params.get('account'):
            return None
        try:
            return Transaction.objects.get(id=self.params["account"]["order_id"])
        except Transaction.DoesNotExist:
            return None

    @classmethod
    def create_payment_link(cls, transaction: Transaction) -> str:
        """
        Generates a payment link for a transaction.

        Args:
            transaction (Transaction): The transaction object.

        Returns:
            str: The generated payment link.
        """
        import urllib.parse

        credentials = get_credentials()
        MERCHANT_KEY = credentials['PAYLOV_API_KEY']
        RETURN_URL = urllib.parse.quote(credentials['PAYLOV_REDIRECT_URL'] + f"?transaction_id={transaction.id}", safe='')

        if MERCHANT_KEY is None:
            raise ValueError("Credentials not found")

        amount = int(transaction.amount)
        query = f"merchant_id={MERCHANT_KEY}&amount={amount}&account.order_id={transaction.id}&return_url={RETURN_URL}"
        encode_params = base64.b64encode(query.encode("utf-8"))
        encode_params = str(encode_params, "utf-8")
        return f"{cls.CHECKOUT_BASE_URL}{encode_params}"

    def validate_transaction(self):
        """
        Validates if the transaction has already been completed.
        """

        if self.transaction.status == Transaction.TransactionStatus.SUCCESS:
            self.error = True
            self.code = self.STATUS_CODES["ORDER_ALREADY_PAID"]

    def validate_amount(self, amount: int):
        """
        Validates the amount of the transaction.

        Args:
            amount (int): The amount to be validated.
        """
        if int(self.transaction.amount) != int(amount):
            self.error = True
            self.code = self.STATUS_CODES["INVALID_AMOUNT"]

    def check_transaction(self) -> Tuple[bool, str]:
        """
        Checks the status of a transaction to ensure it exists and has valid details.

        Returns:
            tuple: A tuple containing a boolean indicating if there was an error and a status code as a string.
        """

        if not self.transaction:
            return True, self.STATUS_CODES["ORDER_NOT_FOUND"]

        self.validate_transaction()
        self.validate_amount(self.params['amount'])

        return self.error, self.code

    def perform_transaction(self) -> Tuple[bool, str]:
        """
        Performs the transaction by validating its status and amount.

        Returns:
            tuple: A tuple containing a boolean indicating if there was an error and a status code as a string.
        """
        if not self.transaction:
            return True, self.STATUS_CODES["ORDER_ALREADY_PAID"]

        if self.transaction.status == Transaction.TransactionStatus.FAILED:
            return True, self.STATUS_CODES["SERVER_ERROR"]

        self.validate_transaction()
        self.validate_amount(self.params["amount"])

        return self.error, self.code