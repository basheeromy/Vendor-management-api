"""
    Views to handle orders.
"""
from rest_framework.generics import (
    ListCreateAPIView,
)

from .models import (
    PurchaseOrder,
)
from .serializers import (
    PurchaseOrderSerializer
)


class PurchaseOrderListCreateView(ListCreateAPIView):
    """
        List all purchase orders with GET method.
        Create New Purchase order with PUT method.
    """
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()
