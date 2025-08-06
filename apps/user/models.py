from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(
        _("Phone number"),
        max_length=20,
        null=True, blank=True
    )
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    telegram_username = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.telegram_id}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")