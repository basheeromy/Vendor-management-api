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
