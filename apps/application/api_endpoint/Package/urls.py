from django.urls import path
from .views import PackageListAPIView, PackageDetailAPIView

urlpatterns = [
    path("list/", PackageListAPIView.as_view()),
    path("detail/<int:pk>/", PackageDetailAPIView.as_view()),
]