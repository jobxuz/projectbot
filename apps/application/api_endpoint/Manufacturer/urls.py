from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.ManufacturerCreateAPIView.as_view()),
    path("detail/<int:pk>/", views.ManufacturerDetailAPIView.as_view()),
    path("list/", views.ManufacturerListAPIView.as_view()),
    path("certificate/", views.ManufacturerCertificateAPIView.as_view()),
    path("company-image/", views.ManufacturerCompanyImageAPIView.as_view()),
]