from django.urls import path
from .views import PackageListAPIView, PackageDetailAPIView

urlpatterns = [
    path("list/", PackageListAPIView.as_view()),
    path("detail/<int:id>/", PackageDetailAPIView.as_view()),
]