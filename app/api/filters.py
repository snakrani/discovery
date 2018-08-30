from django.db.models import Q
from django.db.models.query import QuerySet

from rest_framework.fields import CharField, IntegerField

from rest_framework_filters.filterset import FilterSet, FilterSetMetaclass
from rest_framework_filters.filters import BooleanFilter, NumberFilter, CharFilter, DateFilter, DateTimeFilter, RelatedFilter, BaseInFilter, BaseRangeFilter
from rest_framework_filters.backends import ComplexFilterBackend

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts

import re


class CharInFilter(BaseInFilter, CharFilter):
    pass

class CharRangeFilter(BaseRangeFilter, CharFilter):
    pass

class NumberInFilter(BaseInFilter, NumberFilter):
    pass

class NumberRangeFilter(BaseRangeFilter, NumberFilter):
    pass


class DiscoveryComplexFilterBackend(ComplexFilterBackend):
    operators = {
        '&': QuerySet.intersection,
        '|': QuerySet.union,
        '-': QuerySet.difference,
    }


class MetaFilterSet(FilterSetMetaclass):
    
    def __new__(cls, name, bases, attr):
        
        def _generate_filters(id):
            if id in attr and attr[id]:
                for field in list(attr[id]):
                    components = field.split(':')
                    
                    if len(components) > 1:
                        info = {'name': components[0], 'field': components[1]}
                    else:
                        info = {'name': field, 'field': field}
                    
                    getattr(cls, "{}_filters".format(id))(info, attr)
                    
            if id in attr.keys():
                attr.pop(id)
        
        _generate_filters('_boolean')            
        _generate_filters('_token_text')
        _generate_filters('_fuzzy_text')
        _generate_filters('_number_text')
        _generate_filters('_number')
        _generate_filters('_date_time')
        
        return super(MetaFilterSet, cls).__new__(cls, name, bases, attr)

    
    @classmethod
    def _boolean_filters(cls, info, filters):
        name = info['name']
        field = info['field']
        
        filters[name] = BooleanFilter(field_name = field, lookup_expr='exact')
    
    @classmethod
    def _token_text_filters(cls, info, filters):
        name = info['name']
        field = info['field']
        
        filters[name] = CharFilter(field_name = field, lookup_expr='exact')
        filters['{}__in'.format(name)] = CharInFilter(field_name = field)
        
        for lookup in ('iexact',):
            filters['{}__{}'.format(name, lookup)] = CharFilter(field_name = field, lookup_expr = lookup)
        
    @classmethod
    def _fuzzy_text_filters(cls, info, filters):
        name = info['name']
        field = info['field']
        
        filters[name] = CharFilter(field_name = field, lookup_expr='exact')
        filters['{}__in'.format(name)] = CharInFilter(field_name = field)
        
        for lookup in ('iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith', 'regex', 'iregex'):
            filters['{}__{}'.format(name, lookup)] = CharFilter(field_name = field, lookup_expr = lookup)
    
    @classmethod
    def _number_filters(cls, info, filters):
        name = info['name']
        field = info['field']
        
        filters[name] = NumberFilter(field_name = field, lookup_expr='exact')
        filters['{}__range'.format(name)] = NumberRangeFilter(field_name = field)
        filters['{}__in'.format(name)] = NumberInFilter(field_name = field)
        
        for lookup in ('lt', 'lte', 'gt', 'gte'):
            filters['{}__{}'.format(name, lookup)] = NumberFilter(field_name = field, lookup_expr = lookup)
        
    @classmethod
    def _number_text_filters(cls, info, filters):
        name = info['name']
        field = info['field']
        
        filters[name] = CharFilter(field_name = field, lookup_expr='exact')
        filters['{}__range'.format(name)] = CharRangeFilter(field_name = field)
        filters['{}__in'.format(name)] = CharInFilter(field_name = field)
        
        for lookup in ('lt', 'lte', 'gt', 'gte'):
            filters['{}__{}'.format(name, lookup)] = CharFilter(field_name = field, lookup_expr = lookup)

    @classmethod
    def _date_time_filters(cls, info, filters):
        name = info['name']
        field = info['field']
        
        filters[name] = CharFilter(field_name = field, lookup_expr='startswith')
        
        for lookup in ('year', 'month', 'day', 'week', 'week_day', 'quarter'):
            filters['{}__{}'.format(name, lookup)] = NumberFilter(field_name = field, lookup_expr = lookup)
        

class NaicsFilter(FilterSet, metaclass = MetaFilterSet):
    
    _fuzzy_text = ('code', 'description', 'sin__code', 'keywords__name')
    
    class Meta:
        model = categories.Naics
        fields = ()


class PscFilter(FilterSet, metaclass = MetaFilterSet):
    
    _fuzzy_text = ('code', 'description', 'sin__code', 'keywords__name')
    
    naics = RelatedFilter(NaicsFilter)
    
    class Meta:
        model = categories.PSC
        fields = ()


class VehicleFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('id',)
    _fuzzy_text = ('name',)
    _boolean = ('small_business', 'numeric_pool', 'display_number')
    
    class Meta:
        model = categories.Vehicle
        fields = ()


class PoolFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('id', 'number')
    _fuzzy_text = ('name', 'threshold')
    
    vehicle = RelatedFilter(VehicleFilter)
    naics = RelatedFilter(NaicsFilter)
    
    class Meta:
        model = categories.Pool
        fields = ()


class SetAsideFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('code', 'name')
    _fuzzy_text = ('description',)
    _number = ('far_order',)

    class Meta:
        model = categories.SetAside
        fields = ()


class ZoneFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('states__code',)
    _number = ('id',)
    
    class Meta:
        model = categories.Zone
        fields = ()


class LocationFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('state', 'congressional_district')
    _fuzzy_text = ('address', 'city', 'zipcode')
    
    class Meta:
        model = vendors.Location
        fields = ()


class ContactFilter(FilterSet, metaclass = MetaFilterSet):   
    
    _fuzzy_text = ('name', 'phones__number', 'emails__address')
    _number = ('order',)
    
    class Meta:
        model = vendors.Contact
        fields = ()

        
class PoolMembershipFilter(FilterSet, metaclass = MetaFilterSet):
    
    _fuzzy_text = ('piid',)
    _date_time = ('expiration_8a_date', 'contract_end_date')
    
    pool = RelatedFilter(PoolFilter)
    setasides = RelatedFilter(SetAsideFilter)
    
    zones = RelatedFilter(ZoneFilter)
    contacts = RelatedFilter(ContactFilter)
    
    class Meta:
        model = vendors.PoolMembership
        fields = ()


class VendorFilter(FilterSet, metaclass = MetaFilterSet):
    
    _boolean = ('sam_exclusion',)
    _token_text = ('cage', 'sam_status')
    _fuzzy_text = ('name', 'sam_url')
    _number_text = ('duns',)
    _date_time = ('sam_activation_date', 'sam_expiration_date')
    
    sam_location = RelatedFilter(LocationFilter)
    pools = RelatedFilter(PoolMembershipFilter)
    
    setasides = CharFilter(field_name='setasides', method='filter_setasides')
    
    class Meta:
        model = vendors.Vendor
        fields = ()
        
    def filter_setasides(self, qs, name, value):
        setaside_query = Q()
        pool_ids = []
                
        for code in value.split(','):
            setaside_query.add(Q(setasides__code=code), Q.AND)
        
        memberships = vendors.PoolMembership.objects.filter(setaside_query)
        
        if 'pools__pool__id__in' in self.request.query_params:
            pool_ids = self.request.query_params['pools__pool__id__in'].split(',')
        elif 'pool' in self.request.query_params:
            pool_ids = self.request.query_params['pool'].split(',')
        
        if len(pool_ids):
            memberships = memberships.filter(pool__id__in=pool_ids)
        
        piids = memberships.values_list('piid', flat=True)
        
        if len(piids) > 0:
            qs = qs.filter(pools__piid__in=piids)
        else:
            qs = qs.filter(pools__piid=0)
        
        return qs


class ContractStatusFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('code',)
    _fuzzy_text = ('name',)
    
    class Meta:
        model = contracts.ContractStatus
        fields = ()


class PricingStructureFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('code',)
    _fuzzy_text = ('name',)
   
    class Meta:
        model = contracts.PricingStructure
        fields = ()


class PlaceOfPerformanceFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('country_code', 'state')
    _fuzzy_text = ('country_name', 'zipcode')
    
    class Meta:
        model = contracts.PlaceOfPerformance
        fields = ()


class ContractFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('agency_id',)
    _fuzzy_text = ('piid', 'base_piid', 'agency_name', 'NAICS', 'PSC', 'point_of_contact', 'vendor_phone')
    _number = ('id', 'obligated_amount', 'annual_revenue', 'number_of_employees')
    _date_time = ('date_signed', 'completion_date')
    
    status = RelatedFilter(ContractStatusFilter)
    pricing_type = RelatedFilter(PricingStructureFilter)
        
    vendor = RelatedFilter(VendorFilter)
    vendor_location = RelatedFilter(LocationFilter)
    
    place_of_performance = RelatedFilter(PlaceOfPerformanceFilter)
    
    psc_naics = CharFilter(field_name='NAICS', method='filter_psc_naics')
        
    class Meta:
        model = contracts.Contract
        fields = ()
        
    def filter_psc_naics(self, qs, name, value):
        naics_code = re.sub(r'[^\d]+$', '', value)
        psc_codes = list(categories.PSC.objects.filter(naics__code=naics_code).distinct().values_list('code', flat=True))
        
        return qs.filter(Q(PSC__in=psc_codes) | Q(NAICS=naics_code))
