"""
    Urls to vendor related views.
"""

from django.urls import path
from .views import PurchaseOrderListCreateView


urlpatterns = [
    path(
        '',
        PurchaseOrderListCreateView.as_view(),
        name='list-create-purchase-order'
    ),
]
