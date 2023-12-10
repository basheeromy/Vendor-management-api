"""
    Models to manage vendor.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from faker import Faker
from django.contrib.auth import get_user_model

from django.db.models.signals import (
    post_save
)
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """
        Manager for users
    """

    def create_vendor(
        self,
        email,
        name,
        password=None,
        **extra_fields
    ):
        """
            Create, save and return a new vendor.
        """

        if not email:
            raise ValueError('Vendor must have an email address.')

        if not name:
            raise ValueError('Vendor must have a Name.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        """
            Create and return new super user.
        """

        fake = Faker()
        random_vendor_code = fake.numerify(text='########')
        random_vendor_code = 'superuser'+random_vendor_code
        user = self.create_vendor(
            email,
            name,
            password,
            vendor_code=random_vendor_code,
            is_staff=True,
            is_superuser=True,
            is_seller=False,
            is_active=True,

        )
        user.save(using=self._db)
        return user


class Vendor(AbstractBaseUser, PermissionsMixin):
    """
        Model to create vendor instance.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=150)
    contact_details = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    vendor_code = models.CharField(max_length=50, unique=True, blank=True)
    is_seller = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class VendorPerformance(models.Model):
    """
        Model designed to oversee and record statistical
        data encompassing the performance indexes of vendors.
    """
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)
    po_deli_on_time = models.IntegerField(default=0)
    res_time_total = models.IntegerField(default=0)
    res_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.vendor}'s performance data"


@receiver(post_save, sender=Vendor)
def create_performance_instance(sender, created, instance, **kwargs):
    """
        Create a new performance table instance for the
        created vendor.
    """
    if created:
        vendor = get_user_model().objects.get(id=instance.id)
        VendorPerformance.objects.create(
            vendor=vendor
        )
