from rest_framework import serializers, pagination

from categories.models import Naics, SetAside, Pool, Zone
from vendors.models import Vendor, Manager, Location, SamLoad
from contracts.models import Contract, PlaceOfPerformance, FPDSLoad

import json


class OrderedSerializer(serializers.ModelSerializer):
    @classmethod
    def sort_field(cls, sort):
        if sort: 
            if isinstance(sort, str):
                sort = sort.split(',')
             
            if sort[0] in cls.Meta.fields:
                return sort
        
        return [cls.default_sort()]

    @classmethod
    def default_sort(cls):
        return cls.Meta.fields[0]
    
    @classmethod
    def sort_direction(cls):
        return 'desc'


class NaicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naics
        fields = ('code', 'root_code', 'description')


class SetAsideSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetAside
        fields = ('code', 'name', 'description')


class PoolSerializer(serializers.ModelSerializer):
    naics = NaicsSerializer(many=True)
    
    class Meta:
        model = Pool
        fields = ('id', 'name', 'number', 'vehicle', 'threshold', 'naics')


class ShortPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = ('id', 'name', 'number', 'vehicle')


class ZoneSerializer(serializers.ModelSerializer):
    states = serializers.SerializerMethodField('get_states')
    
    class Meta:
        model = Zone
        fields = ('id', 'states')
        
    def get_states(self, item):
        return item.states()


class LocationSerializer(serializers.ModelSerializer):
    citystate = serializers.SerializerMethodField('get_citystate')
    
    class Meta:
        model = Location
        fields = ('address', 'city', 'state', 'zipcode', 'congressional_district', 'citystate')
    
    def get_citystate(self, item):
        return "{}, {} {}".format(item.city, item.state, item.zipcode)


class ManagerSerializer(serializers.ModelSerializer):
    phones = serializers.SerializerMethodField('get_phones')
    emails = serializers.SerializerMethodField('get_emails')
    
    class Meta:
        model = Manager
        fields = ('name', 'phones', 'emails')
        
    def get_phones(self, item):
        return item.phones()
    
    def get_emails(self, item):
        return item.emails()


class VendorSerializer(OrderedSerializer):
    setasides = SetAsideSerializer(many=True)
    pools = PoolSerializer(many=True)
    sam_location = LocationSerializer(many=False)
    
    managers = ManagerSerializer(many=True)
    
    cms = serializers.SerializerMethodField('get_cms')
    pms = serializers.SerializerMethodField('get_pms')
    
    annual_revenue = serializers.SerializerMethodField('get_annual_revenue')
    number_of_employees = serializers.SerializerMethodField('get_number_of_employees')
    
    class Meta:
        model = Vendor
        fields = ('id', 'name', 'duns', 'duns_4', 'cage', 'sam_status', 
                  'sam_expiration_date', 'sam_activation_date', 'sam_exclusion', 
                  'sam_url', 'sam_location', 'cms', 'pms', 'pools', 'setasides', 
                  'annual_revenue', 'number_of_employees')
           
    def get_cms(self, item):
        try:
            return ManagerSerializer(item.managers.filter(type='CM')).data
            
        except Exception:
            return []
       
    def get_pms(self, item):
        try:
            return ManagerSerializer(item.managers.filter(type='PM')).data
            
        except Exception:
            return []   
    
    def get_annual_revenue(self, item):
        try:
            return Contract.objects.filter(vendor=item).latest('date_signed').annual_revenue
        
        except Exception:
            return 'NA'
    
    def get_number_of_employees(self, item):
        try:
            return Contract.objects.filter(vendor=item).latest('date_signed').number_of_employees
        
        except Exception:
            return 'NA'
    
    @classmethod
    def default_sort(cls):
        return 'name' 

    @classmethod
    def sort_direction(cls):
        return 'asc' 


class ShortVendorSerializer(OrderedSerializer):
    setasides = SetAsideSerializer(many=True)
    num_contracts = serializers.SerializerMethodField('get_vendor_contracts')
    sam_location = LocationSerializer(many=False)    

    class Meta:
        model = Vendor
        fields = ('id', 'name', 'duns', 'duns_4', 'sam_status', 'sam_exclusion', 'sam_url',
                  'sam_location', 'setasides', 'num_contracts')

    def get_vendor_contracts(self, item):
        if 'naics' in self.context and self.context['naics']:
            return Contract.objects.filter(NAICS=self.context['naics'].root_code, vendor=item).count()
        else:
            return Contract.objects.filter(vendor=item).count()
    
    @classmethod
    def default_sort(cls):
        return 'num_contracts' 


class PlaceOfPerformanceSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField('get_location')
    
    class Meta:
        model = PlaceOfPerformance
        fields = ('country_code', 'country_name', 'state', 'zipcode', 'location')
    
    def get_location(self, item):
        state = item.state if item.state else ''
        return "{} {}".format(item.country_name, state)


class ContractSerializer(OrderedSerializer):
    
    pricing_type = serializers.Field(source='get_pricing_type_display')
    piid = serializers.SerializerMethodField('split_piid')
    status = serializers.SerializerMethodField('get_status')
    
    vendor_location = LocationSerializer(many=False)
    place_of_performance = PlaceOfPerformanceSerializer(many=False)   
    
    class Meta:
        model = Contract
        fields = ('piid', 'agency_name', 'NAICS', 'date_signed', 'status', 'obligated_amount', 
                  'point_of_contact', 'pricing_type', 'vendor_location', 'place_of_performance',
                  'annual_revenue', 'number_of_employees')
        
    def split_piid(self, item):
        if '_' in item.piid:
            return item.piid.split('_')[1]
        return item.piid

    def get_status(self, item):
        return item.get_reason_for_modification_display()
    
    @classmethod
    def default_sort(cls):
        return 'date_signed' 


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
