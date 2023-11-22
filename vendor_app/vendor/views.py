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
    ListCreateAPIView
)

class ListCreateVendorView(ListCreateAPIView):

    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
