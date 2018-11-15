from rest_framework.fields import CharField, IntegerField, DateField, ListField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import Serializer, ModelSerializer, HyperlinkedModelSerializer, SerializerMethodField

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts

import os


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
        
    @classmethod    
    def _load_sin(cls, queryset, prefix = ''):
        return queryset.prefetch_related("{}sin".format(prefix))

class NaicsLinkSerializer(BaseNaicsSerializer):
    class Meta(BaseNaicsSerializer.Meta):
        fields = ['code', 'url']

class NaicsSummarySerializer(BaseNaicsSerializer):
    sin = SinSerializer(many=True)
    
    class Meta(BaseNaicsSerializer.Meta):
        fields = BaseNaicsSerializer.Meta.fields + ['sin', 'url']
    
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_sin(queryset, prefix)

class NaicsFullSerializer(BaseNaicsSerializer):
    sin = SinSerializer(many=True)
    
    class Meta(BaseNaicsSerializer.Meta):
        fields = BaseNaicsSerializer.Meta.fields + ['sin']
    
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_sin(queryset, prefix)

class NaicsTestSerializer(NaicsFullSerializer):
    sin = SinTestSerializer(many=True)
    
    class Meta(NaicsFullSerializer.Meta):
        fields = NaicsFullSerializer.Meta.fields + ['url']


class BasePscSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="psc-detail", lookup_field='code')
    
    class Meta:
        model = categories.PSC
        fields = ['code', 'description']
        
    @classmethod    
    def _load_sin(cls, queryset, prefix = ''):
        return queryset.prefetch_related("{}sin".format(prefix))

class PscLinkSerializer(BasePscSerializer):
    class Meta(BasePscSerializer.Meta):
        fields = ['code', 'url']

class PscSummarySerializer(BasePscSerializer):
    sin = SinSerializer(many=True)
    
    class Meta(BasePscSerializer.Meta):
        fields = BasePscSerializer.Meta.fields + ['sin', 'url']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_sin(queryset, prefix)

class PscFullSerializer(BasePscSerializer):
    sin = SinSerializer(many=True)
    
    class Meta(BasePscSerializer.Meta):
        fields = BasePscSerializer.Meta.fields + ['sin']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_sin(queryset, prefix)

class PscTestSerializer(PscFullSerializer):
    sin = SinTestSerializer(many=True)
    
    class Meta(PscFullSerializer.Meta):
        fields = PscFullSerializer.Meta.fields + ['url']


class BaseKeywordSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="keyword-detail", lookup_field='id')

    class Meta:
        model = categories.Keyword
        fields = ['id', 'name']

class KeywordLinkSerializer(BaseKeywordSerializer):
    class Meta(BaseKeywordSerializer.Meta):
        fields = ['id', 'name', 'url']

class KeywordSummarySerializer(BaseKeywordSerializer):
    parent = KeywordLinkSerializer()
    sin = SinSerializer()
    naics = NaicsLinkSerializer()
    psc = PscLinkSerializer()
    
    class Meta(BaseKeywordSerializer.Meta):
        fields = BaseKeywordSerializer.Meta.fields + ['parent', 'sin', 'naics', 'psc', 'calc', 'url']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        if prefix:
            return queryset.prefetch_related(
                "{}sin".format(prefix), 
                "{}naics".format(prefix), 
                "{}psc".format(prefix)
            )
        return queryset.select_related('sin', 'naics', 'psc')

class KeywordFullSerializer(KeywordSummarySerializer):
    naics = NaicsSummarySerializer()
    psc = PscSummarySerializer()

    class Meta(BaseKeywordSerializer.Meta):
        fields = BaseKeywordSerializer.Meta.fields + ['parent', 'sin', 'naics', 'psc', 'calc']

class KeywordTestSerializer(KeywordFullSerializer):
    sin = SinTestSerializer()
    naics = NaicsTestSerializer()
    psc = PscTestSerializer()
    
    class Meta(KeywordFullSerializer.Meta):
        fields = KeywordFullSerializer.Meta.fields + ['url']


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
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        if prefix:
            return queryset.prefetch_related("{}tier".format(prefix))
        return queryset.select_related('tier')

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
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        queryset = VehicleLinkSerializer.load_related(queryset, "{}vehicle__".format(prefix))
        
        if prefix:
            return queryset.prefetch_related("{}vehicle".format(prefix))
        return queryset.select_related('vehicle')
    
    @classmethod    
    def _load_summary(cls, queryset, prefix = ''):
        queryset = VehicleSummarySerializer.load_related(queryset, "{}vehicle__".format(prefix))
        queryset = NaicsSummarySerializer.load_related(queryset, "{}naics__".format(prefix))
        queryset = PscSummarySerializer.load_related(queryset, "{}psc__".format(prefix))
        
        if prefix:
            queryset = queryset.prefetch_related("{}vehicle".format(prefix))
        else:
            queryset = queryset.select_related('vehicle')
        
        return queryset.prefetch_related("{}naics".format(prefix), "{}psc".format(prefix))
    
    @classmethod    
    def _load_full(cls, queryset, prefix = ''):
        queryset = cls._load_summary(queryset, prefix)
        queryset = KeywordSummarySerializer.load_related(queryset, "{}keywords__".format(prefix))
        return queryset.prefetch_related("{}keywords".format(prefix))

class PoolLinkSerializer(BasePoolSerializer):
    class Meta(BasePoolSerializer.Meta):
        fields = ['id', 'vehicle', 'url']

class PoolSummarySerializer(BasePoolSerializer):
    naics = NaicsSummarySerializer(many=True)
    psc = PscSummarySerializer(many=True)
    vehicle = VehicleSummarySerializer()
    
    class Meta(BasePoolSerializer.Meta):
        fields = BasePoolSerializer.Meta.fields + ['naics', 'psc', 'url']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_summary(queryset, prefix)

class PoolFullSerializer(BasePoolSerializer):
    vehicle = VehicleSummarySerializer()
    naics = NaicsSummarySerializer(many=True)
    psc = PscSummarySerializer(many=True)
    keywords = KeywordSummarySerializer(many=True)
    
    class Meta(BasePoolSerializer.Meta):
        fields = BasePoolSerializer.Meta.fields + ['naics', 'psc', 'keywords']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_full(queryset, prefix)

class PoolTestSerializer(PoolFullSerializer):
    vehicle = VehicleTestSerializer()
    naics = NaicsTestSerializer(many=True)
    psc = PscTestSerializer(many=True)
    keywords = KeywordTestSerializer(many=True)
    
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
        
    @classmethod    
    def _load_states(cls, queryset, prefix = ''):
        return queryset.prefetch_related("{}states".format(prefix))
    
class ZoneLinkSerializer(BaseZoneSerializer):
    class Meta(BaseZoneSerializer.Meta):
        fields = ['id', 'url']

class ZoneSummarySerializer(BaseZoneSerializer):
    states = StateSerializer(many=True)
    
    class Meta(BaseZoneSerializer.Meta):
        fields = BaseZoneSerializer.Meta.fields + ['states', 'url']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_states(queryset, prefix)

class ZoneFullSerializer(BaseZoneSerializer):
    states = StateSerializer(many=True)
    
    class Meta(BaseZoneSerializer.Meta):
        fields = BaseZoneSerializer.Meta.fields + ['states']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_states(queryset, prefix)

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
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return queryset.prefetch_related("{}phones".format(prefix), "{}emails".format(prefix))


class BasePoolMembershipSerializer(ModelSerializer):
    capability_statement = SerializerMethodField()
    contacts = SerializerMethodField()
    
    class Meta:
        model = vendors.PoolMembership
        fields = ['id', 'piid', 'contacts', 'expiration_8a_date', 'contract_end_date', 'capability_statement']
        
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
    
    @classmethod    
    def _load_primary(cls, queryset, prefix = ''):
        if prefix:
            queryset = queryset.prefetch_related("{}pool".format(prefix))
        else:
            queryset = queryset.select_related('pool')
        
        return queryset.prefetch_related("{}setasides".format(prefix), "{}zones".format(prefix))
        
    
class PoolMembershipLinkSerializer(BasePoolMembershipSerializer):
    pool = PoolLinkSerializer(many=False)
    setasides = SetasideSummarySerializer(many=True)
    
    zones = ZoneLinkSerializer(many=True)
    
    class Meta(BasePoolMembershipSerializer.Meta):
        fields = BasePoolMembershipSerializer.Meta.fields + ['pool', 'setasides', 'zones']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        queryset = PoolLinkSerializer.load_related(queryset, "{}pool__".format(prefix))
        return cls._load_primary(queryset, prefix)
    
class PoolMembershipSummarySerializer(BasePoolMembershipSerializer):
    pool = PoolSummarySerializer(many=False)
    setasides = SetasideSummarySerializer(many=True)
    
    zones = ZoneSummarySerializer(many=True)
    
    class Meta(BasePoolMembershipSerializer.Meta):
        fields = BasePoolMembershipSerializer.Meta.fields + ['pool', 'setasides', 'zones']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        queryset = PoolSummarySerializer.load_related(queryset, "{}pool__".format(prefix))
        queryset = ZoneSummarySerializer.load_related(queryset, "{}zones__".format(prefix))
        return cls._load_primary(queryset, prefix)

class PoolMembershipTestSerializer(BasePoolMembershipSerializer):
    pool = PoolTestSerializer(many=False)
    setasides = SetasideTestSerializer(many=True)
    
    zones = ZoneTestSerializer(many=True)
    
    class Meta(BasePoolMembershipSerializer.Meta):
        fields = BasePoolMembershipSerializer.Meta.fields + ['pool', 'setasides', 'zones']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        queryset = PoolFullSerializer.load_related(queryset, "{}pool__".format(prefix))
        queryset = ZoneFullSerializer.load_related(queryset, "{}zones__".format(prefix))
        return cls._load_primary(queryset, prefix)


class BaseVendorSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="vendor-detail", lookup_field='duns')
    
    class Meta:
        model = vendors.Vendor
        fields = ['name', 'duns', 'duns_4', 'cage', 
                  'sam_status', 'sam_expiration_date', 'sam_activation_date', 
                  'sam_exclusion', 'sam_url']
        
    @classmethod    
    def _load_summary(cls, queryset, prefix = ''):
        queryset = PoolMembershipLinkSerializer.load_related(queryset, "{}pools__".format(prefix))
        return queryset.prefetch_related("{}pools".format(prefix))

    @classmethod
    def _load_full(clscls, queryset, prefix = ''):
        queryset = PoolMembershipSummarySerializer.load_related(queryset, "{}pools__".format(prefix))
        
        if prefix:
            queryset = queryset.prefetch_related("{}sam_location".format(prefix))
        else:
            queryset = queryset.select_related('sam_location')
        
        return queryset.prefetch_related("{}pools".format(prefix))

class VendorLinkSerializer(BaseVendorSerializer):
    class Meta(BaseVendorSerializer.Meta):
        fields = ['duns', 'url']

class AnnotatedVendorSerializer(BaseVendorSerializer):
    sam_location_citystate = CharField()
    number_of_contracts = IntegerField()


class VendorSummarySerializer(AnnotatedVendorSerializer):
    pools = PoolMembershipLinkSerializer(many=True)
    
    class Meta(BaseVendorSerializer.Meta):
        fields = BaseVendorSerializer.Meta.fields + [
            'number_of_contracts', 'pools',
            'url'
        ]
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_summary(queryset, prefix)

class VendorFullSerializer(AnnotatedVendorSerializer):
    sam_location = LocationSerializer(many=False)
    pools = PoolMembershipLinkSerializer(many=True)
    
    class Meta(BaseVendorSerializer.Meta):
        fields = BaseVendorSerializer.Meta.fields + [
            'sam_location', 
            'pools',
            'number_of_contracts'
        ]
        
    @classmethod
    def load_related(cls, queryset, prefix = ''):
        return cls._load_full(queryset, prefix)

class VendorTestSerializer(BaseVendorSerializer):
    sam_location = LocationSerializer(many=False)
    pools = PoolMembershipTestSerializer(many=True)
    
    class Meta(BaseVendorSerializer.Meta):
        fields = BaseVendorSerializer.Meta.fields + [
            'sam_location', 'pools',
            'url'
        ]
        
    @classmethod
    def load_related(cls, queryset, prefix = ''):
        return cls._load_full(queryset, prefix)

    
class PoolMembershipSummaryVendorSerializer(PoolMembershipSummarySerializer):
    vendor = VendorLinkSerializer(many=False)
    
    class Meta(PoolMembershipSummarySerializer.Meta):
        fields = PoolMembershipSummarySerializer.Meta.fields + ['vendor']
        
    @classmethod
    def load_related(cls, queryset, prefix = ''):
        if prefix:
            return queryset.prefetch_related("{}vendor".format(prefix))
        return queryset.select_related('vendor')
   
class PoolMembershipTestVendorSerializer(PoolMembershipTestSerializer):
    vendor = VendorTestSerializer(many=False)
    
    class Meta(PoolMembershipTestSerializer.Meta):
        fields = PoolMembershipTestSerializer.Meta.fields + ['vendor']

    @classmethod
    def load_related(cls, queryset, prefix = ''):
        queryset = VendorFullSerializer.load_related(queryset, "{}vendor__".format(prefix))
        
        if prefix:
            return queryset.prefetch_related("{}vendor".format(prefix))
        return queryset.select_related('vendor')


class BaseAgencySerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="agency-detail", lookup_field='id')
    
    class Meta:
        model = contracts.Agency
        fields = ['id', 'name']

class AgencyLinkSerializer(BaseAgencySerializer):
    class Meta(BaseAgencySerializer.Meta):
        fields = ['id', 'url']

class AgencySummarySerializer(BaseAgencySerializer):
    class Meta(BaseAgencySerializer.Meta):
        fields = BaseAgencySerializer.Meta.fields + ['url']

class AgencyFullSerializer(BaseAgencySerializer):
    class Meta(BaseAgencySerializer.Meta):
        fields = BaseAgencySerializer.Meta.fields

class AgencyTestSerializer(AgencyFullSerializer):
    class Meta(AgencyFullSerializer.Meta):
        fields = AgencyFullSerializer.Meta.fields + ['url']


class BasePricingStructureSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="pricingstructure-detail", lookup_field='code')
    
    class Meta:
        model = contracts.PricingStructure
        fields = ['code', 'name']

class PricingStructureLinkSerializer(BasePricingStructureSerializer):
    class Meta(BasePricingStructureSerializer.Meta):
        fields = ['code', 'url']

class PricingStructureSummarySerializer(BasePricingStructureSerializer):
    class Meta(BasePricingStructureSerializer.Meta):
        fields = BasePricingStructureSerializer.Meta.fields + ['url']

class PricingStructureFullSerializer(BasePricingStructureSerializer):
    class Meta(BasePricingStructureSerializer.Meta):
        fields = BasePricingStructureSerializer.Meta.fields

class PricingStructureTestSerializer(PricingStructureFullSerializer):
    class Meta(PricingStructureFullSerializer.Meta):
        fields = PricingStructureFullSerializer.Meta.fields + ['url']



class BaseContractStatusSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="contractstatus-detail", lookup_field='code')
    
    class Meta:
        model = contracts.ContractStatus
        fields = ['code', 'name']

class ContractStatusLinkSerializer(BaseContractStatusSerializer):
    class Meta(BaseContractStatusSerializer.Meta):
        fields = ['code', 'url']

class ContractStatusSummarySerializer(BaseContractStatusSerializer):
    class Meta(BaseContractStatusSerializer.Meta):
        fields = BaseContractStatusSerializer.Meta.fields + ['url']

class ContractStatusFullSerializer(BaseContractStatusSerializer):
    class Meta(BaseContractStatusSerializer.Meta):
        fields = BaseContractStatusSerializer.Meta.fields

class ContractStatusTestSerializer(ContractStatusFullSerializer):
    class Meta(ContractStatusFullSerializer.Meta):
        fields = ContractStatusFullSerializer.Meta.fields + ['url']


class BasePlaceOfPerformanceSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="placeofperformance-detail", lookup_field='id')
    
    class Meta:
        model = contracts.PlaceOfPerformance
        fields = ['id', 'country_code', 'country_name', 'state', 'zipcode']

class PlaceOfPerformanceLinkSerializer(BasePlaceOfPerformanceSerializer):
    class Meta(BasePlaceOfPerformanceSerializer.Meta):
        fields = ['id', 'url']

class PlaceOfPerformanceSummarySerializer(BasePlaceOfPerformanceSerializer):
    class Meta(BasePlaceOfPerformanceSerializer.Meta):
        fields = BasePlaceOfPerformanceSerializer.Meta.fields + ['url']

class PlaceOfPerformanceFullSerializer(BasePlaceOfPerformanceSerializer):
    class Meta(BasePlaceOfPerformanceSerializer.Meta):
        fields = BasePlaceOfPerformanceSerializer.Meta.fields

class PlaceOfPerformanceTestSerializer(PlaceOfPerformanceFullSerializer):
    class Meta(PlaceOfPerformanceFullSerializer.Meta):
        fields = PlaceOfPerformanceFullSerializer.Meta.fields + ['url']


class BaseContractSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="contract-detail", lookup_field='id')
    
    class Meta:
        model = contracts.Contract
        fields = ['id', 'piid', 'base_piid', 'NAICS', 'PSC', 'agency', 'vendor',
                  'point_of_contact', 'vendor_phone', 'place_of_performance',
                  'date_signed', 'completion_date', 'status', 'pricing_type', 'obligated_amount']
        
    @classmethod
    def _load_summary(cls, queryset, prefix = ''):
        if prefix:
            return queryset.prefetch_related(
                "{}vendor".format(prefix), 
                "{}place_of_performance".format(prefix), 
                "{}agency".format(prefix),
                "{}status".format(prefix),
                "{}pricing_type".format(prefix)
            )
        return queryset.select_related('vendor', 'place_of_performance', 'agency', 'status', 'pricing_type')
    
    @classmethod
    def _load_full(cls, queryset, prefix = ''):
        queryset = VendorFullSerializer.load_related(queryset, "{}vendor__".format(prefix))
        
        if prefix:
            return queryset.prefetch_related(
                "{}vendor".format(prefix),
                "{}vendor_location".format(prefix), 
                "{}place_of_performance".format(prefix), 
                "{}agency".format(prefix),
                "{}status".format(prefix),
                "{}pricing_type".format(prefix)
            )
        return queryset.select_related('vendor', 'vendor_location', 'place_of_performance', 'agency', 'status', 'pricing_type')

class ContractLinkSerializer(BaseContractSerializer):
    class Meta(BaseContractSerializer.Meta):
        fields = ['id', 'url']

class ContractSummarySerializer(BaseContractSerializer):
    vendor = VendorLinkSerializer(many=False)
    
    place_of_performance = PlaceOfPerformanceSummarySerializer(many=False)
    agency = AgencySummarySerializer(many=False)
    pricing_type = PricingStructureSummarySerializer(many=False)
    status = ContractStatusSummarySerializer(many=False)
    
    class Meta(BaseContractSerializer.Meta):
        fields = BaseContractSerializer.Meta.fields + ['url']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_summary(queryset, prefix)
   
class ContractFullSerializer(BaseContractSerializer):
    vendor = VendorLinkSerializer(many=False)
    vendor_location = LocationSerializer(many=False)
    
    place_of_performance = PlaceOfPerformanceFullSerializer(many=False)
    agency = AgencyFullSerializer(many=False)
    pricing_type = PricingStructureFullSerializer(many=False)
    status = ContractStatusFullSerializer(many=False)
        
    class Meta(BaseContractSerializer.Meta):
        fields = BaseContractSerializer.Meta.fields + ['vendor_location']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_full(queryset, prefix)

class ContractTestSerializer(BaseContractSerializer):
    vendor = VendorTestSerializer(many=False)
    vendor_location = LocationSerializer(many=False)
    
    place_of_performance = PlaceOfPerformanceTestSerializer(many=False)
    agency = AgencyTestSerializer(many=False)
    pricing_type = PricingStructureTestSerializer(many=False)
    status = ContractStatusTestSerializer(many=False)
    
    class Meta(BaseContractSerializer.Meta):
        fields = BaseContractSerializer.Meta.fields + ['vendor_location', 'url']
        
    @classmethod    
    def load_related(cls, queryset, prefix = ''):
        return cls._load_full(queryset, prefix)


class MetadataSerializer(Serializer):
    sam_load_date = DateField()
    fpds_load_date = DateField()
