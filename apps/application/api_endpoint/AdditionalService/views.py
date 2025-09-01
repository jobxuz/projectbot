from django.db.models import Exists, OuterRef
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.application.models import AdditionalService, UserApply
from .serializers import AdditionalServiceSerializer, UserApplySerializer


@extend_schema(tags=["Service"])
class AdditionalServiceListAPIView(ListAPIView):
    queryset = AdditionalService.objects.filter(is_active=True)
    serializer_class = AdditionalServiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        type = self.request.query_params.get('type')
        if type and type in ['customer', 'manufacturer']:
            queryset = queryset.filter(type=type)

        is_active = self.request.query_params.get('is_active')
        if is_active and is_active in ['true', 'false']:
            queryset = queryset.filter(is_active=is_active)

        telegram_id = self.kwargs.get('telegram_id')
        if telegram_id:
            queryset = queryset.annotate(
                is_apply=Exists(UserApply.objects.filter(service_id=OuterRef('id'), user__telegram_id=telegram_id))
            )
        return queryset


class AdditionalServiceApplyAPIView(CreateAPIView):
    queryset = UserApply.objects.all()
    serializer_class = UserApplySerializer
