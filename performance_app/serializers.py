from rest_framework import serializers
from .models import VendorPerformance

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformance
        fields = '__all__'
