from django.db import models

VEHICLE_CHOICES = (
    ('OASISSB', 'OASIS Small Business'),
    ('OASIS', 'OASIS Unrestricted')
)

STATUS_CHOICES = (
    ('P', 'In Progress'),
    ('C', 'Completed'), 
    ('F', 'Cancelled') 
)


class Vendor(models.Model):

    name = models.CharField(max_length=128)
    duns = models.IntegerField()
    duns_4 = models.IntegerField()
    oasis_address = models.CharField(null=True, max_length=128)
    oasis_citystate = models.CharField(null=True, max_length=128)
    cm_name = models.CharField(null=True, max_length=128)
    cm_email = models.CharField(null=True, max_length=128)
    cm_phone = models.CharField(null=True, max_length=128)
    pm_name = models.CharField(null=True, max_length=128)
    pm_email = models.CharField(null=True, max_length=128)
    pm_phone = models.CharField(null=True, max_length=128)
    pools = models.ManyToManyField('Pool', through='PoolPIID')
    setasides = models.ManyToManyField('SetAside', null=True)
    

class Pool(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    number = models.CharField(max_length=128)
    vehicle = models.CharField(choices=VEHICLE_CHOICES, max_length=7)
    naics = models.CharField(max_length=128)
    naics_description = models.TextField()
    threshold = models.CharField(null=True, max_length=128)

class PoolPIID(models.Model):
    vendor = models.ForeignKey('Vendor')
    pool = models.ForeignKey('Pool')
    piid = models.CharField(max_length=128)

class SetAside(models.Model):
    code = models.CharField(unique=True, max_length=128)
    description = models.TextField()
    short_name = models.CharField(max_length=128)

class ContractRecord(models.Model):
    piid = models.CharField(unique=True, max_length=128)
    vendor = models.ForeignKey('Vendor')
    status = models.CharField(choices=STATUS_CHOICES, max_length=3)
    date_signed = models.DateField()
    date_completed = models.DateField(null=True)
    obligated_amount = models.DecimalField(decimal_places=2, max_digits=15, null=True)
    description = models.TextField(null=True)
    naics = models.CharField(null=True, max_length=25)
    psc = models.CharField(null=True, max_length=25)
    fpds_email = models.EmailField(null=True)
    fapiis_email = models.EmailField(null=True)
    fapiis_name = models.CharField(null=True, max_length=128)
    vehicle = models.CharField(choices=VEHICLE_CHOICES, max_length=7, null=True)

