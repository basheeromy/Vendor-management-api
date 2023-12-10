"""
    Models to manage orders.
"""

from django.db import models
from vendor.models import Vendor
from django.core.cache import cache
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import (
    post_save,
    pre_save
)
from django.dispatch import receiver
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)

from vendor.models import VendorPerformance


class PurchaseOrder(models.Model):
    """
        Model to create vendor instance.
    """
    CHOICES = [
        ('pending', 'Pending'),
        ('out-to-deliver', 'Out-to-deliver'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]

    )
    status = models.CharField(
        max_length=30,
        choices=CHOICES,
        default='pending'
    )
    quality_rating = models.FloatField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.00),
            MaxValueValidator(10.00)
        ]

    )
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO: {self.po_number} Vendor: {self.vendor.name}"


@receiver(pre_save, sender=PurchaseOrder)
def update_stats_pre_save(sender, instance, **kwargs):
    # Set delivery date.
    if instance._state.adding:
        current_time = timezone.now()
        date_in_10_days = current_time + timedelta(days=10)
        instance.delivery_date = date_in_10_days

    # Set average response time.
    if instance.id:
        original_instance = PurchaseOrder.objects.get(id=instance.id)
        if (original_instance.acknowledgment_date is None and
                instance.acknowledgment_date is not None):
            time_diff = (
                instance.acknowledgment_date - original_instance.order_date
            )
            response_time = time_diff.days
            perf_ins = VendorPerformance.objects.filter(
                vendor=instance.vendor
            ).first()
            perf_ins.res_time_total += response_time
            perf_ins.res_count += 1
            perf_ins.average_response_time = (
                perf_ins.res_time_total/perf_ins.res_count
            )
            perf_ins.save()


@receiver(post_save, sender=PurchaseOrder)
def update_stats_post_save(sender, created, instance, **kwargs):
    # post save signals to update statistical data.

    # Access performance instance of the vendor.
    perf_ins = VendorPerformance.objects.filter(
                vendor=instance.vendor
            ).first()

    # Access cached data.
    cached_data = cache.get(instance.vendor.vendor_code)

    # Check and populate cache.
    if cached_data is None:
        po_del = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed'
        ).count()

        po_issued = PurchaseOrder.objects.filter(
            vendor=instance.vendor
        ).count()
        perf_data = {
            'po_del': po_del,
            'po_issued': po_issued
        }
        cache.set(instance.vendor.vendor_code, perf_data)
        cached_data = cache.get(instance.vendor.vendor_code)

        # Update fulfillment rate.
        perf_ins.fulfillment_rate = (
            cached_data['po_del']/cached_data['po_issued']
        )

    # If cache is available and new po created.
    elif created:
        # Update the number of po issued.
        # Assuming that the po is directly forwarded
        # to vendor at the time of creating.
        perf_data = {
            'po_del': cached_data['po_del'],
            'po_issued': cached_data['po_issued'] + 1
        }
        cache.set(instance.vendor.vendor_code, perf_data)
        cached_data = cache.get(instance.vendor.vendor_code)

        # Update fulfillment rate.
        perf_ins.fulfillment_rate = (
            cached_data['po_del']/cached_data['po_issued']
        )
    # If cache is available and po instance is updated
    elif instance.status == 'completed':
        # Update the number of po delivered.
        perf_data = {
            'po_del': cached_data['po_del'] + 1,
            'po_issued': cached_data['po_issued']
        }
        cache.set(instance.vendor.vendor_code, perf_data)
        cached_data = cache.get(instance.vendor.vendor_code)

        # Update fulfillment rate.
        perf_ins.fulfillment_rate = (
            cached_data['po_del']/cached_data['po_issued']
        )

    if not created and (
        instance.status == 'completed' and (
            instance.delivery_date is not None
        )
    ):  # trigger only for updates.

        # Set quality rating average.
        if (instance.quality_rating is not None and
                instance.quality_rating > 0):
            quality_rating_avg = PurchaseOrder.objects.filter(
                vendor=instance.vendor,
                status='completed'
            ).aggregate(avg_rating=Avg('quality_rating'))
            perf_ins.quality_rating_avg = quality_rating_avg['avg_rating']

        # Calculate on time delivery rate.
        cached_data = cache.get(instance.vendor.vendor_code)

        current_time = timezone.now()
        if instance.delivery_date >= current_time:
            perf_ins.po_deli_on_time += 1

        perf_ins.on_time_delivery_rate = (
            perf_ins.po_deli_on_time/cached_data['po_del']
        )

    perf_ins.save()
