from django.contrib import admin
from .models import Manufacturer, Customer, AdditionalService, ApplicationAdditionalService, TemporaryContact, BotUser



@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "company_name", "status") 
    search_fields = ("full_name", "company_name")
    list_filter = ("status",)
    list_display_links = ("id", "full_name")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "company_name", "position") 
    search_fields = ("full_name", "company_name") 
    list_display_links = ("id", "full_name")


@admin.register(BotUser)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "phone_number", "language_code") 
    search_fields = ("telegram_id", "phone_number") 
    list_display_links = ("id", "telegram_id")


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "payment_type", "type", "is_active", "created_at") 
    search_fields = ("name",)
    list_filter = ("payment_type", "type", "is_active")
    list_display_links = ("id", "name")




@admin.register(ApplicationAdditionalService)
class ApplicationAdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "manufacturer", "service", "status", "created_at") 
    search_fields = (
        "manufacturer__company_name",  
        "manufacturer__full_name",     
        "service__name",             
    )
    list_filter = ("status",)
    list_display_links = ("id", "manufacturer")



@admin.register(TemporaryContact)
class TemporaryContactAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "contact_id", "deal_id", "created_at") 
    search_fields = ("phone_number",)
    list_display_links = ("id", "phone_number")