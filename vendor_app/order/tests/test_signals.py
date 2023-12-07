"""
    Unit tests for Signals.
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from order.models import PurchaseOrder
from vendor.models import (
    VendorPerformance
)


class TestPurchaseOrderSignals(TestCase):
    """
        Unit test to update Signals in
        PurchaseOrder model.
    """
    def setUp(self):
        """
            Set up data for testing.
        """
        self.vendor = get_user_model().objects.create_vendor(
            email='testvendor@example.com',
            name='test Vendor',
            contact_details='email:tetvendor@example.com',
            address='test address, street one, india',
            vendor_code='87654324',
            password='testpass123'
        )

        # Set purchase order 1
        self.purchase_order1 = PurchaseOrder.objects.create(
            po_number="test-123-po",
            items={
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            quantity=5,
            vendor=self.vendor
        )

        # Set purchase order 2
        self.purchase_order2 = PurchaseOrder.objects.create(
            po_number="test-124-po",
            items={
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            quantity=5,
            vendor=self.vendor
        )
        # Set purchase order 3
        self.purchase_order3 = PurchaseOrder.objects.create(
            po_number="test-125-po",
            items={
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            quantity=5,
            vendor=self.vendor
        )

    def test_update_stats_pre_save(self):
        """
            Test pre save signals.
        """

        # Set acknowledgment dates for two orders.
        acknow_date_1 = timezone.now() + timedelta(days=2)
        acknow_date_2 = timezone.now() + timedelta(days=4)

        # Set to 10 days from now.
        expected_delivery_date = timezone.now() + timedelta(days=10)

        # Test Setting of Delivery date.
        self.assertAlmostEqual(
            self.purchase_order1.delivery_date.timestamp(),
            expected_delivery_date.timestamp(),
            delta=1  # Tolerance in seconds for time comparison
        )

        # Set acknowledgment_date for po 1
        self.purchase_order1.acknowledgment_date = acknow_date_1
        self.purchase_order1.save()

        # Set acknowledgment_date for po 2
        self.purchase_order2.acknowledgment_date = acknow_date_2
        self.purchase_order2.save()

        # Access performance data of vendor
        perf_ins = VendorPerformance.objects.filter(
                vendor=self.vendor
            ).first()

        # Access average response time.
        avg_resp_time = perf_ins.average_response_time

        # Expected average response time.
        expected_avg_resp_time = 3.0   # (2+4)/2 = 3

        self.assertEqual(
            avg_resp_time,
            expected_avg_resp_time
        )

    def test_update_stats_post_save(self):
        """
            Test post save signals.
        """

        # Access performance data of vendor
        perf_ins = VendorPerformance.objects.filter(
                vendor=self.vendor
            ).first()

        # Test resetting of no_po_issued (3, check setUp.)
        self.assertEqual(
            perf_ins.no_po_issued,
            3
        )

        # Set values to trigger signals for po 1
        self.purchase_order1.status = 'completed'
        self.purchase_order1.quality_rating = 8
        self.purchase_order1.save()

        # Set values to trigger signals for po 2
        self.purchase_order2.status = 'completed'
        self.purchase_order2.quality_rating = 4
        self.purchase_order2.save()

        # Access updated performance data of vendor
        perf_ins = VendorPerformance.objects.filter(
                vendor=self.vendor
            ).first()

        # Set expected on time delivery rate.
        expected_on_time_del_rate = 1.0  # 100%

        # Set expected quality rating average.
        expected_quality_rate_avg = 6.0

        # Test on time delivery rate
        self.assertEqual(
            perf_ins.on_time_delivery_rate,
            expected_on_time_del_rate
        )

        # Test on quality rating average.
        self.assertEqual(
            perf_ins.quality_rating_avg,
            expected_quality_rate_avg
        )

        # Set expected Fulfillment rate.
        # 2/3 = 0.66 and rounded to 6.7 as
        # we are using round method.
        expected_fulfillment_rate = 0.67

        self.assertEqual(
            round(perf_ins.fulfillment_rate, 2),
            expected_fulfillment_rate
        )
