from django.urls import path
from apps.bot.views import process_update

app_name = "bot"

urlpatterns = [
    path("<str:token>/", process_update, name="webhook")
]
