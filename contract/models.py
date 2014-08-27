from django.db import models
from vendor.models import Naics, Vendor

PRICING_CHOICES = (
    ('A', 'Fixed Price Redetermination'),
    ('B', 'Fixed Price Level of Effort'),
    ('J', 'Firm Fixed Price'),
    ('K', 'Fixed Price with Economic Price Adjustment'),
    ('L', 'Fixed Price Incentive'),
    ('M', 'Fixed Price Award Fee'),
    ('R', 'Cost Plus Award Fee'),
    ('S', 'Cost No Fee'),
    ('T', 'Cost Sharing'),
    ('U', 'Cost Plus Fixed Fee'),
    ('V', 'Cost Plus Incentive Fee'),
    ('Y', 'Time and Materials'),
    ('Z', 'Labor Hours'),
    ('1', 'Order Dependent'),
    ('2', 'Combination'),
    ('3', 'Other'),
)

TERMINATION_CHOICES = (
    ('C', 'Termination for Default'),
    ('P', 'Termination for Cause'),

)

class FPDSContract(models.Model):
    
    piid = models.CharField(max_length=128, unique=True)
    date_signed = models.DateTimeField(null=True)
    completion_date = models.DateTimeField(null=True)
    vendor = models.ForeignKey(Vendor)
    agency_id = models.CharField(max_length=128, null=True)
    agency_name = models.CharField(max_length=128, null=True)
    pricing_type = models.CharField(choices=PRICING_CHOICES, max_length=2, null=True)
    obligated_amount = models.DecimalField(max_digits=128, decimal_places=2, null=True)
    last_modified_by = models.EmailField(null=True)
    NAICS = models.CharField(max_length=128, null=True)
    PSC = models.CharField(max_length=128, null=True)


class FAPIISRecord(models.Model):
    
    piid = models.CharField(max_length=128, db_index=True)
    agency_id = models.CharField(max_length=128, null=True)
    agency_name = models.CharField(max_length=128, null=True)
    NAICS = models.CharField(max_length=128, null=True)
    PSC = models.CharField(max_length=128, null=True)
    record_type = models.CharField(choices=TERMINATION_CHOICES, max_length=2, null=True)

