"""
    Test cases for serilizers.
"""

from django.test import TestCase
from vendor.models import Vendor
from vendor.serializers import (
    VendorSerializer,
    GenerateTokenSerializer
)
from django.urls import reverse
from rest_framework.test import APIClient


class VendorSerializerTestCase(TestCase):
    """
        Unit test for vendor serializer.
    """
    vendor_data = {
        'email': 'testuser123@example.com',
        'name': 'test Vendor',
        'contact_details': 'email:tetvendor@example.com',
        'address': 'test address, street one, India',
        'vendor_code': '87654324',
        'password': 'testpass123'
    }

    def test_vendor_serializer(self):
        """
            Test validation and serialization process.
        """

        serializer = VendorSerializer(data=self.vendor_data)
        self.assertTrue(serializer.is_valid())

        # Check all fields.
        serialized_data = serializer.data
        self.assertEqual(
            serialized_data['email'],
            'testuser123@example.com'
        )
        self.assertEqual(
            serialized_data['name'],
            'test Vendor'
        )
        self.assertEqual(
            serialized_data['contact_details'],
            'email:tetvendor@example.com'
        )
        self.assertEqual(
            serialized_data['address'],
            'test address, street one, India'
        )
        self.assertEqual(
            serialized_data['vendor_code'],
            '87654324'
        )
        self.assertNotIn(
            'password',
            serialized_data
        )

    def test_vendor_serializer_invalid_data(self):
        """
            Test invalid data fails validation
        """
        # create invalid data for testing
        invalid_data = self.vendor_data.copy()
        invalid_data.pop('name')

        serializer = VendorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_vendor_serializer_create_method(self):
        """
            Test create method in vendor serializer.
        """
        serializer = VendorSerializer()
        vendor = serializer.create(self.vendor_data)
        self.assertIsInstance(vendor, Vendor)

    def test_vendor_serializer_update_method(self):
        """
            Test create method in vendor serializer.
        """
        serializer = VendorSerializer()
        vendor = serializer.create(self.vendor_data)
        data = {
            'email': 'testuser123@example.com',
            'name': 'name edited',
            'password': '1234567'
        }

        updated_vendor = serializer.update(vendor, data)

        self.assertEqual(
            updated_vendor.name,
            'name edited'
        )

        # Check updated password.
        self.assertTrue(updated_vendor.check_password('1234567'))


class GenerateTokenSerializerTest(TestCase):
    """
        Unit test for Generate token serializer.
    """
    def setUp(self):
        """
            Setup data for testing.
        """

        self.vendor_data = {
            'email': 'testuser123@example.com',
            'name': 'test Vendor',
            'contact_details': 'email:tetvendor@example.com',
            'address': 'test address, street one, India',
            'vendor_code': '87654324',
            'password': 'testpass123'
        }

        self.input_data = {
            'email': 'testuser123@example.com',
            'password': 'testpass123'
        }

        # Create a vendor for testing.
        self.client = APIClient()
        create_vendor_url = reverse("list-create-vendor")
        self.vendor = self.client.post(
            create_vendor_url,
            self.vendor_data
        )

    def test_generate_token_serializer(self):
        """
            Test data validation
        """

        # check validation
        serializer = GenerateTokenSerializer(data=self.input_data)
        self.assertTrue(serializer.is_valid())

        # check returned data fields.
        serialized_data = serializer.data
        self.assertEqual(
            serialized_data['email'],
            'testuser123@example.com'
        )
        vendor_instance = Vendor.objects.get(id=1)
        self.assertEqual(
            serialized_data['password'],
            vendor_instance.password
        )

    def test_vendor_serializer_invalid_data(self):
        """
            Test invalid data fails validation
        """
        # create invalid data for testing
        invalid_data = self.input_data.copy()
        invalid_data.pop('email')

        serializer = GenerateTokenSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
