from django_filters import FilterSet, DateTimeFilter
from payment.models import Transaction


class TransactionFilterSet(FilterSet):
    class Meta:
        model = Transaction
        fields = ['is_paid_with_card']


class TransactionListFilterSet(FilterSet):
    paid_at_gte = DateTimeFilter(field_name='paid_at', lookup_expr='gte')
    paid_at_lte = DateTimeFilter(field_name='paid_at', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['order__user', 'provider', 'paid_at_gte', 'paid_at_lte']
