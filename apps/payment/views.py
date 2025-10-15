# from django.db.models import Sum
# from django_filters.rest_framework import DjangoFilterBackend
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import status
# from rest_framework.exceptions import ValidationError, APIException
# from rest_framework.filters import SearchFilter
# from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
# from rest_framework.parsers import MultiPartParser
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from typing import Any, Dict

# from account.permissions import IsWorker
# from .models import UserCard, Transaction, PaymentProvider, Providers
# from . import serializers
# from .card_identifier import get_card_identifier, identify_card_type_four_digits
# from . import filters
# from django.utils.translation import gettext as _


# class CreateOrderAPIView(GenericAPIView):
#     """
#     API view for creating an order.
#     This view handles the creation of an order based on the provided data.
#     """

#     serializer_class = serializers.CreateOrderSerializer
#     permission_classes = [IsAuthenticated]
#     parser_classes = (MultiPartParser,)

#     def post(self, request, *args, **kwargs) -> Response:
#         """
#         Handle POST requests for creating an order.

#         Args:
#             request (Any): The HTTP request object.
#             *args: Additional positional arguments.
#             **kwargs: Additional keyword arguments.

#         Returns:
#             Response: The HTTP response containing the result of the order creation.
#         """

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         try:
#             result = serializer.save()
#             return Response(result, status=status.HTTP_200_OK)
#         except ValidationError as e:
#             raise ValidationError(detail=e.detail, code=e)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['user'] = self.request.user
#         return context


# class AddUserCardAPIView(GenericAPIView):
#     """
#     API view for adding a user card. This view expects a POST request with card details,
#     validates the input data, and creates a user card.
#     """
#     serializer_class = serializers.AddUserCardSerializer
#     permission_classes = (IsAuthenticated,)
#     parser_classes = (MultiPartParser,)
#     queryset = []

#     def post(self, request, *args, **kwargs):
#         """
#         Handles the POST request to add a user card.

#         Args:
#             request (Any): The HTTP request containing card data.
#             *args (Any): Additional positional arguments.
#             **kwargs (Any): Additional keyword arguments.

#         Returns:
#             Response: The HTTP response containing the result of the card creation process.
#         """
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             result = serializer.save()
#             return Response(result, status=status.HTTP_200_OK)


# class ConfirmUserCardAPIView(GenericAPIView):
#     """
#     API view to confirm a user's card.
#     """
#     serializer_class = serializers.ConfirmUserCardSerializer
#     permission_classes = (IsAuthenticated,)
#     parser_classes = (MultiPartParser,)

#     def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
#         """
#         Handle POST request to confirm a user's card.

#         :param request: The request object containing user data.
#         :return: Response object with the result of the card confirmation.
#         """
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             result = serializer.save()
#             return Response(result, status=status.HTTP_200_OK)
#         raise APIException(serializer.errors, code="not_valid")


# class DeleteUserCardAPIView(GenericAPIView):
#     """
#     API view to delete a user's card.
#     """
#     serializer_class = serializers.DeleteUserCardSerializer
#     # permission_classes = (IsAuthenticated,)
#     permission_classes = []

#     parser_classes = (MultiPartParser,)

#     @swagger_auto_schema(request_body=serializers.DeleteUserCardSerializer)
#     def delete(self, request, *args, **kwargs):
#         """
#         Handle DELETE request to remove a user's card.

#         :param request: The request object containing user data.
#         :return: Response object with the result of the card deletion.
#         """
#         data = request.data if request.data.get('id') else request.GET
#         serializer = self.get_serializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response: Dict[str, Any] = {
#                 "detail": "Card removed successfully",
#                 "code": "card_removed",
#                 "status_code": 204
#             }
#             return Response(response, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GetUserCardListAPIView(ListAPIView):
#     """
#     API view to get a list of user cards.
#     """
#     queryset = UserCard.objects.active()
#     serializer_class = serializers.UserCardListSerializer
#     permission_classes = (IsAuthenticated,)
#     pagination_class = None

#     def get_queryset(self):
#         """
#         Get the queryset of user cards for the authenticated user.

#         :return: Queryset filtered by the authenticated user.
#         """

#         qs = super().get_queryset()
#         qs = qs.filter(user=self.request.user, confirmed=True)
#         return qs


# class PayWithCardAPIView(GenericAPIView):
#     serializer_class = serializers.PayWithCardSerializer
#     permission_classes = (IsAuthenticated,)
#     parser_classes = (MultiPartParser,)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             result = serializer.save()
#             return Response(result, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# class TransactionStatusAPIView(RetrieveAPIView):
#     queryset = Transaction.objects.all()
#     serializer_class = serializers.TransactionStatusSerializer
#     permission_classes = (IsAuthenticated,)
#     parser_classes = (MultiPartParser,)


# class PaymentProvidersAPIView(ListAPIView, CreateAPIView):
#     queryset = PaymentProvider.objects.all()
#     serializer_class = serializers.PaymentProvidersSerializer

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return []
#         return [IsAuthenticated]


# class CardIdentifyView(GenericAPIView):
#     serializer_class = serializers.CardIdentifySerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             card_number = serializer.validated_data.get("digits")
#             card_identifier = get_card_identifier(card_number)
#             if card_identifier is not None:
#                 return Response(data=card_identifier)
#             response = identify_card_type_four_digits(card_number)
#             if response:
#                 return Response(data={"source": response, "vendor": response})
#             raise ValidationError(detail=_("Card Number is not supported"), code="invalid_card_number")


# class PaymentHistoryAPIView(ListAPIView):
#     serializer_class = serializers.PaymentHistorySerializer
#     queryset = Transaction.objects.all()
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = filters.TransactionFilterSet

#     def get_queryset(self):
#         return Transaction.objects.filter(
#             order__user=self.request.user, status=Transaction.TransactionStatus.SUCCESS
#         ).order_by("-paid_at")


# class TransactionsHistoryListAPIView(ListAPIView):
#     queryset = Transaction.objects.all()
#     serializer_class = serializers.TransactionHistoryListSerializer
#     user_serializer_class = serializers.TransactionUserSerializer
#     permission_classes = [IsAuthenticated, IsWorker]
#     filterset_class = filters.TransactionListFilterSet
#     search_fields = ["order__user__phone_number", "order__user__full_name", "transaction_id"]
#     filter_backends = [DjangoFilterBackend, SearchFilter]

#     def get_queryset(self):
#         return (
#             Transaction.objects.filter(
#                 status=Transaction.TransactionStatus.SUCCESS
#             ).select_related("order", "order__user").order_by("-paid_at")
#         )

#     def get(self, request, *args, **kwargs):
#         response = super().get(request, *args, **kwargs)
#         if request.query_params.get("order__user"):
#             user = request.query_params.get("order__user")
#             paid_courses_count = Transaction.objects.filter(
#                 order__user=user, status=Transaction.TransactionStatus.SUCCESS
#             ).distinct("order__course").count()
#             total_paid_amount = Transaction.objects.filter(
#                 order__user=user, status=Transaction.TransactionStatus.SUCCESS
#             ).aggregate(total=Sum("amount"))["total"] or 0
#             user_data = self.user_serializer_class(request.user).data
#             user_data["paid_courses_count"] = paid_courses_count
#             user_data["total_paid_amount"] = total_paid_amount
#             response.data["user"] = user_data
#         return response


# class TransactionDetailAPIView(RetrieveAPIView):
#     queryset = Transaction.objects.filter(status=Transaction.TransactionStatus.SUCCESS)
#     serializer_class = serializers.TransactionDetailSerializer
#     permission_classes = [IsAuthenticated, IsWorker]


# class ProviderNameListAPIView(ListAPIView):
#     serializer_class = serializers.ProviderListSerializer
    
#     def get_queryset(self):
#         choices = []
#         for choice in Providers.ProviderChoices.choices:
#             choices.append({"title": choice[1], "slug": choice[0]})
#         return choices