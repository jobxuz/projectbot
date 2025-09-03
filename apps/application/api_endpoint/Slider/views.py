from rest_framework import generics

from apps.application.models import Slider

from .serializers import SliderSerializer

class SliderListAPIView(generics.ListAPIView):
    queryset = Slider.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = SliderSerializer
