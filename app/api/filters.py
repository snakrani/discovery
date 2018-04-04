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
    
    _fuzzy_text = ('code', 'root_code', 'description')
    
    class Meta:
        model = categories.Naics
        fields = ()


class PscFilter(FilterSet, metaclass = MetaFilterSet):
    
    _fuzzy_text = ('code', 'description', 'naics_code')
    
    class Meta:
        model = categories.PSC
        fields = ()


class PoolFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('id', 'number')
    _fuzzy_text = ('name','vehicle', 'threshold')
    
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
    
    _token_text = ('state:state__state',)
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


class ManagerFilter(FilterSet, metaclass = MetaFilterSet):   
    _fuzzy_text = ('name', 'phone:phones__number', 'email:emails__address')


class ContractManagerFilter(ManagerFilter):
    class Meta:
        model = vendors.ContractManager
        fields = ()

        
class ProjectManagerFilter(ManagerFilter):
    class Meta:
        model = vendors.ProjectManager
        fields = ()

        
class PoolMembershipFilter(FilterSet, metaclass = MetaFilterSet):
    
    _fuzzy_text = ('piid',)
    
    pool = RelatedFilter(PoolFilter)
    setasides = RelatedFilter(SetAsideFilter)
    
    zones = RelatedFilter(ZoneFilter)
    
    cms = RelatedFilter(ContractManagerFilter)
    pms = RelatedFilter(ProjectManagerFilter)
    
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
    
    class Meta:
        model = vendors.Vendor
        fields = ()


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
    _fuzzy_text = ('piid', 'agency_name', 'NAICS', 'PSC', 'point_of_contact', 'vendor_phone')
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
        psc_codes = list(categories.PSC.objects.filter(naics_code=re.sub(r'[^\d]+$', '', value)).values_list('code', flat=True))
        
        if len(psc_codes) > 0:
            return qs.filter(PSC__in=psc_codes)
        else:
            return qs