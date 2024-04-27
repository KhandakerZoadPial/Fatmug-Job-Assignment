from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from performance_app.models import VendorPerformance
from django.utils import timezone
from django.db.models import Avg
from django.db import models
from django.db.models import Q
from django.db.models import F





@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    if created or instance.status == 'completed' or instance.quality_rating or instance.acknowledgment_date:
        # Calculate performance metrics for the vendor of the purchase order
        vendor = instance.vendor

        
        if instance.status == 'completed':
            # On-Time Delivery Rate Calculation
            completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
            on_time_delivery_count = completed_orders.filter(
                Q(delivery_date__lte=models.F('delivery_date'))
            ).count()
            total_completed_orders = completed_orders.count()
            on_time_delivery_rate = on_time_delivery_count / total_completed_orders if total_completed_orders > 0 else 0

            # Quality Rating Average Calculation
            total_rating_sum = 0
            total_rated_po = 0
            for order in completed_orders:
                if order.quality_rating:
                    total_rating_sum += order.quality_rating
                    total_rated_po += 1
            quality_rating_avg = total_rating_sum / total_rated_po if total_rated_po > 0 else 0
        

        # Average Response Time Calculation
        completed_orders_with_acknowledge_date = completed_orders.exclude(issue_date__isnull=True).exclude(acknowledgment_date__isnull=True)
        response_times = completed_orders_with_acknowledge_date.annotate(response_time=F('acknowledgment_date') - F('issue_date')).values_list('response_time', flat=True)
        total_response_time = sum(response_times, timezone.timedelta())
        average_response_time = total_response_time / completed_orders.count() if completed_orders_with_acknowledge_date.count() > 0 else timezone.timedelta()


        # Fulfillment Rate Calculation
        total_completed_orders = completed_orders.count()
        successful_fulfillment_count = completed_orders.filter(status='completed').count()
        fulfillment_rate = successful_fulfillment_count / total_completed_orders if total_completed_orders > 0 else 0

        # Update or create VendorPerformance record
        VendorPerformance.objects.update_or_create(
            vendor=vendor,
            date=timezone.now(),
            defaults={
                'on_time_delivery_rate': on_time_delivery_rate,
                'quality_rating_avg': quality_rating_avg,
                'average_response_time': average_response_time.total_seconds() / 60 if average_response_time else 0,  # Converting to minutes
                'fulfillment_rate': fulfillment_rate
            }
        )
