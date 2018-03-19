from django.conf import settings
from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Concat, Coalesce
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from rest_framework_filters.backends import RestFrameworkFilterBackend

from discovery import query
from discovery import metadata
from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts
from api import mixins, filters, serializers, pagination

import re


class DiscoveryReadOnlyModelViewSet(
    mixins.FilterViewSetMixin, 
    mixins.SerializerViewSetMixin, 
    ReadOnlyModelViewSet
): pass
    

@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='list')
@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='retrieve')
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
        'list': (SearchFilter, OrderingFilter),
    }
    search_fields = ['code', 'description']
    ordering_fields = ['code', 'root_code', 'description']
    ordering = 'description'
    
    pagination_class = pagination.ResultSetPagination
    serializer_class = serializers.NaicsSerializer


@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='list')
@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='retrieve')
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
        'list': (SearchFilter, OrderingFilter),
    }
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['code', 'name', 'description', 'far_order']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    serializer_class = serializers.SetAsideSerializer


@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='list')
@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='retrieve')
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
    serializer_class = serializers.PoolSerializer


@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='list')
@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='retrieve')
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
    serializer_class = serializers.ZoneSerializer


@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='list')
@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='retrieve')
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
    serializer_class = serializers.VendorSerializer
    
    def get_queryset(self):
        naics_param_name = 'pools__pool__naics__code'
        
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
            contract_list = contracts.Contract.objects.filter(NAICS=re.sub(r'[^\d]+$', '', self.request.query_params[naics_param_name]), vendor=OuterRef('pk')).values('pk')
        else:
            contract_list = contracts.Contract.objects.filter(vendor=OuterRef('pk')).values('pk')
        
        return queryset.annotate(number_of_contracts = query.QueryCount(contract_list))


@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='list')
@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='retrieve')
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
    search_fields = ['id', 'piid', 'agency_id', 'agency_name', 'NAICS', 'PSC']
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
    serializer_class = serializers.ContractSerializer
    
    def get_queryset(self):
        return self.queryset.annotate(
            place_of_performance_location = Concat('place_of_performance__country_name', Value(' '), Coalesce('place_of_performance__state', Value('')))
        )


@method_decorator(cache_page(60*60*settings.API_CACHE_LIFETIME), name='get')
class ListMetadataView(APIView):
    """
    This endpoint returns metadata for the most recent data loads of SAM and FPDS data. It takes no parameters.
    """
    def get(self, request, format=None):
        mds = serializers.MetadataSerializer(metadata.DiscoveryMetadata())
        return Response(mds.data)
