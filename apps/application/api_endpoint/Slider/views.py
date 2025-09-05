from rest_framework import generics
from rest_framework.filters import OrderingFilter
from apps.application.models import Slider

from .serializers import SliderSerializer

class SliderListAPIView(generics.ListAPIView):
    queryset = Slider.objects.filter(is_active=True)
    serializer_class = SliderSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['order']