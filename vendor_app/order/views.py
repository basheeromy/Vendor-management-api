"""
    Views to handle orders.
"""
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.utils import timezone

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


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


class AcknowledgePOView(APIView):
    """
        Aknowledge Purchase Order.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):

        # Access url parameters.
        id = kwargs.get('id')

        obj = get_object_or_404(PurchaseOrder, id=id)

        if obj.acknowledgment_date is None:
            obj.acknowledgment_date = timezone.now()
            obj.save()
        else:
            return Response(
                "Already acknowledged.",
                status=status.HTTP_200_OK
            )

        return Response(
            "Aknowledged Successfully",
            status=status.HTTP_200_OK
        )
