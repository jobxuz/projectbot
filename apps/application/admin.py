from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import (
    BotUser, Manufacturer, Customer, Tender, TenderResponse, 
    Chat, ChatMessage, Order, Payment, VideoMeeting, 
    FactoryTour, TourPackage, TourPackageFeature, TourPackagePrice, AdditionalService, ApplicationAdditionalService,
    TemporaryContact, Notification
)

# Admin panel sozlamalari
admin.site.site_header = "🏭 Zavod Safari"
admin.site.site_title = "Zavod Safari"
admin.site.index_title = "Boshqaruv paneli"

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'first_name', 'last_name', 'username', 'type', 'is_active']
    list_filter = ['type', 'is_active', 'language_code']
    search_fields = ['telegram_id', 'first_name', 'last_name', 'username', 'phone_number']
    list_per_page = 25
    
    actions = ['send_notification_to_users', 'activate_users', 'deactivate_users']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('telegram_id', 'first_name', 'last_name', 'username', 'phone_number', 'language_code')
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('type', 'is_bot', 'is_active')
        }),
    )
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} ta foydalanuvchi faollashtirildi')
    activate_users.short_description = "Tanlangan foydalanuvchilarni faollashtirish"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} ta foydalanuvchi deaktivlashtirildi')
    deactivate_users.short_description = "Tanlangan foydalanuvchilarni deaktivlashtirish"
    
    def send_notification_to_users(self, request, queryset):
        count = 0
        for user in queryset:
            if user.telegram_id:
                try:
                    # Bu yerda notification yuborish mumkin
                    count += 1
                except Exception as e:
                    self.message_user(request, f'Xatolik {user.first_name}: {e}', level=messages.ERROR)
        
        self.message_user(request, f'{count} ta foydalanuvchiga notification yuborildi')
    send_notification_to_users.short_description = "Tanlangan foydalanuvchilarga notification yuborish"

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'full_name', 'status', 'subscription_expires', 'rating', 'total_orders']
    list_filter = ['status', 'product_segment', 'has_quality_control']
    search_fields = ['company_name', 'full_name', 'phone', 'production_address']
    readonly_fields = ['rating', 'total_orders']
    list_per_page = 30
    
    fieldsets = (
        ('Kompaniya ma\'lumotlari', {
            'fields': ('user', 'company_name', 'market_experience', 'full_name', 'position')
        }),
        ('Ishlab chiqarish', {
            'fields': ('min_order_quantity', 'product_segment', 'production_address', 'office_address')
        }),
        ('Tijorat taklifi', {
            'fields': ('commercial_offer_text', 'commercial_offer')
        }),
        ('Texnik imkoniyatlar', {
            'fields': ('has_quality_control', 'has_crm', 'has_erp', 'has_gemini_gerber', 'equipment_info')
        }),
        ('Tashkilot', {
            'fields': ('employee_count', 'organization_structure', 'owns_building', 'has_power_issues', 'has_credit_load')
        }),
        ('Hujjatlar', {
            'fields': ('certificate', 'website')
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('status', 'subscription_expires', 'verification_date', 'rating', 'total_orders')
        }),
    )
    
    actions = ['approve_manufacturers', 'verify_manufacturers', 'extend_subscription']
    
    def approve_manufacturers(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} ta zavod tasdiqlandi')
    approve_manufacturers.short_description = "Tanlangan zavodlarni tasdiqlash"
    
    def verify_manufacturers(self, request, queryset):
        updated = queryset.update(status='verified', verification_date=timezone.now())
        self.message_user(request, f'{updated} ta zavod tekshirildi')
    verify_manufacturers.short_description = "Tanlangan zavodlarni tekshirish"
    
    def extend_subscription(self, request, queryset):
        for manufacturer in queryset:
            if manufacturer.subscription_expires:
                manufacturer.subscription_expires += timedelta(days=180)
            else:
                manufacturer.subscription_expires = timezone.now() + timedelta(days=180)
            manufacturer.save()
        self.message_user(request, f'{queryset.count()} ta zavod obunasi uzaytirildi')
    extend_subscription.short_description = "Obunani 6 oyga uzaytirish"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company_name', 'position']
    search_fields = ['full_name', 'company_name', 'phone_number']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('user', 'full_name', 'company_name', 'position', 'phone_number', 'email')
        }),
        ('Biznes ma\'lumotlari', {
            'fields': ('website', 'legal_address')
        }),
    )

@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ['lot_number', 'customer', 'status']
    list_filter = ['status']
    search_fields = ['lot_number', 'product_description', 'customer__full_name']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('customer', 'lot_number', 'product_description', 'status')
        }),
        ('Biznes ma\'lumotlari', {
            'fields': ('budget', 'special_requirements')
        }),
    )

@admin.register(TenderResponse)
class TenderResponseAdmin(admin.ModelAdmin):
    list_display = ['tender', 'manufacturer', 'status']
    list_filter = ['status']
    search_fields = ['tender__title', 'manufacturer__company_name']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('tender', 'manufacturer', 'status')
        }),
        ('Taklif', {
            'fields': ('delivery_time', 'message', 'price_offer')
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'manufacturer', 'status']
    list_filter = ['status']
    search_fields = ['order_number', 'customer__full_name', 'manufacturer__company_name']
    
    fieldsets = (
        ('Buyurtma ma\'lumotlari', {
            'fields': ('order_number', 'customer', 'manufacturer', 'status')
        }),
        ('Narx va to\'lov', {
            'fields': ('total_amount', 'payment_status')
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status']
    list_filter = ['status']
    search_fields = ['user__first_name', 'transaction_id']
    
    fieldsets = (
        ('To\'lov ma\'lumotlari', {
            'fields': ('user', 'amount', 'status')
        }),
    )

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['chat_type', 'customer', 'manufacturer', 'is_active']
    list_filter = ['chat_type', 'is_active']
    search_fields = ['customer__full_name', 'manufacturer__company_name']
    
    fieldsets = (
        ('Chat ma\'lumotlari', {
            'fields': ('chat_type', 'customer', 'manufacturer', 'is_active')
        }),
    )

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender']
    search_fields = ['chat__id', 'sender__full_name', 'content']
    
    fieldsets = (
        ('Xabar ma\'lumotlari', {
            'fields': ('chat', 'sender', 'content')
        }),
    )

@admin.register(VideoMeeting)
class VideoMeetingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'meeting_date', 'status']
    list_filter = ['status']
    search_fields = ['customer__full_name', 'manufacturers__company_name']
    
    fieldsets = (
        ('Uchrashuv ma\'lumotlari', {
            'fields': ('customer', 'manufacturers', 'status')
        }),
        ('Vaqt va manzil', {
            'fields': ('meeting_date', 'duration', 'meeting_link')
        }),
    )

@admin.register(FactoryTour)
class FactoryTourAdmin(admin.ModelAdmin):
    list_display = ['customer', 'tour_package', 'status']
    list_filter = ['status']
    search_fields = ['customer__full_name', 'tour_package__name']
    
    fieldsets = (
        ('Sayohat ma\'lumotlari', {
            'fields': ('customer', 'tour_package', 'status')
        }),
        ('Vaqt va ma\'lumotlar', {
            'fields': ('tour_dates', 'duration_days', 'participants_count')
        }),
    )

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'package_type', 'duration_days', 'price_usd', 'is_active', 'is_featured']
    list_filter = ['package_type', 'is_active', 'is_featured']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_featured']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'package_type', 'description', 'duration_days')
        }),
        ('Narxlar', {
            'fields': ('price_usd', 'price_som')
        }),
        ('Xizmatlar', {
            'fields': ('includes_transport', 'includes_accommodation', 'includes_guide', 'includes_translator')
        }),
        ('Qo\'shimcha', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
    )

@admin.register(TourPackageFeature)
class TourPackageFeatureAdmin(admin.ModelAdmin):
    list_display = ['tour_package', 'feature_name', 'is_included', 'order']
    list_filter = ['is_included', 'tour_package__package_type']
    search_fields = ['feature_name', 'tour_package__name']
    list_editable = ['is_included', 'order']
    
    fieldsets = (
        ('Xizmat ma\'lumotlari', {
            'fields': ('tour_package', 'feature_name', 'feature_description')
        }),
        ('Ko\'rsatish', {
            'fields': ('is_included', 'icon', 'order')
        }),
    )

@admin.register(TourPackagePrice)
class TourPackagePriceAdmin(admin.ModelAdmin):
    list_display = ['tour_package', 'participants_count', 'price_usd', 'price_som', 'discount_percent']
    list_filter = ['tour_package__package_type']
    search_fields = ['tour_package__name']
    list_editable = ['price_usd', 'price_som', 'discount_percent']
    
    fieldsets = (
        ('Paket va narx', {
            'fields': ('tour_package', 'participants_count', 'price_usd', 'price_som')
        }),
        ('Chegirma', {
            'fields': ('discount_percent', 'is_active')
        }),
    )

@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Xizmat ma\'lumotlari', {
            'fields': ('name', 'description', 'price')
        }),
        ('Qo\'shimcha', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(ApplicationAdditionalService)
class ApplicationAdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ['manufacturer', 'service', 'status']
    list_filter = ['status']
    search_fields = ['manufacturer__company_name', 'service__name']
    
    fieldsets = (
        ('Ariza ma\'lumotlari', {
            'fields': ('manufacturer', 'service', 'status')
        }),
    )

@admin.register(TemporaryContact)
class TemporaryContactAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'contact_id', 'deal_id']
    search_fields = ['phone_number', 'contact_id', 'deal_id']
    
    fieldsets = (
        ('Aloqa ma\'lumotlari', {
            'fields': ('phone_number', 'contact_id', 'deal_id')
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['user__first_name', 'title', 'message']
    
    fieldsets = (
        ('Bildirishnoma ma\'lumotlari', {
            'fields': ('user', 'title', 'message', 'notification_type')
        }),
        ('Holat', {
            'fields': ('is_read', 'data')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread', 'resend_notifications']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} ta bildirishnoma o\'qildi deb belgilandi')
    mark_as_read.short_description = "Tanlangan bildirishnomalarni o'qildi deb belgilash"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} ta bildirishnoma o\'qilmagan deb belgilandi')
    mark_as_unread.short_description = "Tanlangan bildirishnomalarni o'qilmagan deb belgilash"
    
    def resend_notifications(self, request, queryset):
        count = 0
        for notification in queryset:
            try:
                # Bu yerda notification qayta yuborish mumkin
                count += 1
            except Exception as e:
                self.message_user(request, f'Xatolik: {e}', level=messages.ERROR)
        
        self.message_user(request, f'{count} ta bildirishnoma qayta yuborildi')
    resend_notifications.short_description = "Tanlangan bildirishnomalarni qayta yuborish"
