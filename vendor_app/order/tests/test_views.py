"""
    Unit test for views.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from order.models import PurchaseOrder

from order.serializers import PurchaseOrderSerializer

import json


class PurchaseOrderListCreateViewTest(TestCase):
    """
        Unit test for PurchaseOrderListCreateView.
    """

    def setUp(self):
        """
            Setup data for testing.
        """
        self.client = APIClient()

        # Create vendor instance.
        self.vendor_data = {
            'email': 'testuser123@example.com',
            'name': 'test Vendor',
            'password': 'testpass1234',
            'vendor_data': {
                "contact_details": "test contact details",
                "address": "test address, street one, India",
                "vendor_code": "87654324"
            }
        }

        create_vendor_url = reverse("list-create-vendor")
        response = self.client.post(
            create_vendor_url,
            self.vendor_data,
            format='json'
        )
        id = response.json()['id']
        self.vendor = get_user_model().objects.get(id=id)

        # Generate access token
        input_data = {
            "email": "testuser123@example.com",
            "password": 'testpass1234'
        }
        access_token_url = reverse('obtain-token-pair')
        response = self.client.post(access_token_url, input_data)
        self.access_token = response.json().get('access')

        # Configure url with token.
        self.client = APIClient()
        self.url = reverse('list-create-purchase-order')
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

        self.purchase_order_data = {
            "po_number": "test-123-po",
            "items": {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            "quantity": 5,
            "vendor": self.vendor
        }
        self.purchase_order = PurchaseOrder.objects.create(
            **self.purchase_order_data
        )

    def test_listing_purchase_orders(self):
        """
            Test GET request for listing purchase orders.
        """

        response = self.client.get(self.url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        # Validate response data
        expected_response = PurchaseOrderSerializer(
            instance=self.purchase_order
        ).data
        self.assertEqual(response.data[0], expected_response)

    def test_creating_purchase_order(self):
        """
            Test POST request to create a new vendor
        """

        new_po_data = json.dumps({
            "po_number": "test-124-po",
            "items": {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            "quantity": 5,
            "vendor": 1
        })
        response = self.client.post(
            self.url,
            new_po_data,
            headers=self.headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        # Check if the new purchase order is created in the database
        new_po = PurchaseOrder.objects.filter(po_number='test-124-po').first()
        self.assertIsNotNone(new_po)


class ManagePurchaseOrderViewTest(TestCase):
    """
        Unit test for ManagePurchaseOrderView.
    """

    def setUp(self):
        """
            Setup data for testing.
        """

        # Set up client
        self.client = APIClient()

        # Create a vendor for testing.
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
        # Create vendor instance.
        create_vendor_url = reverse("list-create-vendor")
        response = self.client.post(
            create_vendor_url,
            self.vendor_data,
            format='json'
        )
        self.vendor = get_user_model().objects.get(id=1)

        # Create purchase order instance
        self.purchase_order_data = {
            "po_number": "test-123-po",
            "items": {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            "quantity": 5,
            "vendor": self.vendor
        }
        self.purchase_order = PurchaseOrder.objects.create(
            **self.purchase_order_data
        )

        # Generate expected data
        self.expected_data = PurchaseOrderSerializer(
            instance=self.purchase_order
        ).data

        # Generate access token
        access_token_url = reverse('obtain-token-pair')
        response = self.client.post(access_token_url, input_data)
        self.accesstoken = response.json().get('access')

        # Configure url with token.
        self.client = APIClient()
        self.url = reverse('manage-purchase-order', kwargs={'id': 1})
        self.headers = {'Authorization': f'Bearer {self.accesstoken}'}

    def test_GET_purchase_order(self):
        """
            Test GET request to retrieve a purchase order with id.
        """
        # Send get request.
        response = self.client.get(self.url, headers=self.headers)

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Compare expected data with response
        self.assertEqual(response.data, self.expected_data)

    def test_purchase_order_update(self):
        """
            Test PUT request.
        """
        updated_data = json.dumps({
            "po_number": "testedit-123",
            "items": {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string",
            },
            "quantity": 5,
            "vendor": 1
        })
        response = self.client.put(
            self.url,
            updated_data,
            headers=self.headers,
            content_type="application/json"
        )
        id = response.json()["id"]
        updated_po = PurchaseOrder.objects.get(id=id)

        self.assertEqual(updated_po.po_number, 'testedit-123')

    def test_purchase_order_delete(self):
        """
            Test DELETE request.
        """
        response = self.client.delete(self.url, headers=self.headers)
        self.assertEqual(response.status_code, 204)
        deleted_po = PurchaseOrder.objects.filter(
            id=self.expected_data['id']
        ).first()
        self.assertIsNone(deleted_po)


class AcknowledgePOViewTest(TestCase):
    """
        Unit test for AcknowledgePOView.
    """
    def setUp(self):

        self.client = APIClient()

        # Create vendor instance.
        self.vendor_data = {
            'email': 'testuser123@example.com',
            'name': 'test Vendor',
            'password': 'testpass1234',
            'vendor_data': {
                "contact_details": "test contact details",
                "address": "test address, street one, India",
                "vendor_code": "87654324"
            }
        }

        create_vendor_url = reverse("list-create-vendor")
        response = self.client.post(
            create_vendor_url,
            self.vendor_data,
            format='json'
        )
        self.vendor = get_user_model().objects.get(id=1)

        # Generate access token
        input_data = {
            "email": "testuser123@example.com",
            "password": 'testpass1234'
        }
        access_token_url = reverse('obtain-token-pair')
        response = self.client.post(
            access_token_url,
            input_data,
            format='json'
        )
        self.access_token = response.json().get('access')
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

        po_data = json.dumps({
            "po_number": "test-124-po",
            "items": {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            "quantity": 5,
            "vendor": 1
        })
        po_url = reverse('list-create-purchase-order')
        response = self.client.post(
            po_url,
            po_data,
            headers=self.headers,
            content_type='application/json'
        )
        self.po_id = response.json()["id"]

        # Configure url and url params with headers.
        self.url = reverse('acknowledge-po', kwargs={'id': self.po_id})

    def test_acknowledgement(self):
        # Send a PATCH request to acknowledge the Purchase Order
        ackn_resp = self.client.patch(
            self.url,
            {},
            headers=self.headers,
            format='json'
        )
        self.assertEqual(ackn_resp.status_code, 200)
        self.assertEqual(ackn_resp.json(), "Acknowledged Successfully")

        # Try to acknowledge again
        second_resp = self.client.patch(
            self.url,
            {},
            headers=self.headers,
            format='json'
        )
        self.assertEqual(second_resp.json(), "Already acknowledged.")


class MarkCompletedViewTest(TestCase):
    """
        Unit test for AcknowledgePOView.
    """
    def setUp(self):

        self.client = APIClient()

        # Create vendor instance.
        self.vendor_data = {
            'email': 'testuser123@example.com',
            'name': 'test Vendor',
            'password': 'testpass1234',
            'vendor_data': {
                "contact_details": "test contact details",
                "address": "test address, street one, India",
                "vendor_code": "87654324"
            }
        }

        create_vendor_url = reverse("list-create-vendor")
        response = self.client.post(
            create_vendor_url,
            self.vendor_data,
            format='json'
        )
        self.vendor = get_user_model().objects.get(id=1)

        # Generate access token
        input_data = {
            "email": "testuser123@example.com",
            "password": 'testpass1234'
        }
        access_token_url = reverse('obtain-token-pair')
        response = self.client.post(access_token_url, input_data)
        self.access_token = response.json().get('access')
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

        # Purchase order one
        po_data = json.dumps({
            "po_number": "test-124-po",
            "items": {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            "quantity": 5,
            "vendor": 1
        })
        po_url = reverse('list-create-purchase-order')
        res = self.client.post(
            po_url,
            po_data,
            headers=self.headers,
            content_type='application/json'
        )
        self.po_id = res.json()["id"]

        ack_url = reverse('acknowledge-po', kwargs={'id': self.po_id})

        self.client.patch(
            ack_url,
            {},
            headers=self.headers,
            format='json'
        )

        # Purchase Order two.
        po_2_data = json.dumps({
            "po_number": "test-125-po",
            "items": {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            "quantity": 7,
            "vendor": 1
        })
        po_2_url = reverse('list-create-purchase-order')
        res = self.client.post(
            po_2_url,
            po_2_data,
            headers=self.headers,
            content_type='application/json'
        )
        self.po_2_id = res.json()["id"]

        ack_url = reverse('acknowledge-po', kwargs={'id': self.po_2_id})

        self.client.patch(
            ack_url,
            {},
            headers=self.headers,
            format='json'
        )

        # Configure url and url params with headers.
        self.url = reverse(
            'mark-completed',
            kwargs={'id': self.po_id}
        )

        self.second_url = reverse(
            'mark-completed',
            kwargs={'id': self.po_2_id}
        )

    def test_put_method(self):
        """
            Test view functioning.
        """
        response = self.client.put(
            self.url,
            {
                "quality_rating": 8
            },
            headers=self.headers,
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            "Purchase order marked as "
            "completed with quality rating."
        )

        # Test repeated request.
        response = self.client.put(
            self.url,
            {
                "quality_rating": 8
            },
            headers=self.headers,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            "Already updated."
        )

        # Test without payload.
        response = self.client.put(
            self.second_url,
            {},
            headers=self.headers,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            "Purchase order marked as "
            "completed without quality rating."
        )

        # Test request with invalid data fails.
        response = self.client.put(
            self.second_url,
            {
                "quality_rating": 15
            },
            headers=self.headers,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            "Data validation failed."
        )
