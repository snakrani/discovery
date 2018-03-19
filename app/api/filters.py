from django.db.models.query import QuerySet

from rest_framework.fields import CharField, IntegerField

from rest_framework_filters.filterset import FilterSet
from rest_framework_filters.filters import BooleanFilter, NumberFilter, CharFilter, DateFilter, DateTimeFilter, RelatedFilter, BaseInFilter, BaseRangeFilter
from rest_framework_filters.backends import ComplexFilterBackend

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts


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


class NaicsFilter(FilterSet):
    
    code = CharFilter(field_name='code', lookup_expr='exact')
    code__iexact = CharFilter(field_name='code', lookup_expr='iexact')
    code__in = CharInFilter(field_name='code', lookup_expr='in')
    code__contains = CharFilter(field_name='code', lookup_expr='contains')
    code__icontains = CharFilter(field_name='code', lookup_expr='icontains')
    code__startswith = CharFilter(field_name='code', lookup_expr='startswith')
    code__istartswith = CharFilter(field_name='code', lookup_expr='istartswith')
    code__endswith = CharFilter(field_name='code', lookup_expr='endswith')
    code__iendswith = CharFilter(field_name='code', lookup_expr='iendswith')
    code__regex = CharFilter(field_name='code', lookup_expr='regex')
    code__iregex = CharFilter(field_name='code', lookup_expr='iregex')
    
    root_code = CharFilter(field_name='root_code', lookup_expr='exact')
    root_code__iexact = CharFilter(field_name='root_code', lookup_expr='iexact')
    root_code__in = CharInFilter(field_name='root_code', lookup_expr='in')
    root_code__contains = CharFilter(field_name='root_code', lookup_expr='contains')
    root_code__icontains = CharFilter(field_name='root_code', lookup_expr='icontains')
    root_code__startswith = CharFilter(field_name='root_code', lookup_expr='startswith')
    root_code__istartswith = CharFilter(field_name='root_code', lookup_expr='istartswith')
    root_code__endswith = CharFilter(field_name='root_code', lookup_expr='endswith')
    root_code__iendswith = CharFilter(field_name='root_code', lookup_expr='iendswith')
    root_code__regex = CharFilter(field_name='root_code', lookup_expr='regex')
    root_code__iregex = CharFilter(field_name='root_code', lookup_expr='iregex')
    
    description = CharFilter(field_name='description', lookup_expr='exact')
    description__iexact = CharFilter(field_name='description', lookup_expr='iexact')
    description__in = CharInFilter(field_name='description', lookup_expr='in')
    description__contains = CharFilter(field_name='description', lookup_expr='contains')
    description__icontains = CharFilter(field_name='description', lookup_expr='icontains')
    description__startswith = CharFilter(field_name='description', lookup_expr='startswith')
    description__istartswith = CharFilter(field_name='description', lookup_expr='istartswith')
    description__endswith = CharFilter(field_name='description', lookup_expr='endswith')
    description__iendswith = CharFilter(field_name='description', lookup_expr='iendswith')
    description__regex = CharFilter(field_name='description', lookup_expr='regex')
    description__iregex = CharFilter(field_name='description', lookup_expr='iregex')
    
    class Meta:
        model = categories.Naics
        fields = ['code', 'root_code', 'description']


class SetAsideFilter(FilterSet):
    
    code = CharFilter(field_name='code', lookup_expr='exact')
    code__iexact = CharFilter(field_name='code', lookup_expr='iexact')
    code__in = CharInFilter(field_name='code', lookup_expr='in')
    
    name = CharFilter(field_name='name', lookup_expr='exact')
    name__iexact = CharFilter(field_name='name', lookup_expr='iexact')
    name__in = CharInFilter(field_name='name', lookup_expr='in')
    
    description = CharFilter(field_name='description', lookup_expr='exact')
    description__iexact = CharFilter(field_name='description', lookup_expr='iexact')
    description__in = CharInFilter(field_name='description', lookup_expr='in')
    description__contains = CharFilter(field_name='description', lookup_expr='contains')
    description__icontains = CharFilter(field_name='description', lookup_expr='icontains')
    description__startswith = CharFilter(field_name='description', lookup_expr='startswith')
    description__istartswith = CharFilter(field_name='description', lookup_expr='istartswith')
    description__endswith = CharFilter(field_name='description', lookup_expr='endswith')
    description__iendswith = CharFilter(field_name='description', lookup_expr='iendswith')
    description__regex = CharFilter(field_name='description', lookup_expr='regex')
    description__iregex = CharFilter(field_name='description', lookup_expr='iregex')
    
    far_order = NumberFilter(field_name='far_order', lookup_expr='exact')
    far_order__range = NumberFilter(field_name='far_order', lookup_expr='range')
    far_order__in = NumberInFilter(field_name='far_order', lookup_expr='in')
    far_order__lt = NumberFilter(field_name='far_order', lookup_expr='lt')
    far_order__lte = NumberFilter(field_name='far_order', lookup_expr='lte')
    far_order__gt = NumberFilter(field_name='far_order', lookup_expr='gt')
    far_order__gte = NumberFilter(field_name='far_order', lookup_expr='gte')
    
    class Meta:
        model = categories.SetAside
        fields = []


class PoolFilter(FilterSet):
        
    id = CharFilter(field_name='id', lookup_expr='exact')
    id__iexact = CharFilter(field_name='id', lookup_expr='iexact')
    id__in = CharInFilter(field_name='id', lookup_expr='in')
    
    name = CharFilter(field_name='name', lookup_expr='exact')
    name__iexact = CharFilter(field_name='name', lookup_expr='iexact')
    name__in = CharInFilter(field_name='name', lookup_expr='in')
    name__contains = CharFilter(field_name='name', lookup_expr='contains')
    name__icontains = CharFilter(field_name='name', lookup_expr='icontains')
    name__startswith = CharFilter(field_name='name', lookup_expr='startswith')
    name__istartswith = CharFilter(field_name='name', lookup_expr='istartswith')
    name__endswith = CharFilter(field_name='name', lookup_expr='endswith')
    name__iendswith = CharFilter(field_name='name', lookup_expr='iendswith')
    name__regex = CharFilter(field_name='name', lookup_expr='regex')
    name__iregex = CharFilter(field_name='name', lookup_expr='iregex')
    
    number = CharFilter(field_name='number', lookup_expr='exact')
    number__iexact = CharFilter(field_name='number', lookup_expr='iexact')
    number__in = CharInFilter(field_name='number', lookup_expr='in')
    
    vehicle = CharFilter(field_name='vehicle', lookup_expr='exact')
    vehicle__iexact = CharFilter(field_name='vehicle', lookup_expr='iexact')
    vehicle__in = CharInFilter(field_name='vehicle', lookup_expr='in')
    vehicle__contains = CharFilter(field_name='vehicle', lookup_expr='contains')
    vehicle__icontains = CharFilter(field_name='vehicle', lookup_expr='icontains')
    vehicle__startswith = CharFilter(field_name='vehicle', lookup_expr='startswith')
    vehicle__istartswith = CharFilter(field_name='vehicle', lookup_expr='istartswith')
    vehicle__endswith = CharFilter(field_name='vehicle', lookup_expr='endswith')
    vehicle__iendswith = CharFilter(field_name='vehicle', lookup_expr='iendswith')
    vehicle__regex = CharFilter(field_name='vehicle', lookup_expr='regex')
    vehicle__iregex = CharFilter(field_name='vehicle', lookup_expr='iregex')
    
    threshold = CharFilter(field_name='threshold', lookup_expr='exact')
    threshold__iexact = CharFilter(field_name='threshold', lookup_expr='iexact')
    threshold__in = CharInFilter(field_name='threshold', lookup_expr='in')
    threshold__contains = CharFilter(field_name='threshold', lookup_expr='contains')
    threshold__icontains = CharFilter(field_name='threshold', lookup_expr='icontains')
    threshold__startswith = CharFilter(field_name='threshold', lookup_expr='startswith')
    threshold__istartswith = CharFilter(field_name='threshold', lookup_expr='istartswith')
    threshold__endswith = CharFilter(field_name='threshold', lookup_expr='endswith')
    threshold__iendswith = CharFilter(field_name='threshold', lookup_expr='iendswith')
    threshold__regex = CharFilter(field_name='threshold', lookup_expr='regex')
    threshold__iregex = CharFilter(field_name='threshold', lookup_expr='iregex')
    
    naics = RelatedFilter(NaicsFilter)
    
    class Meta:
        model = categories.Pool
        fields = []


class ZoneFilter(FilterSet):
    
    id = NumberFilter(field_name='id', lookup_expr='exact')
    id__range = NumberFilter(field_name='id', lookup_expr='range')
    id__in = NumberInFilter(field_name='id', lookup_expr='in')
    id__lt = NumberFilter(field_name='id', lookup_expr='lt')
    id__lte = NumberFilter(field_name='id', lookup_expr='lte')
    id__gt = NumberFilter(field_name='id', lookup_expr='gt')
    id__gte = NumberFilter(field_name='id', lookup_expr='gte')
    
    state = CharFilter(field_name="state__state", lookup_expr='exact')
    state__iexact = CharFilter(field_name="state__state", lookup_expr='iexact')
    state__in = CharInFilter(field_name="state__state", lookup_expr='in')
     
    class Meta:
        model = categories.Zone
        fields = []


class LocationFilter(FilterSet):
    
    address = CharFilter(field_name='address', lookup_expr='exact')
    address__iexact = CharFilter(field_name='address', lookup_expr='iexact')
    address__in = CharInFilter(field_name='address', lookup_expr='in')
    address__contains = CharFilter(field_name='address', lookup_expr='contains')
    address__icontains = CharFilter(field_name='address', lookup_expr='icontains')
    address__startswith = CharFilter(field_name='address', lookup_expr='startswith')
    address__istartswith = CharFilter(field_name='address', lookup_expr='istartswith')
    address__endswith = CharFilter(field_name='address', lookup_expr='endswith')
    address__iendswith = CharFilter(field_name='address', lookup_expr='iendswith')
    address__regex = CharFilter(field_name='address', lookup_expr='regex')
    address__iregex = CharFilter(field_name='address', lookup_expr='iregex')
    
    city = CharFilter(field_name='city', lookup_expr='exact')
    city__iexact = CharFilter(field_name='city', lookup_expr='iexact')
    city__in = CharInFilter(field_name='city', lookup_expr='in')
    city__contains = CharFilter(field_name='city', lookup_expr='contains')
    city__icontains = CharFilter(field_name='city', lookup_expr='icontains')
    city__startswith = CharFilter(field_name='city', lookup_expr='startswith')
    city__istartswith = CharFilter(field_name='city', lookup_expr='istartswith')
    city__endswith = CharFilter(field_name='city', lookup_expr='endswith')
    city__iendswith = CharFilter(field_name='city', lookup_expr='iendswith')
    city__regex = CharFilter(field_name='city', lookup_expr='regex')
    city__iregex = CharFilter(field_name='city', lookup_expr='iregex')
    
    state = CharFilter(field_name='state', lookup_expr='exact')
    state__iexact = CharFilter(field_name='state', lookup_expr='iexact')
    state__in = CharInFilter(field_name='state', lookup_expr='in')
    
    zipcode = CharFilter(field_name='zipcode', lookup_expr='exact')
    zipcode__iexact = CharFilter(field_name='zipcode', lookup_expr='iexact')
    zipcode__in = CharInFilter(field_name='zipcode', lookup_expr='in')
    zipcode__contains = CharFilter(field_name='zipcode', lookup_expr='contains')
    zipcode__icontains = CharFilter(field_name='zipcode', lookup_expr='icontains')
    zipcode__startswith = CharFilter(field_name='zipcode', lookup_expr='startswith')
    zipcode__istartswith = CharFilter(field_name='zipcode', lookup_expr='istartswith')
    zipcode__endswith = CharFilter(field_name='zipcode', lookup_expr='endswith')
    zipcode__iendswith = CharFilter(field_name='zipcode', lookup_expr='iendswith')
    zipcode__regex = CharFilter(field_name='zipcode', lookup_expr='regex')
    zipcode__iregex = CharFilter(field_name='zipcode', lookup_expr='iregex')
    
    congressional_district = CharFilter(field_name='congressional_district', lookup_expr='exact')
    congressional_district__iexact = CharFilter(field_name='congressional_district', lookup_expr='iexact')
    congressional_district__in = CharInFilter(field_name='congressional_district', lookup_expr='in')

    class Meta:
        model = vendors.Location
        fields = ['address', 'city', 'state', 'zipcode', 'congressional_district']


class ManagerFilter(FilterSet):
    
    name = CharFilter(field_name='name', lookup_expr='exact')
    name__iexact = CharFilter(field_name='name', lookup_expr='iexact')
    name__in = CharInFilter(field_name='name', lookup_expr='in')
    name__contains = CharFilter(field_name='name', lookup_expr='contains')
    name__icontains = CharFilter(field_name='name', lookup_expr='icontains')
    name__startswith = CharFilter(field_name='name', lookup_expr='startswith')
    name__istartswith = CharFilter(field_name='name', lookup_expr='istartswith')
    name__endswith = CharFilter(field_name='name', lookup_expr='endswith')
    name__iendswith = CharFilter(field_name='name', lookup_expr='iendswith')
    name__regex = CharFilter(field_name='name', lookup_expr='regex')
    name__iregex = CharFilter(field_name='name', lookup_expr='iregex')

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
        fields = []

        
class ProjectManagerFilter(ManagerFilter):
    class Meta:
        model = vendors.ProjectManager
        fields = []

        
class PoolMembershipFilter(FilterSet):
    
    piid = CharFilter(field_name='piid', lookup_expr='exact')
    piid__iexact = CharFilter(field_name='piid', lookup_expr='iexact')
    piid__in = CharInFilter(field_name='piid', lookup_expr='in')
    piid__contains = CharFilter(field_name='piid', lookup_expr='contains')
    piid__icontains = CharFilter(field_name='piid', lookup_expr='icontains')
    piid__startswith = CharFilter(field_name='piid', lookup_expr='startswith')
    piid__istartswith = CharFilter(field_name='piid', lookup_expr='istartswith')
    piid__endswith = CharFilter(field_name='piid', lookup_expr='endswith')
    piid__iendswith = CharFilter(field_name='piid', lookup_expr='iendswith')
    piid__regex = CharFilter(field_name='piid', lookup_expr='regex')
    piid__iregex = CharFilter(field_name='piid', lookup_expr='iregex')
    
    pool = RelatedFilter(PoolFilter)
    setasides = RelatedFilter(SetAsideFilter)
    
    zones = RelatedFilter(ZoneFilter)
    
    cms = RelatedFilter(ContractManagerFilter)
    pms = RelatedFilter(ProjectManagerFilter)
    
    class Meta:
        model = vendors.PoolMembership
        fields = []


class VendorFilter(FilterSet):
    
    name = CharFilter(field_name='name', lookup_expr='exact')
    name__iexact = CharFilter(field_name='name', lookup_expr='iexact')
    name__in = CharInFilter(field_name='name', lookup_expr='in')
    name__contains = CharFilter(field_name='name', lookup_expr='contains')
    name__icontains = CharFilter(field_name='name', lookup_expr='icontains')
    name__startswith = CharFilter(field_name='name', lookup_expr='startswith')
    name__istartswith = CharFilter(field_name='name', lookup_expr='istartswith')
    name__endswith = CharFilter(field_name='name', lookup_expr='endswith')
    name__iendswith = CharFilter(field_name='name', lookup_expr='iendswith')
    name__regex = CharFilter(field_name='name', lookup_expr='regex')
    name__iregex = CharFilter(field_name='name', lookup_expr='iregex')
    
    duns__range = CharRangeFilter(field_name='duns')
    duns__in = CharInFilter(field_name='duns')
    duns__lt = CharFilter(field_name='duns', lookup_expr='lt')
    duns__lte = CharFilter(field_name='duns', lookup_expr='lte')
    duns__gt = CharFilter(field_name='duns', lookup_expr='gt')
    duns__gte = CharFilter(field_name='duns', lookup_expr='gte')
    
    cage = CharFilter(field_name='cage', lookup_expr='exact')
    cage__iexact = CharFilter(field_name='cage', lookup_expr='iexact')
    cage__in = CharInFilter(field_name='cage', lookup_expr='in')
    
    sam_status = CharFilter(field_name='sam_status', lookup_expr='exact')
    sam_status__iexact = CharFilter(field_name='sam_status', lookup_expr='iexact')
    sam_status__in = CharInFilter(field_name='sam_status', lookup_expr='in')
    
    sam_activation_date = CharFilter(field_name="sam_activation_date", lookup_expr="startswith")
    sam_activation_date__year = NumberFilter(field_name='sam_activation_date', lookup_expr='year')
    sam_activation_date__month = NumberFilter(field_name='sam_activation_date', lookup_expr='month')
    sam_activation_date__day = NumberFilter(field_name='sam_activation_date', lookup_expr='day')
    sam_activation_date__week = NumberFilter(field_name='sam_activation_date', lookup_expr='week')
    sam_activation_date__week_day = NumberFilter(field_name='sam_activation_date', lookup_expr='week_day')
    sam_activation_date__quarter = NumberFilter(field_name='sam_activation_date', lookup_expr='quarter')
        
    sam_expiration_date = CharFilter(field_name="sam_expiration_date", lookup_expr="startswith")
    sam_expiration_date__year = NumberFilter(field_name='sam_expiration_date', lookup_expr='year')
    sam_expiration_date__month = NumberFilter(field_name='sam_expiration_date', lookup_expr='month')
    sam_expiration_date__day = NumberFilter(field_name='sam_expiration_date', lookup_expr='day')
    sam_expiration_date__week = NumberFilter(field_name='sam_expiration_date', lookup_expr='week')
    sam_expiration_date__week_day = NumberFilter(field_name='sam_expiration_date', lookup_expr='week_day')
    sam_expiration_date__quarter = NumberFilter(field_name='sam_expiration_date', lookup_expr='quarter')
    
    sam_exclusion = BooleanFilter(field_name="sam_exclusion", lookup_expr="exact")
    
    sam_url = CharFilter(field_name='sam_url', lookup_expr='exact')
    sam_url__iexact = CharFilter(field_name='sam_url', lookup_expr='iexact')
    sam_url__in = CharInFilter(field_name='sam_url', lookup_expr='in')
    sam_url__contains = CharFilter(field_name='sam_url', lookup_expr='contains')
    sam_url__icontains = CharFilter(field_name='sam_url', lookup_expr='icontains')
    sam_url__startswith = CharFilter(field_name='sam_url', lookup_expr='startswith')
    sam_url__istartswith = CharFilter(field_name='sam_url', lookup_expr='istartswith')
    sam_url__endswith = CharFilter(field_name='sam_url', lookup_expr='endswith')
    sam_url__iendswith = CharFilter(field_name='sam_url', lookup_expr='iendswith')
    sam_url__regex = CharFilter(field_name='sam_url', lookup_expr='regex')
    sam_url__iregex = CharFilter(field_name='sam_url', lookup_expr='iregex')
    
    sam_location = RelatedFilter(LocationFilter)
    pools = RelatedFilter(PoolMembershipFilter)
    
    class Meta:
        model = vendors.Vendor
        fields = []


class ContractStatusFilter(FilterSet):
    
    code = CharFilter(field_name='code', lookup_expr='exact')
    code__iexact = CharFilter(field_name='code', lookup_expr='iexact')
    code__in = CharInFilter(field_name='code', lookup_expr='in')
    
    name = CharFilter(field_name='name', lookup_expr='exact')
    name__iexact = CharFilter(field_name='name', lookup_expr='iexact')
    name__in = CharInFilter(field_name='name', lookup_expr='in')
    name__contains = CharFilter(field_name='name', lookup_expr='contains')
    name__icontains = CharFilter(field_name='name', lookup_expr='icontains')
    name__startswith = CharFilter(field_name='name', lookup_expr='startswith')
    name__istartswith = CharFilter(field_name='name', lookup_expr='istartswith')
    name__endswith = CharFilter(field_name='name', lookup_expr='endswith')
    name__iendswith = CharFilter(field_name='name', lookup_expr='iendswith')
    name__regex = CharFilter(field_name='name', lookup_expr='regex')
    name__iregex = CharFilter(field_name='name', lookup_expr='iregex')
    
    class Meta:
        model = contracts.ContractStatus
        fields = []


class PricingStructureFilter(FilterSet):
    
    code = CharFilter(field_name='code', lookup_expr='exact')
    code__iexact = CharFilter(field_name='code', lookup_expr='iexact')
    code__in = CharInFilter(field_name='code', lookup_expr='in')
    
    name = CharFilter(field_name='name', lookup_expr='exact')
    name__iexact = CharFilter(field_name='name', lookup_expr='iexact')
    name__in = CharInFilter(field_name='name', lookup_expr='in')
    name__contains = CharFilter(field_name='name', lookup_expr='contains')
    name__icontains = CharFilter(field_name='name', lookup_expr='icontains')
    name__startswith = CharFilter(field_name='name', lookup_expr='startswith')
    name__istartswith = CharFilter(field_name='name', lookup_expr='istartswith')
    name__endswith = CharFilter(field_name='name', lookup_expr='endswith')
    name__iendswith = CharFilter(field_name='name', lookup_expr='iendswith')
    name__regex = CharFilter(field_name='name', lookup_expr='regex')
    name__iregex = CharFilter(field_name='name', lookup_expr='iregex')
    
    class Meta:
        model = contracts.PricingStructure
        fields = []


class PlaceOfPerformanceFilter(FilterSet):
    
    country_code = CharFilter(field_name='country_code', lookup_expr='exact')
    country_code__iexact = CharFilter(field_name='country_code', lookup_expr='iexact')
    country_code__in = CharInFilter(field_name='country_code', lookup_expr='in')
    
    country_name = CharFilter(field_name='country_name', lookup_expr='exact')
    country_name__iexact = CharFilter(field_name='country_name', lookup_expr='iexact')
    country_name__in = CharInFilter(field_name='country_name', lookup_expr='in')
    country_name__contains = CharFilter(field_name='country_name', lookup_expr='contains')
    country_name__icontains = CharFilter(field_name='country_name', lookup_expr='icontains')
    country_name__startswith = CharFilter(field_name='country_name', lookup_expr='startswith')
    country_name__istartswith = CharFilter(field_name='country_name', lookup_expr='istartswith')
    country_name__endswith = CharFilter(field_name='country_name', lookup_expr='endswith')
    country_name__iendswith = CharFilter(field_name='country_name', lookup_expr='iendswith')
    country_name__regex = CharFilter(field_name='country_name', lookup_expr='regex')
    country_name__iregex = CharFilter(field_name='country_name', lookup_expr='iregex')
    
    state = CharFilter(field_name='state', lookup_expr='exact')
    state__iexact = CharFilter(field_name='state', lookup_expr='iexact')
    state__in = CharInFilter(field_name='state', lookup_expr='in')
    
    zipcode = CharFilter(field_name='zipcode', lookup_expr='exact')
    zipcode__iexact = CharFilter(field_name='zipcode', lookup_expr='iexact')
    zipcode__in = CharInFilter(field_name='zipcode', lookup_expr='in')
    zipcode__contains = CharFilter(field_name='zipcode', lookup_expr='contains')
    zipcode__icontains = CharFilter(field_name='zipcode', lookup_expr='icontains')
    zipcode__startswith = CharFilter(field_name='zipcode', lookup_expr='startswith')
    zipcode__istartswith = CharFilter(field_name='zipcode', lookup_expr='istartswith')
    zipcode__endswith = CharFilter(field_name='zipcode', lookup_expr='endswith')
    zipcode__iendswith = CharFilter(field_name='zipcode', lookup_expr='iendswith')
    zipcode__regex = CharFilter(field_name='zipcode', lookup_expr='regex')
    zipcode__iregex = CharFilter(field_name='zipcode', lookup_expr='iregex')
    
    class Meta:
        model = contracts.PlaceOfPerformance
        fields = []


class ContractFilter(FilterSet):
    
    id = NumberFilter(field_name='id', lookup_expr='exact')
    id__range = NumberFilter(field_name='id', lookup_expr='range')
    id__in = NumberInFilter(field_name='id', lookup_expr='in')
    id__lt = NumberFilter(field_name='id', lookup_expr='lt')
    id__lte = NumberFilter(field_name='id', lookup_expr='lte')
    id__gt = NumberFilter(field_name='id', lookup_expr='gt')
    id__gte = NumberFilter(field_name='id', lookup_expr='gte')
    
    piid = CharFilter(field_name='piid', lookup_expr='exact')
    piid__iexact = CharFilter(field_name='piid', lookup_expr='iexact')
    piid__in = CharInFilter(field_name='piid', lookup_expr='in')
    piid__contains = CharFilter(field_name='piid', lookup_expr='contains')
    piid__icontains = CharFilter(field_name='piid', lookup_expr='icontains')
    piid__startswith = CharFilter(field_name='piid', lookup_expr='startswith')
    piid__istartswith = CharFilter(field_name='piid', lookup_expr='istartswith')
    piid__endswith = CharFilter(field_name='piid', lookup_expr='endswith')
    piid__iendswith = CharFilter(field_name='piid', lookup_expr='iendswith')
    piid__regex = CharFilter(field_name='piid', lookup_expr='regex')
    piid__iregex = CharFilter(field_name='piid', lookup_expr='iregex')
    
    agency_id = CharFilter(field_name='agency_id', lookup_expr='exact')
    agency_id__iexact = CharFilter(field_name='agency_id', lookup_expr='iexact')
    agency_id__in = CharInFilter(field_name='agency_id', lookup_expr='in')
    
    agency_name = CharFilter(field_name='agency_name', lookup_expr='exact')
    agency_name__iexact = CharFilter(field_name='agency_name', lookup_expr='iexact')
    agency_name__in = CharInFilter(field_name='agency_name', lookup_expr='in')
    agency_name__contains = CharFilter(field_name='agency_name', lookup_expr='contains')
    agency_name__icontains = CharFilter(field_name='agency_name', lookup_expr='icontains')
    agency_name__startswith = CharFilter(field_name='agency_name', lookup_expr='startswith')
    agency_name__istartswith = CharFilter(field_name='agency_name', lookup_expr='istartswith')
    agency_name__endswith = CharFilter(field_name='agency_name', lookup_expr='endswith')
    agency_name__iendswith = CharFilter(field_name='agency_name', lookup_expr='iendswith')
    agency_name__regex = CharFilter(field_name='agency_name', lookup_expr='regex')
    agency_name__iregex = CharFilter(field_name='agency_name', lookup_expr='iregex')
    
    NAICS = CharFilter(field_name='NAICS', lookup_expr='exact')
    NAICS__iexact = CharFilter(field_name='NAICS', lookup_expr='iexact')
    NAICS__in = CharInFilter(field_name='NAICS', lookup_expr='in')
    NAICS__contains = CharFilter(field_name='NAICS', lookup_expr='contains')
    NAICS__icontains = CharFilter(field_name='NAICS', lookup_expr='icontains')
    NAICS__startswith = CharFilter(field_name='NAICS', lookup_expr='startswith')
    NAICS__istartswith = CharFilter(field_name='NAICS', lookup_expr='istartswith')
    NAICS__endswith = CharFilter(field_name='NAICS', lookup_expr='endswith')
    NAICS__iendswith = CharFilter(field_name='NAICS', lookup_expr='iendswith')
    NAICS__regex = CharFilter(field_name='NAICS', lookup_expr='regex')
    NAICS__iregex = CharFilter(field_name='NAICS', lookup_expr='iregex')
    
    PSC = CharFilter(field_name='PSC', lookup_expr='exact')
    PSC__iexact = CharFilter(field_name='PSC', lookup_expr='iexact')
    PSC__in = CharInFilter(field_name='PSC', lookup_expr='in')
    PSC__contains = CharFilter(field_name='PSC', lookup_expr='contains')
    PSC__icontains = CharFilter(field_name='PSC', lookup_expr='icontains')
    PSC__startswith = CharFilter(field_name='PSC', lookup_expr='startswith')
    PSC__istartswith = CharFilter(field_name='PSC', lookup_expr='istartswith')
    PSC__endswith = CharFilter(field_name='PSC', lookup_expr='endswith')
    PSC__iendswith = CharFilter(field_name='PSC', lookup_expr='iendswith')
    PSC__regex = CharFilter(field_name='PSC', lookup_expr='regex')
    PSC__iregex = CharFilter(field_name='PSC', lookup_expr='iregex')
    
    date_signed = CharFilter(field_name="date_signed", lookup_expr="startswith")
    date_signed__year = DateFilter(field_name='date_signed', lookup_expr='year')
    date_signed__month = DateFilter(field_name='date_signed', lookup_expr='month')
    date_signed__day = DateFilter(field_name='date_signed', lookup_expr='day')
    date_signed__week = DateFilter(field_name='date_signed', lookup_expr='week')
    date_signed__week_day = DateFilter(field_name='date_signed', lookup_expr='week_day')
    date_signed__quarter = DateFilter(field_name='date_signed', lookup_expr='quarter')
    
    completion_date = CharFilter(field_name="completion_date", lookup_expr="startswith")
    completion_date__year = DateFilter(field_name='completion_date', lookup_expr='year')
    completion_date__month = DateFilter(field_name='completion_date', lookup_expr='month')
    completion_date__day = DateFilter(field_name='completion_date', lookup_expr='day')
    completion_date__week = DateFilter(field_name='completion_date', lookup_expr='week')
    completion_date__week_day = DateFilter(field_name='completion_date', lookup_expr='week_day')
    completion_date__quarter = DateFilter(field_name='completion_date', lookup_expr='quarter')
    
    obligated_amount = NumberFilter(field_name='obligated_amount', lookup_expr='exact')
    obligated_amount__range = NumberFilter(field_name='obligated_amount', lookup_expr='range')
    obligated_amount__in = NumberInFilter(field_name='obligated_amount', lookup_expr='in')
    obligated_amount__lt = NumberFilter(field_name='obligated_amount', lookup_expr='lt')
    obligated_amount__lte = NumberFilter(field_name='obligated_amount', lookup_expr='lte')
    obligated_amount__gt = NumberFilter(field_name='obligated_amount', lookup_expr='gt')
    obligated_amount__gte = NumberFilter(field_name='obligated_amount', lookup_expr='gte')
    
    point_of_contact = CharFilter(field_name='point_of_contact', lookup_expr='exact')
    point_of_contact__iexact = CharFilter(field_name='point_of_contact', lookup_expr='iexact')
    point_of_contact__in = CharInFilter(field_name='point_of_contact', lookup_expr='in')
    point_of_contact__contains = CharFilter(field_name='point_of_contact', lookup_expr='contains')
    point_of_contact__icontains = CharFilter(field_name='point_of_contact', lookup_expr='icontains')
    point_of_contact__startswith = CharFilter(field_name='point_of_contact', lookup_expr='startswith')
    point_of_contact__istartswith = CharFilter(field_name='point_of_contact', lookup_expr='istartswith')
    point_of_contact__endswith = CharFilter(field_name='point_of_contact', lookup_expr='endswith')
    point_of_contact__iendswith = CharFilter(field_name='point_of_contact', lookup_expr='iendswith')
    point_of_contact__regex = CharFilter(field_name='point_of_contact', lookup_expr='regex')
    point_of_contact__iregex = CharFilter(field_name='point_of_contact', lookup_expr='iregex')
    
    vendor_phone = CharFilter(field_name='vendor_phone', lookup_expr='exact')
    vendor_phone__iexact = CharFilter(field_name='vendor_phone', lookup_expr='iexact')
    vendor_phone__in = CharInFilter(field_name='vendor_phone', lookup_expr='in')
    vendor_phone__contains = CharFilter(field_name='vendor_phone', lookup_expr='contains')
    vendor_phone__icontains = CharFilter(field_name='vendor_phone', lookup_expr='icontains')
    vendor_phone__startswith = CharFilter(field_name='vendor_phone', lookup_expr='startswith')
    vendor_phone__istartswith = CharFilter(field_name='vendor_phone', lookup_expr='istartswith')
    vendor_phone__endswith = CharFilter(field_name='vendor_phone', lookup_expr='endswith')
    vendor_phone__iendswith = CharFilter(field_name='vendor_phone', lookup_expr='iendswith')
    vendor_phone__regex = CharFilter(field_name='vendor_phone', lookup_expr='regex')
    vendor_phone__iregex = CharFilter(field_name='vendor_phone', lookup_expr='iregex')
    
    annual_revenue = NumberFilter(field_name='annual_revenue', lookup_expr='exact')
    annual_revenue__range = NumberFilter(field_name='annual_revenue', lookup_expr='range')
    annual_revenue__in = NumberInFilter(field_name='annual_revenue', lookup_expr='in')
    annual_revenue__lt = NumberFilter(field_name='annual_revenue', lookup_expr='lt')
    annual_revenue__lte = NumberFilter(field_name='annual_revenue', lookup_expr='lte')
    annual_revenue__gt = NumberFilter(field_name='annual_revenue', lookup_expr='gt')
    annual_revenue__gte = NumberFilter(field_name='annual_revenue', lookup_expr='gte')
    
    number_of_employees = NumberFilter(field_name='number_of_employees', lookup_expr='exact')
    number_of_employees__range = NumberFilter(field_name='number_of_employees', lookup_expr='range')
    number_of_employees__in = NumberInFilter(field_name='number_of_employees', lookup_expr='in')
    number_of_employees__lt = NumberFilter(field_name='number_of_employees', lookup_expr='lt')
    number_of_employees__lte = NumberFilter(field_name='number_of_employees', lookup_expr='lte')
    number_of_employees__gt = NumberFilter(field_name='number_of_employees', lookup_expr='gt')
    number_of_employees__gte = NumberFilter(field_name='number_of_employees', lookup_expr='gte')
    
    status = RelatedFilter(ContractStatusFilter)
    pricing_type = RelatedFilter(PricingStructureFilter)
        
    vendor = RelatedFilter(VendorFilter)
    vendor_location = RelatedFilter(LocationFilter)
    
    place_of_performance = RelatedFilter(PlaceOfPerformanceFilter)
        
    class Meta:
        model = contracts.Contract
        fields = []
