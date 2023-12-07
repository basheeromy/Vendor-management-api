"""
    Serializers to manage vendors.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VendorPerformance


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'name',
            'contact_details',
            'address',
            'vendor_code',
            'password'

        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
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
