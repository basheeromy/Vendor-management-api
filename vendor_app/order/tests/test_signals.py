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

    def test_update_stats_pre_save(self):

        # Set order dates for two orders.
        acknow_date_1 = timezone.now() + timedelta(days=2)
        acknow_date_2 = timezone.now() + timedelta(days=4)

        expected_avg_resp_time = 3.0   # (2+4)/2 = 3

        # Set purchase order 1
        purchase_order1 = PurchaseOrder.objects.create(
            po_number="test-123-po",
            items={
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            quantity=5,
            vendor=self.vendor
        )

        # Set to 10 days from now.pwd
        expected_delivery_date = timezone.now() + timedelta(days=10)

        # Test Setting of Delivery date.
        self.assertAlmostEqual(
            purchase_order1.delivery_date.timestamp(),
            expected_delivery_date.timestamp(),
            delta=1  # Tolerance in seconds for time comparison
        )

        # Set aknowledgement_date for po 1
        purchase_order1.acknowledgment_date = acknow_date_1
        purchase_order1.save()

        # Set purchase order 2
        purchase_order2 = PurchaseOrder.objects.create(
            po_number="test-124-po",
            items={
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            quantity=5,
            vendor=self.vendor
        )

        # Set aknowledgement_date for po 2
        purchase_order2.acknowledgment_date = acknow_date_2
        purchase_order2.save()

        # Access performance data of vendor
        perf_ins = VendorPerformance.objects.filter(
                vendor=self.vendor
            ).first()

        # Access average response time.
        avg_resp_time = perf_ins.average_response_time

        self.assertEqual(
            avg_resp_time,
            expected_avg_resp_time
        )
