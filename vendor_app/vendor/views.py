"""
    Views to manage vendor related functionalities.
"""

from .serializers import (
    VendorSerializer,
    GenerateTokenSerializer,
    VendorPerformanceSerializer
)
from .models import (
    User,
    VendorPerformance
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView
)
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class ListCreateVendorView(ListCreateAPIView):
    """
        List All vendors with GET method.
        Create a new vendor using POST method.
        Ensure that the vendor_code field does not
        commence with the keyword "superuser".

        Use application/json mode to test creating
        vendor from swagger UI

        Use request method PATCH for partial updating,
        Exclude the vendor_code field unless we want to
        edit (Unique constraint of the field will lead
        to error).
    """
    serializer_class = VendorSerializer
    queryset = User.objects.filter(
        is_seller=True
    ).prefetch_related('vendor_data')


class ManageVendorView(RetrieveUpdateDestroyAPIView):
    """
        manage vendor by id.
        fetch, update and delete a single vendor instance.
    """

    serializer_class = VendorSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class GenerateTokenView(APIView):
    """
    View to generate tokens.
    """
    serializer_class = GenerateTokenSerializer

    @extend_schema(request=GenerateTokenSerializer, responses=None)
    def post(self, request, *args, **kwargs):
        serializer = GenerateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        refresh = RefreshToken.for_user(data)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )


class VendorPerformanceStatsView(RetrieveAPIView):
    """
        View to get statistical data of a
        Vendor's performance.

        Give vendor's user id as input (path params)
        to get performance data.
    """

    serializer_class = VendorPerformanceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = VendorPerformance.objects.all()
    lookup_field = 'vendor'
