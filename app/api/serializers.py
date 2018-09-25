from rest_framework.fields import CharField, IntegerField, DateField, ListField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import Serializer, ModelSerializer, HyperlinkedModelSerializer, SerializerMethodField

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts

import os


class KeywordSerializer(ModelSerializer):
    class Meta:
        model = categories.Keyword
        fields = ['id', 'name']
   
class KeywordTestSerializer(ModelSerializer):
    class Meta:
        model = categories.Keyword
        fields = ['id', 'name']


class SinSerializer(ModelSerializer):
    class Meta:
        model = categories.SIN
        fields = ['code']
        
    def to_representation(self, instance):
        return instance.code
    
class SinTestSerializer(ModelSerializer):
    class Meta:
        model = categories.SIN
        fields = ['code']


class BaseNaicsSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="naics-detail", lookup_field='code')
    
    class Meta:
        model = categories.Naics
        fields = ['code', 'description']

class NaicsLinkSerializer(BaseNaicsSerializer):
    class Meta(BaseNaicsSerializer.Meta):
        fields = ['code', 'url']

class NaicsSummarySerializer(BaseNaicsSerializer):
    sin = SinSerializer(many=True)
    
    class Meta(BaseNaicsSerializer.Meta):
        fields = BaseNaicsSerializer.Meta.fields + ['sin', 'url']

class NaicsFullSerializer(BaseNaicsSerializer):
    sin = SinSerializer(many=True)
    
    class Meta(BaseNaicsSerializer.Meta):
        fields = BaseNaicsSerializer.Meta.fields + ['sin']

class NaicsTestSerializer(NaicsFullSerializer):
    sin = SinTestSerializer(many=True)
    
    class Meta(NaicsFullSerializer.Meta):
        fields = NaicsFullSerializer.Meta.fields + ['url']


class BasePscSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="psc-detail", lookup_field='code')
    
    class Meta:
        model = categories.PSC
        fields = ['code', 'description']

class PscLinkSerializer(BasePscSerializer):
    class Meta(BasePscSerializer.Meta):
        fields = ['code', 'url']

class PscSummarySerializer(BasePscSerializer):
    sin = SinSerializer(many=True)
    
    class Meta(BasePscSerializer.Meta):
        fields = BasePscSerializer.Meta.fields + ['sin', 'url']

class PscFullSerializer(BasePscSerializer):
    sin = SinSerializer(many=True)
    
    class Meta(BasePscSerializer.Meta):
        fields = BasePscSerializer.Meta.fields + ['sin']

class PscTestSerializer(PscFullSerializer):
    sin = SinTestSerializer(many=True)
    
    class Meta(PscFullSerializer.Meta):
        fields = PscFullSerializer.Meta.fields + ['url']


class TierSerializer(ModelSerializer):
    class Meta:
        model = categories.Tier
        fields = ['number', 'name']

class TierTestSerializer(ModelSerializer):
    class Meta:
        model = categories.Tier
        fields = ['number', 'name']


class BaseVehicleSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="vehicle-detail", lookup_field='id')
    tier = TierSerializer()
    
    class Meta:
        model = categories.Vehicle
        fields = ['id', 'name', 'tier', 'poc', 'ordering_guide', 'small_business', 'numeric_pool', 'display_number']

class VehicleLinkSerializer(BaseVehicleSerializer):
    class Meta(BaseVehicleSerializer.Meta):
        fields = ['id', 'url']

class VehicleSummarySerializer(BaseVehicleSerializer):
    class Meta(BaseVehicleSerializer.Meta):
        fields = BaseVehicleSerializer.Meta.fields + ['url']

class VehicleFullSerializer(BaseVehicleSerializer):
    

    class Meta(BaseVehicleSerializer.Meta):
        fields = BaseVehicleSerializer.Meta.fields

class VehicleTestSerializer(VehicleFullSerializer):
    tier = TierTestSerializer()

    class Meta(VehicleFullSerializer.Meta):
        fields = VehicleFullSerializer.Meta.fields + ['url']


class BasePoolSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="pool-detail", lookup_field='id')
    vehicle = VehicleLinkSerializer()
    
    class Meta:
        model = categories.Pool
        fields = ['id', 'name', 'number', 'vehicle', 'threshold']

class PoolLinkSerializer(BasePoolSerializer):
    class Meta(BasePoolSerializer.Meta):
        fields = ['id', 'vehicle', 'url']

class PoolSummarySerializer(BasePoolSerializer):
    naics = NaicsSummarySerializer(many=True)
    psc = PscSummarySerializer(many=True)
    vehicle = VehicleSummarySerializer()
    
    class Meta(BasePoolSerializer.Meta):
        fields = BasePoolSerializer.Meta.fields + ['naics', 'psc', 'url']

class PoolFullSerializer(BasePoolSerializer):
    vehicle = VehicleSummarySerializer()
    naics = NaicsSummarySerializer(many=True)
    psc = PscSummarySerializer(many=True)
    
    class Meta(BasePoolSerializer.Meta):
        fields = BasePoolSerializer.Meta.fields + ['naics', 'psc']

class PoolTestSerializer(PoolFullSerializer):
    vehicle = VehicleTestSerializer()
    naics = NaicsTestSerializer(many=True)
    psc = PscTestSerializer(many=True)
    
    class Meta(PoolFullSerializer.Meta):
        fields = PoolFullSerializer.Meta.fields + ['url']


class BaseSetasideSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="setaside-detail", lookup_field='code')
    
    class Meta:
        model = categories.SetAside
        fields = ['code', 'name', 'description', 'far_order']

class SetasideLinkSerializer(BaseSetasideSerializer):
    class Meta(BaseSetasideSerializer.Meta):
        fields = ['code', 'url']

class SetasideSummarySerializer(BaseSetasideSerializer):
    class Meta(BaseSetasideSerializer.Meta):
        fields = BaseSetasideSerializer.Meta.fields + ['url']

class SetasideFullSerializer(BaseSetasideSerializer):
    class Meta(BaseSetasideSerializer.Meta):
        pass

class SetasideTestSerializer(SetasideFullSerializer):
    class Meta(SetasideFullSerializer.Meta):
        fields = SetasideFullSerializer.Meta.fields + ['url']


class StateSerializer(ModelSerializer):
    class Meta:
        model = categories.State
        fields = ['code']
                
    def to_representation(self, instance):
        return instance.code

class StateTestSerializer(ModelSerializer):
    class Meta:
        model = categories.State
        fields = ['code']


class BaseZoneSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="zone-detail", lookup_field='id')
    
    class Meta:
        model = categories.Zone
        fields = ['id']
    
class ZoneLinkSerializer(BaseZoneSerializer):
    class Meta(BaseZoneSerializer.Meta):
        fields = ['id', 'url']

class ZoneSummarySerializer(BaseZoneSerializer):
    states = StateSerializer(many=True)
    
    class Meta(BaseZoneSerializer.Meta):
        fields = BaseZoneSerializer.Meta.fields + ['states', 'url']

class ZoneFullSerializer(BaseZoneSerializer):
    states = StateSerializer(many=True)
    
    class Meta(BaseZoneSerializer.Meta):
        fields = BaseZoneSerializer.Meta.fields + ['states']

class ZoneTestSerializer(ZoneFullSerializer):
    states = StateTestSerializer(many=True)
    
    class Meta(ZoneFullSerializer.Meta):
        fields = ZoneFullSerializer.Meta.fields + ['url']


class LocationSerializer(ModelSerializer):
    class Meta:
        model = vendors.Location
        fields = ['address', 'city', 'state', 'zipcode', 'congressional_district']


class PhoneSerializer(ModelSerializer):
    class Meta:
        model = vendors.ContactPhone
        fields = ['number']

class EmailSerializer(ModelSerializer):
    class Meta:
        model = vendors.ContactEmail
        fields = ['address']

class ContactSerializer(ModelSerializer):
    phones = PhoneSerializer(many=True)
    emails = EmailSerializer(many=True)
    
    class Meta:
        model = vendors.Contact
        fields = ['order', 'name', 'phones', 'emails']


class BasePoolMembershipSerializer(ModelSerializer):
    capability_statement = SerializerMethodField()
    contacts = SerializerMethodField()
    
    class Meta:
        model = vendors.PoolMembership
        fields = ['piid', 'contacts', 'expiration_8a_date', 'contract_end_date', 'capability_statement']
        
    def get_capability_statement(self, item):
        request = self.context.get('request')
        duns = item.vendor.duns
        vehicle = item.pool.vehicle.id
        
        cs_path = "static/discovery_site/capability_statements/{}/{}.pdf".format(vehicle, duns)
        cs_url = request.build_absolute_uri("/discovery_site/capability_statements/{}/{}.pdf".format(vehicle, duns))
    
        if vehicle and os.path.isfile(cs_path):
            return cs_url    
        return ''
    
    def get_contacts(self, item):
        queryset = vendors.Contact.objects.filter(responsibility=item).order_by('order')
        return ContactSerializer(queryset, many=True, context=self.context).data
        
    
class PoolMembershipLinkSerializer(BasePoolMembershipSerializer):
    pool = PoolLinkSerializer(many=False)
    setasides = SetasideSummarySerializer(many=True)
    
    zones = ZoneLinkSerializer(many=True)
    
    class Meta(BasePoolMembershipSerializer.Meta):
        fields = BasePoolMembershipSerializer.Meta.fields + ['pool', 'setasides', 'zones']
    
class PoolMembershipSummarySerializer(BasePoolMembershipSerializer):
    pool = PoolSummarySerializer(many=False)
    setasides = SetasideSummarySerializer(many=True)
    
    zones = ZoneSummarySerializer(many=True)
    
    class Meta(BasePoolMembershipSerializer.Meta):
        fields = BasePoolMembershipSerializer.Meta.fields + ['pool', 'setasides', 'zones']

class PoolMembershipTestSerializer(BasePoolMembershipSerializer):
    pool = PoolTestSerializer(many=False)
    setasides = SetasideTestSerializer(many=True)
    
    zones = ZoneTestSerializer(many=True)
    
    class Meta(BasePoolMembershipSerializer.Meta):
        fields = BasePoolMembershipSerializer.Meta.fields + ['pool', 'setasides', 'zones']


class BaseVendorSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="vendor-detail", lookup_field='duns')
    
    class Meta:
        model = vendors.Vendor
        fields = ['name', 'duns', 'duns_4', 'cage', 
                  'sam_status', 'sam_expiration_date', 'sam_activation_date', 
                  'sam_exclusion', 'sam_url']

class VendorLinkSerializer(BaseVendorSerializer):
    class Meta(BaseVendorSerializer.Meta):
        fields = ['duns', 'url']

class AnnotatedVendorSerializer(BaseVendorSerializer):
    sam_location_citystate = CharField()
    
    annual_revenue = IntegerField()
    number_of_employees = IntegerField()
    number_of_contracts = IntegerField()


class VendorSummarySerializer(AnnotatedVendorSerializer):
    pools = PoolMembershipLinkSerializer(many=True)
    
    class Meta(BaseVendorSerializer.Meta):
        fields = BaseVendorSerializer.Meta.fields + [
            'annual_revenue', 'number_of_employees', 
            'number_of_contracts', 'pools',
            'url'
        ]

class VendorFullSerializer(AnnotatedVendorSerializer):
    sam_location = LocationSerializer(many=False)
    pools = PoolMembershipLinkSerializer(many=True)
    
    class Meta(BaseVendorSerializer.Meta):
        fields = BaseVendorSerializer.Meta.fields + [
            'sam_location', 
            'pools',
            'annual_revenue', 'number_of_employees', 
            'number_of_contracts'
        ]

class VendorTestSerializer(BaseVendorSerializer):
    sam_location = LocationSerializer(many=False)
    pools = PoolMembershipTestSerializer(many=True)
    
    class Meta(BaseVendorSerializer.Meta):
        fields = BaseVendorSerializer.Meta.fields + [
            'sam_location', 'pools',
            'url'
        ]


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


class BaseContractSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="contract-detail", lookup_field='id')
    
    status = ContractStatusSerializer(many=False)
    pricing_type = PricingStructureSerializer(many=False)
    
    class Meta:
        model = contracts.Contract
        fields = ['id', 'piid', 'base_piid', 'agency_id', 'agency_name', 'NAICS', 'PSC',
                  'point_of_contact', 'vendor_phone',
                  'date_signed', 'completion_date', 'status', 'pricing_type', 'obligated_amount', 
                  'annual_revenue', 'number_of_employees']

class ContractLinkSerializer(BaseContractSerializer):
    class Meta(BaseContractSerializer.Meta):
        fields = ['id', 'url']
        
class AnnotatedContractSerializer(BaseContractSerializer):
    place_of_performance_location = CharField()

class ContractSummarySerializer(AnnotatedContractSerializer):
    class Meta(BaseContractSerializer.Meta):
        fields = BaseContractSerializer.Meta.fields + [
            'place_of_performance_location',
            'url'
        ]
   
class ContractFullSerializer(AnnotatedContractSerializer):
    vendor = VendorSummarySerializer(many=False)
    vendor_location = LocationSerializer(many=False)
    
    place_of_performance = PlaceOfPerformanceSerializer(many=False)
        
    class Meta(BaseContractSerializer.Meta):
        fields = BaseContractSerializer.Meta.fields + [
            'vendor', 'vendor_location', 
            'place_of_performance'
        ]

class ContractTestSerializer(BaseContractSerializer):
    vendor = VendorTestSerializer(many=False)
    vendor_location = LocationSerializer(many=False)
    
    place_of_performance = PlaceOfPerformanceSerializer(many=False)
    
    class Meta(BaseContractSerializer.Meta):
        fields = BaseContractSerializer.Meta.fields + [
            'vendor', 'vendor_location', 
            'place_of_performance',
            'url'
        ]


class MetadataSerializer(Serializer):
    sam_load_date = DateField()
    fpds_load_date = DateField()
