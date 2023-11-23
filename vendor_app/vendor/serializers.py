"""
    Serializers to manage vendors.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model


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
