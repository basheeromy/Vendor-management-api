"""
    Urls to vendor related views.
"""

from django.urls import path
from .views import (
    ListCreateVendorView,
    ManageVendorView,
    GenerateTokenView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('', ListCreateVendorView.as_view(), name="list-create-vendor"),
    path('<str:id>', ManageVendorView.as_view(), name='manage-vendor'),
    path('token/', GenerateTokenView.as_view(), name='obtain-token-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token')
]
