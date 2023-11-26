"""
    Serializer to manage Puchase orders.
"""

from rest_framework import serializers
from .models import PurchaseOrder


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
        Serialize and validate Purchase order.
    """

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
