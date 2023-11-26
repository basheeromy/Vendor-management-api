"""
    Test cases for serilizers.
"""

from django.test import TestCase

from order.serializers import PurchaseOrderSerializer
from order.models import PurchaseOrder
from vendor.models import Vendor


class PurchaseOrderSerializerTestCase(TestCase):
    """
        Unit test for PurchaseOrderSerializer.
    """

    def setUp(self):

        self.vendor = Vendor.objects.create(
            email='testuser13@example.com',
            name='test Vendor1',
            contact_details='email:tetvendor@example.com',
            address='test address, street one, India',
            vendor_code='87654325',
            password='testpass123'
        )
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
            "vendor": 1
        }

    def test_purchase_order_serilizer(self):
        """
            Check validation and serialization.
        """
        serializer = PurchaseOrderSerializer(data=self.purchase_order_data)
        self.assertTrue(serializer.is_valid())

        # Check all fields
        serialized_data = serializer.data
        self.assertEqual(
            serialized_data['po_number'],
            'test-123-po'
        )
        self.assertEqual(
            serialized_data['delivery_date'],
            '2023-11-26T19:04:23.379000Z'
        )
        self.assertEqual(
            serialized_data['items'],
            {
                "testProp1": "test_string",
                "testProp2": "test_string",
                "testProp3": "test_string"
            }
        )
        self.assertEqual(
            serialized_data['quantity'],
            5
        )
        self.assertEqual(
            serialized_data['status'],
            'pending'
        )
        self.assertEqual(
            serialized_data['quality_rating'],
            8.5
        )
        self.assertEqual(
            serialized_data['issue_date'],
            '2023-11-26T19:04:23.379000Z'
        )
        self.assertEqual(
            serialized_data['acknowledgment_date'],
            '2023-11-26T19:04:23.379000Z'
        )
        self.assertEqual(
            serialized_data['vendor'],
            1
        )

        # test with invalid data
        invalid_data = self.purchase_order_data.copy()
        invalid_data['quantity'] = -1
        sserializer = PurchaseOrderSerializer(data=invalid_data)
        self.assertFalse(sserializer.is_valid())

    def test_PO_serializer_create_update_methods(self):
        """
            Test create method in Purchase
            Order Serializer.
        """
        self.purchase_order_data['vendor'] = self.vendor
        serializer = PurchaseOrderSerializer()

        # Check create method.
        po_instance = serializer.create(self.purchase_order_data)
        self.assertIsInstance(po_instance, PurchaseOrder)

        # Check update method.
        self.purchase_order_data['po_number'] = 'updated_po123'
        updated_instance = serializer.update(
            po_instance,
            self.purchase_order_data
        )
        self.assertEqual(
            updated_instance.po_number,
            'updated_po123'
        )