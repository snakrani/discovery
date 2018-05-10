from django.conf import settings
from django.db.models import Subquery, OuterRef, Value, Q
from django.db.models.functions import Concat, Coalesce
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from rest_framework_filters.backends import RestFrameworkFilterBackend

from discovery.utils import check_api_test
from discovery import query
from discovery import metadata
from discovery import models as system
from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts
from api import mixins, filters, serializers, pagination

import re


@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='list')
@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='retrieve')
class DiscoveryReadOnlyModelViewSet(
    mixins.FilterViewSetMixin,
    mixins.PaginationViewSetMixin,
    mixins.SerializerViewSetMixin, 
    ReadOnlyModelViewSet
):
    def list(self, request, *args, **kwargs):
        page, created = system.CachePage.objects.get_or_create(url=request.build_absolute_uri())
        page.count += 1
        page.save()
        
        return super(DiscoveryReadOnlyModelViewSet, self).list(request, *args, **kwargs)
        
    def retrieve(self, request, *args, **kwargs):
        page, created = system.CachePage.objects.get_or_create(url=request.build_absolute_uri())
        page.count += 1
        page.save()
        
        return super(DiscoveryReadOnlyModelViewSet, self).retrieve(request, *args, **kwargs)
    

class NaicsViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related NAICS code information.
    
    retrieve:
    Returns information for a single NAICS code.
    
    list:
    Returns all of the NAICS codes that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.Naics.objects.all().distinct()
    lookup_field = 'code'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
    }
    filter_class = filters.NaicsFilter
    search_fields = ['code', 'description', 'keywords__name']
    ordering_fields = ['code', 'root_code', 'description']
    ordering = 'description'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers = {
        'list': serializers.NaicsSummarySerializer,
        'retrieve': serializers.NaicsFullSerializer,
        'test': serializers.NaicsTestSerializer
    }


class PscViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related PSC code information.
    
    retrieve:
    Returns information for a single PSC code.
    
    list:
    Returns all of the PSC codes that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.PSC.objects.all().distinct()
    lookup_field = 'code'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
    }
    filter_class = filters.PscFilter
    search_fields = ['code', 'description', 'naics__code', 'naics__description', 'keywords__name']
    ordering_fields = ['code', 'description', 'naics__code', 'naics__root_code', 'naics__description']
    ordering = 'description'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers = {
        'list': serializers.PscSummarySerializer,
        'retrieve': serializers.PscFullSerializer,
        'test': serializers.PscTestSerializer
    }


class PoolViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related vendor pool information.
    
    retrieve:
    Returns information for a single vendor pool.
    
    list:
    Returns all of the vendor pools that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.Pool.objects.all().distinct()
    lookup_field = 'id'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
    }
    filter_class = filters.PoolFilter
    search_fields = ['id', 'name', 'number', 'vehicle']
    ordering_fields = ['id', 'name', 'number', 'vehicle']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers = {
        'list': serializers.PoolSummarySerializer,
        'retrieve': serializers.PoolFullSerializer,
        'test': serializers.PoolTestSerializer
    }


class SetAsideViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related business setaside information.
    
    retrieve:
    Returns information for a single business setaside code.
    
    list:
    Returns all of the business setasides that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.SetAside.objects.all().distinct()
    lookup_field = 'code'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
    }
    filter_class = filters.SetAsideFilter
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['code', 'name', 'description', 'far_order']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers = {
        'list': serializers.SetasideSummarySerializer,
        'retrieve': serializers.SetasideFullSerializer,
        'test': serializers.SetasideTestSerializer
    }


class ZoneViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery vendor pool zone information.
    
    retrieve:
    Returns information for a single vendor pool zone.
    
    list:
    Returns all of the vendor pool zones that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.Zone.objects.all().distinct()
    lookup_field = 'id'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, OrderingFilter),
    }
    filter_class = filters.ZoneFilter
    ordering_fields = ['id']
    ordering = 'id'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers = {
        'list': serializers.ZoneSummarySerializer,
        'retrieve': serializers.ZoneFullSerializer,
        'test': serializers.ZoneTestSerializer
    }


class VendorViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to vendor information in the Discovery universe.
    
    retrieve:
    Returns information for a single vendor.
    
    list:
    Returns all of the vendors that contract through the acquisition vehicles in the Discovery universe.
    """
    queryset = vendors.Vendor.objects.all().distinct()
    lookup_field = 'duns'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
    }
    filter_class = filters.VendorFilter
    search_fields = ['name', 'duns', 'cage']
    ordering_fields = [
        'name', 'duns', 'cage', 
        'sam_status', 'sam_exclusion', 'sam_url',
        'sam_location__address', 'sam_location__city', 'sam_location__state', 
        'sam_location__zipcode', 'sam_location__congressional_district', 'sam_location_citystate',
        'annual_revenue', 'number_of_employees', 'number_of_contracts'
    ]
    ordering = '-number_of_contracts'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers = {
        'list': serializers.VendorSummarySerializer,
        'retrieve': serializers.VendorFullSerializer,
        'test': serializers.VendorTestSerializer
    }
    
    def get_queryset(self):
        naics_param_name = 'contract_naics'
        
        queryset = self.queryset.annotate(
            annual_revenue=Subquery(
                contracts.Contract.objects.filter(vendor=OuterRef('pk')).order_by('-date_signed').values('annual_revenue')[:1]
            ),
            number_of_employees=Subquery(
                contracts.Contract.objects.filter(vendor=OuterRef('pk')).order_by('-date_signed').values('number_of_employees')[:1]
            ),
            sam_location_citystate = Concat('sam_location__city', Value(', '), 'sam_location__state', Value(' '), 'sam_location__zipcode')
        )
        if naics_param_name in self.request.query_params and self.request.query_params[naics_param_name]:
            naics_code = re.sub(r'[^\d]+$', '', self.request.query_params[naics_param_name])
            psc_codes = list(categories.PSC.objects.filter(naics__root_code=naics_code).distinct().values_list('code', flat=True))
            
            contract_list = contracts.Contract.objects.filter(Q(PSC__in=psc_codes) | Q(NAICS=naics_code), vendor=OuterRef('pk')).values('pk')
        else:
            contract_list = contracts.Contract.objects.filter(vendor=OuterRef('pk')).values('pk')
        
        return queryset.annotate(number_of_contracts = query.QueryCount(contract_list))


class ContractViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to contract information for vendors in the Discovery universe.
    
    retrieve:
    Returns information for a single contract.
    
    list:
    Returns all of the contracts for vendors in the Discovery universe.
    """
    queryset = contracts.Contract.objects.all().distinct()
    lookup_field = 'id'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
    }
    filter_class = filters.ContractFilter
    search_fields = ['piid', 'agency_name']
    ordering_fields = [
        'id', 'piid', 
        'agency_id', 'agency_name', 
        'NAICS', 'PSC',
        'date_signed', 'completion_date', 'obligated_amount',
        'vendor__duns', 'vendor__cage', 'vendor__name',
        'point_of_contact', 'vendor_phone',
        'vendor_location__address', 
        'vendor_location__city', 
        'vendor_location__state', 
        'vendor_location__zipcode', 
        'vendor_location__congressional_district', 
        'status__name', 'pricing_type__name',
        'place_of_performance_location',
        'annual_revenue', 'number_of_employees'
    ]
    ordering = '-date_signed'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers = {
        'list': serializers.ContractSummarySerializer,
        'retrieve': serializers.ContractFullSerializer,
        'test': serializers.ContractTestSerializer
    }
    
    def get_queryset(self):
        return self.queryset.annotate(
            place_of_performance_location = Concat('place_of_performance__country_name', Value(' '), Coalesce('place_of_performance__state', Value('')))
        )


@method_decorator(cache_page(60*60), name='get')
class ListKeywordView(ListAPIView):
    """
    This endpoint returns keyword autocomplete results based on input text.
    """
    queryset = categories.Keyword.objects.all()
    
    def get_serializer_class(self):
        if check_api_test(self.request):
            return serializers.KeywordTestSerializer
        else:
            return serializers.KeywordSerializer
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if 'q' in request.query_params and request.query_params['q']:
            queryset = queryset.filter(name__istartswith = request.query_params['q'])
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({ 'results': serializer.data })


@method_decorator(cache_page(60*60), name='get')
class ListMetadataView(APIView):
    """
    This endpoint returns metadata for the most recent data loads of SAM and FPDS data. It takes no parameters.
    """
    def get(self, request, format=None):
        mds = serializers.MetadataSerializer(metadata.DiscoveryMetadata())
        return Response(mds.data)
