"""
    Tests for models.
"""

from django.test import TestCase
from faker import Faker
from django.contrib.auth import get_user_model

from vendor.models import VendorPerformance


class ModelTest(TestCase):
    """
        Test models.
    """

    fake = Faker()

    def test_create_vendor(self):
        """
            Test creating a vendor and
            it's __str__ method.
        """
        email = 'test@example.com'
        name = 'test Vendor'
        contact_details = ('email:tetvendor@example.com')
        address = 'test address, street one, india'
        vendor_code = '87654324'
        password = 'testpass123'

        vendor = get_user_model().objects.create_vendor(
            email=email,
            name=name,
            contact_details=contact_details,
            address=address,
            vendor_code=vendor_code,
            password=password,
        )

        self.assertEqual(vendor.name, name)
        self.assertEqual(vendor.contact_details, contact_details)
        self.assertEqual(vendor.address, address)
        self.assertEqual(vendor.vendor_code, vendor_code)
        self.assertTrue(vendor.check_password(password))

        # Test vendor model's __str__ method.
        self.assertEqual(str(vendor), 'test Vendor')

    def test_new_vendor_email_normalized(self):
        """
            Test email normalized for new vendor.
        """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            random_vendor_code = self.fake.numerify(text='########')
            extra = {
                'contact_details': 'contactme',
                'address': 'test address, street one, india',
                'vendor_code': random_vendor_code,
            }
            user = get_user_model().objects.create_vendor(
                email,
                'name of vendor',
                'sample123',
                **extra,
            )
            self.assertEqual(user.email, expected)

    def test_new_vendor_without_email_raises_error(self):
        """
        Test that creating a vendor, without an email raises a valueError.
        """

        with self.assertRaises(ValueError):

            random_vendor_code = self.fake.numerify(text='########')
            extra = {
                'contact_details': 'contactme',
                'address': 'test address, street one, india',
                'vendor_code': random_vendor_code,
            }
            get_user_model().objects.create_vendor(
                '',
                'name of vendor',
                'sample123',
                **extra,
            )

    def test_create_superuser(self):
        """Test creating superuser."""
        user = get_user_model().objects.create_superuser(
            'testexample.com',
            'testname',
            'testpass123',
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class VendorPerformanceModelTest(TestCase):

    def setUp(self):

        self.vendor = get_user_model().objects.create_vendor(
            email='test@example.com',
            name='test Vendor',
            contact_details='email:tetvendor@example.com',
            address='test address, street one, india',
            vendor_code='87654324',
            password='testpass123'
        )

    def test_create_performance_sheet(self):
        """
            Test creating a vendor's  performance sheet
            and it's __str__ method.
        """
        on_time_delivery_rate = 95.0
        quality_rating_avg = 4.5
        average_response_time = 2.3
        fulfillment_rate = 98.0
        po_delivered = 10
        po_deli_on_time = 5

        perf_data = VendorPerformance.objects.create(
            vendor=self.vendor,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate,
            po_delivered=po_delivered ,
            po_deli_on_time=po_deli_on_time

        )

        self.assertEqual(
            perf_data.vendor,
            self.vendor
        )
        self.assertEqual(
            perf_data.on_time_delivery_rate,
            on_time_delivery_rate
        )
        self.assertEqual(
            perf_data.quality_rating_avg,
            quality_rating_avg
        )
        self.assertEqual(
            perf_data.average_response_time,
            average_response_time
        )
        self.assertEqual(
            perf_data.fulfillment_rate,
            fulfillment_rate
        )
        self.assertEqual(
            perf_data.po_delivered,
            po_delivered
        )
        self.assertEqual(
            perf_data.po_deli_on_time,
            po_deli_on_time
        )

        # Test VendorPerformance model's __str__ method.
        self.assertEqual(str(perf_data), "test Vendor's performance data")
