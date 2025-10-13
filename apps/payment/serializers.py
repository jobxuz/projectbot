from typing import Dict, Any

from django.utils.translation import gettext as _
from rest_framework import serializers

from account.models import User
from common.serializers import MediaURLSerializer
from study.models import PromoCode, Course, GroupMember
from payment.models import Providers, Order, Transaction, UserCard, PaymentProvider
from payment.validators import validate_card_expire_date
from payment.paylov.client import PaylovClient
from payment import exceptions
from datetime import date
from rest_framework.exceptions import NotFound, APIException, ValidationError

from .card_identifier import get_card_identifier
from book.models import Book

from .utils import get_discount_for_payment


class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer for creating an order and transaction.

    This serializer handles the creation of an order and associated transaction with payment provider details.
    """

    provider = serializers.ChoiceField(choices=Providers.ProviderChoices.choices)
    promo_code = serializers.CharField(required=False)
    course_id = serializers.IntegerField(required=False)
    book_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        course_id = attrs.get("course_id")
        user = self.context.get('user', None)

        if not course_id and not attrs.get("book_id"):
            raise serializers.ValidationError(_("Either course_id or book_id must be provided."))
        if course_id and attrs.get("book_id"):
            raise serializers.ValidationError("Only one book or course can be given")

        if GroupMember.objects.filter(group__flow__course__id=course_id, student=user).exists():
            raise ValidationError(_("A StudentLesson with this student, lesson, and flow already exists."))

        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an order and transaction.

        Args:
            validated_data (dict): Validated data containing the amount and provider details.

        Returns:
            dict: A dictionary containing the payment URL for the created transaction.
        Raises:
            serializers.ValidationError: If credentials are not found or an unexpected error occurs.
        """
        today = date.today()
        user = self.context['request'].user

        course_id = validated_data.get('course_id', None)
        book_id = validated_data.get('book_id', None)

        book = Book.objects.filter(id=book_id).first() if book_id else None
        course = Course.objects.filter(id=course_id).first() if course_id else None

        if book_id and not book:
            raise NotFound(detail=_("Book not found"), code="book_not_found")

        if course_id and not course:
            raise NotFound(detail=_("Course not found"), code="course_not_found")

        amount = book.price if book else course.price

        discount = get_discount_for_payment(book, course, today)
        if discount:
            discount_price = int((amount / 100) * discount.percentage)
            amount -= discount_price

        promo_code = PromoCode.objects.filter(
            code=validated_data.get('promo_code'),
            start_date__lte=today,
            end_date__gte=today,
        ).first()

        if promo_code and user not in promo_code.users_who_used.all():
            amount -= promo_code.amount
            # NOTE: can't add user to promo list before checking the status of the transaction

        if amount < 0:
            raise ValidationError(detail=_("Amount cannot be negative"), code="invalid_amount")

        order = Order.objects.create(
            user=user,
            amount=amount,
            orginal_price=book.price if book else course.price,
            promo_code=promo_code,
            discount=discount,
            course=course,
            book=book,
        )

        transaction: Transaction = Transaction.objects.create(
            order=order,
            amount=order.amount,
            provider=validated_data["provider"]
        )

        try:
            payment_url = transaction.get_payment_url()
        except ValueError:
            raise serializers.ValidationError(detail=_("Credentials not found"), code="invalid")
        except Exception as e:
            raise serializers.ValidationError(detail=_(f"Something went wrong: {str(e)}"), code="invalid")

        return {"payment_url": payment_url, 'transaction_id': transaction.id}


class AddUserCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, min_length=16)
    expire_date = serializers.CharField(validators=[validate_card_expire_date])

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a user card with the given validated data.

        Args:
            validated_data (Dict[str, Any]): The validated data containing card information.

        Returns:
            Dict[str, Any]: The response data from the card creation process.

        Raises:
            serializers.ValidationError: If the card creation fails due to invalid credentials or other errors.
        """

        user = self.context["request"].user
        try:
            card_number = validated_data["card_number"]
            expire_date = validated_data["expire_date"]

            user_card = UserCard.objects.filter(card_number=card_number, expire_date=expire_date).first()
            
            if user_card:
                raise exceptions.PaymentFailureException(
                    detail=_("Card is already registered."),
                    code="payment_failure"
                )
                
            client = PaylovClient()
            success, response_data = client.create_user_card(user, card_number, expire_date)

            if not success:
                raise exceptions.PaymentFailureException(
                    detail={response_data.get("code"): [response_data.get("detail")]},
                    code="payment_failure"
                )
            return response_data

        except exceptions.PaymentFailureException as e:
            raise serializers.ValidationError(
                detail=e.detail,
                code=e.code
            )

        except Exception as e:
            raise serializers.ValidationError(
                detail=_(f"Something went wrong. {str(e)}"),
                code="unknown_error"
            )


class ConfirmUserCardSerializer(serializers.Serializer):
    """
    Serializer for confirming a user's card.
    """
    card_id = serializers.IntegerField()
    otp = serializers.CharField()

    def create(self, validated_data):
        """
        Confirm a user's card with the provided OTP.

        :param validated_data: Validated data containing card ID and OTP.
        :return: Response data from the PaylovClient.
        :raises: serializers.ValidationError with appropriate error messages and codes.
        """
        user = self.context["request"].user
        try:
            card_id = validated_data["card_id"]
            otp = validated_data["otp"]

            client = PaylovClient()
            success, response_data = client.confirm_user_card(user, card_id, str(otp))

            if not success:
                raise exceptions.PaymentFailureException(
                    detail=_("OTP is invalid."),
                    code="payment_failure"
                )
            return response_data

        except exceptions.PaymentFailureException as e:
            raise serializers.ValidationError(detail=e.detail, code=e.code)

        except Exception as e:
            raise serializers.ValidationError(
                detail=_(f"Something went wrong. {str(e)}"), 
                code="unknown_error")


class DeleteUserCardSerializer(serializers.Serializer):
    """
    Serializer for deleting a user's card.
    """
    id = serializers.IntegerField()

    def create(self, validated_data):
        """
        Delete a user's card with the provided card ID.

        :param validated_data: Validated data containing the card ID.
        :return: Response data from the PaylovClient.
        :raises: serializers.ValidationError with appropriate error messages and codes.
        """
        user = self.context["request"].user
        card_id = validated_data["id"]
        try:
            user_card = UserCard.objects.filter(id=card_id, user=user).first()
            if not user_card:
                raise NotFound("User card not found", code="card_not_found")
            else:
                client = PaylovClient()
                success, response_data = client.delete_user_card(user, card_id)

                if not success:
                    raise exceptions.PaymentFailureException(**response_data)
            return response_data

        except exceptions.PaymentFailureException as e:
            raise NotFound(detail=f"{e.detail} in Paylov", code=e.code)

        except Exception as e:
            raise APIException(detail=_(f"Something went wrong. {str(e)}"), code="unknown_error")


class UserCardListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing user cards.
    """
    title = serializers.SerializerMethodField()
    expire_date = serializers.SerializerMethodField()
    card_type = serializers.SerializerMethodField()

    class Meta:
        model = UserCard
        fields = ("id", "title", "expire_date", "confirmed", 'provider', 'card_type')

    def get_title(self, obj):
        return obj.title

    def get_expire_date(self, obj):
        """
        Get the expiration date of the user card.

        :param obj: UserCard instance.
        :return: Expiration date of the card.
        """
        return obj.exp_date

    def get_card_type(self, obj):
        first_4_dig = obj.card_number[0:5]
        card_identifier = get_card_identifier(first_4_dig)
        if card_identifier is not None:
            return card_identifier
        else:
            return None


class PayWithCardSerializer(serializers.Serializer):
    """
    Serializer for confirming a user's card.
    """
    card_id = serializers.IntegerField()
    course_id = serializers.IntegerField(required=False)
    book_id = serializers.IntegerField(required=False)
    promo_code = serializers.CharField(required=False)

    def validate(self, attrs):
        if not attrs.get('course_id') and not attrs.get('book_id'):
            raise ValidationError(_("Either course_id or book_id must be provided."))
        if attrs.get("course_id") and attrs.get("book_id"):
            raise ValidationError(_("Only one book or course can be given"))

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        card_id = validated_data["card_id"]
        promo_code = validated_data.get("promo_code")
        course_id = validated_data.get("course_id")
        book_id = validated_data.get("book_id")

        try:
            course = Course.objects.get(pk=course_id) if course_id else None
            book = Book.objects.get(pk=book_id) if book_id else None
        except Course.DoesNotExist:
            raise NotFound(detail=_("Course does not exist."), code="course_not_found")
        except Book.DoesNotExist:
            raise NotFound(detail=_("Book does not exist."), code="book_not_found")

        amount = book.price if book else course.price

        try:
            client = PaylovClient()
            created, response_data = client.create_receipt(user, card_id, amount, course_id, book_id, promo_code)

            if not created:
                raise exceptions.PaymentFailureException(**response_data)

            transaction = response_data["transaction"]
            user_card = response_data["user_card"]

            success, response_data = client.pay_receipt(transaction, user_card)

            if not success:
                raise exceptions.PaymentFailureException(**response_data)

            return response_data

        except exceptions.PaymentFailureException as e:
            raise serializers.ValidationError({"detail": e.detail, "code": e.code})

        except Exception as e:
            raise serializers.ValidationError(
                detail=_(f"Something went wrong. {str(e)}"), 
                code="unknown_error")


class TransactionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("status", )


class PaymentProvidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = ('provider', 'icon', 'title',)


class CardIdentifySerializer(serializers.Serializer):
    digits = serializers.CharField(max_length=6, required=True)


class OrderCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'id')


class PaymentHistorySerializer(serializers.ModelSerializer):
    course = OrderCourseSerializer(source='order.course', read_only=True, allow_null=True)
    card = UserCardListSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Transaction
        fields = ('amount', 'status', 'paid_at', 'provider', 'is_paid_with_card', 'card', 'course')


class TransactionUserSerializer(serializers.ModelSerializer):
    avatar = MediaURLSerializer()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'avatar')


class TransactionHistoryListSerializer(serializers.ModelSerializer):
    user = TransactionUserSerializer(source='order.user', read_only=True)
    course = serializers.SerializerMethodField()
    is_joined_group = serializers.BooleanField(source='order.is_joined_group', read_only=True)

    class Meta:
        model = Transaction
        fields = (
            'id',
            'provider', 'transaction_id',
            'amount', 'paid_at',
            'user', 'course', 
            'is_joined_group'
        )

    def get_course(self, obj):
        course = obj.order.course
        if course:
            return {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "price": course.price
            }
        return None


class TransactionDetailSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'provider', 'paid_at', 'transaction_id', 'course')
        
    def get_course(self, obj):
        course = obj.order.course
        if course:
            return {
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'price': course.price,
            }
        return None
    
    
class ProviderListSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.CharField()
