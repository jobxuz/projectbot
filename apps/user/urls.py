from django.urls import path
from .api_endpoint.auth import views



urlpatterns = [
    path("auth/register/", views.RegisterView.as_view(), name="rgister"),
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
]
