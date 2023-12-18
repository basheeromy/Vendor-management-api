"""
    Configure django admin page.
"""

from django.contrib import admin

from .models import (
    User,
    VendorPerformance,
    Vendor
)

admin.site.register(User)
admin.site.register(VendorPerformance)
admin.site.register(Vendor)
