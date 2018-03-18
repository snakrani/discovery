from django.db.models.query import QuerySet

from rest_framework.fields import CharField, IntegerField

from rest_framework_filters.filterset import FilterSet
from rest_framework_filters.filters import NumberFilter, CharFilter, DateFilter, DateTimeFilter, RelatedFilter, BaseInFilter
from rest_framework_filters.backends import ComplexFilterBackend

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts


EQUALITY_BOOL_FILTERS = [
    'exact'
]

EQUALITY_CHAR_FILTERS = [
    'exact',
    'iexact',
    'in'
]

FUZZY_CHAR_FILTERS = [
    'contains',
    'icontains',
    'startswith',
    'istartswith',
    'endswith', 
    'iendswith',
    'regex',
    'iregex'
]


DATE_FILTERS = [
    'date',
    'year',
    'month',
    'day',
    'week',
    'week_day',
    'quarter'
]

NUM_FILTERS = [
    'exact',
    'lt',
    'lte', 
    'gt', 
    'gte',
    'range',
    'in'
]


NAICS_FIELDS = {
    'code': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'root_code': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'description': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
}

SETASIDE_FIELDS = {
    'code': EQUALITY_CHAR_FILTERS, 
    'name': EQUALITY_CHAR_FILTERS, 
    'description': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
    'far_order': NUM_FILTERS
}

POOL_FIELDS = {
    'id': EQUALITY_CHAR_FILTERS, 
    'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'number': EQUALITY_CHAR_FILTERS, 
    'vehicle': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'threshold': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
}

ZONE_FIELDS = {
    'id': NUM_FILTERS
}

LOCATION_FIELDS = {
    'address': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'city': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
    'state': EQUALITY_CHAR_FILTERS,
    'zipcode': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
    'congressional_district': EQUALITY_CHAR_FILTERS
}

MANAGER_FIELDS = {
    'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
}


POOL_MEMBERSHIP_FIELDS = {
    'piid': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
}


VENDOR_FIELDS = {
    'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'duns': NUM_FILTERS, 
    'cage': EQUALITY_CHAR_FILTERS, 
    'sam_status': EQUALITY_CHAR_FILTERS, 
    'sam_activation_date': DATE_FILTERS, 
    'sam_expiration_date': DATE_FILTERS, 
    'sam_exclusion': EQUALITY_BOOL_FILTERS, 
    'sam_url': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
}

PLACE_OF_PERFORMANCE_FIELDS = {
    'country_code': EQUALITY_CHAR_FILTERS, 
    'country_name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
    'state': EQUALITY_CHAR_FILTERS,
    'zipcode': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
}

PRICING_STRUCTURE_FIELDS = {
    'code': EQUALITY_CHAR_FILTERS, 
    'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
}

CONTRACT_STATUS_FIELDS = {
    'code': EQUALITY_CHAR_FILTERS, 
    'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
}

CONTRACT_FIELDS = {
    'id': NUM_FILTERS, 
    'piid': NUM_FILTERS, 
    'agency_id': EQUALITY_CHAR_FILTERS, 
    'agency_name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'NAICS': EQUALITY_CHAR_FILTERS, 
    'PSC': EQUALITY_CHAR_FILTERS,
    'date_signed': DATE_FILTERS, 
    'completion_date': DATE_FILTERS,
    'obligated_amount': NUM_FILTERS,
    'point_of_contact': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'vendor_phone': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'annual_revenue': NUM_FILTERS, 
    'number_of_employees': NUM_FILTERS
}


class CharInFilter(BaseInFilter, CharFilter):
    pass


class DiscoveryComplexFilterBackend(ComplexFilterBackend):
    operators = {
        '&': QuerySet.intersection,
        '|': QuerySet.union,
        '-': QuerySet.difference,
    }


class NaicsFilter(FilterSet):
    class Meta:
        model = categories.Naics
        fields = NAICS_FIELDS


class SetAsideFilter(FilterSet):
    class Meta:
        model = categories.SetAside
        fields = SETASIDE_FIELDS


class PoolFilter(FilterSet):
    naics = RelatedFilter(NaicsFilter)
    
    class Meta:
        model = categories.Pool
        fields = POOL_FIELDS


class ZoneFilter(FilterSet):
    state = CharFilter(field_name="state__state", lookup_expr='exact')
    state__iexact = CharFilter(field_name="state__state", lookup_expr='iexact')
    state__in = CharInFilter(field_name="state__state", lookup_expr='in')
     
    class Meta:
        model = categories.Zone
        fields = ZONE_FIELDS


class LocationFilter(FilterSet):
    class Meta:
        model = vendors.Location
        fields = LOCATION_FIELDS


class ManagerFilter(FilterSet):

    phone = CharFilter(field_name='phone__number', lookup_expr='exact')
    phone__iexact = CharFilter(field_name='phone__number', lookup_expr='iexact')
    phone__in = CharInFilter(field_name='phone__number', lookup_expr='in')
    phone__contains = CharFilter(field_name='phone__number', lookup_expr='contains')
    phone__icontains = CharFilter(field_name='phone__number', lookup_expr='icontains')
    phone__startswith = CharFilter(field_name='phone__number', lookup_expr='startswith')
    phone__istartswith = CharFilter(field_name='phone__number', lookup_expr='istartswith')
    phone__endswith = CharFilter(field_name='phone__number', lookup_expr='endswith')
    phone__iendswith = CharFilter(field_name='phone__number', lookup_expr='iendswith')
    phone__regex = CharFilter(field_name='phone__number', lookup_expr='regex')
    phone__iregex = CharFilter(field_name='phone__number', lookup_expr='iregex')
    
    email = CharFilter(field_name='email__address', lookup_expr='exact')
    email__iexact = CharFilter(field_name='email__address', lookup_expr='iexact')
    email__in = CharInFilter(field_name='email__address', lookup_expr='in')
    email__contains = CharFilter(field_name='email__address', lookup_expr='contains')
    email__icontains = CharFilter(field_name='email__address', lookup_expr='icontains')
    email__startswith = CharFilter(field_name='email__address', lookup_expr='startswith')
    email__istartswith = CharFilter(field_name='email__address', lookup_expr='istartswith')
    email__endswith = CharFilter(field_name='email__address', lookup_expr='endswith')
    email__iendswith = CharFilter(field_name='email__address', lookup_expr='iendswith')
    email__regex = CharFilter(field_name='email__address', lookup_expr='regex')
    email__iregex = CharFilter(field_name='email__address', lookup_expr='iregex')


class ContractManagerFilter(ManagerFilter):
    class Meta:
        model = vendors.ContractManager
        fields = MANAGER_FIELDS

        
class ProjectManagerFilter(ManagerFilter):
    class Meta:
        model = vendors.ProjectManager
        fields = MANAGER_FIELDS

        
class PoolMembershipFilter(FilterSet):
    pool = RelatedFilter(PoolFilter)
    setasides = RelatedFilter(SetAsideFilter)
    
    zones = RelatedFilter(ZoneFilter)
    
    cms = RelatedFilter(ContractManagerFilter)
    pms = RelatedFilter(ProjectManagerFilter)
    
    class Meta:
        model = vendors.PoolMembership
        fields = POOL_MEMBERSHIP_FIELDS


class VendorFilter(FilterSet):
    sam_location = RelatedFilter(LocationFilter)
    pools = RelatedFilter(PoolMembershipFilter)
    
    sam_activation_date = CharFilter(field_name="sam_activation_date", lookup_expr="startswith")
    sam_expiration_date = CharFilter(field_name="sam_expiration_date", lookup_expr="startswith")
    
    class Meta:
        model = vendors.Vendor
        fields = VENDOR_FIELDS


class ContractStatusFilter(FilterSet):
    class Meta:
        model = contracts.ContractStatus
        fields = CONTRACT_STATUS_FIELDS


class PricingStructureFilter(FilterSet):
    class Meta:
        model = contracts.PricingStructure
        fields = PRICING_STRUCTURE_FIELDS


class PlaceOfPerformanceFilter(FilterSet):
    class Meta:
        model = contracts.PlaceOfPerformance
        fields = PLACE_OF_PERFORMANCE_FIELDS


class ContractFilter(FilterSet): 
    status = RelatedFilter(ContractStatusFilter)
    pricing_type = RelatedFilter(PricingStructureFilter)
    
    place_of_performance = RelatedFilter(PlaceOfPerformanceFilter)
    vendor_location = RelatedFilter(LocationFilter)
    
    vendor = RelatedFilter(VendorFilter)
    
    class Meta:
        model = contracts.Contract
        fields = CONTRACT_FIELDS
