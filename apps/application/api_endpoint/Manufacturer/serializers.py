from rest_framework import serializers
from apps.application.models import Manufacturer, ManufacturerCompanyImage, ManufacturerSertificate


class ManufacturerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class ManufacturerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'company_name', 'full_name', 'logo']
        
        
class ManufacturerCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerSertificate
        fields = '__all__'



class ManufacturerCompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerCompanyImage
        fields = '__all__'



class ManufacturerDetailSerializer(serializers.ModelSerializer):
    from apps.application.api_endpoint.Segment.serializers import SegmentListSerializer
    sertificates = ManufacturerCertificateSerializer(many=True)
    product_segment = SegmentListSerializer(many=True)
    images = ManufacturerCompanyImageSerializer(many=True)
    
    class Meta:
        model = Manufacturer
        fields = [
            'id',
            'user',
            'company_name',
            'market_experience',
            'full_name',
            'position',
            'min_order_quantity',
            'commercial_offer_text',
            'commercial_offer',
            'production_address',
            'office_address',
            'website',
            'has_quality_control',
            'has_crm',
            'has_erp',
            'has_gemini_gerber',
            'employee_count',
            'owns_building',
            'has_power_issues',
            'has_credit_load',
            'organization_structure',
            'equipment_info',
            'phone',
            'status',
            'order',
            'logo',
            'product_segment',
            'sertificates',
            'images',

        ]