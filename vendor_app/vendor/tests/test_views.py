"""
    Unit test for views.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from vendor.models import (
    Vendor,
    User,
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
        email = 'test@example.com'
        name = 'test Vendor'
        password = 'testpass123'
        vendor_data = {
            "contact_details": "contact me here",
            "address": "test address, street one, india",
            "vendor_code": "87654324"
        }

        self.vendor = get_user_model().objects.create_vendor(
            email=email,
            name=name,
            password=password,
            vendor_data=vendor_data
        )

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
            'email': 'testuser124@example.com',
            'name': 'test Vendor 124',
            'password': 'testpass123',
            'vendor_data': {
                "contact_details": "test contact details",
                "address": "test address, street one, India",
                "vendor_code": "87654325"
            }
        }
        response = self.client.post(
            self.url,
            new_vendor_data,
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        # Check if the new vendor is created in the database
        new_vendor = User.objects.filter(email='testuser124@example.com').first()
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
            'email': 'testuser123@example.com',
            'name': 'test Vendor',
            'password': 'testpass123',
            'vendor_data': {
                "contact_details": "test contact details",
                "address": "test address, street one, India",
                "vendor_code": "87654324"
            }
        }
        input_data = {
            "email": "testuser123@example.com",
            "password": 'testpass123'
        }

        # Create a vendor for testing.
        create_vendor_url = reverse("list-create-vendor")
        self.vendor = self.client.post(
            create_vendor_url,
            self.vendor_data,
            format='json'
        )
        # self.expected_data = Vendor.objects.create(**self.vendor_data)

        # generate access token
        access_token_url = reverse('obtain-token-pair')
        response = self.client.post(
            access_token_url,
            input_data,
            format='json'
        )
        self.access_token = response.json().get('access')
        self.refresh_token = response.json().get('refresh')

        self.url = reverse(
            'manage-vendor',
            kwargs={'id': self.vendor.json()['id']}
        )
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def test_vendor_retrieve(self):
        """
            Test GET request to retrieve a vendor
        """
        # send get request.
        response = self.client.get(self.url, headers=self.headers)

        # check status code
        self.assertEqual(response.status_code, 200)

        # compare response data with expected data.
        self.assertEqual(response.data, self.vendor.json())

    def test_vendor_update(self):
        """
            Test PUT request to update a vendor
        """
        updated_data = {
            'email': 'testuser123@example.com',
            'name': 'updated test Vendor',
            'password': 'updatedpass321',
            'vendor_data': {
                "contact_details": "edited contact details",
                "address": "test address, street one, India"
            }
        }
        response = self.client.patch(
            self.url,
            updated_data,
            headers=self.headers,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        updated_vendor = User.objects.get(id=self.vendor.json()['id'])
        self.assertEqual(updated_vendor.name, 'updated test Vendor')
        self.assertEqual(
            updated_vendor.vendor_data.contact_details,
            'edited contact details'
        )
        self.assertTrue(
            updated_vendor.check_password('updatedpass321')
        )

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
            'email': 'testuser123@example.com',
            'name': 'test Vendor',
            'password': 'testpass123',
            'vendor_data': {
                "contact_details": "test contact details",
                "address": "test address, street one, India",
                "vendor_code": "87654324"
            }
        }
        input_data = {
            "email": "testuser123@example.com",
            "password": 'testpass123'
        }

        # Create a vendor for testing.
        create_vendor_url = reverse("list-create-vendor")
        vendor_response = self.client.post(
            create_vendor_url,
            self.vendor_data,
            format='json'
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
