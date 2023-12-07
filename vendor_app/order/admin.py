"""
    Configure django admin page.
"""

from django.contrib import admin
from .models import PurchaseOrder


admin.site.register(PurchaseOrder)
