"""
    Views to handle orders.
"""
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

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


class ManagePurchaseOrderView(RetrieveUpdateDestroyAPIView):
    """
        manage order by id.
        fetch, update and delete purchase order instance.
    """

    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
