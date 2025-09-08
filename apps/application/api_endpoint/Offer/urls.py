from django.urls import path
from .views import OfferListAPIView, OfferUpdateAPIView

urlpatterns = [
    path("list/", OfferListAPIView.as_view()),
    path("update/<int:id>/", OfferUpdateAPIView.as_view(), name="offer-update"),
]
   