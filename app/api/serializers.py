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
        fields = ['code', 'name', 'description']


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
    citystate = SerializerMethodField()
    
    class Meta:
        model = vendors.Location
        fields = ['address', 'city', 'state', 'zipcode', 'congressional_district', 'citystate']
    
    def get_citystate(self, item):
        return "{}, {} {}".format(item.city, item.state, item.zipcode)


class ManagerSerializer(ModelSerializer):
    phones = SerializerMethodField()
    emails = SerializerMethodField()
    
    class Meta:
        model = vendors.Manager
        fields = ['name', 'phones', 'emails']
        
    def get_phones(self, item):
        return item.phones()
    
    def get_emails(self, item):
        return item.emails()


class VendorSerializer(ModelSerializer):
    sam_location = LocationSerializer(many=False)
    setasides = SetAsideSerializer(many=True)
    pools = PoolSerializer(many=True)
    
    annual_revenue = IntegerField()
    number_of_employees = IntegerField()
    number_of_contracts = IntegerField()
    
    cms = SerializerMethodField()
    pms = SerializerMethodField()
    
    class Meta:
        model = vendors.Vendor
        fields = ['id', 'name', 'duns', 'duns_4', 'cage', 'sam_status', 
                  'sam_expiration_date', 'sam_activation_date', 'sam_exclusion', 
                  'sam_url', 'sam_location', 'cms', 'pms', 'pools', 'setasides', 
                  'annual_revenue', 'number_of_employees', 'number_of_contracts']
           
    def get_cms(self, item):
        return ManagerSerializer(item.managers.filter(type='CM'), many=True).data
       
    def get_pms(self, item):
        return ManagerSerializer(item.managers.filter(type='PM'), many=True).data


class ShortVendorSerializer(ModelSerializer):
    sam_location = LocationSerializer(many=False)
    setasides = SetAsideSerializer(many=True)
        
    annual_revenue = IntegerField()
    number_of_employees = IntegerField()
    number_of_contracts = IntegerField()
    
    class Meta:
        model = vendors.Vendor
        fields = ['id', 'name', 'duns', 'duns_4', 'sam_status', 'sam_exclusion', 'sam_url',
                  'sam_location', 'setasides', 'annual_revenue', 'number_of_employees', 'number_of_contracts']


class CoreVendorSerializer(ModelSerializer):
    sam_location = LocationSerializer(many=False)
    setasides = SetAsideSerializer(many=True)
     
    class Meta:
        model = vendors.Vendor
        fields = ['id', 'name', 'duns', 'duns_4', 
                  'sam_status', 'sam_exclusion', 'sam_url',
                  'sam_location', 'setasides']


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


class ShortContractSerializer(ModelSerializer):
    status = ContractStatusSerializer(many=False)
    pricing_type = PricingStructureSerializer(many=False)
    
    place_of_performance_location = CharField()
        
    class Meta:
        model = contracts.Contract
        fields = ['id', 'piid', 'agency_id', 'agency_name', 'NAICS', 'PSC', 
                  'date_signed', 'completion_date', 'pricing_type', 'obligated_amount', 'status', 
                  'point_of_contact', 'place_of_performance_location']


class MetadataSerializer(Serializer):
    sam_load_date = DateField()
    fpds_load_date = DateField()
