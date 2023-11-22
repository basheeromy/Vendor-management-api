"""
    Tests for models.
"""

from django.test import TestCase
from vendor.models import Vendor

class ModelTest(TestCase):
    """
        Test models.
    """

    def test_create_vendor(self):
        """
            Test creating a vendor and
            it's __str__ method.
        """
        name = 'test Vendor'
        contact_details = ('email:tetvendor@example.com')
        address = 'test address, street one, india'
        vendor_code = '87654324'
        on_time_delivery_rate=95.0
        quality_rating_avg=4.5
        average_response_time=2.3
        fulfillment_rate=98.0

        vendor = Vendor.objects.create(
            name = name,
            contact_details = contact_details,
            address = address,
            vendor_code = vendor_code,
            on_time_delivery_rate = on_time_delivery_rate,
            quality_rating_avg = quality_rating_avg,
            average_response_time = average_response_time,
            fulfillment_rate = fulfillment_rate
        )


        self.assertEqual(vendor.name, name)
        self.assertEqual(vendor.contact_details, contact_details)
        self.assertEqual(vendor.address, address)
        self.assertEqual(vendor.vendor_code, vendor_code)
        self.assertEqual(vendor.on_time_delivery_rate, on_time_delivery_rate)
        self.assertEqual(vendor.quality_rating_avg, quality_rating_avg)
        self.assertEqual(vendor.average_response_time, average_response_time)
        self.assertEqual(vendor.fulfillment_rate, fulfillment_rate)

        # Test vendor model's __str__ method.
        self.assertEqual(str(vendor), 'test Vendor')
