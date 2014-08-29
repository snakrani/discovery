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
    duns = models.CharField(max_length=9, unique=True)
    duns_4 = models.CharField(max_length=13, unique=True)
    sam_address = models.CharField(null=True, max_length=128)
    sam_citystate = models.CharField(null=True, max_length=128)
    cm_name = models.CharField(null=True, max_length=128)
    cm_email = models.CharField(null=True, max_length=128)
    cm_phone = models.CharField(null=True, max_length=128)
    pm_name = models.CharField(null=True, max_length=128)
    pm_email = models.CharField(null=True, max_length=128)
    pm_phone = models.CharField(null=True, max_length=128)
    pools = models.ManyToManyField('Pool', through='PoolPIID')
    setasides = models.ManyToManyField('SetAside', null=True)
    sam_status = models.CharField(null=True, max_length=128)
    sam_exclusion = models.NullBooleanField(null=True)
    sam_url = models.URLField(null=True)
    annual_revenue = models.CharField(null=True, max_length=128)
    number_of_employees = models.IntegerField(null=True)


    def __str__(self):
        return self.name


class Pool(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    number = models.CharField(max_length=128)
    vehicle = models.CharField(choices=VEHICLE_CHOICES, max_length=7)
    naics = models.ManyToManyField('Naics')
    threshold = models.CharField(null=True, max_length=128)

    def __str__(self):
        return "Pool {0} - {1}".format(self.number, self.get_vehicle_display())


class PoolPIID(models.Model):
    vendor = models.ForeignKey('Vendor')
    pool = models.ForeignKey('Pool')
    piid = models.CharField(max_length=128)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.vendor.name, self.pool.id, self.piid)


class SetAside(models.Model):
    code = models.CharField(unique=True, max_length=128)
    description = models.TextField()
    short_name = models.CharField(max_length=128)

    def  __str__(self):
        return self.description


class Naics(models.Model):
    code = models.CharField(max_length=128)
    description = models.TextField()
    short_code = models.CharField(unique=True, max_length=25)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.description)


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


class SamLoad(models.Model):
    sam_load = models.DateTimeField()
