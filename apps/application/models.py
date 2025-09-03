from ast import mod
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


class UserType(models.TextChoices):
    MANUFACTURER = "manufacturer", _("Ishlab chiqaruvchi")
    CUSTOMER = "customer", _("Buyurtmachi")


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    language_code = models.CharField(max_length=10, null=True, blank=True)
    is_bot = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.CUSTOMER)


class Manufacturer(models.Model):
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = "in_progress", _("Jarayonda")
        APPROVED = "approved", _("Tasdiqlandi")
        PAID = "paid", _("To‘lov qilindi")

    user = models.OneToOneField(BotUser, on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi"))
    company_name = models.CharField(max_length=255, verbose_name=_("Kompaniya nomi"))
    market_experience = models.CharField(max_length=100, verbose_name=_("Bozor tajribasi"))
    full_name = models.CharField(max_length=255, verbose_name=_("F.I.SH"))
    position = models.CharField(max_length=100, verbose_name=_("Lavozim"))
    min_order_quantity = models.CharField(max_length=100, verbose_name=_("Minimal buyurtma hajmi"))
    product_segment = models.CharField(max_length=100, verbose_name=_("Maxsulot segmenti"))
    commercial_offer_text = models.TextField(verbose_name=_("Tijorat taklifi"))
    commercial_offer = models.FileField(
        upload_to="offers/",
        verbose_name=_("Tijorat taklifi fayl"),
        null=True, blank=True
    )
    production_address = models.TextField(verbose_name=_("Ishlab chiqarish manzili"))
    office_address = models.TextField(verbose_name=_("Ofis manzili"))
    website = models.CharField(
        max_length=100,
        verbose_name=_("Sayt manzili"),
        blank=True, null=True
    )
    has_quality_control = models.BooleanField(
        default=False,
        verbose_name=_("Sifat nazorati mavjudmi")
    )
    has_crm = models.BooleanField(default=False, verbose_name=_("CRM tizimi mavjudmi "))
    has_erp = models.BooleanField(default=False, verbose_name=_("ERP tizimi mavjudmi"))
    has_gemini_gerber = models.BooleanField(default=False, verbose_name=_("Gemini/Gerber mavjudmi"))
    employee_count = models.IntegerField(verbose_name=_("Hodimlar soni"))
    owns_building = models.BooleanField(verbose_name=_("Bino o‘zlariniki yoki ijaradami"))
    has_power_issues = models.BooleanField(verbose_name=_("Elektr/gaz uzilishlari bormi"))
    has_credit_load = models.BooleanField(verbose_name=_("Kredit yuki mavjudmi"))
    organization_structure = models.TextField(verbose_name=_("Tashkilot tuzilmasi"))
    equipment_info = models.TextField(verbose_name=_("Uskunalar haqida ma'lumot"))
    certificate = models.FileField(
        upload_to="offers/",
        verbose_name=_("Sertificat"),
        null=True, blank=True
    )
    phone = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.IN_PROGRESS,
        verbose_name=_("Holat")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.telegram_id}"

    class Meta:
        default_related_name='manufacturers'
        verbose_name = _("Ishlab chiqaruvchi")
        verbose_name_plural = _("Ishlab chiqaruvchilar")


class Customer(models.Model):
    user = models.OneToOneField(BotUser, on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi"))
    full_name = models.CharField(max_length=255, verbose_name=_("F.I.SH"))
    position = models.CharField(max_length=100, verbose_name=_("Lavozim"))
    company_name = models.CharField(max_length=255, verbose_name=_("Kompaniya nomi"))
    website = models.CharField(blank=True, null=True, verbose_name=_("Sayt manzili"))
    legal_address = models.TextField(verbose_name=_("Yuridik manzil"))
    marketplace_brand = models.CharField(
        max_length=255,
        verbose_name=_("Marketplace-lardagi brendi")
    )
    annual_order_volume = models.CharField(
        max_length=100,
        verbose_name=_("Yillik buyurtmalar hajmi")
    )
    segment = models.CharField(max_length=100, verbose_name=_("Segment"))
    cooperation_terms = models.CharField(
        max_length=250,
        verbose_name=_("Hamkorlik shartlari (Incoterms)")
    )
    payment_terms = models.CharField(max_length=250, verbose_name=_("To'lov shartlari"))
    phone = models.CharField(max_length=30, null=True, blank=True)
    total_orders = models.IntegerField(default=0, verbose_name=_("Jami buyurtmalar"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        default_related_name='customers'
        verbose_name = _("Buyurtmachi")
        verbose_name_plural = _("Buyurtmachilar")


class ServiceType(models.TextChoices):
    CUSTOMER = "customer"
    MANUFACTURER = 'manufacturer'


class ServiceOption(models.TextChoices):
    VIDEO_REVIEW = "video_review", "Video sharh"
    INVITE_MANAGER = "invite_manager", "Sotuv menejerini taklif qilish"
    TRAINING_REPS = "training_reps", "ROPlarni o‘qitish"
    PLACE_ORDER = "place_order", "Buyurtma joylashtirish"
    SELECT_FACTORY = "select_factory", "Fabrika tanlash"
    ONLINE_B2B = "online_b2b", "Online B2B"
    CUSTOM_ORDER = "custom_order", "Tur buyurtma"


class PaymentType(models.TextChoices):
    ONE_TIME = "one_time", _("1 martalik to'lov")
    MONTHLY = "monthly", _("Oylik to'lov")


class AdditionalService(models.Model):
    type = models.CharField(max_length=20, choices=ServiceType.choices, default=ServiceType.CUSTOMER)
    option = models.CharField(
        max_length=100,
        choices=ServiceOption.choices,
        default=ServiceOption.VIDEO_REVIEW
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.ONE_TIME)
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqti"))
    order = models.IntegerField(default=0, verbose_name=_("Tartib raqami"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Qo'shimcha xizmat")
        verbose_name_plural = _("Qo'shimcha xizmatlar")
        ordering = ["order"]


class UserApply(models.Model):
    service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE)
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "applied_service"


class ApplicationAdditionalService(models.Model):
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = "in_progress", _("Jarayonda")
        APPROVED = "approved", _("Tasdiqlandi")
        PAID = "paid", _("To‘lov qilindi")

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="service_requests"
    )
    service = models.ForeignKey(
        AdditionalService,
        on_delete=models.CASCADE,
        related_name="service_requests"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.IN_PROGRESS,
        verbose_name=_("Holat")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("manufacturer", "service")
        verbose_name = _("Qo‘shimcha xizmat arizasi")
        verbose_name_plural = _("Qo‘shimcha xizmat arizalari")

    def __str__(self):
        return f"{self.manufacturer.company_name}"


class TemporaryContact(models.Model):
    phone_number = models.CharField(verbose_name=_("Phone number"), max_length=128)
    contact_id = models.CharField(verbose_name=_("Contact ID"), max_length=128, null=True, blank=True)
    deal_id = models.CharField(verbose_name=_("Deal ID"), max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _("Temporary contact")
        verbose_name_plural = _("Temporary contacts")



class Slider(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    description = models.TextField(verbose_name=_("Tavsif"))
    image = models.ImageField(upload_to='sliders/', verbose_name=_("Rasm"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan sana"))

    class Meta:
        verbose_name = _("Slayder")
        verbose_name_plural = _("Slayderlar")

    def __str__(self):
        return self.title
