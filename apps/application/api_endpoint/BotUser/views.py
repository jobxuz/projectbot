from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.application.models import BotUser
from .serializers import BotUserRegisterSerializer

class BotUserRegisterAPIView(APIView):
    serializer_class = BotUserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        telegram_id = serializer.validated_data.get('telegram_id')
        existing_user = BotUser.objects.filter(telegram_id=telegram_id).first()
            
        if existing_user:
            return Response({
                'success': True,
                'message': 'Foydalanuvchi allaqachon mavjud',
                'user_id': existing_user.id,
                'is_new': False
            }, status=status.HTTP_200_OK)
            
        user = serializer.save()
        return Response({
            'success': True,
            'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi',
            'user_id': user.id,
            'is_new': True
        }, status=status.HTTP_201_CREATED)
