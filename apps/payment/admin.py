from django.contrib import admin
from payment.models import Providers, Order, Transaction, UserCard, PaymentProvider


@admin.register(Providers)
class ProvidersAdmin(admin.ModelAdmin):
    list_display = ("provider", "key", "get_value", "key_description", "is_active",)
    ordering = ("provider",)
    # readonly_fields = ("provider", "key",)

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def get_value(self, obj):
        if obj.value:
            return str(obj.value)[:3] + "*" * (len(obj.value) - 3)
        return obj.value

    get_value.short_description = "VALUE"


class HasBookFilter(admin.SimpleListFilter):
    title = "Book orders"
    parameter_name = "has_book"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Has book"),
            ("no", "No book"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(book__isnull=False)
        if self.value() == "no":
            return queryset.filter(book__isnull=True)
        return queryset


class HasCourse(admin.SimpleListFilter):
    title = "Has Course"
    parameter_name = "has_course"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Has Course"),
            ("no", "No Course")
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(course__isnull=False)
        if self.value() == "no":
            return queryset.filter(course__isnull=True)
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "is_paid", "course", "book")
    list_filter = ('is_paid', HasBookFilter, HasCourse)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', "order", "provider", "status", "amount", "created_at", "paid_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    

@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "get_card_number", "expire_date", "is_deleted")
    search_fields = ("user__full_name", "card_number",)
    list_filter = ("is_deleted",)
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_or_change_permission(self, request, obj=None):
        if obj:
            return False
        return True

    def get_card_number(self, obj):
        if obj.is_deleted:
            return obj.card_number[:4] + len(obj.card_number[4:]) * "*"
        return None

    get_card_number.short_description = "Card number"


@admin.register(PaymentProvider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("provider", 'icon', 'title',)
    list_display_links = ('provider', 'icon', 'title')
