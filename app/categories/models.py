from django.db import models


class SIN(models.Model):
    code = models.CharField(primary_key=True, max_length=25)
    
    def __str__(self):
        return "{0}".format(self.code)


class Naics(models.Model):
    code = models.CharField(primary_key=True, max_length=25)
    description = models.TextField()
    sin = models.ManyToManyField(SIN, blank=True)
    
    def __str__(self):
        return "{0} - {1}".format(self.code, self.description)


class PSC(models.Model):
    code = models.CharField(primary_key=True, max_length=25)
    description = models.TextField()
    sin = models.ManyToManyField(SIN, blank=True)
     
    def __str__(self):
        return "{0} - {1}".format(self.code, self.description)


class Keyword(models.Model):
    name = models.CharField(max_length=1000, null=True)
    parent = models.ForeignKey("Keyword", null=True, on_delete=models.CASCADE, db_index=True)
    calc = models.CharField(max_length=1000, null=True, db_index=True)

    sin = models.ForeignKey(SIN, null=True, on_delete=models.CASCADE, db_index=True)
    naics = models.ForeignKey(Naics, null=True, on_delete=models.CASCADE, db_index=True)
    psc = models.ForeignKey(PSC, null=True, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.id)


class SetAside(models.Model):
    code = models.CharField(unique=True, max_length=25)
    name = models.CharField(unique=True, max_length=25, null=True, db_index=True)
    description = models.CharField(max_length=128)
    far_order = models.IntegerField(null=True, db_index=True)

    def  __str__(self):
        return self.name


class Tier(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
  

class Vehicle(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128, db_index=True)
    tier = models.ForeignKey(Tier, null=True, on_delete=models.CASCADE, db_index=True)
    poc = models.CharField(max_length=256, null=True)
    ordering_guide = models.CharField(max_length=256, null=True)
    small_business = models.NullBooleanField(null=True)
    numeric_pool = models.NullBooleanField(null=True)
    display_number = models.NullBooleanField(null=True)

    def __str__(self):
        return "{0} {1}".format(self.id, self.name)

class Pool(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128, default='Pool', db_index=True)
    number = models.CharField(max_length=128, db_index=True)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.CASCADE, db_index=True)
    threshold = models.CharField(null=True, max_length=128)
    naics = models.ManyToManyField(Naics)
    psc = models.ManyToManyField(PSC)
    keywords = models.ManyToManyField(Keyword, blank=True)
    
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

