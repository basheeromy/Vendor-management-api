"""
    Models to manage orders.
"""

from django.db import models
from vendor.models import Vendor
from django.core.cache import cache
from django.db.models import Avg
from django.db.models import (
    F,
    DurationField,
    ExpressionWrapper,
    Sum,
    Count
)
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
    date_delivered = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO: {self.po_number} Vendor: {self.vendor.name}"


def update_cache(cached_data, data):
    """
        This function is meant to update
        data in cache.

    Args:
        cached_data(type = dict/None)
        data (type = dict)
    Returns:
        cached_data(type = dict)
    """
    try:
        cached_data.update(data)
    except AttributeError:
        cached_data = data

    return cached_data


@receiver(pre_save, sender=PurchaseOrder)
def update_stats_pre_save(sender, instance, **kwargs):
    """
        This pre save signal function is meant to
        update different statistical data's related
        to vendor's performance.

    Args:
        sender(type = model)
        instance (type = model instance) to be updated.
        **kwargs (type = key word arguments)
    Returns:
        None
    """

    current_time = timezone.now()

    # Set delivery date.
    if instance._state.adding:
        date_in_10_days = current_time + timedelta(days=10)
        instance.delivery_date = date_in_10_days

    # Check if updating.
    if instance.id:
        original_instance = PurchaseOrder.objects.get(id=instance.id)

        # Set the date delivered the product.
        if (
            original_instance.date_delivered is None and (
                instance.status == 'completed'
            )
        ):
            instance.date_delivered = current_time

        # Set average response time.
        if (original_instance.acknowledgment_date is None and
                instance.acknowledgment_date is not None):

            # Calculate the response time for the current instance
            response_time = (
                instance.acknowledgment_date - original_instance.order_date
            )

            # Find the performance instance of the vendor.
            perf_ins = VendorPerformance.objects.filter(
                vendor=instance.vendor
            ).first()

            # Access cached data.
            cached_data = cache.get(instance.vendor.vendor_code)

            # set expiration time
            expire_in = 86400  # seconds (1 day)

            # print(cached_data)
            if cached_data is None or (
                'res_time_total' not in cached_data.keys() or (
                    'res_count' not in cached_data.keys()
                )
            ):

                # Expression used to calculate the response time of each po
                expression = ExpressionWrapper(
                    F('acknowledgment_date') - F('order_date'),
                    output_field=DurationField()
                )

                """
                    Find the sum of the response time of all purchase orders
                    and count of total purchase orders vendor responded.
                """
                result = (
                    PurchaseOrder.objects.annotate(
                        difference=expression
                    ).aggregate(
                        total_resp_time=Sum('difference'),
                        total_resp_count=Count(
                            'id',
                            filter=~models.Q(
                                acknowledgment_date__isnull=True
                            )
                        )
                    )
                )

                """
                    Check the scenarios which can derive from
                    presence or the absence of data. adjust data
                    with what we get from db and what we have.
                """
                if result['total_resp_time'] is None:
                    result['total_resp_time'] = response_time
                    result['total_resp_count'] = 1

                elif result['total_resp_time'] is not None:
                    result['total_resp_time'] += response_time
                    result['total_resp_count'] += 1

                # Handle cache.
                data = {
                        'res_time_total': result['total_resp_time'],
                        'res_count': result['total_resp_count']
                    }
                cached_data = update_cache(cached_data, data)

                cache.set(
                    instance.vendor.vendor_code,
                    cached_data,
                    timeout=expire_in
                )

                # Retrieved updated cache.
                cached_data = cache.get(instance.vendor.vendor_code)

                # Update and save the average response time of the vendor.
                perf_ins.average_response_time = (
                    (cached_data['res_time_total']).days /
                    cached_data['res_count']
                )

            else:
                # Case of both cache and the respective keys are present.

                # Update the data.
                cached_data.update({
                    'res_time_total': (
                        cached_data['res_time_total'] + response_time
                    ),
                    'res_count': cached_data['res_count'] + 1
                })

                # Set cache.
                cache.set(
                    instance.vendor.vendor_code,
                    cached_data,
                    timeout=expire_in
                )

                # Update and save the average response time of the vendor.
                perf_ins.average_response_time = (
                    (cached_data['res_time_total']).days /
                    cached_data['res_count']
                )

            # Save performance instance.
            perf_ins.save()


@receiver(post_save, sender=PurchaseOrder)
def update_stats_post_save(sender, created, instance, **kwargs):
    """
        This post save signal function is meant to
        update different statistical data's related
        to vendor's performance.

    Args:
        sender(type = model)
        created (type = boolean)
        instance (type = model instance). updated
        **kwargs (type = key word arguments)
    Returns:
        None
    """

    # Access performance instance of the vendor.
    perf_ins = VendorPerformance.objects.filter(
                vendor=instance.vendor
            ).first()

    # Access cached data.
    cached_data = cache.get(instance.vendor.vendor_code)

    # set expiration time
    expire_in = 86400  # seconds (1 day)

    # Check and populate cache.
    if cached_data is None or (
        'po_delivered' not in cached_data.keys() or (
            'po_issued' not in cached_data.keys()
        )
    ):
        po_delivered = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed'
        ).count()

        po_issued = PurchaseOrder.objects.filter(
            vendor=instance.vendor
        ).count()

        data = {
                'po_delivered': po_delivered,
                'po_issued': po_issued
            }
        cached_data = update_cache(cached_data, data)
        cache.set(
            instance.vendor.vendor_code,
            cached_data,
            timeout=expire_in
        )
        cached_data = cache.get(instance.vendor.vendor_code)

        # Update fulfillment rate.
        perf_ins.fulfillment_rate = (
            cached_data['po_delivered']/cached_data['po_issued']
        )

    elif created:
        """
            If cache is available and new po created.

            Update the number of po issued.
            Assuming that the po is directly forwarded
            to vendor at the time of creating.
        """
        data = {
                'po_issued': cached_data['po_issued'] + 1
            }
        cached_data = update_cache(cached_data, data)
        cache.set(
            instance.vendor.vendor_code,
            cached_data,
            timeout=expire_in
        )
        cached_data = cache.get(instance.vendor.vendor_code)

        # Update fulfillment rate.
        perf_ins.fulfillment_rate = (
            cached_data['po_delivered']/cached_data['po_issued']
        )

    elif instance.status == 'completed':
        # If cache is available and po instance is updated

        # Update the number of po delivered.
        data = {
                'po_delivered': cached_data['po_delivered'] + 1
            }
        cached_data = update_cache(cached_data, data)
        cache.set(
            instance.vendor.vendor_code,
            cached_data,
            timeout=expire_in
        )
        cached_data = cache.get(instance.vendor.vendor_code)

        # Update fulfillment rate.
        perf_ins.fulfillment_rate = (
            cached_data['po_delivered']/cached_data['po_issued']
        )

        if instance.delivery_date is not None:

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

                if 'po_delivered_on_time' in cached_data.keys():
                    data = {
                            'po_delivered_on_time': (
                                cached_data['po_delivered_on_time'] + 1
                            )
                        }
                    cached_data = update_cache(cached_data, data)
                    cache.set(
                        instance.vendor.vendor_code,
                        cached_data,
                        timeout=expire_in
                    )
                    cached_data = cache.get(instance.vendor.vendor_code)
                    perf_ins.on_time_delivery_rate = (
                        cached_data['po_delivered_on_time'] /
                        cached_data['po_delivered']
                    )
                else:
                    po_delivered_on_time = PurchaseOrder.objects.filter(
                        delivery_date__gt=F('date_delivered')
                    ).count()

                    data = {
                            'po_delivered_on_time': po_delivered_on_time
                        }
                    cached_data = update_cache(cached_data, data)
                    cache.set(
                        instance.vendor.vendor_code,
                        cached_data,
                        timeout=expire_in
                    )
                    cached_data = cache.get(instance.vendor.vendor_code)
                    perf_ins.on_time_delivery_rate = (
                        cached_data['po_delivered_on_time'] /
                        cached_data['po_delivered']
                    )

    # Save the performance instance with changes.
    perf_ins.save()
