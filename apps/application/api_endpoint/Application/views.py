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
            "👤 User": application.user,
            "🏭 Manufacturer": application.manufacturer,
            "👥 Customer": application.customer,
            "🛎 Service": application.service,
            "📦 Package": application.package,
            "📊 Segment": application.segment,
            "🎯 Work purpose": application.work_purpose,
            "🏭 Interested factories": application.interested_factories,
            "🔢 Quantity to see": application.quantity_to_see,
            "📅 Planned stay days": application.planned_stay_days,
            "📆 Planned arrival dates": application.planned_arrival_dates,
            "🗺 Needs tourist program": application.needs_tourist_program,
            "📦 Product description": application.product_description,
            "📐 Order volume": application.order_volume,
            "⏳ Delivery time": application.production_delivery_time,
            "⚙️ Special requirements": application.special_requirements,
            "💰 Budget": application.budget_estimated_price,
            "📂 Segment category": application.segment_category,
            "📝 Notes": application.additional_notes,
            "📞 Phone": application.contact_phone,
            "📧 Email": application.contact_email,
            "⚡️ Status": application.get_status_display(),
        }

        text_lines = ["📌 <b>Yangi Application</b>\n"]
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
