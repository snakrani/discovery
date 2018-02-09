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
    code = models.CharField(unique=True, max_length=25)
    root_code = models.CharField(max_length=25, null=True)
    description = models.TextField()
    
    def __str__(self):
        return "{0} - {1}".format(self.code, self.description)


class SetAside(models.Model):
    code = models.CharField(unique=True, max_length=25)
    name = models.CharField(unique=True, max_length=25, null=True)
    description = models.CharField(max_length=128)
    far_order = models.IntegerField(null=True)

    def  __str__(self):
        return self.name


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
    name = models.CharField(max_length=128) # from CSV
    duns = models.CharField(max_length=9, unique=True) # from CSV
    duns_4 = models.CharField(max_length=13, unique=True) # generated from CSV
    cage = models.CharField(max_length=15, null=True) #from SAM

    sam_status = models.CharField(null=True, max_length=128) # from SAM
    sam_activation_date = models.DateTimeField(null=True) # from SAM
    sam_expiration_date = models.DateTimeField(null=True) # from SAM
    sam_exclusion = models.NullBooleanField(null=True) # from SAM
    
    sam_url = models.URLField(null=True) # from SAM
    sam_location = models.ForeignKey(Location, null=True, on_delete=models.CASCADE) # from SAM
  
    pools = models.ManyToManyField(Pool, through='PoolPIID') # from CSV
    setasides = models.ManyToManyField(SetAside, blank=True) # from CSV
  
    def __str__(self):
        return self.name


class Manager(models.Model):
    vendor = models.ForeignKey(Vendor, null=True, related_name='managers', on_delete=models.CASCADE)
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
    manager = models.ForeignKey(Manager, null=True, related_name='phones', on_delete=models.CASCADE)
    number = models.CharField(null=True, max_length=128)

    def __str__(self):
        return "{0} ({1})".format(self.manager.name, self.number)


class ManagerEmail(models.Model):
    manager = models.ForeignKey(Manager, null=True, related_name='emails', on_delete=models.CASCADE)
    address = models.CharField(null=True, max_length=128)

    def __str__(self):
        return "{0} ({1})".format(self.manager.name, self.address)
    

class PoolPIID(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    piid = models.CharField(max_length=128)
    zone = models.CharField(max_length=128, null=True)

    def __str__(self):
        return "{0} - {1}/{2} ({3})".format(self.vendor.name, self.pool.id, self.zone, self.piid)
