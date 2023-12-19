# """
#     Unit tests for Purchase order model.
# """
# from django.test import TestCase
# from django.utils import timezone
# from django.core.exceptions import ValidationError

# from order.models import PurchaseOrder
# from vendor.models import (
#     Vendor
# )

# import json


# class PurchaseOrderModelTest(TestCase):

#     def setUp(self):
#         """
#             configure requirements for test.
#         """

#         self.vendor = Vendor.objects.create(
#             email='testuser123@example.com',
#             name='test Vendor1',
#             contact_details='email:tetvendor@example.com',
#             address='test address, street one, India',
#             vendor_code='87654324',
#             password='testpass123'
#         )
#         test_data = {
#             "item1": {
#                 "product_id": "pr1",
#                 "quantity": 20,
#             },
#             "item2": {
#                 "product_id": "pr2",
#                 "quantity": 10,
#             }
#         }
#         self.json_data = json.dumps(test_data)

#     def test_create_purchase_order(self):
#         """
#             Unit test for creation of database
#             instances with PurchaseOrder model.
#         """

#         po_number = "po-n123"
#         vendor = self.vendor
#         # use time zone to avoid warning about time zone
#         now = timezone.now()
#         order_date = now
#         delivery_date = order_date + timezone.timedelta(days=10)
#         items = self.json_data
#         quantity = 30

#         purchase_order = PurchaseOrder.objects.create(
#             po_number=po_number,
#             vendor=vendor,
#             delivery_date=delivery_date,
#             items=items,
#             quantity=quantity,
#             quality_rating=8.5,
#             acknowledgment_date=now
#         )
#         self.assertEqual(purchase_order.po_number, po_number)
#         self.assertEqual(purchase_order.vendor, vendor)
#         # check auto now add functionality of order_date.
#         self.assertAlmostEqual(
#             purchase_order.order_date.timestamp(),
#             order_date.timestamp(),
#             delta=1  # Tolerance in seconds for time comparison
#         )
#         self.assertAlmostEqual(
#             purchase_order.delivery_date.timestamp(),
#             delivery_date.timestamp(),
#             delta=1
#         )
#         self.assertEqual(purchase_order.items, items)
#         self.assertEqual(purchase_order.quantity, quantity)
#         """
#             check default status
#             get_status_display() function will return the
#             corresponding Value instead of key.
#         """
#         self.assertEqual(
#             purchase_order.get_status_display(),
#             'Pending'
#         )
#         # assign new value to status field.
#         purchase_order.status = 'out-to-deliver'
#         purchase_order.save()
#         self.assertEqual(
#             purchase_order.get_status_display(),
#             'Out-to-deliver'
#         )

#         # Test the str representation of model instance.
#         self.assertEqual(
#             str(purchase_order),
#             'PO: po-n123 Vendor: test Vendor1'
#         )

#         # Check Validators. (Min and Max)

#         # Test quantity validator
#         with self.assertRaises(ValidationError):
#             # Create an instance with a negative quantity
#             purchase_order.quantity = -2
#             purchase_order.full_clean()

#         # Test quality rating validator with negative value.
#         with self.assertRaises(ValidationError):
#             # Create an instance with a negative rating
#             purchase_order.quality_rating = -2
#             purchase_order.full_clean()

#         # Test quality rating validator with value > 10.
#         with self.assertRaises(ValidationError):
#             # Create an instance with a positive rating
#             purchase_order.quality_rating = 10.1
#             purchase_order.full_clean()
