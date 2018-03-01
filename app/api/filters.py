from django.db.models import Q

from django_filters.constants import EMPTY_VALUES
from django_filters.fields import Lookup
from django_filters.rest_framework import (
    FilterSet,
    BooleanFilter,
    NumberFilter,
    CharFilter,
    DateTimeFilter
)

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts


EQUALITY_BOOL_FILTERS = [
    'exact',
    'not_exact'
]

EQUALITY_CHAR_FILTERS = [
    'exact', 
    'iexact', 
    'not_exact',
    'inot_exact',
]

FUZZY_CHAR_FILTERS = [
    'contains',
    'icontains',
    'not_contains',
    'inot_contains', 
    'startswith',
    'istartswith',
    'endswith',
    'iendswith'
]

NUM_FILTERS = [
    'exact',
    'not_exact', 
    'lt',
    'lte', 
    'gt', 
    'gte',
]


def filter_queryset(queryset, field_name, value):
    if isinstance(value, Lookup):
        lookup = str(value.lookup_type)
        value = value.value
    else:
        lookup = self.lookup_expr
    
    if value in EMPTY_VALUES:
        return queryset
    
    return queryset.filter(**{'%s__%s' % (field_name, lookup): value})


class PoolFilter(FilterSet):
    
    id = CharFilter(field_name="id", label="Pool ID", lookup_expr=EQUALITY_CHAR_FILTERS)
    name = CharFilter(field_name="name", label="Pool name", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    number = NumberFilter(field_name="number", label="Pool number", lookup_expr=NUM_FILTERS)
    vehicle = CharFilter(field_name="vehicle", label="Pool vehicle ID", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    threshold = CharFilter(field_name="threshold", label="Pool threshold", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)   
    
    naics_code = CharFilter(field_name='naics__code', label="Pool NAICS code", lookup_expr=EQUALITY_CHAR_FILTERS)
    naics_root_code = CharFilter(field_name='naics__root_code', label="Pool NAICS root code", lookup_expr=EQUALITY_CHAR_FILTERS)
    naics_description = CharFilter(field_name='naics__description', label="Pool NAICS description", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    
    class Meta:
        model = categories.Pool
        fields = [
            'id', 'name', 'number', 'vehicle', 'threshold', 
            'naics_code', 'naics_root_code', 'naics_description'
        ]


class ZoneFilter(FilterSet):
    id = NumberFilter(field_name="id", label="Zone ID", lookup_expr=NUM_FILTERS)
    state = CharFilter(field_name="state__state", label="Zone state", lookup_expr=EQUALITY_CHAR_FILTERS)
     
    class Meta:
        model = categories.Zone
        fields = ['id', 'state']


class VendorFilter(FilterSet):
    
    id = CharFilter(field_name="id", label="Vendor ID", lookup_expr=EQUALITY_CHAR_FILTERS)
    name = CharFilter(field_name="name", label="Vendor name", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    duns = NumberFilter(field_name="duns", label="Vendor DUNS number", lookup_expr=NUM_FILTERS)
    cage = CharFilter(field_name="cage", label="Vendor CAGE code", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    
    sam_status = CharFilter(field_name="sam_status", label="Vendor SAM status", lookup_expr=EQUALITY_CHAR_FILTERS)
    sam_activation_date = DateTimeFilter(field_name="sam_activation_date", label="Vendor SAM activation date", lookup_expr=NUM_FILTERS)
    sam_expiration_date = NumberFilter(field_name="sam_expiration_date", label="Vendor SAM expiration date", lookup_expr=NUM_FILTERS)
    sam_exclusion = BooleanFilter(field_name="sam_exclusion", label="Vendor SAM exclusion", lookup_expr=EQUALITY_BOOL_FILTERS)
    sam_url = CharFilter(field_name="sam_url", label="Vendor SAM URL", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    
    annual_revenue = NumberFilter(field_name="annual_revenue", label="Annual revenue (most recent)", lookup_expr=NUM_FILTERS)
    number_of_employees = NumberFilter(field_name="number_of_employees", label="Employee count (most recent)", lookup_expr=NUM_FILTERS)
    number_of_contracts = NumberFilter(field_name="number_of_contracts", label="Contract count (total or filtered by NAICS if pools naics root code specified)", lookup_expr=NUM_FILTERS)
    
    sam_address = CharFilter(field_name="sam_location__address", label="SAM address", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    sam_city = CharFilter(field_name="sam_location__city", label="SAM city", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    sam_state = CharFilter(field_name="sam_location__state", label="SAM state", lookup_expr=EQUALITY_CHAR_FILTERS)
    sam_zipcode = NumberFilter(field_name="sam_location__zipcode", label="SAM zipcode", lookup_expr=NUM_FILTERS)
    sam_congressional_district = CharFilter(field_name="sam_location__congressional_district", label="SAM congressional district", lookup_expr=EQUALITY_CHAR_FILTERS)
     
    cm_name = CharFilter(field_name='managers__name', method='filter_cm', label="Contract manager name", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    cm_phone = CharFilter(field_name='managers__phone', method='filter_cm', label="Contract manager phone", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    cm_email = CharFilter(field_name='managers__email', method='filter_cm', label="Contract manager email", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    
    pm_name = CharFilter(field_name='managers__name', method='filter_pm', label="Project manager name", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    pm_phone = CharFilter(field_name='managers__phone', method='filter_pm', label="Project manager phone", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    pm_email = CharFilter(field_name='managers__email', method='filter_pm', label="Project manager email", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    
    pool_id = CharFilter(field_name='pools__id', label="Pool ID", lookup_expr=EQUALITY_CHAR_FILTERS)
    pool_name = CharFilter(field_name='pools__name', label="Pool name", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    pool_number = NumberFilter(field_name="pools__number", label="Pool number", lookup_expr=NUM_FILTERS)
    pool_vehicle = CharFilter(field_name='pools__vehicle', label="Pool vehicle", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    pool_threshold = CharFilter(field_name='pools__threshold', label="Pool threshold", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    pool_naics_code = CharFilter(field_name='pools__naics__code', label="Pool NAICS code", lookup_expr=EQUALITY_CHAR_FILTERS)
    pool_naics_root_code = CharFilter(field_name='pools__naics__root_code', label="Pool NAICS root code", lookup_expr=EQUALITY_CHAR_FILTERS)
    pool_naics_description = CharFilter(field_name='pools__naics__description', label="Pool NAICS description", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    
    setaside_code = CharFilter(field_name='setasides__code', label="Setaside code", lookup_expr=EQUALITY_CHAR_FILTERS)
    setaside_name = CharFilter(field_name='setasides__name', label="Setaside name", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
    setaside_description = CharFilter(field_name='setasides__description', label="Setaside description", lookup_expr=EQUALITY_CHAR_FILTERS + FUZZY_CHAR_FILTERS)
         
    class Meta:
        model = vendors.Vendor
        fields = [
            'id', 'name', 'duns', 'cage', 'sam_status', 
            'sam_activation_date', 'sam_expiration_date', 'sam_exclusion', 
            'sam_url', 'sam_address', 'sam_city', 'sam_state', 
            'sam_zipcode', 'sam_congressional_district',
            'annual_revenue', 'number_of_employees', 'number_of_contracts',
            'cm_name', 'cm_phone', 'cm_email',
            'pm_name', 'pm_phone', 'pm_email',
            'setaside_code', 'setaside_name', 'setaside_description',
            'pool_id', 'pool_name', 'pool_number', 'pool_vehicle', 'pool_threshold',
            'pool_naics_code', 'pool_naics_root_code', 'pool_naics_description'
        ]
       
    def filter_cm(self, queryset, name, value):
        return filter_queryset(queryset.filter(managers__type="CM"), name, value)
    
    def filter_pm(self, queryset, name, value):
        return filter_queryset(queryset.filter(managers__type="PM"), name, value)


class ContractFilter(FilterSet):
    pass
