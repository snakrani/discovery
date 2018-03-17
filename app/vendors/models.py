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
    vendor = models.ForeignKey(Vendor, related_name='pools', on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.DO_NOTHING)
    piid = models.CharField(max_length=128) # from CSV
    
    setasides = models.ManyToManyField(SetAside, blank=True) # from CSV
    
    def __str__(self):
        return "{0} - {1}/{2} ({3})".format(self.vendor.name, self.pool.id, self.zone, self.piid)


class PoolMembershipZone(models.Model):
    membership = models.ForeignKey(PoolMembership, null=True, related_name='zone', on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{0}".format(self.zone)


class Manager(models.Model):
    name = models.CharField(null=True, max_length=128)
    
    def __str__(self):
        return "{0}".format(self.name)
    
    def phones(self):
        return self.phone.values_list('number', flat=True)
    
    def emails(self):
        return self.email.values_list('address', flat=True)
    

class ContractManager(Manager):
    responsibility = models.ForeignKey(PoolMembership, null=True, related_name='cms', on_delete=models.DO_NOTHING)


class ProjectManager(Manager):
    responsibility = models.ForeignKey(PoolMembership, null=True, related_name='pms', on_delete=models.DO_NOTHING)


class ManagerPhoneNumber(models.Model):
    manager = models.ForeignKey(Manager, null=True, related_name='phone', on_delete=models.CASCADE)
    number = models.CharField(null=True, max_length=128)

    def __str__(self):
        return "{0} ({1})".format(self.manager.name, self.number)


class ManagerEmail(models.Model):
    manager = models.ForeignKey(Manager, null=True, related_name='email', on_delete=models.CASCADE)
    address = models.CharField(null=True, max_length=128)

    def __str__(self):
        return "{0} ({1})".format(self.manager.name, self.address)
