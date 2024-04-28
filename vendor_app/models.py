from django.db import models

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=20)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=10, unique=True)
