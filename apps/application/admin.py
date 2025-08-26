from django.contrib import admin
from .models import Manufacturer, Customer, AdditionalService, ApplicationAdditionalService



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



@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "is_active", "created_at") 
    search_fields = ("name",)
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