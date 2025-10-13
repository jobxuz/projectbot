from django.urls import path

from payment.click.Complete.views import ClickCompleteAPIView
from payment.click.Prepare.views import ClickPrepareAPIView

urlpatterns = [
    path("click/prepare/", ClickPrepareAPIView.as_view(), ),
    path("click/complete/", ClickCompleteAPIView.as_view(), ),
]
