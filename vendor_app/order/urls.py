"""
    Urls to vendor related views.
"""

from django.urls import path
from .views import (
    PurchaseOrderListCreateView,
    ManagePurchaseOrderView
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
    )
]
