"""
    Models to manage vendor.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.db.models.signals import (
    post_save
)
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """
        Manager for users
    """

    def create_user(self, email, name, password=None, **extra_fields):
        """
            Create and return a normal user
        """

        if not email:
            raise ValueError('User must have an email address.')

        if not name:
            raise ValueError('User must have a Name.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_vendor(
        self,
        **extra_fields
    ):
        """
            Create, save and return a new vendor.
        """

        vendor_data = extra_fields.pop('vendor')
        vendor_data = dict(vendor_data)
        user = self.create_user(
            is_seller=True,
            **extra_fields
        )

        vendor = Vendor.objects.create(
            user=user,
            **vendor_data
        )

        user.__dict__['vendor'] = vendor.__dict__

        return user.__dict__

    def create_superuser(self, email, name, password=None):
        """
            Create and return new super user.
        """
        user = self.create_user(
            email,
            name,
            password,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
        Model to create vendor instance.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class Vendor(models.Model):
    """
        Model designed to handle vendor-specific
        fields enables the decoupling of vendors
        from normal users.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='vendor'
    )
    contact_details = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    vendor_code = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.user.name


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

    def __str__(self):
        return f"{self.vendor}'s performance data"


@receiver(post_save, sender=Vendor)
def create_performance_instance(sender, created, instance, **kwargs):
    """
        Create a new performance table instance for the
        created vendor.
    """
    if created:
        vendor = Vendor.objects.get(id=instance.id)
        VendorPerformance.objects.create(
            vendor=vendor
        )
