from django.contrib import admin

from .models import (
    Vendor,
    VendorPerformance,
)

admin.site.register(Vendor)
admin.site.register(VendorPerformance)
