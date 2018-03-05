from django.db import models, IntegrityError

from categories.models import Naics
from vendors.models import Location, Vendor


class FPDSLoad(models.Model):
    vendor = models.OneToOneField(Vendor, null=True, on_delete=models.CASCADE)
    load_date = models.DateField()


class ContractStatus(models.Model):
    code = models.CharField(max_length=5, null=False, primary_key=True)
    name = models.CharField(max_length=128, null=False)


class PricingStructure(models.Model):
    code = models.CharField(max_length=5, null=False, primary_key=True)
    name = models.CharField(max_length=128, null=False)


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
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    point_of_contact = models.EmailField(null=True)
    
    pricing_type = models.ForeignKey(PricingStructure, null=True, on_delete=models.DO_NOTHING)
    obligated_amount = models.DecimalField(max_digits=128, decimal_places=2, null=True)
    
    status = models.ForeignKey(ContractStatus, null=True, on_delete=models.DO_NOTHING)
    
    annual_revenue = models.BigIntegerField(null=True)
    number_of_employees = models.IntegerField(null=True)
    
    vendor_phone = models.CharField(null=True, max_length=128)
    vendor_location = models.ForeignKey(Location, null=True, on_delete=models.DO_NOTHING)
    
    place_of_performance = models.ForeignKey(PlaceOfPerformance, null=True, on_delete=models.DO_NOTHING)

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
