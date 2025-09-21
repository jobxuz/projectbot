from drf_spectacular.utils import extend_schema

from apps.application.models import Segment
from .serializers import SegmentListSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import UpdateAPIView


    
    
@extend_schema(tags=["Segment"])
class SegmentListAPIView(ListAPIView):
    queryset = Segment.objects.all()
    serializer_class = SegmentListSerializer
    filter_backends = [SearchFilter] 
    search_fields = ["title"]
