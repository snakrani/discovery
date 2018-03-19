from django.db import models

from categories.models import SetAside, Pool, Zone


class SamLoad(models.Model):
    sam_load = models.DateField()


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
    
    def __str__(self):
        return self.name


class PoolMembership(models.Model):
    piid = models.CharField(max_length=128) # from CSV
    
    vendor = models.ForeignKey(Vendor, related_name='pools', on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.DO_NOTHING)
        
    setasides = models.ManyToManyField(SetAside, blank=True) # from CSV
    zones = models.ManyToManyField(Zone, blank=True) # from CSV
    
    def __str__(self):
        return "{0} - {1}/{2} ({3})".format(self.vendor.name, self.pool.id, self.zone, self.piid)


class Manager(models.Model):
    name = models.CharField(null=True, max_length=128)
    
    def __str__(self):
        return "{0}".format(self.name)
    
    def phone(self):
        return self.phones.values_list('number', flat=True)
    
    def email(self):
        return self.emails.values_list('address', flat=True)
    

class ContractManager(Manager):
    responsibility = models.ForeignKey(PoolMembership, null=True, related_name='cms', on_delete=models.DO_NOTHING)


class ProjectManager(Manager):
    responsibility = models.ForeignKey(PoolMembership, null=True, related_name='pms', on_delete=models.DO_NOTHING)


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
