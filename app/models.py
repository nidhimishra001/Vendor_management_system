from django.db import models
from django.db.models import JSONField
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=200)
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)        


    def calculate_performance_metrics(self):
        completed_pos = self.purchase_orders.filter(status='completed')
        
        on_time_delivery_count = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        total_completed_pos = completed_pos.count()
        self.on_time_delivery_rate = (on_time_delivery_count / total_completed_pos) * 100 if total_completed_pos > 0 else 0
        
        quality_ratings = completed_pos.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        self.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0
        
        response_times = completed_pos.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=models.ExpressionWrapper(models.F('acknowledgment_date') - models.F('issue_date'), output_field=models.DurationField())
        ).values_list('response_time', flat=True)
        self.average_response_time = sum(response_times, timezone.timedelta()) / len(response_times) if response_times else timezone.timedelta()
        
        fulfilled_pos = completed_pos.exclude(issue_date__isnull=True)
        successful_fulfillments = fulfilled_pos.count()
        self.fulfillment_rate = (successful_fulfillments / total_completed_pos) * 100 if total_completed_pos > 0 else 0
        
        self.save()
        

class PurchaseOrder(models.Model):
    PO_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=PO_STATUS_CHOICES)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.status == 'completed' and self.delivery_date and not self.pk:
            self.vendor.calculate_performance_metrics()
        super().save(*args, **kwargs)



class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()