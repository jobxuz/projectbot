from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from apps.application.models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer, PaymentWebhookSerializer

@extend_schema(tags=["Payment"])
class PaymentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user.botuser)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user.botuser)
        
        # To'lov tizimiga yuborish
        from apps.application.services.payment_service import create_payment
        payment_data = create_payment(payment)
        
        return Response({
            'payment_id': payment.id,
            'payment_url': payment_data.get('payment_url'),
            'transaction_id': payment_data.get('transaction_id')
        })

@extend_schema(tags=["Payment"])
class PaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user.botuser)

@extend_schema(tags=["Payment"])
@api_view(['POST'])
@permission_classes([AllowAny])
def payment_webhook(request, provider):
    """
    To'lov provayderlari webhook
    """
    serializer = PaymentWebhookSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    try:
        payment = Payment.objects.get(transaction_id=data['transaction_id'])
        
        if provider == 'click':
            from apps.application.services.payment_service import process_click_webhook
            process_click_webhook(payment, data)
        elif provider == 'payme':
            from apps.application.services.payment_service import process_payme_webhook
            process_payme_webhook(payment, data)
        elif provider == 'visa':
            from apps.application.services.payment_service import process_visa_webhook
            process_visa_webhook(payment, data)
        
        return Response({'status': 'success'})
        
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=["Payment"])
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_subscription_payment(request):
    """
    Zavod obuna uchun to'lov
    """
    from apps.application.services.payment_service import create_subscription_payment
    
    try:
        payment_data = create_subscription_payment(request.user.botuser)
        return Response(payment_data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Payment"])
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_catalog_access_payment(request):
    """
    Katalog kirish uchun to'lov
    """
    from apps.application.services.payment_service import create_catalog_access_payment
    
    try:
        payment_data = create_catalog_access_payment(request.user.botuser)
        return Response(payment_data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
