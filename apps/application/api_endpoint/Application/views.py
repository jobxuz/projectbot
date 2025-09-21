from drf_spectacular.utils import extend_schema

from apps.application.models import Application
from apps.application.utils import send_telegram_message
from .serializers import ApplicationListSerializer, ApplicationCreateSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema(tags=["Application"])
class ApplicationCreateAPIView(CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer

    def perform_create(self, serializer):
        application = serializer.save()

        fields = {
            "👤 Пользователь": application.user.telegram_id,
            "🏭 Производитель": application.manufacturer,
            "👥 Заказчик": application.customer,
            "🛎 Услуга": application.service,
            "📦 Пакет": application.package,
            "📊 Сегмент": application.segment,
            "🎯 Цель труда": application.work_purpose,
            "🏭 Интересующие фабрики": application.interested_factories,
            "🔢 Количество к просмотру": application.quantity_to_see,
            "📅 Планируемые дни пребывания": application.planned_stay_days,
            "📆 Планируемые даты приезда": application.planned_arrival_dates,
            "🗺 Нужна туристическая программа": application.needs_tourist_program,
            "📦 Описание продукта": application.product_description,
            "📐 Объем заказа": application.order_volume,
            "⏳ Срок производства и доставки": application.production_delivery_time,
            "⚙️ Специальные требования": application.special_requirements,
            "💰 Бюджет / примерная цена": application.budget_estimated_price,
            "📂 Сегмент / категория": application.segment_category,
            "📝 Дополнительная информация": application.additional_notes,
            "📞 Контактный телефон": application.contact_phone,
            "📧 Email адрес": application.contact_email,
            "⚡️ Статус": application.get_status_display(),
        }

        text_lines = ["📌 <b>Новая заявка</b>\n"]
        for label, value in fields.items():
            if value not in [None, "", []]:
                text_lines.append(f"{label}: {value}")

        message = "\n".join(text_lines)

        send_telegram_message(message)

    
    
@extend_schema(tags=["Application"])
class ApplicationListAPIView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'created_at']
