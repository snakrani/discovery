from django.db.models.query import QuerySet

from rest_framework.fields import CharField, IntegerField

from rest_framework_filters.filterset import FilterSet
from rest_framework_filters.filters import NumberFilter, CharFilter, RelatedFilter, BaseInFilter
from rest_framework_filters.backends import ComplexFilterBackend

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts


EQUALITY_BOOL_FILTERS = [
    'exact',
    'isnull'
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
    'quarter',
    'range',
    'in'
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
    'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'type': EQUALITY_CHAR_FILTERS,
    'phone': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
    'email': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
}

VENDOR_FIELDS = {
    'id': NUM_FILTERS, 
    'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
    'duns': EQUALITY_CHAR_FILTERS, 
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
    phone = CharFilter(field_name='phone__number')
    email = CharFilter(field_name='email__address')
    
    class Meta:
        model = vendors.Manager
        fields = MANAGER_FIELDS


class VendorFilter(FilterSet):
    sam_location = RelatedFilter(LocationFilter)
    
    setasides = RelatedFilter(SetAsideFilter)
    pools = RelatedFilter(PoolFilter)
    
    managers = RelatedFilter(ManagerFilter)
    
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
