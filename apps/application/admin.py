from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from apps.application.utils import send_telegram_message
from .models import (
    Manufacturer, Customer, AdditionalService, Application, Offer, Segment, 
    TemporaryContact, BotUser, Slider, Package, PackageItem, UserApply
)

admin.site.unregister(Group)

admin.site.site_header = _("Администрация")
admin.site.index_title = _("Панель управления")



@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "company_name", "status", "created_at") 
    search_fields = ("full_name", "company_name", "phone")
    list_filter = ("status", "created_at")
    list_display_links = ("id", "full_name")
    readonly_fields = ("created_at", "updated_at")
    
    class Meta:
        verbose_name = _("Производитель")
        verbose_name_plural = _("Производители")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "company_name", "position", "created_at") 
    search_fields = ("full_name", "company_name", "phone") 
    list_display_links = ("id", "full_name")
    readonly_fields = ("created_at", "updated_at")
    
    class Meta:
        verbose_name = _("Заказчик")
        verbose_name_plural = _("Заказчики")


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "first_name", "last_name", "phone_number", "type", "is_active", "created_at") 
    search_fields = ("telegram_id", "first_name", "last_name", "phone_number", "username") 
    list_filter = ("type", "is_active", "is_bot", "created_at")
    list_display_links = ("id", "telegram_id")
    readonly_fields = ("created_at",)
    
    class Meta:
        verbose_name = _("Пользователь бота")
        verbose_name_plural = _("Пользователи бота")


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "payment_type", "type", "is_active", "order", "created_at") 
    search_fields = ("name", "description")
    list_filter = ("payment_type", "type", "is_active", "created_at")
    list_display_links = ("id", "name")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("order", "is_active")
    
    class Meta:
        verbose_name = _("Дополнительная услуга")
        verbose_name_plural = _("Дополнительные услуги")



class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1    
    fields = ("user", "manufacturer", "customer", "service", "status")
    

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "manufacturer", "customer", "package", "status", "created_at") 
    search_fields = (
        "user__first_name", "user__last_name", "user__phone_number",
        "manufacturer__company_name", "manufacturer__full_name",     
        "customer__company_name", "customer__full_name",
        "package__name", "service__name",             
    )
    list_filter = ("status", "created_at")
    list_display_links = ("id", "user")
    autocomplete_fields = ("user", "manufacturer", "customer", "service", "package")
    readonly_fields = ("created_at", "updated_at")
    inlines = [OfferInline]
    
    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")

    def save_model(self, request, obj, form, change):
        if change:  
            old_obj = Application.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                chat_id = getattr(obj.user, "telegram_id", None)
                if chat_id:
                    message = (
                        f"📌 Ваша заявка №{obj.id} обновлена!\n\n"
                        f"⚡️ Новый статус: <b>{obj.get_status_display()}</b>"
                    )
                    send_telegram_message(message, chat_id=chat_id)

        super().save_model(request, obj, form, change)
    


    

class PackageItemInline(admin.TabularInline):
    model = PackageItem
    extra = 1
    fields = ("name", "order")
    ordering = ("order",)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "order", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at", )
    list_display_links = ("id", "name")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("order",)
    inlines = [PackageItemInline]
    
    class Meta:
        verbose_name = _("Пакет")
        verbose_name_plural = _("Пакеты")


@admin.register(TemporaryContact)
class TemporaryContactAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "contact_id", "deal_id", "created_at") 
    search_fields = ("phone_number", "contact_id", "deal_id")
    list_display_links = ("id", "phone_number")
    readonly_fields = ("created_at", "updated_at")
    
    class Meta:
        verbose_name = _("Временный контакт")
        verbose_name_plural = _("Временные контакты")


@admin.register(Segment)
class SegmanrAdmin(admin.ModelAdmin):
    list_display = ("id", "title") 
    search_fields = ("title", )
    list_display_links = ("id", "title")
    readonly_fields = ("created_at", "updated_at")
    
    class Meta:
        verbose_name = _("Сегмент")
        verbose_name_plural = _("Сегмент")


@admin.register(UserApply)
class UserApplyAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "service", "created_at")
    search_fields = ("user__first_name", "user__last_name", "service__name")
    list_filter = ("created_at", "service__type")
    list_display_links = ("id", "user")
    readonly_fields = ("created_at", "updated_at")
    
    class Meta:
        verbose_name = _("Заявка пользователя")
        verbose_name_plural = _("Заявки пользователей")



@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "created_at", "updated_at") 
    search_fields = ("title", "description")
    list_filter = ("is_active", "created_at")
    list_display_links = ("id", "title")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("is_active",)
    
    class Meta:
        verbose_name = _("Слайдер")
        verbose_name_plural = _("Слайдеры")


# Organize admin apps
from django.apps import AppConfig

class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.application'
    verbose_name = _('UzTextile Application')