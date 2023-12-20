"""
    Test cases for serilizers.
"""

from django.test import TestCase

from order.serializers import PurchaseOrderSerializer
from order.models import PurchaseOrder
from django.contrib.auth import get_user_model


class PurchaseOrderSerializerTestCase(TestCase):
    """
        Unit test for PurchaseOrderSerializer.
    """

    def setUp(self):

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
            "acknowledgment_date": "2023-11-26T19:04:23.379000Z",
            "vendor": self.vendor.id
        }

    def test_purchase_order_serializer(self):
        """
            Check validation and serialization.
        """
        serializer = PurchaseOrderSerializer(data=self.purchase_order_data)

        self.assertTrue(serializer.is_valid())

        # Check fields
        serialized_data = serializer.validated_data
        self.assertEqual(
            serialized_data['po_number'],
            'test-123-po'
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
            serialized_data['vendor'],
            self.vendor
        )

        # Check read only field excluded in creation.(writing.)
        self.assertNotIn('status', serializer.validated_data)
        self.assertNotIn('delivery_date', serializer.validated_data)
        self.assertNotIn('quality_rating', serializer.validated_data)
        self.assertNotIn('acknowledgment_date', serializer.validated_data)
        self.assertNotIn('order_date', serializer.validated_data)
        self.assertNotIn('date_delivered', serializer.validated_data)

        # test with invalid data
        invalid_data = self.purchase_order_data.copy()
        invalid_data['quantity'] = -1
        serializer = PurchaseOrderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

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
