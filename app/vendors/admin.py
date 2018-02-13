from django.contrib import admin

from vendors.models import Location, Manager, Vendor, PoolPIID


admin.site.register(Vendor)
admin.site.register(Manager)
admin.site.register(Location)
admin.site.register(PoolPIID)
