from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
    is_bot = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.CUSTOMER)
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.telegram_id})"

    class Meta:
        verbose_name = _("Bot foydalanuvchisi")
        verbose_name_plural = _("Bot foydalanuvchilari")

class Manufacturer(models.Model): 
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = "in_progress", _("Jarayonda")
        APPROVED = "approved", _("Tasdiqlandi")
        PAID = "paid", _("To'lov qilindi")
        VERIFIED = "verified", _("Tekshirildi")
    
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
    owns_building = models.BooleanField(default=False, verbose_name=_("Bino o'zlariniki yoki ijaradami"))
    has_power_issues = models.BooleanField(default=False, verbose_name=_("Elektr/gaz uzilishlari bormi"))
    has_credit_load = models.BooleanField(default=False, verbose_name=_("Kredit yuki mavjudmi"))
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
    subscription_expires = models.DateTimeField(null=True, blank=True, verbose_name=_("Obuna muddati"))
    verification_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Tekshirish sanasi"))
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name=_("Reyting"))
    total_orders = models.IntegerField(default=0, verbose_name=_("Jami buyurtmalar"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.telegram_id}"
    
    class Meta:
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
        verbose_name = _("Buyurtmachi")
        verbose_name_plural = _("Buyurtmachilar")

class Tender(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "active", _("Faol")
        CLOSED = "closed", _("Yopilgan")
        COMPLETED = "completed", _("Bajarilgan")
        CANCELLED = "cancelled", _("Bekor qilingan")
    
    class ProductSegmentChoices(models.TextChoices):
        KNITWEAR = "knitwear", _("Trikotaj")
        DENIM = "denim", _("Jinsi")
        HOME_TEXTILES = "home_textiles", _("Uy to'qimachilik")
        WORKWEAR = "workwear", _("Ish kiyimlari")
        FABRICS = "fabrics", _("Matolar")
        OTHER = "other", _("Boshqa")
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Mijoz"))
    lot_number = models.CharField(max_length=50, unique=True, verbose_name=_("Lot raqami"))
    product_description = models.TextField(verbose_name=_("Mahsulot tavsifi"))
    order_quantity = models.CharField(max_length=100, verbose_name=_("Buyurtma hajmi"))
    delivery_date = models.DateField(verbose_name=_("Yetkazib berish sanasi"))
    special_requirements = models.TextField(blank=True, null=True, verbose_name=_("Maxsus talablar"))
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name=_("Byudjet"))
    product_segment = models.CharField(max_length=20, choices=ProductSegmentChoices.choices, verbose_name=_("Mahsulot segmenti"))
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    responses_count = models.IntegerField(default=0, verbose_name=_("Javoblar soni"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bitrix_deal_id = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Bitrix24 bitim ID"))

    def __str__(self):
        return f"Lot #{self.lot_number} - {self.customer.company_name}"

    class Meta:
        verbose_name = _("Tender")
        verbose_name_plural = _("Tenderlar")

class TenderResponse(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        APPROVED = "approved", _("Tasdiqlandi")
        REJECTED = "rejected", _("Rad etildi")
        SELECTED = "selected", _("Tanlandi")
    
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, verbose_name=_("Tender"))
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name=_("Ishlab chiqaruvchi"))
    message = models.TextField(verbose_name=_("Xabar"))
    price_offer = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name=_("Narx taklifi"))
    delivery_time = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Yetkazib berish vaqti"))
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    bitrix_comment_id = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Bitrix24 izoh ID"))

    def __str__(self):
        return f"{self.manufacturer.company_name} - Lot #{self.tender.lot_number}"

    class Meta:
        verbose_name = _("Tender javobi")
        verbose_name_plural = _("Tender javoblari")
        unique_together = ("tender", "manufacturer")

class Chat(models.Model):
    class ChatTypeChoices(models.TextChoices):
        TENDER = "tender", _("Tender")
        DIRECT = "direct", _("To'g'ridan-to'g'ri")
        SUPPORT = "support", _("Qo'llab-quvvatlash")
    
    chat_type = models.CharField(max_length=20, choices=ChatTypeChoices.choices, verbose_name=_("Chat turi"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Mijoz"))
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Ishlab chiqaruvchi"))
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Tender"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat {self.id} - {self.customer.company_name}"

    class Meta:
        verbose_name = _("Chat")
        verbose_name_plural = _("Chatlar")

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name=_("Chat"))
    sender = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name=_("Yuboruvchi"))
    message = models.TextField(verbose_name=_("Xabar"))
    file = models.FileField(upload_to="chat_files/", null=True, blank=True, verbose_name=_("Fayl"))
    is_read = models.BooleanField(default=False, verbose_name=_("O'qilganmi"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.first_name} - {self.message[:50]}"

    class Meta:
        verbose_name = _("Chat xabari")
        verbose_name_plural = _("Chat xabarlari")
        ordering = ["created_at"]

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        CONFIRMED = "confirmed", _("Tasdiqlandi")
        IN_PRODUCTION = "in_production", _("Ishlab chiqarishda")
        READY = "ready", _("Tayyor")
        SHIPPED = "shipped", _("Yuborildi")
        DELIVERED = "delivered", _("Yetkazildi")
        CANCELLED = "cancelled", _("Bekor qilindi")
    
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, verbose_name=_("Tender"))
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name=_("Ishlab chiqaruvchi"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Mijoz"))
    order_number = models.CharField(max_length=50, unique=True, verbose_name=_("Buyurtma raqami"))
    quantity = models.IntegerField(verbose_name=_("Miqdori"))
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Birlik narxi"))
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Jami summa"))
    delivery_date = models.DateField(verbose_name=_("Yetkazib berish sanasi"))
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    contract_file = models.FileField(upload_to="contracts/", null=True, blank=True, verbose_name=_("Shartnoma fayli"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bitrix_deal_id = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Bitrix24 bitim ID"))

    def __str__(self):
        return f"Buyurtma #{self.order_number} - {self.customer.company_name}"

    class Meta:
        verbose_name = _("Buyurtma")
        verbose_name_plural = _("Buyurtmalar")

class Payment(models.Model):
    class PaymentTypeChoices(models.TextChoices):
        SUBSCRIPTION = "subscription", _("Obuna")
        CATALOG_ACCESS = "catalog_access", _("Katalog kirish")
        VIDEO_MEETING = "video_meeting", _("Video uchrashuv")
        FACTORY_TOUR = "factory_tour", _("Zavod sayohati")
        VERIFICATION = "verification", _("Tekshirish")
        PERSONAL_MANAGER = "personal_manager", _("Shaxsiy menejer")
        TRAINING = "training", _("O'qitish")
    
    class PaymentStatusChoices(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        COMPLETED = "completed", _("Bajarildi")
        FAILED = "failed", _("Xatolik")
        REFUNDED = "refunded", _("Qaytarildi")
    
    class PaymentMethodChoices(models.TextChoices):
        CLICK = "click", _("Click")
        PAYME = "payme", _("Payme")
        VISA = "visa", _("Visa")
        MASTERCARD = "mastercard", _("Mastercard")
        UZCARD = "uzcard", _("Uzcard")
        HUMO = "humo", _("Humo")
    
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi"))
    payment_type = models.CharField(max_length=20, choices=PaymentTypeChoices.choices, verbose_name=_("To'lov turi"))
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Summa"))
    currency = models.CharField(max_length=3, default="USD", verbose_name=_("Valyuta"))
    payment_method = models.CharField(max_length=20, choices=PaymentMethodChoices.choices, verbose_name=_("To'lov usuli"))
    status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    transaction_id = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Tranzaksiya ID"))
    payment_data = models.JSONField(null=True, blank=True, verbose_name=_("To'lov ma'lumotlari"))
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Bajarilgan vaqti"))

    def __str__(self):
        return f"{self.user.first_name} - {self.get_payment_type_display()} - {self.amount}"

    class Meta:
        verbose_name = _("To'lov")
        verbose_name_plural = _("To'lovlar")

class VideoMeeting(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        SCHEDULED = "scheduled", _("Rejalashtirilgan")
        COMPLETED = "completed", _("Bajarildi")
        CANCELLED = "cancelled", _("Bekor qilindi")
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Mijoz"))
    manufacturers = models.ManyToManyField(Manufacturer, verbose_name=_("Ishlab chiqaruvchilar"))
    meeting_date = models.DateTimeField(verbose_name=_("Uchrashuv vaqti"))
    duration = models.IntegerField(default=60, verbose_name=_("Davomiyligi (minut)"))
    meeting_link = models.URLField(null=True, blank=True, verbose_name=_("Uchrashuv havolasi"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("Izohlar"))
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name=_("To'lov"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video uchrashuv - {self.customer.company_name} - {self.meeting_date}"

    class Meta:
        verbose_name = _("Video uchrashuv")
        verbose_name_plural = _("Video uchrashuvlar")

class TourPackage(models.Model):
    class PackageTypeChoices(models.TextChoices):
        STANDARD = "standard", _("Standart")
        BUSINESS = "business", _("Biznes")
        PREMIUM = "premium", _("Premium")
        CUSTOM = "custom", _("Maxsus")
    
    name = models.CharField(max_length=255, verbose_name=_("Paket nomi"))
    package_type = models.CharField(max_length=20, choices=PackageTypeChoices.choices, verbose_name=_("Paket turi"))
    description = models.TextField(verbose_name=_("Tavsif"))
    duration_days = models.IntegerField(default=1, verbose_name=_("Davomiyligi (kun)"))
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Narxi (USD)"))
    price_som = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Narxi (So'm)"))
    
    # Paketga kiritilgan xizmatlar
    includes_transport = models.BooleanField(default=True, verbose_name=_("Tashish kiritilgan"))
    includes_accommodation = models.BooleanField(default=False, verbose_name=_("Turar joy kiritilgan"))
    includes_guide = models.BooleanField(default=True, verbose_name=_("Gid kiritilgan"))
    includes_translator = models.BooleanField(default=False, verbose_name=_("Tarjimon kiritilgan"))
    includes_cultural_program = models.BooleanField(default=False, verbose_name=_("Madaniy dastur"))
    
    # Maxsus xizmatlar
    max_manufacturers = models.IntegerField(default=3, verbose_name=_("Maksimal zavodlar soni"))
    max_participants = models.IntegerField(default=5, verbose_name=_("Maksimal ishtirokchilar"))
    
    # Paket rasmlari
    package_image = models.ImageField(upload_to="tour_packages/", null=True, blank=True, verbose_name=_("Paket rasmi"))
    gallery_images = models.JSONField(default=list, blank=True, verbose_name=_("Galereya rasmlari"))
    
    # Qo'shimcha ma'lumotlar
    highlights = models.JSONField(default=list, blank=True, verbose_name=_("Asosiy afzalliklar"))
    itinerary = models.JSONField(default=list, blank=True, verbose_name=_("Kunlik dastur"))
    
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Tavsiya etiladi"))
    order = models.IntegerField(default=0, verbose_name=_("Tartib raqami"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_package_type_display()}"

    class Meta:
        verbose_name = _("Sayohat paketi")
        verbose_name_plural = _("Sayohat paketlari")
        ordering = ["order", "price_usd"]

class TourPackageFeature(models.Model):
    """Sayohat paketiga kiritilgan xizmatlar"""
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name="features")
    feature_name = models.CharField(max_length=255, verbose_name=_("Xizmat nomi"))
    feature_description = models.TextField(blank=True, verbose_name=_("Xizmat tavsifi"))
    is_included = models.BooleanField(default=True, verbose_name=_("Kiritilganmi"))
    icon = models.CharField(max_length=50, blank=True, verbose_name=_("Ikonka"))
    order = models.IntegerField(default=0, verbose_name=_("Tartib raqami"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))

    def __str__(self):
        return f"{self.tour_package.name} - {self.feature_name}"

    class Meta:
        verbose_name = _("Paket xizmati")
        verbose_name_plural = _("Paket xizmatlari")
        ordering = ["order"]

class TourPackagePrice(models.Model):
    """Sayohat paketi narxlari (valyuta va ishtirokchilar soniga qarab)"""
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name="prices")
    participants_count = models.IntegerField(verbose_name=_("Ishtirokchilar soni"))
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Narxi (USD)"))
    price_som = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Narxi (So'm)"))
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_("Chegirma (%)"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))

    def __str__(self):
        return f"{self.tour_package.name} - {self.participants_count} kishi"

    class Meta:
        verbose_name = _("Paket narxi")
        verbose_name_plural = _("Paket narxlari")
        unique_together = ("tour_package", "participants_count")

class FactoryTour(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        CONFIRMED = "confirmed", _("Tasdiqlandi")
        IN_PROGRESS = "in_progress", _("Jarayonda")
        COMPLETED = "completed", _("Bajarildi")
        CANCELLED = "cancelled", _("Bekor qilindi")
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Mijoz"))
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, verbose_name=_("Sayohat paketi"))
    tour_dates = models.DateField(verbose_name=_("Sayohat sanasi"))
    duration_days = models.IntegerField(default=1, verbose_name=_("Davomiyligi (kun)"))
    participants_count = models.IntegerField(default=1, verbose_name=_("Ishtirokchilar soni"))
    preferred_segments = models.CharField(max_length=255, verbose_name=_("Afzal ko'rilgan segmentlar"))
    accommodation_needed = models.BooleanField(default=False, verbose_name=_("Turar joy kerakmi"))
    special_requests = models.TextField(blank=True, null=True, verbose_name=_("Maxsus so'rovlar"))
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name=_("Jami narx"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Zavod sayohati - {self.customer.company_name} - {self.tour_dates}"

    class Meta:
        verbose_name = _("Zavod sayohati")
        verbose_name_plural = _("Zavod sayohatlari")

class AdditionalService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqti"))
    order = models.IntegerField(default=0, verbose_name=_("Tartib raqami"))
    is_apply = models.BooleanField(default=False, verbose_name=_("Qo'llab-quvvatlanadi"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Qo'shimcha xizmat")
        verbose_name_plural = _("Qo'shimcha xizmatlar")
        ordering = ["order"]

class ApplicationAdditionalService(models.Model):
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = "in_progress", _("Jarayonda")
        APPROVED = "approved", _("Tasdiqlandi")
        PAID = "paid", _("To'lov qilindi")

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
        verbose_name = _("Qo'shimcha xizmat arizasi")
        verbose_name_plural = _("Qo'shimcha xizmat arizalari")

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

class Notification(models.Model):
    class NotificationTypeChoices(models.TextChoices):
        TENDER_RESPONSE = "tender_response", _("Tender javobi")
        ORDER_UPDATE = "order_update", _("Buyurtma yangilanishi")
        PAYMENT_SUCCESS = "payment_success", _("To'lov muvaffaqiyatli")
        SUBSCRIPTION_EXPIRES = "subscription_expires", _("Obuna muddati tugaydi")
        SYSTEM = "system", _("Tizim xabari")
    
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi"))
    notification_type = models.CharField(max_length=20, choices=NotificationTypeChoices.choices, verbose_name=_("Xabar turi"))
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    message = models.TextField(verbose_name=_("Xabar"))
    is_read = models.BooleanField(default=False, verbose_name=_("O'qilganmi"))
    data = models.JSONField(null=True, blank=True, verbose_name=_("Qo'shimcha ma'lumotlar"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.title}"

    class Meta:
        verbose_name = _("Bildirishnoma")
        verbose_name_plural = _("Bildirishnomalar")
        ordering = ["-created_at"]