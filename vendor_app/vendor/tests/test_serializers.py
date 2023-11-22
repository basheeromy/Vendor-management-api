"""
    Test cases for serilizers.
"""

from django.test import TestCase
from vendor.models import Vendor
from vendor.serializers import VendorSerializer


class VendorSerializerTestCase(TestCase):
    """
        Unit test for vendor serializer.
    """
    vendor_data ={
        'name': 'test Vendor',
        'contact_details': 'email:tetvendor@example.com',
        'address': 'test address, street one, India',
        'vendor_code': '87654324',
        'on_time_delivery_rate': 95.0,
        'quality_rating_avg': 7.5,
        'average_response_time': 4.3,
        'fulfillment_rate': 89.5
    }

    def test_vendor_serializer(self):
        """
            Test validation and serialization process.
        """

        serializer = VendorSerializer(data=self.vendor_data)
        self.assertTrue(serializer.is_valid())

        # Check all fields.
        serialized_data = serializer.data
        self.assertEqual(serialized_data['name'], 'test Vendor')
        self.assertEqual(serialized_data['contact_details'], 'email:tetvendor@example.com')
        self.assertEqual(serialized_data['address'], 'test address, street one, India')
        self.assertEqual(serialized_data['vendor_code'], '87654324')
        self.assertEqual(serialized_data['on_time_delivery_rate'], 95.0)
        self.assertEqual(serialized_data['quality_rating_avg'], 7.5)
        self.assertEqual(serialized_data['average_response_time'], 4.3)
        self.assertEqual(serialized_data['fulfillment_rate'], 89.5)

    def test_vendor_serializer_invalid_data(self):
        """
            Test invalid data fails validation
        """
        # create invalid data for testing
        invalid_data = self.vendor_data.copy()
        invalid_data.pop('name')

        serializer = VendorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
