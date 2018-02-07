from django.db import models

VEHICLE_CHOICES = (
    ('OASIS_SB', 'OASIS Small Business'),
    ('OASIS', 'OASIS Unrestricted'),
    ('HCATS_SB', 'HCATS Small Business'),
    ('HCATS', 'HCATS Unrestricted')
)

STATUS_CHOICES = (
    ('P', 'In Progress'),
    ('C', 'Completed'), 
    ('F', 'Cancelled') 
)

MANAGEMENT_TYPES = (
    ('CM', 'Contract Manager'),
    ('PM', 'Project Manager')
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
    vehicle = models.CharField(choices=VEHICLE_CHOICES, max_length=20)
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
        return "{}, {}, {} {}".format(self.address, self.city, self.state, self.zipcode)


class Vendor(models.Model):
    name = models.CharField(max_length=128)
    duns = models.CharField(max_length=9, unique=True)
    duns_4 = models.CharField(max_length=13, unique=True)
    cage = models.CharField(max_length=15, null=True)

    sam_status = models.CharField(null=True, max_length=128)
    sam_activation_date = models.DateTimeField(null=True)
    sam_expiration_date = models.DateTimeField(null=True)
    sam_exclusion = models.NullBooleanField(null=True)
    
    sam_url = models.URLField(null=True)
    sam_location = models.ForeignKey(Location, null=True)
  
    pools = models.ManyToManyField(Pool, through='PoolPIID')
    setasides = models.ManyToManyField(SetAside, blank=True)
  
    def __str__(self):
        return self.name


class Manager(models.Model):
    vendor = models.ForeignKey(Vendor, null=True, related_name='managers')
    name = models.CharField(null=True, max_length=128)
    type = models.CharField(choices=MANAGEMENT_TYPES, max_length=10)
    
    def phone(self):
        return self.phones.values_list('number', flat=True)
    
    def email(self):
        return self.emails.values_list('address', flat=True)

    def __str__(self):
        info = "{0} {1}".format(self.vendor.name, self.pool.id, self.piid)
        return "{0} ({1} / {2})".format(info, ", ".join(self.phone()), ", ".join(self.email()))


class ManagerPhoneNumber(models.Model):
    manager = models.ForeignKey(Manager, null=True, related_name='phones')
    number = models.CharField(null=True, max_length=128)

    def __str__(self):
        return "{0} ({1})".format(self.manager.name, self.number)


class ManagerEmail(models.Model):
    manager = models.ForeignKey(Manager, null=True, related_name='emails')
    address = models.CharField(null=True, max_length=128)

    def __str__(self):
        return "{0} ({1})".format(self.manager.name, self.address)
    

class PoolPIID(models.Model):
    vendor = models.ForeignKey(Vendor)
    pool = models.ForeignKey(Pool)
    piid = models.CharField(max_length=128)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.vendor.name, self.pool.id, self.piid)
