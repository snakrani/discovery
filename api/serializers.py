from rest_framework import serializers
from vendor.models import Vendor, Pool, Naics

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('name', 'duns', 'duns_4', 'sam_address', 'sam_citystate', 'pools', 'setasides', 'sam_status', 'sam_exclusion', 'sam_url')
