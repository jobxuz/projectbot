from django.core.management.base import BaseCommand
import asyncio
from apps.bot.misc import start_webhook


class Command(BaseCommand):
    help = 'Start Telegram bot webhook'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting bot webhook...'))
        
        try:
            asyncio.run(start_webhook())
            self.stdout.write(self.style.SUCCESS('Bot webhook started successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Bot start error: {e}'))
