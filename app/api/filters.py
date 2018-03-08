from rest_framework_filters.filterset import FilterSet
from rest_framework_filters.filters import NumberFilter, CharFilter, RelatedFilter

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
    'in'
]

NUM_FILTERS = [
    'exact', 
    'lt',
    'lte', 
    'gt', 
    'gte',
    'in'
]


class NaicsFilter(FilterSet):
    class Meta:
        model = categories.Naics
        fields = {
            'code': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
            'root_code': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
            'description': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
        }


class SetAsideFilter(FilterSet):
    class Meta:
        model = categories.SetAside
        fields = {
            'code': EQUALITY_CHAR_FILTERS, 
            'name': EQUALITY_CHAR_FILTERS, 
            'description': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
            'far_order': NUM_FILTERS
        }


class PoolFilter(FilterSet):
    naics = RelatedFilter(NaicsFilter, name='naics', queryset=categories.Naics.objects.all())
    
    class Meta:
        model = categories.Pool
        fields = {
            'id': EQUALITY_CHAR_FILTERS, 
            'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
            'number': NUM_FILTERS, 
            'vehicle': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
            'threshold': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
        }


class ZoneFilter(FilterSet):
    state = CharFilter(name="state__state")
     
    class Meta:
        model = categories.Zone
        fields = {
            'id': NUM_FILTERS,
            'state': EQUALITY_CHAR_FILTERS
        }


class LocationFilter(FilterSet):
    class Meta:
        model = vendors.Location
        fields = {
            'address': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
            'city': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
            'state': EQUALITY_CHAR_FILTERS,
            'zipcode': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
            'congressional_district': EQUALITY_CHAR_FILTERS
        }


class ManagerFilter(FilterSet):
    phone = CharFilter(name='phone__number')
    email = CharFilter(name='email__address')
    
    class Meta:
        model = vendors.Manager
        fields = {
            'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS, 
            'type': EQUALITY_CHAR_FILTERS,
            'phone': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
            'email': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
        }


class VendorFilter(FilterSet):
    sam_location = RelatedFilter(LocationFilter, name='sam_location', queryset=vendors.Location.objects.all())
    
    setasides = RelatedFilter(SetAsideFilter, name='setasides', queryset=categories.SetAside.objects.all())
    pools = RelatedFilter(PoolFilter, name='pools', queryset=categories.Pool.objects.all())
    
    managers = RelatedFilter(ManagerFilter, name='managers', queryset=vendors.Manager.objects.all())
    
    class Meta:
        model = vendors.Vendor
        fields = {
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


class ContractStatusFilter(FilterSet):
    class Meta:
        model = contracts.ContractStatus
        fields = {
            'code': EQUALITY_CHAR_FILTERS, 
            'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
        }


class PricingStructureFilter(FilterSet):
    class Meta:
        model = contracts.PricingStructure
        fields = {
            'code': EQUALITY_CHAR_FILTERS, 
            'name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
        }


class PlaceOfPerformanceFilter(FilterSet):
    class Meta:
        model = contracts.PlaceOfPerformance
        fields = {
            'country_code': EQUALITY_CHAR_FILTERS, 
            'country_name': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS,
            'state': EQUALITY_CHAR_FILTERS,
            'zipcode': FUZZY_CHAR_FILTERS + EQUALITY_CHAR_FILTERS
        }


class ContractFilter(FilterSet): 
    status = RelatedFilter(ContractStatusFilter, name='status', queryset=contracts.ContractStatus.objects.all())
    pricing_type = RelatedFilter(PricingStructureFilter, name='pricing_type', queryset=contracts.PricingStructure.objects.all())
    
    place_of_performance = RelatedFilter(PlaceOfPerformanceFilter, name='place_of_performance', queryset=contracts.PlaceOfPerformance.objects.all())
    vendor_location = RelatedFilter(LocationFilter, name='vendor_location', queryset=vendors.Location.objects.all())
    
    vendor = RelatedFilter(VendorFilter, name='vendor', queryset=vendors.Vendor.objects.all())
    
    class Meta:
        model = contracts.Contract
        fields = {
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
