from rest_framework.fields import CharField, IntegerField, DateField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import Serializer, ModelSerializer, HyperlinkedModelSerializer, SerializerMethodField

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts


class BaseNaicsSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="naics-detail", lookup_field='code')
    
    class Meta:
        model = categories.Naics
        fields = ['code', 'root_code', 'description']

class NaicsLinkSerializer(BaseNaicsSerializer):
    class Meta(BaseNaicsSerializer.Meta):
        fields = ['code', 'url']

class NaicsSummarySerializer(BaseNaicsSerializer):
    class Meta(BaseNaicsSerializer.Meta):
        fields = BaseNaicsSerializer.Meta.fields + ['url']

class NaicsFullSerializer(BaseNaicsSerializer):
    class Meta(BaseNaicsSerializer.Meta):
        pass

class NaicsTestSerializer(NaicsFullSerializer):
    class Meta(NaicsFullSerializer.Meta):
        fields = NaicsFullSerializer.Meta.fields + ['url']


class BasePoolSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="pool-detail", lookup_field='id')
    
    class Meta:
        model = categories.Pool
        fields = ['id', 'name', 'number', 'vehicle', 'threshold']

class PoolLinkSerializer(BasePoolSerializer):
    class Meta(BasePoolSerializer.Meta):
        fields = ['id', 'url']

class PoolSummarySerializer(BasePoolSerializer):
    class Meta(BasePoolSerializer.Meta):
        fields = BasePoolSerializer.Meta.fields + ['url']

class PoolFullSerializer(BasePoolSerializer):
    naics = NaicsLinkSerializer(many=True)
    
    class Meta(BasePoolSerializer.Meta):
        fields = BasePoolSerializer.Meta.fields + ['naics']

class PoolTestSerializer(PoolFullSerializer):
    naics = NaicsTestSerializer(many=True)
    
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


class BaseZoneSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="zone-detail", lookup_field='id')
    state = SerializerMethodField()
    
    class Meta:
        model = categories.Zone
        fields = ['id', 'state']
        
    def get_state(self, item):
        return item.states()
    
class ZoneLinkSerializer(BaseZoneSerializer):
    class Meta(BaseZoneSerializer.Meta):
        fields = ['id', 'url']

class ZoneSummarySerializer(BaseZoneSerializer):
    class Meta(BaseZoneSerializer.Meta):
        fields = BaseZoneSerializer.Meta.fields + ['url']

class ZoneFullSerializer(BaseZoneSerializer):
    class Meta(BaseZoneSerializer.Meta):
        pass

class ZoneTestSerializer(ZoneFullSerializer):
    class Meta(ZoneFullSerializer.Meta):
        fields = ZoneFullSerializer.Meta.fields + ['url']


class LocationSerializer(ModelSerializer):
    class Meta:
        model = vendors.Location
        fields = ['address', 'city', 'state', 'zipcode', 'congressional_district']


class ContractManagerSerializer(ModelSerializer):
    class Meta:
        model = vendors.ContractManager
        fields = ['name', 'phone', 'email']

class ProjectManagerSerializer(ModelSerializer):
    class Meta:
        model = vendors.ProjectManager
        fields = ['name', 'phone', 'email']


class BasePoolMembershipSerializer(ModelSerializer):
    cms = ContractManagerSerializer(many=True)
    pms = ProjectManagerSerializer(many=True)
    
    class Meta:
        model = vendors.PoolMembership
        fields = ['piid', 'cms', 'pms']
    
class PoolMembershipLinkSerializer(BasePoolMembershipSerializer):
    pool = PoolLinkSerializer(many=False)
    setasides = SetasideLinkSerializer(many=True)
    
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
    class Meta(BaseVendorSerializer.Meta):
        fields = BaseVendorSerializer.Meta.fields + [
            'sam_location_citystate', 
            'annual_revenue', 'number_of_employees', 
            'number_of_contracts',
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
        fields = ['id', 'piid', 'agency_id', 'agency_name', 'NAICS', 'PSC',
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
