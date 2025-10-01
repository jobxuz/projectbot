from django.urls import path
from .views import ManufacturerCreateAPIView, ManufacturerDetailAPIView, ManufacturerListAPIView, ManufacturerCertificateAPIView

urlpatterns = [
    path("create/", ManufacturerCreateAPIView.as_view()),
    path("detail/<int:id>/", ManufacturerDetailAPIView.as_view()),
    path("list/", ManufacturerListAPIView.as_view()),
    path("certificate/", ManufacturerCertificateAPIView.as_view()),
]