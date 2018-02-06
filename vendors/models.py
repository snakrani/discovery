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


class SamLoad(models.Model):
    sam_load = models.DateField()


class Naics(models.Model):
    code = models.CharField(max_length=128)
    description = models.TextField()
    short_code = models.CharField(unique=True, max_length=25)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.description)


class SetAside(models.Model):
    code = models.CharField(unique=True, max_length=128)
    short_name = models.CharField(max_length=128)
    abbreviation = models.CharField(max_length=10, null=True)
    far_order = models.IntegerField(null=True)

    def  __str__(self):
        return self.short_name


class Pool(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128, default='Pool')
    number = models.CharField(max_length=128)
    vehicle = models.CharField(choices=VEHICLE_CHOICES, max_length=7)
    naics = models.ManyToManyField(Naics)
    threshold = models.CharField(null=True, max_length=128)

    def __str__(self):
        return "Pool {0} - {1}".format(self.number, self.get_vehicle_display())


class Location(models.Model):
    address = models.CharField(max_length=128)
    
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    
    congressional_district = models.CharField(null=True, max_length=50)
    
    def __str__(self):
        return "{}, {}".format(self.address, self.citystate)


class Vendor(models.Model):
    name = models.CharField(max_length=128)
    duns = models.CharField(max_length=9, unique=True)
    duns_4 = models.CharField(max_length=13, unique=True)
    cage = models.CharField(max_length=15, null=True)
    
    cm_name = models.CharField(null=True, max_length=128)
    cm_email = models.CharField(null=True, max_length=128)
    cm_phone = models.CharField(null=True, max_length=128)
    
    pm_name = models.CharField(null=True, max_length=128)
    pm_email = models.CharField(null=True, max_length=128)
    pm_phone = models.CharField(null=True, max_length=128)
  
    sam_status = models.CharField(null=True, max_length=128)
    sam_activation_date = models.DateTimeField(null=True)
    sam_expiration_date = models.DateTimeField(null=True)
    sam_exclusion = models.NullBooleanField(null=True)
    
    sam_location = models.ForeignKey(Location, null=True)
    sam_url = models.URLField(null=True)
    
    pools = models.ManyToManyField(Pool, through='PoolPIID')
    setasides = models.ManyToManyField(SetAside, blank=True)
  
    def __str__(self):
        return self.name


class PoolPIID(models.Model):
    vendor = models.ForeignKey(Vendor)
    pool = models.ForeignKey(Pool)
    piid = models.CharField(max_length=128)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.vendor.name, self.pool.id, self.piid)
