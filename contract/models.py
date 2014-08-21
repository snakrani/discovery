from django.db import models
from vendor.models import Naics

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

class FPDSContract(models.Model):
    
    piid = models.CharField(max_length=128)
    date_signed = models.DateField()
    completion_date = models.DateField(null=True)
    agency_id = models.IntegerField()
    agency_name = models.CharField(max_length=128)
    pricing_type = models.CharField(choices=PRICING_CHOICES, max_length=2, null=True)
    obligated_amount = models.DecimalField(max_digits=128, decimal_places=2, null=True)
    last_modified_by = models.EmailField(null=True)
    NAICS = models.ForeignKey(Naics, null=True)
    PSC = models.CharField(max_length=128, null=True)

