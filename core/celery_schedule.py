from celery.schedules import crontab

# Celery Beat schedule configuration
CELERY_BEAT_SCHEDULE = {
    # Har kuni soat 10:00 da obuna muddati tekshiruvi
    'check-subscription-expiry': {
        'task': 'apps.application.tasks.check_subscription_expiry',
        'schedule': crontab(hour=10, minute=0),  # Har kuni 10:00 da
    },
    
    # Har hafta eski notificationlarni tozalash
    'cleanup-old-notifications': {
        'task': 'apps.application.tasks.cleanup_old_notifications',
        'schedule': crontab(hour=2, minute=0, day_of_week=1),  # Dushanba kuni 02:00 da
    },
    
    # Har kuni kechqurun kunlik hisobot yuborish
    'send-daily-summary': {
        'task': 'apps.application.tasks.send_daily_summary',
        'schedule': crontab(hour=20, minute=0),  # Har kuni 20:00 da
    },
    
    # Har 30 daqiqada notification tizimini tekshirish
    'check-notification-health': {
        'task': 'apps.application.tasks.check_notification_health',
        'schedule': crontab(minute='*/30'),  # Har 30 daqiqada
    },
    
    # Har kuni tushda faol foydalanuvchilar statistikasi
    'daily-user-stats': {
        'task': 'apps.application.tasks.daily_user_stats',
        'schedule': crontab(hour=12, minute=0),  # Har kuni 12:00 da
    },
    
    # Har hafta standart tour paketlarini tekshirish
    'check-tour-packages': {
        'task': 'apps.application.tasks.create_default_tour_packages',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),  # Dushanba kuni 09:00 da
    },
}
