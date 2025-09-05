from django.urls import path
from .views import SliderListAPIView

urlpatterns = [
    path("list/", SliderListAPIView.as_view()),
]