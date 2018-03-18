from rest_framework.fields import CharField, IntegerField, DateField
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts


class NaicsSerializer(ModelSerializer):
    class Meta:
        model = categories.Naics
        fields = ['code', 'root_code', 'description']


class SetAsideSerializer(ModelSerializer):
    class Meta:
        model = categories.SetAside
        fields = ['code', 'name', 'description', 'far_order']


class PoolSerializer(ModelSerializer):
    naics = NaicsSerializer(many=True)
    
    class Meta:
        model = categories.Pool
        fields = ['id', 'name', 'number', 'vehicle', 'threshold', 'naics']


class ZoneSerializer(ModelSerializer):
    states = SerializerMethodField()
    
    class Meta:
        model = categories.Zone
        fields = ['id', 'states']
        
    def get_states(self, item):
        return item.states()


class LocationSerializer(ModelSerializer):
    class Meta:
        model = vendors.Location
        fields = ['address', 'city', 'state', 'zipcode', 'congressional_district']


class ContractManagerSerializer(ModelSerializer):
    class Meta:
        model = vendors.ContractManager
        fields = ['name', 'phones', 'emails']

class ProjectManagerSerializer(ModelSerializer):
    class Meta:
        model = vendors.ProjectManager
        fields = ['name', 'phones', 'emails']


class PoolMembershipSerializer(ModelSerializer):
    pool = PoolSerializer(many=False)
    setasides = SetAsideSerializer(many=True)
    
    zones = ZoneSerializer(many=True)
    
    cms = ContractManagerSerializer(many=True)
    pms = ProjectManagerSerializer(many=True)
    
    class Meta:
        model = vendors.PoolMembership
        fields = ['piid', 'pool', 'setasides', 'zones', 'cms', 'pms']


class VendorSerializer(ModelSerializer):
    sam_location = LocationSerializer(many=False)
    sam_location_citystate = CharField()
    
    pools = PoolMembershipSerializer(many=True)
    
    annual_revenue = IntegerField()
    number_of_employees = IntegerField()
    number_of_contracts = IntegerField()
    
    class Meta:
        model = vendors.Vendor
        fields = ['name', 'duns', 'duns_4', 'cage', 
                  'sam_status', 'sam_expiration_date', 'sam_activation_date', 'sam_exclusion', 
                  'sam_url', 'sam_location', 'sam_location_citystate', 
                  'pools', 'annual_revenue', 'number_of_employees', 'number_of_contracts']


class CoreVendorSerializer(ModelSerializer):
    sam_location = LocationSerializer(many=False)
     
    class Meta:
        model = vendors.Vendor
        fields = ['name', 'duns', 'duns_4', 'cage',
                  'sam_status', 'sam_exclusion', 'sam_url',
                  'sam_location']


class ContractStatusSerializer(ModelSerializer):
    class Meta:
        model = contracts.ContractStatus
        fields = ['code', 'name']


class PricingStructureSerializer(ModelSerializer):
    class Meta:
        model = contracts.PricingStructure
        fields = ['code', 'name']


class PlaceOfPerformanceSerializer(ModelSerializer):
    class Meta:
        model = contracts.PlaceOfPerformance
        fields = ['country_code', 'country_name', 'state', 'zipcode']


class ContractSerializer(ModelSerializer):
    vendor = CoreVendorSerializer(many=False)
    
    place_of_performance = PlaceOfPerformanceSerializer(many=False)
    vendor_location = LocationSerializer(many=False)
    
    status = ContractStatusSerializer(many=False)
    pricing_type = PricingStructureSerializer(many=False)
        
    place_of_performance_location = CharField()
        
    class Meta:
        model = contracts.Contract
        fields = ['id', 'piid', 'agency_id', 'agency_name', 'NAICS', 'PSC', 
                  'date_signed', 'completion_date', 'pricing_type', 'obligated_amount', 'status', 
                  'point_of_contact', 'place_of_performance', 'place_of_performance_location', 'vendor_location', 
                  'vendor_phone', 'vendor',
                  'annual_revenue', 'number_of_employees']


class MetadataSerializer(Serializer):
    sam_load_date = DateField()
    fpds_load_date = DateField()
