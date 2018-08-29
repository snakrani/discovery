from django.db import models


VEHICLE_CHOICES = (
    ('OASIS_SB', 'OASIS Small Business'),
    ('OASIS', 'OASIS Unrestricted'),
    ('HCATS_SB', 'HCATS Small Business'),
    ('HCATS', 'HCATS Unrestricted'),
    ('BMO_SB', 'BMO Small Business'),
    ('BMO', 'BMO Unrestricted'),
    ('PSS', 'Professional Services Schedule')
)


class Keyword(models.Model):
    name = models.CharField(max_length=1000, null=True)
    
    def __str__(self):
        return "{0} ({1})".format(self.name, self.id)


class SIN(models.Model):
    code = models.CharField(primary_key=True, max_length=25)
    keywords = models.ManyToManyField(Keyword, blank=True)
    
    def __str__(self):
        return "{0}".format(self.code)


class Naics(models.Model):
    code = models.CharField(primary_key=True, max_length=25)
    description = models.TextField()
    sin = models.ManyToManyField(SIN, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    
    def __str__(self):
        return "{0} - {1}".format(self.code, self.description)


class PSC(models.Model):
    code = models.CharField(primary_key=True, max_length=25)
    description = models.TextField()
    naics = models.ManyToManyField(Naics)
    sin = models.ManyToManyField(SIN, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
     
    def __str__(self):
        return "{0} - {1}".format(self.code, self.description)


class SetAside(models.Model):
    code = models.CharField(unique=True, max_length=25)
    name = models.CharField(unique=True, max_length=25, null=True)
    description = models.CharField(max_length=128)
    far_order = models.IntegerField(null=True)

    def  __str__(self):
        return self.name


class Vehicle(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128)
    small_business = models.NullBooleanField(null=True)
    numeric_pool = models.NullBooleanField(null=True)
    display_number = models.NullBooleanField(null=True)

    def __str__(self):
        return "{0} {1}".format(self.id, self.name)

class Pool(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128, default='Pool')
    number = models.CharField(max_length=128)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.CASCADE)
    naics = models.ManyToManyField(Naics)
    threshold = models.CharField(null=True, max_length=128)

    def __str__(self):
        return "{0} {1}".format(self.name, self.number)


class State(models.Model):
    code = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return "{0}".format(self.code)

class Zone(models.Model):
    states = models.ManyToManyField(State, blank=True)

    def __str__(self):
        return "Zone {0}".format(self.id)

