from django.shortcuts import render
from .models import Vendor

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import VendorSerializer

# authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendors(request, vendor_id=None):
    if request.method == 'GET':
        if vendor_id is not None:
            # Retrieve a specific vendor's details
            try:
                vendor = Vendor.objects.get(pk=vendor_id)
                serializer = VendorSerializer(vendor)
                return Response(serializer.data)
            except Vendor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # List all vendors
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        # Create a new vendor
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        # Update a vendor's details
        if vendor_id is not None:
            try:
                vendor = Vendor.objects.get(pk=vendor_id)
                serializer = VendorSerializer(vendor, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Vendor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Delete a vendor
        if vendor_id is not None:
            try:
                vendor = Vendor.objects.get(pk=vendor_id)
                vendor.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Vendor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)