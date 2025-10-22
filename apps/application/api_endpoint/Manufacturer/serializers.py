from rest_framework import serializers
from apps.application.models import Manufacturer, ManufacturerSertificate


class ManufacturerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class ManufacturerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'company_name', 'full_name']
        
        
class ManufacturerCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerSertificate
        fields = '__all__'


class ManufacturerDetailSerializer(serializers.ModelSerializer):
    from apps.application.api_endpoint.Segment.serializers import SegmentListSerializer
    sertificates = ManufacturerCertificateSerializer(many=True)
    product_segment = SegmentListSerializer(many=True)
    
    class Meta:
        model = Manufacturer
        fields = ['id', 'company_name', 'full_name', 'min_order_quantity', 'office_address', 'website', 'has_crm', 'employee_count', 'sertificates', 'product_segment']