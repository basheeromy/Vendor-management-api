"""
    Views to manage vendor related functionalities.
"""

from django.shortcuts import render
from .serializers import (
    VendorSerializer
)
from .models import Vendor

from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

class ListCreateVendorView(ListCreateAPIView):
    """
        List all vendors with get method,
        Create new vendor with post method.
    """
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()


class ManageVendorView(RetrieveUpdateDestroyAPIView):
    """
        manage vendor by id.
        fetch, update and delete a single vendor instance.
    """

    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    lookup_field = 'id'
    