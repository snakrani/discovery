from django.db import models, IntegrityError
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
    
class FPDSContract(models.Model):
    
    piid = models.CharField(max_length=128, db_index=True)
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

    def save(self, *args, **kwargs):
        
        try:
            obj = FPDSContract.objects.get(piid=self.piid, agency_id=self.agency_id)
            #piid with that vendor already exists
            if obj.id == self.id:
                super(FPDSContract, self).save(*args, **kwargs)
            else:
                raise IntegrityError("FPDSContract already exists for that vendor and piid")
        except:
            super(FPDSContract, self).save(*args, **kwargs)
"""
class FAPIISRecord(models.Model):
    
    piid = models.CharField(max_length=128, db_index=True)
    agency_id = models.CharField(max_length=128, null=True)
    agency_name = models.CharField(max_length=128, null=True)
    NAICS = models.CharField(max_length=128, null=True)
    PSC = models.CharField(max_length=128, null=True)
    record_type = models.CharField(max_length=128, null=True)
    record_code = models.CharField(max_length=1, null=True)
    vendor = models.ForeignKey(Vendor, null=True)
"""

class Contract(models.Model):

    piid = models.CharField(max_length=128, db_index=True)
    agency_id = models.CharField(max_length=128, null=True)
    agency_name = models.CharField(max_length=128, null=True)
    NAICS = models.CharField(max_length=128, null=True) #should be foreign key, when we get all NAICS
    PSC = models.CharField(max_length=128, null=True)
    date_signed = models.DateTimeField(null=True)
    completion_date = models.DateTimeField(null=True)
    vendor = models.ForeignKey(Vendor)
    pricing_type = models.CharField(choices=PRICING_CHOICES, max_length=2, null=True)
    obligated_amount = models.DecimalField(max_digits=128, decimal_places=2, null=True)
    status = models.CharField(max_length=128, null=True)
    point_of_contact = models.EmailField(null=True)




