from django_filters import FilterSet, CharFilter
from apps.application.models import Manufacturer


class ManufacturerFilterSet(FilterSet):
    product_segment = CharFilter(method='filter_product_segment')
    
    class Meta:
        model = Manufacturer
        fields = ['min_order_quantity', 'product_segment']
    
    def filter_product_segment(self, queryset, name, value):
        """
        Filter by product_segment IDs. Accepts comma-separated values like "4,3"
        """
        if not value:
            return queryset
        
        # Split comma-separated values and convert to integers
        try:
            segment_ids = [id.strip() for id in value.split(',') if id.strip()]
            return queryset.filter(product_segment__id__in=segment_ids)
        except (ValueError, TypeError):
            # If conversion fails, return empty queryset
            return queryset.none()
