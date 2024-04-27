from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer

# authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_orders(request, po_id=None):
    if request.method == 'GET':
        if po_id is not None:
            # Retrieve details of a specific purchase order
            try:
                purchase_order = PurchaseOrder.objects.get(pk=po_id)
                serializer = PurchaseOrderSerializer(purchase_order)
                return Response(serializer.data)
            except PurchaseOrder.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # List all purchase orders with an option to filter by vendor
            vendor_id = request.query_params.get('vendor')
            if vendor_id:
                purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
            else:
                purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        # Create a purchase order
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # Update a purchase order
        if po_id is not None:
            try:
                purchase_order = PurchaseOrder.objects.get(pk=po_id)
                serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except PurchaseOrder.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete a purchase order
        if po_id is not None:
            try:
                purchase_order = PurchaseOrder.objects.get(pk=po_id)
                purchase_order.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except PurchaseOrder.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
