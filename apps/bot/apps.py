from django.apps import AppConfig
import asyncio
import threading


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bot'
