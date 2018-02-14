from django.db import models, IntegrityError

from categories.models import Naics
from vendors.models import Location, Vendor


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

REASON_FOR_MODIFICATION_CHOICES = (
    ('A', 'Additional Work'),
    ('B', 'Supplemental Agreement for work within scope'),
    ('C', 'Funding Only Action'),
    ('D', 'Change Order'),
    ('E', 'Terminated for Default'),
    ('F', 'Terminated for Convenience'),
    ('G', 'Exercise an Option'),
    ('H', 'Definitize Letter Contract'),
    ('J', 'Novation Agreement'),
    ('K', 'Close out'),
    ('L', 'Definitize Letter Contract'),
    ('M', 'Other Adminitrative Action'),
    ('N', 'Legal Contract Cancellation'),
    ('P', 'Representation of non-Novated Merger/Acquisitoin'),
    ('R', 'Rerepresentation'),
    ('S', 'Change PIID'),
    ('T', 'Transfer Action'),
    ('V', 'Vendor DUNS Change'),
    ('W', 'Vendor Address Change'),
    ('X', 'Terminated for Cause'),
    ('C1', 'Completed'),
    ('C2', 'Current'),
)


class FPDSLoad(models.Model):
    vendor = models.OneToOneField(Vendor, null=True)
    load_date = models.DateField()


class PlaceOfPerformance(models.Model):
    country_code = models.CharField(max_length=50, null=True)
    country_name = models.CharField(max_length=128, null=True)
    
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=10, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.country_code, self.country_name)


class Contract(models.Model):
    piid = models.CharField(max_length=128, db_index=True)
    date_signed = models.DateTimeField(null=True)
    completion_date = models.DateTimeField(null=True)
    
    NAICS = models.CharField(max_length=128, null=True) #should be foreign key, when we get all NAICS
    PSC = models.CharField(max_length=128, null=True)   
    
    agency_id = models.CharField(max_length=128, null=True)
    agency_name = models.CharField(max_length=128, null=True)
    
    vendor = models.ForeignKey(Vendor)
    point_of_contact = models.EmailField(null=True)
    
    pricing_type = models.CharField(choices=PRICING_CHOICES, max_length=2, null=True)
    obligated_amount = models.DecimalField(max_digits=128, decimal_places=2, null=True)
    
    reason_for_modification = models.CharField(choices=REASON_FOR_MODIFICATION_CHOICES, max_length=2, null=True)
    
    annual_revenue = models.BigIntegerField(null=True)
    number_of_employees = models.IntegerField(null=True)
    
    vendor_phone = models.CharField(null=True, max_length=128)
    vendor_location = models.ForeignKey(Location, null=True)
    
    place_of_performance = models.ForeignKey(PlaceOfPerformance, null=True)

    def save(self, *args, **kwargs):    
        try:
            obj = Contract.objects.get(piid=self.piid, agency_id=self.agency_id)
            #piid with that vendor already exists
            if obj.id == self.id:
                super(Contract, self).save(*args, **kwargs)
            else:
                raise IntegrityError("Contract already exists for that vendor and piid")
        except:
            super(Contract, self).save(*args, **kwargs)
