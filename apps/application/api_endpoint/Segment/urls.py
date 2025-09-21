from django.urls import path
from .views import SegmentListAPIView

urlpatterns = [
    path("list/", SegmentListAPIView.as_view()),
]
   