"""
    Unit test for views.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from vendor.models import (
    Vendor,
    VendorPerformance
)
from vendor.serializers import (
    VendorSerializer,
    VendorPerformanceSerializer
)


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
        self.vendor_data = {
            'email': 'testvendor@example.com',
            'name': 'test Vendor',
            'contact_details': 'contactme',
            'address': 'test address, street one, India',
            'vendor_code': '87654378',
            'password': 'testpass123'
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
            'email': 'testvendor2@example.com',
            'name': 'test Vendor2',
            'contact_details': 'contact me',
            'address': 'test address2, street one, India',
            'vendor_code': '876543782',
            'password': 'testpass123'
        }
        response = self.client.post(self.url, new_vendor_data)
        self.assertEqual(response.status_code, 201)

        # Check if the new vendor is created in the database
        new_vendor = Vendor.objects.filter(name='test Vendor2').first()
        self.assertIsNotNone(new_vendor)


class ManageVendorViewTest(TestCase):
    """
        Unit test for ManageVendorView.
        This test class tests GenerateTokenView and
        refresh token generating endpoint too
    """

    def setUp(self):
        """
            Setup data for testing.
        """
        self.client = APIClient()
        self.vendor_data = {
            'email': 'testvendor@example.com',
            'name': 'test Vendor',
            'contact_details': 'email:tetvendor@example.com',
            'address': 'test address, street one, India',
            'vendor_code': '87654378',
            'password': 'testpass1234'
        }
        input_data = {
            "email": "testvendor@example.com",
            "password": 'testpass1234'
        }

        # Create a vendor for testing.
        create_vendor_url = reverse("list-create-vendor")
        self.vendor = self.client.post(create_vendor_url, self.vendor_data)
        # self.expected_data = Vendor.objects.create(**self.vendor_data)

        # generate access token
        access_token_url = reverse('obtain-token-pair')
        response = self.client.post(access_token_url, input_data)
        self.access_token = response.json().get('access')
        self.refresh_token = response.json().get('refresh')

        self.url = reverse('manage-vendor', kwargs={'id': 1})
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def test_vendor_retrieve(self):
        """
            Test GET request to retrieve a vendor
        """
        # send get request.
        response = self.client.get(self.url, headers=self.headers)

        # check status code
        self.assertEqual(response.status_code, 200)

        # generate expected data
        expected_data = VendorSerializer(instance=self.vendor.json()).data

        # compare expected data with response
        self.assertEqual(response.data, expected_data)

    def test_vendor_update(self):
        """
            Test PUT request to update a vendor
        """
        updated_data = {
            'email': 'testvendor@example.com',
            'name': 'updated vendor',
            'contact_details': 'updated@example.com',
            'address': 'test address, street one, India',
            'vendor_code': '87654378',
            'password': 'updatedpass321'

        }
        response = self.client.put(
            self.url,
            updated_data,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        updated_vendor = Vendor.objects.get(id=self.vendor.json()['id'])
        self.assertEqual(updated_vendor.name, 'updated vendor')
        self.assertEqual(updated_vendor.contact_details, 'updated@example.com')
        self.assertTrue(updated_vendor.check_password('updatedpass321'))

    def test_vendor_delete(self):
        """
            Test DELETE request to delete a vendor
        """
        response = self.client.delete(self.url, headers=self.headers)
        self.assertEqual(response.status_code, 204)
        deleted_vendor = Vendor.objects.filter(
            id=self.vendor.json()['id']
        ).first()
        self.assertIsNone(deleted_vendor)

    def test_refresh_token_endpoint(self):
        """
            Test generating new access token with refresh token.
        """
        refresh_token_url = reverse('refresh-token')
        input_data = {
            "refresh": self.refresh_token
        }
        response = self.client.post(refresh_token_url, input_data)
        self.access_token = response.json().get('access')
        self.refresh_token = response.json().get('refresh')

        # Check new access token.
        # send get request.
        response = self.client.get(self.url, headers=self.headers)

        # check status code
        self.assertEqual(response.status_code, 200)


class VendorPerformanceStatsViewTest(TestCase):
    """
        Unit test for VendorPerformanceStatsView.
    """

    def setUp(self):
        """
            Setup data for testing.
        """
        self.client = APIClient()
        self.vendor_data = {
            'email': 'testvendor@example.com',
            'name': 'test Vendor',
            'contact_details': 'email:tetvendor@example.com',
            'address': 'test address, street one, India',
            'vendor_code': '87654378',
            'password': 'testpass1234'
        }
        input_data = {
            "email": "testvendor@example.com",
            "password": 'testpass1234'
        }

        # Create a vendor for testing.
        create_vendor_url = reverse("list-create-vendor")
        vendor_response = self.client.post(
            create_vendor_url,
            self.vendor_data
        )
        self.vendor = Vendor.objects.get(id=vendor_response.data['id'])

        # generate access token
        access_token_url = reverse('obtain-token-pair')
        response = self.client.post(access_token_url, input_data)
        self.access_token = response.json().get('access')
        self.refresh_token = response.json().get('refresh')

        self.url = reverse('vendor-performance', kwargs={'vendor': 1})
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def test_vendor_performance_retrieve(self):
        """
            Test GET request to retrieve a vendor
        """

        perf_data = VendorPerformance.objects.filter(
            vendor=self.vendor
        ).first()

        # Send get request.
        response = self.client.get(self.url, headers=self.headers)
        # print(response.json())  # to check errors. un comment this.

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Generate expected data
        # Use serializer to exclude write only fields.
        expected_data = VendorPerformanceSerializer(instance=perf_data).data

        # Compare expected data with response
        self.assertEqual(response.data, expected_data)
