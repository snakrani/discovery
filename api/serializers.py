from rest_framework import serializers
from vendor.models import Vendor, Pool, Naics, SetAside

class SetAsideSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetAside
        fields = ('code', 'description')

class NaicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naics
        fields = ('code', 'description', 'short_code')


class PoolSerializer(serializers.ModelSerializer):
    naics = NaicsSerializer(many=True)

    class Meta:
        model = Pool
        fields = ('id', 'number', 'vehicle', 'naics', 'threshold')

class VendorSerializer(serializers.ModelSerializer):
    setasides = SetAsideSerializer(many=True)
    pools = PoolSerializer(many=True)

    class Meta:
        model = Vendor
        fields = ('name', 'duns', 'duns_4', 'sam_address', 'sam_citystate', 'pools', 'setasides', 'sam_status', 'sam_exclusion', 'sam_url')

    

