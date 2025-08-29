from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from drf_spectacular.utils import extend_schema

from apps.application.models import Tender, TenderResponse
from .serializers import (
    TenderSerializer, TenderCreateSerializer, TenderDetailSerializer,
    TenderResponseSerializer, TenderResponseCreateSerializer
)

@extend_schema(tags=["Tender"])
class TenderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tender.objects.filter(status='active').order_by('-created_at')
    serializer_class = TenderSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TenderCreateSerializer
        return TenderSerializer
    
    def perform_create(self, serializer):
        # Lot raqamini avtomatik yaratish
        import random
        import string
        
        while True:
            lot_number = ''.join(random.choices(string.digits, k=6))
            if not Tender.objects.filter(lot_number=lot_number).exists():
                break
        
        # Customer ni topish
        customer = self.request.user.botuser.customer
        tender = serializer.save(
            customer=customer,
            lot_number=lot_number
        )
        
        # Bitrix24 ga yuborish
        from apps.application.tasks import create_bitrix_deal
        create_bitrix_deal.delay(tender.id)

@extend_schema(tags=["Tender"])
class TenderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'lot_number'
    
    def get_queryset(self):
        return Tender.objects.select_related('customer').prefetch_related('responses__manufacturer')

@extend_schema(tags=["Tender"])
class TenderResponseCreateAPIView(generics.CreateAPIView):
    queryset = TenderResponse.objects.all()
    serializer_class = TenderResponseCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        tender_id = self.kwargs.get('tender_id')
        tender = Tender.objects.get(id=tender_id)
        manufacturer = self.request.user.botuser.manufacturer
        
        response = serializer.save(
            tender=tender,
            manufacturer=manufacturer
        )
        
        # Tender javoblar sonini yangilash
        tender.responses_count = tender.responses.count()
        tender.save()
        
        # Bitrix24 ga izoh qo'shish
        from apps.application.tasks import add_bitrix_comment
        add_bitrix_comment.delay(response.id)

@extend_schema(tags=["Tender"])
class TenderSearchAPIView(generics.ListAPIView):
    serializer_class = TenderSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Tender.objects.filter(status='active')
        
        # Filtrlash
        product_segment = self.request.query_params.get('product_segment')
        if product_segment:
            queryset = queryset.filter(product_segment=product_segment)
        
        # Qidiruv
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(product_description__icontains=search) |
                Q(customer__company_name__icontains=search)
            )
        
        return queryset.order_by('-created_at')

@extend_schema(tags=["Tender"])
class MyTendersAPIView(generics.ListAPIView):
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'botuser') and hasattr(user.botuser, 'customer'):
            return Tender.objects.filter(customer=user.botuser.customer)
        elif hasattr(user, 'botuser') and hasattr(user.botuser, 'manufacturer'):
            # Zavod javob bergan tenderlar
            return Tender.objects.filter(
                responses__manufacturer=user.botuser.manufacturer
            ).distinct()
        return Tender.objects.none()
