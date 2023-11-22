"""
    Models to manage vendor.
"""

from django.db import models



class Vendor(models.Model):
    """
        Model to create vendor instance.
    """
    name = models.CharField(max_length=150)
    contact_details = models.TextField(null=True)
    address = models.TextField(null=True)
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    def __str__(self):
        return self.name