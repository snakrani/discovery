from django.db.models import Q

from django_filters.constants import EMPTY_VALUES
from django_filters.fields import Lookup
from django_filters.rest_framework import (
    FilterSet,
    BooleanFilter,
    NumberFilter,
    CharFilter,
    DateFilter
)

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts


EQUALITY_BOOL_FILTERS = [
    'exact',
    'not_exact'
]

EQUALITY_CHAR_FILTERS = [
    'iexact',
    'exact', 
    'inot_exact',
    'not_exact'
]

FUZZY_CHAR_FILTERS = [
    'icontains',
    'contains',
    'inot_contains',
    'not_contains',
    'istartswith', 
    'startswith',
    'iendswith',
    'endswith'
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
    
    id = CharFilter(field_name="id", label="Pool ID (id)", lookup_expr=EQUALITY_CHAR_FILTERS)
    name = CharFilter(field_name="name", label="Pool name (name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    number = NumberFilter(field_name="number", label="Pool number (number)", lookup_expr=NUM_FILTERS)
    vehicle = CharFilter(field_name="vehicle", label="Pool vehicle ID (vehicle)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    threshold = CharFilter(field_name="threshold", label="Pool threshold (threshold)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)   
    
    naics_code = CharFilter(field_name='naics__code', label="Pool NAICS code (naics_code)", lookup_expr=EQUALITY_CHAR_FILTERS)
    naics_root_code = CharFilter(field_name='naics__root_code', label="Pool NAICS root code (naics_root_code)", lookup_expr=EQUALITY_CHAR_FILTERS)
    naics_description = CharFilter(field_name='naics__description', label="Pool NAICS description (naics_description)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    
    class Meta:
        model = categories.Pool
        fields = [
            'id', 'name', 'number', 'vehicle', 'threshold', 
            'naics_code', 'naics_root_code', 'naics_description'
        ]


class ZoneFilter(FilterSet):
    
    id = NumberFilter(field_name="id", label="Zone ID (id)", lookup_expr=NUM_FILTERS)
    state = CharFilter(field_name="state__state", label="Zone state (state)", lookup_expr=EQUALITY_CHAR_FILTERS)
     
    class Meta:
        model = categories.Zone
        fields = ['id', 'state']


class VendorFilter(FilterSet):
    
    id = CharFilter(field_name="id", label="Vendor ID (id)", lookup_expr=EQUALITY_CHAR_FILTERS)
    name = CharFilter(field_name="name", label="Vendor name (name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    duns = NumberFilter(field_name="duns", label="Vendor DUNS number (duns)", lookup_expr=NUM_FILTERS)
    cage = CharFilter(field_name="cage", label="Vendor CAGE code (cage)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    
    sam_status = CharFilter(field_name="sam_status", label="Vendor SAM status (sam_status)", lookup_expr=EQUALITY_CHAR_FILTERS)
    sam_activation_date = DateFilter(field_name="sam_activation_date", label="Vendor SAM activation date (sam_activation_date)", lookup_expr=NUM_FILTERS)
    sam_expiration_date = DateFilter(field_name="sam_expiration_date", label="Vendor SAM expiration date (sam_expiration_date)", lookup_expr=NUM_FILTERS)
    sam_exclusion = BooleanFilter(field_name="sam_exclusion", label="Vendor SAM exclusion (sam_exclusion)", lookup_expr=EQUALITY_BOOL_FILTERS)
    sam_url = CharFilter(field_name="sam_url", label="Vendor SAM URL (sam_url)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    
    annual_revenue = NumberFilter(field_name="annual_revenue", label="Annual revenue (annual_revenue)", lookup_expr=NUM_FILTERS)
    number_of_employees = NumberFilter(field_name="number_of_employees", label="Employee count (number_of_employees)", lookup_expr=NUM_FILTERS)
    number_of_contracts = NumberFilter(field_name="number_of_contracts", label="Contract count (number_of_contracts)", lookup_expr=NUM_FILTERS)
    
    sam_address = CharFilter(field_name="sam_location__address", label="SAM address (sam_address)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    sam_city = CharFilter(field_name="sam_location__city", label="SAM city (sam_city)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    sam_state = CharFilter(field_name="sam_location__state", label="SAM state (sam_state)", lookup_expr=EQUALITY_CHAR_FILTERS)
    sam_zipcode = NumberFilter(field_name="sam_location__zipcode", label="SAM zipcode (sam_zipcode)", lookup_expr=NUM_FILTERS)
    sam_congressional_district = CharFilter(field_name="sam_location__congressional_district (sam_congressional_district)", label="SAM congressional district", lookup_expr=EQUALITY_CHAR_FILTERS)
     
    cm_name = CharFilter(field_name='managers__name', method='filter_cm', label="Contract manager name (cm_name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    cm_phone = CharFilter(field_name='managers__phone', method='filter_cm', label="Contract manager phone (cm_phone)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    cm_email = CharFilter(field_name='managers__email', method='filter_cm', label="Contract manager email (cm_email)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    
    pm_name = CharFilter(field_name='managers__name', method='filter_pm', label="Project manager name (pm_name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    pm_phone = CharFilter(field_name='managers__phone', method='filter_pm', label="Project manager phone (pm_phone)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    pm_email = CharFilter(field_name='managers__email', method='filter_pm', label="Project manager email (pm_email)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    
    pool_id = CharFilter(field_name='pools__id', label="Pool ID (pool_id)", lookup_expr=EQUALITY_CHAR_FILTERS)
    pool_name = CharFilter(field_name='pools__name', label="Pool name (pool_name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    pool_number = NumberFilter(field_name="pools__number", label="Pool number (pool_number)", lookup_expr=NUM_FILTERS)
    pool_vehicle = CharFilter(field_name='pools__vehicle', label="Pool vehicle (pool_vehicle)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    pool_threshold = CharFilter(field_name='pools__threshold', label="Pool threshold (pool_threshold)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    pool_naics_code = CharFilter(field_name='pools__naics__code', label="Pool NAICS code (pool_naics_code)", lookup_expr=EQUALITY_CHAR_FILTERS)
    pool_naics_root_code = CharFilter(field_name='pools__naics__root_code', label="Pool NAICS root code (pool_naics_root_code)", lookup_expr=EQUALITY_CHAR_FILTERS)
    pool_naics_description = CharFilter(field_name='pools__naics__description', label="Pool NAICS description (pool_naics_description)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    
    setaside_code = CharFilter(field_name='setasides__code', label="Setaside code (setaside_code)", lookup_expr=EQUALITY_CHAR_FILTERS)
    setaside_name = CharFilter(field_name='setasides__name', label="Setaside name (setaside_name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    setaside_description = CharFilter(field_name='setasides__description', label="Setaside description (setaside_description)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
         
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
    
    id = NumberFilter(field_name="id", label="Internal contract ID (id)", lookup_expr=NUM_FILTERS)
    piid = NumberFilter(field_name="piid", label="Vendor PIID (piid)", lookup_expr=NUM_FILTERS)
    agency_id = CharFilter(field_name="agency_id", label="Agency ID (agency_id)", lookup_expr=EQUALITY_CHAR_FILTERS)
    agency_name = CharFilter(field_name="agency_name", label="Agency name (agency_name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    
    naics = CharFilter(field_name='NAICS', label="Contract NAICS code (naics)", lookup_expr=EQUALITY_CHAR_FILTERS)
    psc = CharFilter(field_name='PSC', label="Contract NAICS code (psc)", lookup_expr=EQUALITY_CHAR_FILTERS)
    
    date_signed = DateFilter(field_name='date_signed', label="Contract signed date (date_signed)", lookup_expr=EQUALITY_CHAR_FILTERS)
    completion_date = DateFilter(field_name='completion_date', label="Contract completed date (completion_date)", lookup_expr=EQUALITY_CHAR_FILTERS)

    pricing_type_code = CharFilter(field_name='pricing_type__code', label="Pricing structure code (pricing_type_code)", lookup_expr=EQUALITY_CHAR_FILTERS)
    pricing_type_name = CharFilter(field_name='pricing_type__name', label="Pricing structure name (pricing_type_name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    obligated_amount = NumberFilter(field_name="obligated_amount", label="Obligated amount (obligated_amount)", lookup_expr=NUM_FILTERS)
    point_of_contact = CharFilter(field_name="point_of_contact", label="Point of contact (point_of_contact)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    
    vendor_id = NumberFilter(field_name="vendor__id", label="Internal vendor ID (vendor_id)", lookup_expr=NUM_FILTERS)
    vendor_name = CharFilter(field_name="vendor__name", label="Vendor name (vendor_name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    vendor_duns = CharFilter(field_name="vendor__duns", label="Vendor DUNS number (vendor_duns)", lookup_expr=NUM_FILTERS)
    vendor_cage = CharFilter(field_name="vendor__cage", label="Vendor CAGE code (vendor_cage)", lookup_expr=EQUALITY_CHAR_FILTERS)
    vendor_sam_status = CharFilter(field_name='vendor__sam_status', label="Vendor SAM status (vendor_sam_status)", lookup_expr=EQUALITY_CHAR_FILTERS)
    vendor_sam_activation_date = DateFilter(field_name='vendor__sam_activation_date', label="Vendor SAM activation date (vendor_sam_activation_date)", lookup_expr=EQUALITY_CHAR_FILTERS)
    vendor_sam_expiration_date = DateFilter(field_name='vendor__sam_expiration_date', label="Vendor SAM expiration date (vendor_sam_expiration_date)", lookup_expr=EQUALITY_CHAR_FILTERS)
    
    vendor_phone = CharFilter(field_name="vendor_phone", label="Vendor phone (vendor_phone)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS) 
    
    annual_revenue = NumberFilter(field_name="annual_revenue", label="Annual revenue (annual_revenue)", lookup_expr=NUM_FILTERS)
    number_of_employees = NumberFilter(field_name="number_of_employees", label="Employee count (number_of_employees)", lookup_expr=NUM_FILTERS)
    
    vendor_address = CharFilter(field_name="vendor_location__address", label="Vendor address (vendor_address)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    vendor_city = CharFilter(field_name="vendor_location__city", label="Vendor city (vendor_city)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    vendor_state = CharFilter(field_name="vendor_location__state", label="Vendor state (vendor_state)", lookup_expr=EQUALITY_CHAR_FILTERS)
    vendor_zipcode = NumberFilter(field_name="vendor_location__zipcode", label="Vendor zipcode (vendor_zipcode)", lookup_expr=NUM_FILTERS)
    vendor_congressional_district = CharFilter(field_name="vendor_location__congressional_district", label="Vendor congressional district (vendor_congressional_district)", lookup_expr=EQUALITY_CHAR_FILTERS)
    
    pop_country_code = CharFilter(field_name="place_of_performance__country_code", label="Primary place of performance country code (pop_country_code)", lookup_expr=EQUALITY_CHAR_FILTERS)
    pop_country_name = CharFilter(field_name="place_of_performance__country_name", label="Primary place of performance country name (pop_country_name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
    pop_state = CharFilter(field_name="place_of_performance__state", label="Primary place of performance state (pop_state)", lookup_expr=EQUALITY_CHAR_FILTERS)
    pop_zipcode = NumberFilter(field_name="place_of_performance__zipcode", label="Primary place of performance zipcode (pop_zipcode)", lookup_expr=NUM_FILTERS)
    
    status_id = NumberFilter(field_name="status__id", label="Contract status ID (status_id)", lookup_expr=NUM_FILTERS)
    status_name = CharFilter(field_name="status__name", label="Contract status name (status_name)", lookup_expr=FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS)
         
    class Meta:
        model = contracts.Contract
        fields = [
            'id', 'piid', 'agency_id', 'agency_name', 'naics', 'psc',
            'date_signed', 'completion_date',
            'pricing_type_code', 'pricing_type_name', 'obligated_amount',
            'point_of_contact', 'vendor_phone', 'vendor_id', 'vendor_name', 'vendor_duns', 'vendor_cage',   
            'vendor_sam_status', 'vendor_sam_activation_date', 'vendor_sam_expiration_date', 
            'annual_revenue', 'number_of_employees',
            'vendor_address', 'vendor_city', 'vendor_state', 'vendor_zipcode', 'vendor_congressional_district', 
            'pop_country_code', 'pop_country_name', 'pop_state', 'pop_zipcode',
            'status_id', 'status_name'
        ]
