"""
    Tests for models.
"""

from django.test import TestCase
from faker import Faker
from django.contrib.auth import get_user_model


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
        password = 'testpass123'
        vendor_data = {
            "contact_details": "contact me here",
            "address": "test address, street one, india",
            "vendor_code": "87654324"
        }

        vendor = get_user_model().objects.create_vendor(
            email=email,
            name=name,
            password=password,
            vendor_data=vendor_data
        )

        self.assertEqual(vendor.name, name)
        self.assertEqual(vendor.email, email)
        self.assertTrue(vendor.check_password(password))

        # Test vendor profile data. use vendor.vendor to access vendor data
        self.assertEqual(
            vendor.vendor_data.contact_details,
            vendor_data['contact_details']
        )
        self.assertEqual(
            vendor.vendor_data.address,
            vendor_data['address']
        )
        self.assertEqual(
            vendor.vendor_data.vendor_code,
            vendor_data['vendor_code']
        )

        # Test vendor model's __str__ method.

        self.assertEqual(str(vendor), vendor.name)

        # Test vendor's vendor profile model's __str__ method.
        self.assertEqual(str(vendor.vendor_data), f"{vendor.name}'s profile")

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
            vendor_data = {
                'contact_details': 'contact me',
                'address': 'test address, street one, india',
                'vendor_code': random_vendor_code,
            }
            user = get_user_model().objects.create_vendor(
                email=email,
                name='name of vendor',
                password='testpass123',
                vendor_data=vendor_data,
            )
            self.assertEqual(user.email, expected)

    def test_new_vendor_without_email_raises_error(self):
        """
        Test that creating a vendor, without an email raises a valueError.
        """

        with self.assertRaises(ValueError):

            random_vendor_code = self.fake.numerify(text='########')
            vendor_data = {
                'contact_details': 'contact me',
                'address': 'test address, street one, india',
                'vendor_code': random_vendor_code,
            }
            get_user_model().objects.create_vendor(
                email='',
                name='name of vendor',
                password='sample123',
                vendor_data=vendor_data,
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
