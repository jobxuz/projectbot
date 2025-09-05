from django.urls import path
from .views import AdditionalServiceListAPIView, AdditionalServiceApplyAPIView

urlpatterns = [
    path("list/", AdditionalServiceListAPIView.as_view()),
    path("apply/", AdditionalServiceApplyAPIView.as_view()),
]