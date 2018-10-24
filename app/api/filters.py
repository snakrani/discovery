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
    
    _fuzzy_text = ('code', 'description', 'sin__code')
    
    class Meta:
        model = categories.Naics
        fields = ()


class PscFilter(FilterSet, metaclass = MetaFilterSet):
    
    _fuzzy_text = ('code', 'description', 'sin__code')
    
    class Meta:
        model = categories.PSC
        fields = ()


class KeywordFilter(FilterSet, metaclass = MetaFilterSet):
    
    _number = ('id', 'parent__id')
    _fuzzy_text = ('name', 'parent__name', 'calc', 'sin__code')

    naics = RelatedFilter(NaicsFilter)
    psc = RelatedFilter(PscFilter)
    
    class Meta:
        model = categories.Keyword
        fields = ()


class VehicleFilter(FilterSet, metaclass = MetaFilterSet):
    
    _number = ('tier__number',)
    _token_text = ('id',)
    _fuzzy_text = ('name', 'poc', 'ordering_guide', 'tier__name')
    _boolean = ('small_business', 'numeric_pool', 'display_number')
    
    class Meta:
        model = categories.Vehicle
        fields = ()


class PoolFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('id', 'number')
    _fuzzy_text = ('name', 'threshold')
    
    vehicle = RelatedFilter(VehicleFilter)
    naics = RelatedFilter(NaicsFilter)
    psc = RelatedFilter(PscFilter)
    keywords = RelatedFilter(KeywordFilter)
    
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
    
    contract = RelatedFilter("ContractBaseFilter")
    
    setasides = CharFilter(field_name='setasides', method='filter_setasides')
    
    class Meta:
        model = vendors.Vendor
        fields = ()
        
    def filter_setasides(self, qs, name, value):
        value_components = value.split(':')
        setasides = value_components[0].split(',')
        pool_ids = value_components[1].split(',') if len(value_components) > 1 else []

        if len(pool_ids):
            ids = list(vendors.PoolMembership.objects.filter(pool__id__in=pool_ids).values_list('id', flat=True))
        else:
            ids = []

        for code in setasides:
            if len(ids):
                memberships = vendors.PoolMembership.objects.filter(setasides__code=code, id__in=ids)
            else:
                memberships = vendors.PoolMembership.objects.filter(setasides__code=code)

            setaside_ids = list(memberships.values_list('id', flat=True))
            ids = list(set(ids) & set(setaside_ids))

        if len(ids) > 0:
            qs = qs.filter(pools__id__in=ids)
        else:
            qs = qs.filter(pools__id=0)
        
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
    _number = ('id',)
    
    class Meta:
        model = contracts.PlaceOfPerformance
        fields = ()


class AgencyFilter(FilterSet, metaclass = MetaFilterSet):
    
    _token_text = ('id',)
    _fuzzy_text = ('name',)
    
    class Meta:
        model = contracts.Agency
        fields = ()


class ContractBaseFilter(FilterSet, metaclass = MetaFilterSet):
    
    _fuzzy_text = ('piid', 'base_piid', 'NAICS', 'PSC', 'point_of_contact', 'vendor_phone')
    _number = ('id', 'obligated_amount', 'annual_revenue', 'number_of_employees')
    _date_time = ('date_signed', 'completion_date')
    
    status = RelatedFilter(ContractStatusFilter)
    pricing_type = RelatedFilter(PricingStructureFilter)
    
    agency = RelatedFilter(AgencyFilter)
    vendor_location = RelatedFilter(LocationFilter)
    place_of_performance = RelatedFilter(PlaceOfPerformanceFilter)
    
    class Meta:
        model = contracts.Contract
        fields = ()


class ContractFilter(ContractBaseFilter, metaclass = MetaFilterSet):

    vendor = RelatedFilter(VendorFilter)
    
    psc_naics = CharFilter(field_name='NAICS', method='filter_psc_naics')
        
    class Meta:
        model = contracts.Contract
        fields = ()
        
    def filter_psc_naics(self, qs, name, value):
        naics_code = re.sub(r'[^\d]+$', '', value)
        
        try:
            naics = categories.Naics.objects.get(code=naics_code)
            sin_codes = list(naics.sin.all().values_list('code', flat=True))
            psc_codes = list(categories.PSC.objects.filter(sin__code__in=sin_codes).distinct().values_list('code', flat=True))
            return qs.filter(Q(PSC__in=psc_codes) | Q(NAICS=naics_code))
        
        except Exception:
            pass
        
        return qs.filter(NAICS=naics_code)
