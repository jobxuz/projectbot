from django.contrib import admin
from .models import Manufacturer, Customer



@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "company_name", "position") 
    search_fields = ("full_name", "company_name")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "company_name", "position") 
    search_fields = ("full_name", "company_name") 
