from django.urls import path
from .views import ApplicationListAPIView, ApplicationCreateAPIView

urlpatterns = [
    path("list/", ApplicationListAPIView.as_view()),
    path("create/", ApplicationCreateAPIView.as_view()),
]