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
        extra_kwargs = {
            'order_date': {
                'read_only': True
            },
            'delivery_date': {
                'read_only': True
            },
            'status': {
                'read_only': True
            },
            'quality_rating': {
                'read_only': True
            },
            'acknowledgment_date': {
                'read_only': True
            }
        }
