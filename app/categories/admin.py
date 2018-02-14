from django.contrib import admin

from categories.models import Naics, Pool, SetAside, Zone


admin.site.register(Naics)
admin.site.register(Pool)
admin.site.register(SetAside)
admin.site.register(Zone)
