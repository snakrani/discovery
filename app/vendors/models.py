from django.db import models

from categories.models import SetAside, Pool, Zone


class Location(models.Model):
    address = models.CharField(max_length=128)
    
    city = models.CharField(max_length=128, db_index=True)
    state = models.CharField(max_length=50, db_index=True)
    zipcode = models.CharField(max_length=10, db_index=True)
    
    congressional_district = models.CharField(null=True, max_length=50, db_index=True)
    
    def __str__(self):
        return "{}, {}, {} {}".format(self.address, self.city, self.state, self.zipcode)


class Vendor(models.Model):
    name = models.CharField(max_length=128, db_index=True) # from XLS
    duns = models.CharField(max_length=9, unique=True, db_index=True) # from XLS
    duns_4 = models.CharField(max_length=13, unique=True, db_index=True) # generated from XLS
    cage = models.CharField(max_length=15, null=True, db_index=True) #from SAM

    sam_status = models.CharField(null=True, max_length=128, db_index=True) # from SAM
    sam_activation_date = models.DateTimeField(null=True, db_index=True) # from SAM
    sam_expiration_date = models.DateTimeField(null=True, db_index=True) # from SAM
    sam_exclusion = models.NullBooleanField(null=True, db_index=True) # from SAM
    
    sam_url = models.URLField(null=True) # from SAM
    sam_location = models.ForeignKey(Location, null=True, on_delete=models.CASCADE) # from SAM
    
    def __str__(self):
        return self.name


class PoolMembership(models.Model):
    piid = models.CharField(max_length=128) # from XLS
    
    vendor = models.ForeignKey(Vendor, related_name='pools', on_delete=models.CASCADE, db_index=True)
    pool = models.ForeignKey(Pool, on_delete=models.DO_NOTHING, db_index=True)
        
    setasides = models.ManyToManyField(SetAside, blank=True) # from XLS
    zones = models.ManyToManyField(Zone, blank=True) # from XLS
    
    expiration_8a_date = models.DateField(null=True, db_index=True) # from XLS
    contract_end_date = models.DateField(null=True, db_index=True) # from XLS
    
    def __str__(self):
        return "{} {} ({})".format(self.pool.id, self.vendor.name, self.piid)


class Contact(models.Model):
    responsibility = models.ForeignKey(PoolMembership, null=True, related_name='contacts', on_delete=models.DO_NOTHING)
    order = models.IntegerField(null=False, default=1, db_index=True)
    name = models.CharField(null=True, max_length=128, db_index=True)
    
    def __str__(self):
        return "{}".format(self.name)
    

class ContactPhone(models.Model):
    contact = models.ForeignKey(Contact, null=True, related_name='phones', on_delete=models.CASCADE)
    number = models.CharField(null=True, max_length=128, db_index=True)

    def __str__(self):
        return "{0} ({1})".format(self.contact.name, self.number)


class ContactEmail(models.Model):
    contact = models.ForeignKey(Contact, null=True, related_name='emails', on_delete=models.CASCADE)
    address = models.CharField(null=True, max_length=128, db_index=True)

    def __str__(self):
        return "{0} ({1})".format(self.contact.name, self.address)


class SamLoad(models.Model):
    vendor = models.OneToOneField(Vendor, unique=True, null=True, on_delete=models.CASCADE)
    load_time = models.DateTimeField(null=True, db_index=True)
