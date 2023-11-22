"""
    Urls to vendor related views.
"""

from django.urls import path
from django.urls import include, path
from .views import (
    ListCreateVendorView,
)

urlpatterns = [
    path('', ListCreateVendorView.as_view(), name="list-create-vendor"),

]
