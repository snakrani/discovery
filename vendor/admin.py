from django.contrib import admin
from vendor.models import Naics, Pool, Vendor, SetAside

admin.site.register(Naics)
admin.site.register(Vendor)
admin.site.register(Pool)
admin.site.register(SetAside)
# Register your models here.
