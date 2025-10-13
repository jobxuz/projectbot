from django.db import models


class UserCardManager(models.Manager):
    def active(self):
        return super().get_queryset().filter(is_deleted=False)