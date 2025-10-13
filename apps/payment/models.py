import datetime
from django.db import models

from payment import managers
from django.contrib.auth import get_user_model

User = get_user_model()

class ProviderChoices(models.TextChoices):
    PAYLOV = "paylov", "Paylov"
    PAYME = "payme", "Payme"
    CLICK = "click", "Click UP"


class Transaction(models.Model):
    class TransactionStatus(models.TextChoices):
        WAITING = "waiting", "Waiting"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(User, related_name="orders", on_delete=models.PROTECT)
    provider = models.CharField(choices=ProviderChoices.choices, max_length=15, default=ProviderChoices.PAYLOV)
    status = models.CharField(choices=TransactionStatus.choices, max_length=15, default=TransactionStatus.WAITING)
    amount = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    payment_url = models.CharField(null=True, blank=True, max_length=512)
    reference = models.TextField(null=True, blank=True)
    transaction_id = models.CharField(max_length=512, null=True, blank=True)
    is_paid_with_card = models.BooleanField(default=False)
    card = models.ForeignKey("payment.UserCard", null=True, blank=True, on_delete=models.PROTECT)

    extra = models.JSONField(null=True, blank=True)

    def get_payment_url(self):
        payment_link = None
        if self.provider == ProviderChoices.PAYLOV:
            from payment.paylov.client import PaylovClient
            payment_link = PaylovClient.create_payment_link(self)

        if self.provider == ProviderChoices.PAYME:
            from payment.payme.client import PaymeClient
            payment_link = PaymeClient.create_payment_link(self)

        if self.provider == ProviderChoices.CLICK:
            from payment.click.client import ClickUPClient
            payment_link = ClickUPClient.create_payment_link(self)
        self.payment_url = payment_link
        self.save(update_fields=["payment_url"])

        return payment_link

    def apply_transaction(self, provider: ProviderChoices = None, transaction_id: int = None,
                          is_paid_with_card: bool = False, card: object = None):
        if not self.transaction_id and transaction_id:
            self.transaction_id = transaction_id
        self.provider = provider
        self.paid_at = datetime.datetime.now()
        self.status = self.TransactionStatus.SUCCESS
        self.is_paid_with_card = is_paid_with_card
        self.card = card
        self.save(update_fields=["paid_at", "status", "transaction_id", "provider", "is_paid_with_card", "card"])

        self.order.is_paid = True
        self.order.save(update_fields=["is_paid"])

    def cancel_transaction(self, reason):
        self.cancelled_at = datetime.datetime.now()
        self.status = self.TransactionStatus.CANCELLED
        self.extra = {"payme_cancel_reason": reason}
        self.save(update_fields=["cancelled_at", "status", "extra"])

        self.order.is_paid = False
        self.order.save(update_fields=["is_paid"])

        return self


class UserCard(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="cards")
    card_number = models.CharField(max_length=255, )
    expire_date = models.CharField(max_length=255, )
    card_id = models.CharField(max_length=255, )
    token = models.CharField(max_length=255, null=True)
    provider = models.CharField(choices=ProviderChoices.choices, max_length=15, default=ProviderChoices.PAYLOV)
    confirmed = models.BooleanField(default=False, )
    is_deleted = models.BooleanField(default=False, editable=False)

    objects = managers.UserCardManager()

    def soft_delete(self):
        self.card_number = f"{self.card_number}_{self.card_id}_deleted"
        self.is_deleted = True
        self.save(update_fields=["card_number", "is_deleted"])

    @property
    def title(self):
        card_number = self.card_number
        if self.is_deleted:
            card_number = self.card_number.split("_")[0]
        return f'{card_number[:4]} **** **** {card_number[-4:]}'

    @property
    def exp_date(self):
        expire_date = str(self.expire_date)
        return f"{expire_date[2:]}/{expire_date[:2]}"

    class Meta:
        unique_together = ("user", "card_number")


class PaymentProvider(models.Model):
    provider = models.CharField(max_length=32, verbose_name="Provider", choices=ProviderChoices.choices)
    icon = models.FileField(upload_to="providers/", null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Title", null=True, blank=True)

    def __str__(self):
        return self.title
