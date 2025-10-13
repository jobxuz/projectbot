from django.urls import path, include
from payment import views

urlpatterns = [
    path('generate-payment-link/', views.CreateOrderAPIView.as_view()),
    path("cards/add/", views.AddUserCardAPIView.as_view()),
    path("cards/confirm/", views.ConfirmUserCardAPIView.as_view()),
    path("cards/delete/", views.DeleteUserCardAPIView.as_view()),
    path("cards/list/", views.GetUserCardListAPIView.as_view()),
    path("cards/pay-with-card/", views.PayWithCardAPIView.as_view()),
    path("payment/status/<int:pk>/", views.TransactionStatusAPIView.as_view()),
    path("callbacks/", include("payment.paylov.urls")),
    path("callbacks/", include("payment.payme.urls")),
    path("callbacks/", include("payment.click.urls")),
    path('payment-providers/', views.PaymentProvidersAPIView.as_view()),
    path('card-identify/', views.CardIdentifyView.as_view()),
    path('payment-history/', views.PaymentHistoryAPIView.as_view()),
    path('transactions/histroy/', views.TransactionsHistoryListAPIView.as_view()),
    path('transactions/<int:pk>/', views.TransactionDetailAPIView.as_view()),
    path('providers/list/', views.ProviderNameListAPIView.as_view()),
]
