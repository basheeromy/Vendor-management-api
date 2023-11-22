"""
    Unit test for views.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from vendor.models import Vendor
from vendor.serializers import VendorSerializer

class ListCreateVendorViewTest(TestCase):
    """
        Unit test for ListCreateVendorView.
    """

    def setUp(self):
        """
            Setup data for testing.
        """
        self.client = APIClient()
        self.url = reverse('list-create-vendor')
        self.vendor_data ={
            'name': 'test Vendor',
            'contact_details': 'email:tetvendor@example.com',
            'address': 'test address, street one, India',
            'vendor_code': '87654378',
            'on_time_delivery_rate': 95.0,
            'quality_rating_avg': 7.5,
            'average_response_time': 4.3,
            'fulfillment_rate': 89.5
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_listing_vendor(self):
        """
            Test GET request for listing vendors.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Validate response data
        expected_response = VendorSerializer(instance=self.vendor).data
        self.assertEqual(response.data[0], expected_response)

    def test_vendor_create(self):
        """
            Test POST request to create a new vendor
        """

        new_vendor_data = {
            'name': 'test Vendor2',
            'contact_details': 'email:tetvendor2@example.com',
            'address': 'test address2, street one, India',
            'vendor_code': '876543782',
            'on_time_delivery_rate': 95.0,
            'quality_rating_avg': 7.5,
            'average_response_time': 4.3,
            'fulfillment_rate': 89.5
        }
        response = self.client.post(self.url, new_vendor_data)
        self.assertEqual(response.status_code, 201)

        # Check if the new vendor is created in the database
        new_vendor = Vendor.objects.filter(name='test Vendor2').first()
        self.assertIsNotNone(new_vendor)


class ManageVendorViewTest(TestCase):
    """
        Unit test for ManageVendorView.
    """

    def setUp(self):
        """
            Setup data for testing.
        """
        self.client = APIClient()
        self.url = reverse('list-create-vendor')
        self.vendor_data ={
            'name': 'test Vendor',
            'contact_details': 'email:tetvendor@example.com',
            'address': 'test address, street one, India',
            'vendor_code': '87654378',
            'on_time_delivery_rate': 95.0,
            'quality_rating_avg': 7.5,
            'average_response_time': 4.3,
            'fulfillment_rate': 89.5
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)
        self.url = reverse('manage-vendor', kwargs={'id': self.vendor.id})

    def test_vendor_retrieve(self):
        """
            Test GET request to retrieve a vendor
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected_data = VendorSerializer(instance=self.vendor).data
        self.assertEqual(response.data, expected_data)

    def test_vendor_update(self):
        """
            Test PUT request to update a vendor
        """
        updated_data = {
            'name': 'updated vendor',
            'contact_details': 'updated@example.com',
            'address': 'test address, street one, India',
            'vendor_code': '87654378',
            'on_time_delivery_rate': 95.0,
            'quality_rating_avg': 7.5,
            'average_response_time': 4.3,
            'fulfillment_rate': 89.5
        }
        response = self.client.put(self.url, updated_data)
        self.assertEqual(response.status_code, 200)
        updated_vendor = Vendor.objects.get(id=self.vendor.id)
        self.assertEqual(updated_vendor.name, 'updated vendor')
        self.assertEqual(updated_vendor.contact_details, 'updated@example.com')

    def test_vendor_delete(self):
        """
            Test DELETE request to delete a vendor
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        deleted_vendor = Vendor.objects.filter(id=self.vendor.id).first()
        self.assertIsNone(deleted_vendor)
