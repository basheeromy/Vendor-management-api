

from django.test import TestCase
from django.contrib.auth import get_user_model
from vendor.models import VendorPerformance


class VendorModelSignalsTest(TestCase):
    """
        Test Working of signals in
        Vendor model
    """
    def setUp(self):

        self.vendor = get_user_model().objects.create_vendor(
            email='test@example.com',
            name='test Vendor',
            password='testpass123',
            vendor_data={
                "contact_details": "contact me here",
                "address": "test address, street one, india",
                "vendor_code": "87654324"
            }
        )

    def test_create_performance_instance(self):
        """
            Test creating a vendor's  performance sheet
            and it's __str__ method.
        """
        on_time_delivery_rate = None
        quality_rating_avg = None
        average_response_time = None
        fulfillment_rate = None

        perf_data = VendorPerformance.objects.filter(
            vendor=self.vendor
        ).first()

        self.assertEqual(
            perf_data.vendor,
            self.vendor
        )
        self.assertEqual(
            perf_data.on_time_delivery_rate,
            on_time_delivery_rate
        )
        self.assertEqual(
            perf_data.quality_rating_avg,
            quality_rating_avg
        )
        self.assertEqual(
            perf_data.average_response_time,
            average_response_time
        )
        self.assertEqual(
            perf_data.fulfillment_rate,
            fulfillment_rate
        )

        # Test VendorPerformance model's __str__ method.
        self.assertEqual(str(perf_data), "test Vendor's performance data")
