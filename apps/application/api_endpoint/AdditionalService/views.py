from django.db.models import Exists, OuterRef
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.application.models import AdditionalService, UserApply
from .serializers import AdditionalServiceSerializer, UserApplySerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema(tags=["Service"])
class AdditionalServiceListAPIView(ListAPIView):
    queryset = AdditionalService.objects.filter(is_active=True)
    serializer_class = AdditionalServiceSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['type', 'option']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

@extend_schema(tags=["Service"])
class AdditionalServiceApplyAPIView(CreateAPIView):
    queryset = UserApply.objects.all()
    serializer_class = UserApplySerializer
