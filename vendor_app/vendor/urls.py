"""
    Urls to vendor related views.
"""

from django.urls import path
from django.urls import include, path
from .views import (
    ListCreateVendorView,
    ManageVendorView
)

urlpatterns = [
    path('', ListCreateVendorView.as_view(), name="list-create-vendor"),
    path('<str:id>', ManageVendorView.as_view(), name='manage-vendor' ),
]
