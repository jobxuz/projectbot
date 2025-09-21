from rest_framework import serializers
from apps.application.api_endpoint.Manufacturer.serializers import ManufacturerListSerializer
from apps.application.models import Segment


class SegmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ["id", "title"]
        

