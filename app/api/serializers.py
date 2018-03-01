from rest_framework.serializers import ModelSerializer, Field, IntegerField, SerializerMethodField

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


class ShortPoolSerializer(ModelSerializer):
    class Meta:
        model = categories.Pool
        fields = ['id', 'name', 'number', 'vehicle']

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


class PlaceOfPerformanceSerializer(ModelSerializer):
    location = SerializerMethodField()
    
    class Meta:
        model = contracts.PlaceOfPerformance
        fields = ('country_code', 'country_name', 'state', 'zipcode', 'location')
    
    def get_location(self, item):
        state = item.state if item.state else ''
        return "{} {}".format(item.country_name, state)


class ContractSerializer(ModelSerializer):
    
    pricing_type = Field(source='get_pricing_type_display')
    piid = SerializerMethodField()
    status = SerializerMethodField()
    
    vendor_location = LocationSerializer(many=False)
    place_of_performance = PlaceOfPerformanceSerializer(many=False)   
    
    class Meta:
        model = Contract
        fields = ('piid', 'agency_name', 'NAICS', 'date_signed', 'status', 'obligated_amount', 
                  'point_of_contact', 'pricing_type', 'vendor_location', 'place_of_performance',
                  'annual_revenue', 'number_of_employees')
        
    def get_piid(self, item):
        if '_' in item.piid:
            return item.piid.split('_')[1]
        return item.piid

    def get_status(self, item):
        return item.get_reason_for_modification_display()

'''
class Metadata(object):
    def __init__(self):
        sam_md = SamLoad.objects.all().order_by('-sam_load')
        fpds_md = FPDSLoad.objects.all().order_by('-load_date')
        if len(sam_md) > 0:
            self.sam_load_date = sam_md[0].sam_load
        else: 
            self.sam_load_date = None
        if len(fpds_md) > 0:
            self.fpds_load_date = fpds_md[0].load_date
        else:
            self.fpds_load_date = None


class MetadataSerializer(serializers.Serializer):
    sam_load_date = serializers.DateField()
    fpds_load_date = serializers.DateField()
'''