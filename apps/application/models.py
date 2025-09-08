from ast import mod
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.user.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    
    class Meta:
        abstract = True

class UserType(models.TextChoices):
    MANUFACTURER = "manufacturer", _("Производитель")
    CUSTOMER = "customer", _("Заказчик")


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True, verbose_name=_("Telegram ID"))
    first_name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Фамилия"))
    username = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Имя пользователя"))
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Номер телефона"))
    language_code = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Код языка"))
    is_bot = models.BooleanField(default=False, verbose_name=_("Бот"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активен"))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Дата создания"))
    type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.CUSTOMER, verbose_name=_("Тип пользователя"))
    
    class Meta:
        verbose_name = _("Пользователь бота")
        verbose_name_plural = _("Пользователи бота")


class Manufacturer(BaseModel):
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = "in_progress", _("В процессе")
        APPROVED = "approved", _("Одобрено")
        PAID = "paid", _("Оплачено")

    user = models.OneToOneField(BotUser, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    company_name = models.CharField(max_length=255, verbose_name=_("Название компании"))
    market_experience = models.CharField(max_length=100, verbose_name=_("Опыт на рынке"))
    full_name = models.CharField(max_length=255, verbose_name=_("Ф.И.О"))
    position = models.CharField(max_length=100, verbose_name=_("Должность"))
    min_order_quantity = models.CharField(max_length=100, verbose_name=_("Минимальный объем заказа"))
    product_segment = models.CharField(max_length=100, verbose_name=_("Сегмент продукции"))
    commercial_offer_text = models.TextField(verbose_name=_("Коммерческое предложение"))
    commercial_offer = models.FileField(
        upload_to="offers/",
        verbose_name=_("Файл коммерческого предложения"),
        null=True, blank=True
    )
    production_address = models.TextField(verbose_name=_("Адрес производства"))
    office_address = models.TextField(verbose_name=_("Офисный адрес"))
    website = models.CharField(
        max_length=100,
        verbose_name=_("Адрес сайта"),
        blank=True, null=True
    )
    has_quality_control = models.BooleanField(
        default=False,
        verbose_name=_("Есть ли контроль качества")
    )
    has_crm = models.BooleanField(default=False, verbose_name=_("Есть ли CRM система"))
    has_erp = models.BooleanField(default=False, verbose_name=_("Есть ли ERP система"))
    has_gemini_gerber = models.BooleanField(default=False, verbose_name=_("Есть ли Gemini/Gerber"))
    employee_count = models.IntegerField(verbose_name=_("Количество сотрудников"))
    owns_building = models.BooleanField(verbose_name=_("Здание собственное или арендованное"))
    has_power_issues = models.BooleanField(verbose_name=_("Есть ли проблемы с электричеством/газом"))
    has_credit_load = models.BooleanField(verbose_name=_("Есть ли кредитная нагрузка"))
    organization_structure = models.TextField(verbose_name=_("Организационная структура"))
    equipment_info = models.TextField(verbose_name=_("Информация об оборудовании"))
    certificate = models.FileField(
        upload_to="offers/",
        verbose_name=_("Сертификат"),
        null=True, blank=True
    )
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("Телефон"))
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.IN_PROGRESS,
        verbose_name=_("Статус")
    )
    order = models.IntegerField(default=0, verbose_name=_("Порядковый номер"))

    def __str__(self):
        return f"{self.user.telegram_id}"

    class Meta:
        default_related_name='manufacturers'
        verbose_name = _("Производитель")
        verbose_name_plural = _("Производители")


class Customer(BaseModel):
    user = models.OneToOneField(BotUser, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    full_name = models.CharField(max_length=255, verbose_name=_("Ф.И.О"))
    position = models.CharField(max_length=100, verbose_name=_("Должность"))
    company_name = models.CharField(max_length=255, verbose_name=_("Название компании"))
    website = models.CharField(blank=True, null=True, verbose_name=_("Адрес сайта"))
    legal_address = models.TextField(verbose_name=_("Юридический адрес"))
    marketplace_brand = models.CharField(
        max_length=255,
        verbose_name=_("Бренд на маркетплейсах")
    )
    annual_order_volume = models.CharField(
        max_length=100,
        verbose_name=_("Годовой объем заказов")
    )
    segment = models.CharField(max_length=100, verbose_name=_("Сегмент"))
    cooperation_terms = models.CharField(
        max_length=250,
        verbose_name=_("Условия сотрудничества (Incoterms)")
    )
    payment_terms = models.CharField(max_length=250, verbose_name=_("Условия оплаты"))
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("Телефон"))
    total_orders = models.IntegerField(default=0, verbose_name=_("Всего заказов"))

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        default_related_name='customers'
        verbose_name = _("Заказчик")
        verbose_name_plural = _("Заказчики")


class ServiceType(models.TextChoices):
    CUSTOMER = "customer"
    MANUFACTURER = 'manufacturer'


class ServiceOption(models.TextChoices):
    VIDEO_REVIEW = "video_review", _("Видео обзор")
    INVITE_MANAGER = "invite_manager", _("Пригласить менеджера по продажам")
    TRAINING_REPS = "training_reps", _("Обучение представителей")
    PLACE_ORDER = "place_order", _("Размещение заказа")
    SELECT_FACTORY = "select_factory", _("Выбор фабрики")
    ONLINE_B2B = "online_b2b", _("Онлайн B2B")
    CUSTOM_ORDER = "custom_order", _("Тур заказ")


class PaymentType(models.TextChoices):
    ONE_TIME = "one_time", _("Одноразовая оплата")
    MONTHLY = "monthly", _("Ежемесячная оплата")


class AdditionalService(BaseModel):
    type = models.CharField(max_length=20, choices=ServiceType.choices, default=ServiceType.CUSTOMER, verbose_name=_("Тип"))
    option = models.CharField(
        max_length=100,
        choices=ServiceOption.choices,
        default=ServiceOption.VIDEO_REVIEW,
        verbose_name=_("Опция")
    )
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.ONE_TIME, verbose_name=_("Тип оплаты"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активен"))
    order = models.IntegerField(default=0, verbose_name=_("Порядковый номер"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Дополнительная услуга")
        verbose_name_plural = _("Дополнительные услуги")
        ordering = ["order"]


class UserApply(BaseModel):
    service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE, verbose_name=_("Услуга"))
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name=_("Пользователь"))

    class Meta:
        default_related_name = "applied_service"
        verbose_name = _("Заявка пользователя")
        verbose_name_plural = _("Заявки пользователей")
        
class Package(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    banner = models.ImageField(upload_to='packages/', verbose_name=_("Баннер"), null=True, blank=True)
    order = models.IntegerField(default=0, verbose_name=_("Порядковый номер"))
    
    class Meta:
        verbose_name = _("Пакет")
        verbose_name_plural = _("Пакеты")
        
    def __str__(self):
        return self.name
    
class PackageItem(BaseModel):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name=_("Пакет"))
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    order = models.IntegerField(default=0, verbose_name=_("Порядковый номер"))
    
    class Meta:
        default_related_name = "package_items"
        verbose_name = _("Услуга пакета")
        verbose_name_plural = _("Услуги пакетов")


class Application(BaseModel):
    class StatusChoices(models.TextChoices):
        IN_PROGRESS = "in_progress", _("В процессе")
        APPROVED = "approved", _("Одобрено")
        PAID = "paid", _("Оплачено")
        REJECTED = "rejected", _("Отклонено")
      
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name=_("Пользователь"), null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Производитель"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Заказчик"))
    service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Услуга"))
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Пакет"))
    
    # Factory visit fields
    segment = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Сегмент"))
    work_purpose = models.TextField(null=True, blank=True, verbose_name=_("Цель труда"))
    interested_factories = models.TextField(null=True, blank=True, verbose_name=_("Какие фабрики интересуют"))
    quantity_to_see = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Какое количество хотелось бы посмотреть"))
    planned_stay_days = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Сколько дней планируется пребывание"))
    planned_arrival_dates = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("В каких датах планируется приезд"))
    needs_tourist_program = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Нужна ли туристическая программа"))
    
    # Product order fields
    product_description = models.TextField(null=True, blank=True, verbose_name=_("Описание продукта"))
    order_volume = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Объем заказа"))
    production_delivery_time = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Срок производства и доставки"))
    special_requirements = models.TextField(null=True, blank=True, verbose_name=_("Специальные требования"))
    budget_estimated_price = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Бюджет или примерная цена"))
    segment_category = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Сегмент/категория"))
    
    # Additional information
    additional_notes = models.TextField(null=True, blank=True, verbose_name=_("Дополнительная информация"))
    contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Контактный телефон"))
    contact_email = models.EmailField(null=True, blank=True, verbose_name=_("Email адрес"))
    
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.IN_PROGRESS, 
        verbose_name=_("Статус")
    )

    class Meta:
        default_related_name = "applications"
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заявка #{self.id}"


class TemporaryContact(BaseModel):
    phone_number = models.CharField(verbose_name=_("Номер телефона"), max_length=128)
    contact_id = models.CharField(verbose_name=_("ID контакта"), max_length=128, null=True, blank=True)
    deal_id = models.CharField(verbose_name=_("ID сделки"), max_length=128, null=True, blank=True)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _("Временный контакт")
        verbose_name_plural = _("Временные контакты")



class Slider(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    description = models.TextField(verbose_name=_("Описание"))
    image = models.ImageField(upload_to='sliders/', verbose_name=_("Изображение"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активен"))
    order = models.IntegerField(default=0, verbose_name=_("Порядковый номер"))

    class Meta:
        verbose_name = _("Слайдер")
        verbose_name_plural = _("Слайдеры")

    def __str__(self):
        return self.title
