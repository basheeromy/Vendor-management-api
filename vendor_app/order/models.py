"""
    Models to manage orders.
"""

from django.db import models
from vendor.models import Vendor
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
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO: {self.po_number} Vendor: {self.vendor.name}"


@receiver(pre_save, sender=PurchaseOrder)
def add_delivery_date(sender, instance, **kwargs):
    if instance._state.adding:
        current_time = timezone.now()
        date_in_10_days = current_time + timedelta(days=10)
        instance.delivery_date = date_in_10_days


@receiver(post_save, sender=PurchaseOrder)
def status_updated(sender, created, instance, **kwargs):
    if not created:  # trigger only for updation.
        if (instance.status == 'completed' and
                instance.delivery_date is not None):
            perf_ins = VendorPerformance.objects.filter(
                vendor=instance.vendor
            ).first()
            perf_ins.po_delivered += 1

            current_time = timezone.now()
            if instance.delivery_date >= current_time:
                perf_ins.po_deli_on_time += 1

            perf_ins.on_time_delivery_rate = (
                perf_ins.po_deli_on_time/perf_ins.po_delivered
            )
            if instance.quality_rating > 0:
                quality_rating_avg = PurchaseOrder.objects.filter(
                    vendor=instance.vendor,
                    status='completed'
                ).aggregate(avg_rating=Avg('quality_rating'))
                perf_ins.quality_rating_avg = quality_rating_avg['avg_rating']
            perf_ins.save()
