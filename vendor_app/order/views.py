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
    PurchaseOrderSerializer,
    PO_CompleteSerializer
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
        Acknowledge Purchase Order.
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
            "Acknowledged Successfully",
            status=status.HTTP_200_OK
        )


class MarkCompletedView(APIView):
    """
        Mark Purchase Order as Completed.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PO_CompleteSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Access url parameters.
            id = kwargs.get('id')
            # Purchase Order object.
            obj = get_object_or_404(PurchaseOrder, id=id)

            # Check the order is acknowledged or not
            if obj.acknowledgment_date is None:
                return Response(
                    "Order not yet acknowledged.",
                    status=status.HTTP_403_FORBIDDEN
                )

            # Mark as completed.
            if obj.status != 'completed':
                obj.status = 'completed'
                if request.data and request.data['quality_rating']:
                    obj.quality_rating = int(request.data['quality_rating'])
                    obj.save()

                    return Response(
                            "Purchase order marked as "
                            "completed with quality rating.",
                            status=status.HTTP_200_OK
                    )
                else:
                    obj.save()

                    return Response(
                        "Purchase order marked as "
                        "completed without quality rating.",
                        status=status.HTTP_200_OK
                    )

            else:
                return Response(
                            "Already updated.",
                            status=status.HTTP_200_OK
                    )
        else:
            return Response(
                "Data validation failed.",
                status=status.HTTP_400_BAD_REQUEST
            )
