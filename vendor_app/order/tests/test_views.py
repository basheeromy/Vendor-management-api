"""
    Unit test for views.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from order.models import PurchaseOrder
from vendor.models import Vendor

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
        self.vendor = Vendor.objects.create(
            email='testuser13@example.com',
            name='test Vendor1',
            contact_details='email:tetvendor@example.com',
            address='test address, street one, India',
            vendor_code='87654325',
            password='testpass123'
        )
        self.client = APIClient()
        self.url = reverse('list-create-purchase-order')
        self.purchase_order_data = {
            "po_number": "test-123-po",
            "delivery_date": "2023-11-26T19:04:23.379000Z",
            "items": {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            "quantity": 5,
            "status": "pending",
            "quality_rating": 8.5,
            "issue_date": "2023-11-26T19:04:23.379000Z",
            "acknowledgment_date": "2023-11-26T19:04:23.379000Z",
            "vendor": self.vendor
        }
        self.purchase_order = PurchaseOrder.objects.create(
            **self.purchase_order_data
        )

    def test_listing_purchase_orders(self):
        """
            Test GET request for listing purchase orders.
        """

        response = self.client.get(self.url)
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
            "delivery_date": "2023-11-26T19:04:23.379000Z",
            "items": {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            },
            "quantity": 5,
            "status": "pending",
            "quality_rating": 8.5,
            "issue_date": "2023-11-26T19:04:23.379000Z",
            "acknowledgment_date": "2023-11-26T19:04:23.379000Z",
            "vendor": 1
        })
        response = self.client.post(
            self.url,
            new_po_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        # Check if the new purchase order is created in the database
        new_po = PurchaseOrder.objects.filter(po_number='test-124-po').first()
        self.assertIsNotNone(new_po)
