from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.application.models import BotUser, Customer, Manufacturer
from .serializers import BotUserRegisterSerializer
from rest_framework.exceptions import ValidationError

@extend_schema(tags=["BotUser"])
class BotUserRegisterAPIView(APIView):
    serializer_class = BotUserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        telegram_id = serializer.validated_data.get('telegram_id')
        existing_user = BotUser.objects.filter(telegram_id=telegram_id).first()
        customer = Customer.objects.select_related('user').filter(user__telegram_id=telegram_id).first()
        manufacturer = Manufacturer.objects.select_related('user').filter(user__telegram_id=telegram_id).first()
            
        if existing_user:
            return Response({
                'success': True,
                'message': 'Foydalanuvchi allaqachon mavjud',
                'user_id': existing_user.id,
                'is_new': False,
                'customer': customer.id if customer else None,
                "manufacturer": manufacturer.id if manufacturer else None
            }, status=status.HTTP_200_OK)
            
        user = serializer.save()
        return Response({
            'success': True,
            'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi',
            'user_id': user.id,
            'is_new': True,
            'customer': customer.id if customer else None,
            "manufacturer": manufacturer.id if manufacturer else None
        }, status=status.HTTP_201_CREATED)
        
@extend_schema(tags=["BotUser"],
               parameters=[
            OpenApiParameter(
                name='type',
                description="Type of user to delete",
                type=OpenApiTypes.STR,
                enum=['customer', 'manufacturer', 'both'],
                required=True
            )
        ])
class DeleteAccountAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, user_id, *args, **kwargs):
        type = request.query_params.get('type')
        if not type in ['customer', 'manufacturer', 'both']:
            raise ValidationError("type is not valid")
        
        user = BotUser.objects.filter(id=user_id).first()
        if user is None:
            raise ValidationError("User does not found")
        
        customer = getattr(user, 'customer', None)
        manufacturer = getattr(user, 'manufacturer', None)
        
        if type == 'customer' and not customer:
            return Response({
                'success': False,
                'message': 'User is not a customer'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if type == 'manufacturer' and not manufacturer:
            return Response({
                'success': False,
                'message': 'User is not a manufacturer'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()
        
        return Response({
            'success': True,
            'message': 'Account successfully deleted',
            'deleted_customer': customer is not None,
            'deleted_manufacturer': manufacturer is not None
        }, status=status.HTTP_200_OK)
            
        