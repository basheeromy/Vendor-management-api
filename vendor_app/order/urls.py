"""
    Urls to vendor related views.
"""

from django.urls import path
from .views import (
    PurchaseOrderListCreateView,
    ManagePurchaseOrderView,
    AcknowledgePOView
)


urlpatterns = [
    path(
        '',
        PurchaseOrderListCreateView.as_view(),
        name='list-create-purchase-order'
    ),
    path(
        '<str:id>',
        ManagePurchaseOrderView.as_view(),
        name='manage-purchase-order'
    ),
    path(
        '<str:id>/acknowledge',
        AcknowledgePOView.as_view(),
        name='acknowledge-po'
    )
]
