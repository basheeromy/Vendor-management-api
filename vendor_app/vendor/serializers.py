"""
    Serializers to manage vendors.
"""
from drf_writable_nested.serializers import WritableNestedModelSerializer

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import VendorPerformance
from .models import (Vendor)


class VendorProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for Vendor model which
        stores additional data of users
        registered as vendors.
    """

    class Meta:
        model = Vendor
        fields = [
            'id',
            'user',
            'contact_details',
            'address',
            'vendor_code'
        ]
        extra_kwargs = {
            'user': {
                'read_only': True
            },
        }


class VendorSerializer(WritableNestedModelSerializer):
    """
        Manage operations related to creation and updation
        of new vendor profile.

        As we are using nested serializer, default .update()
        method does not support writable nested fields.
        So, here we are using a serializer available in drf-writable-nested
        package.

        Use request method PATCH for partial updating, Exclude the vendor_code
        field unless we want to edit (Unique constraint of the field will lead
        to error).

        Key for nested vendor data is "vendor".

        {
            "id": 0,
            "email": "user@example.com",
            "name": "string",
            "vendor": {
            "id": 0,
            "user": 0,
            "contact_details": "string",
            "address": "string",
            "vendor_code": "string"
            }
        }

    """
    vendor = VendorProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'name',
            'password',
            'vendor'

        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            },
        }

    def create(self, validated_data):
        """
            Create and return a vendor with encrypted password.
        """

        return get_user_model().objects.create_vendor(**validated_data)

    def update(self, instance, validated_data):
        """
            Handle updating vendor.
        """

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class GenerateTokenSerializer(serializers.Serializer):
    """
    Serializer to take input for generating token.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data['email']
        password = data['password']
        if not email:
            raise serializers.ValidationError("Email is required.")
        elif not password:
            raise serializers.ValidationError("Password is required.")

        vendor = get_user_model().objects.filter(email__iexact=email)

        if not vendor.exists():
            raise serializers.ValidationError(
                "Vendor does not exist! Please register."
            )

        vendor = vendor.first()
        if vendor.check_password(password) is False:
            raise serializers.ValidationError("Incorrect Password.")

        return vendor


class VendorPerformanceSerializer(serializers.ModelSerializer):
    """
        Serializer to provide statistics related
        fields from vendor model
    """
    class Meta:
        model = VendorPerformance
        fields = '__all__'
        extra_kwargs = {
            'po_delivered': {
                'write_only': True
            },
            'po_deli_on_time': {
                'write_only': True
            },
            'res_time_total': {
                'write_only': True
            },
            'res_count': {
                'write_only': True
            },
            'no_po_issued': {
                'write_only': True
            },
        }
