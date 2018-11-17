from collections import OrderedDict
from datetime import datetime, date

from django.conf import settings
from django.core.cache import cache
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
from discovery.cache import track_page_load
from discovery import query
from discovery import metadata
from discovery import models as system
from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts
from api import mixins, filters, serializers, pagination

import re
import json


class DiscoveryReadOnlyModelViewSet(
    mixins.FilterViewSetMixin,
    mixins.PaginationViewSetMixin,
    mixins.SerializerViewSetMixin, 
    ReadOnlyModelViewSet
):
    def get_queryset(self):
        queryset = super(DiscoveryReadOnlyModelViewSet, self).get_queryset()
        serializer_cls = self.get_serializer_class()
        
        if serializer_cls:
            load_related = getattr(serializer_cls, "load_related", None)
            if callable(load_related):
                return load_related(queryset)

        return queryset

    @method_decorator(cache_page(settings.PAGE_CACHE_LIFETIME, cache='page_cache'))
    def list(self, request, *args, **kwargs):
        track_page_load(request)
        return super(DiscoveryReadOnlyModelViewSet, self).list(request, *args, **kwargs)
    
    @method_decorator(cache_page(settings.PAGE_CACHE_LIFETIME, cache='page_cache'))    
    def retrieve(self, request, *args, **kwargs):
        track_page_load(request)
        return super(DiscoveryReadOnlyModelViewSet, self).retrieve(request, *args, **kwargs)
    
    @method_decorator(cache_page(settings.PAGE_CACHE_LIFETIME, cache='page_cache'))   
    def values(self, request, *args, **kwargs):
        field_lookup = kwargs['field_lookup']
        queryset = self.filter_queryset(self.get_queryset().order_by(field_lookup))
        values = []
        
        for value in queryset.values_list(field_lookup, flat=True):
            if value is not None:
                if isinstance(value, (datetime, date)):
                    value = value.isoformat()
                    if value.endswith('+00:00'):
                        value = value[:-6] + 'Z'
                
                values.append(value)
        
        track_page_load(request)
        return Response(OrderedDict([
            ('count', len(values)),
            ('results', values)
        ]))
    
    @method_decorator(cache_page(settings.PAGE_CACHE_LIFETIME, cache='page_cache'))
    def count(self, request, *args, **kwargs):
        field_lookup = kwargs['field_lookup']
        queryset = self.filter_queryset(self.get_queryset())
        
        track_page_load(request)
        return Response({'count': queryset.values_list(field_lookup).count()})
   

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
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.NaicsFilter
    search_fields = ['code', 'description', 'sin__code']
    ordering_fields = ['code', 'description']
    ordering = 'description'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
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
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.PscFilter
    search_fields = ['code', 'description', 'sin__code']
    ordering_fields = ['code', 'description']
    ordering = 'description'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
    action_serializers = {
        'list': serializers.PscSummarySerializer,
        'retrieve': serializers.PscFullSerializer,
        'test': serializers.PscTestSerializer
    }


class KeywordViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery keyword information.
    
    retrieve:
    Returns information for a keyword.
    
    list:
    Returns all of the keywords that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.Keyword.objects.all().distinct()
    lookup_field = 'id'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.KeywordFilter
    search_fields = ['id', 'name', 'calc']
    ordering_fields = ['id', 'name', 'calc', 'parent__id', 'sin__code', 'naics__code', 'psc__code']
    ordering = 'id'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
    action_serializers = {
        'list': serializers.KeywordSummarySerializer,
        'retrieve': serializers.KeywordFullSerializer,
        'test': serializers.KeywordTestSerializer
    }


class VehicleViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related vendor vehicle information.
    
    retrieve:
    Returns information for a single vendor vehicle.
    
    list:
    Returns all of the vendor vehicles in the Discovery universe.
    """
    queryset = categories.Vehicle.objects.all().distinct()
    lookup_field = 'id'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.VehicleFilter
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name', 'tier__number', 'tier__name', 'poc', 'ordering_guide', 'small_business', 'numeric_pool', 'display_number']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
    action_serializers = {
        'list': serializers.VehicleSummarySerializer,
        'retrieve': serializers.VehicleFullSerializer,
        'test': serializers.VehicleTestSerializer
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
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.PoolFilter
    search_fields = ['id', 'name', 'number', 'threshold', 'vehicle__id', 'vehicle__name', 'keywords__name']
    ordering_fields = ['id', 'name', 'number', 'threshold', 'vehicle__id', 'vehicle__name']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
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
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.SetAsideFilter
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['code', 'name', 'description', 'far_order']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
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
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend)
    }
    filter_class = filters.ZoneFilter
    ordering_fields = ['id']
    ordering = 'id'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
    action_serializers = {
        'list': serializers.ZoneSummarySerializer,
        'retrieve': serializers.ZoneFullSerializer,
        'test': serializers.ZoneTestSerializer
    }


class MembershipViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related vendor pool membership information.
    
    retrieve:
    Returns information for a single vendor pool membership.
    
    list:
    Returns all of the vendor pool memberships that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = vendors.PoolMembership.objects.all().distinct()
    lookup_field = 'id'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.PoolMembershipVendorFilter
    search_fields = ['piid', 'vendor__name']
    ordering_fields = [
        'id', 'piid', 
        'vendor__duns', 'vendor__name', 
        'pool__id', 'pool__name', 'pool__number', 'pool__threshold', 
        'pool__vehicle__id', 'pool__vehicle__name'
    ]
    ordering = 'piid'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = False
    
    action_serializers = {
        'list': serializers.PoolMembershipSummaryVendorSerializer,
        'retrieve': serializers.PoolMembershipSummaryVendorSerializer,
        'test': serializers.PoolMembershipTestVendorSerializer
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
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.VendorFilter
    search_fields = ['name', 'duns', 'cage']
    ordering_fields = [
        'name', 'duns', 'cage', 
        'sam_status', 'sam_exclusion', 'sam_url',
        'sam_location__address', 'sam_location__city', 'sam_location__state', 
        'sam_location__zipcode', 'sam_location__congressional_district',
        'number_of_contracts'
    ]
    ordering = '-number_of_contracts'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = False
    
    action_serializers = {
        'list': serializers.VendorSummarySerializer,
        'retrieve': serializers.VendorFullSerializer,
        'test': serializers.VendorTestSerializer
    }
    
    def get_queryset(self):
        queryset = super(VendorViewSet, self).get_queryset()
        naics_param_name = 'contract_naics'
        
        if naics_param_name in self.request.query_params and self.request.query_params[naics_param_name]:
            naics_code = re.sub(r'[^\d]+$', '', self.request.query_params[naics_param_name])
            psc_codes = list(categories.PSC.objects.filter(naics__code=naics_code).distinct().values_list('code', flat=True))
            
            contract_list = contracts.Contract.objects.filter(Q(PSC__in=psc_codes) | Q(NAICS=naics_code), vendor=OuterRef('pk')).values('pk')
        else:
            contract_list = contracts.Contract.objects.filter(vendor=OuterRef('pk')).values('pk')
        
        return queryset.annotate(number_of_contracts = query.QueryCount(contract_list))


class AgencyViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related agency information.
    
    retrieve:
    Returns information for a single agency.
    
    list:
    Returns all of the agencies that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = contracts.Agency.objects.all().distinct()
    lookup_field = 'id'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.AgencyFilter
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
    action_serializers = {
        'list': serializers.AgencySummarySerializer,
        'retrieve': serializers.AgencyFullSerializer,
        'test': serializers.AgencyTestSerializer
    }


class PricingViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery pricing related contract information.
    
    retrieve:
    Returns information for a single pricing type.
    
    list:
    Returns all of the pricing types that are relevant to the contracts in the Discovery universe.
    """
    queryset = contracts.PricingStructure.objects.all().distinct()
    lookup_field = 'code'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.PricingStructureFilter
    search_fields = ['name']
    ordering_fields = ['code', 'name']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
    action_serializers = {
        'list': serializers.PricingStructureSummarySerializer,
        'retrieve': serializers.PricingStructureFullSerializer,
        'test': serializers.PricingStructureTestSerializer
    }


class StatusViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery status related contract information.
    
    retrieve:
    Returns information for a single contract status.
    
    list:
    Returns all of the statuses that are relevant to the contracts in the Discovery universe.
    """
    queryset = contracts.ContractStatus.objects.all().distinct()
    lookup_field = 'code'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.ContractStatusFilter
    search_fields = ['name']
    ordering_fields = ['code', 'name']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
    action_serializers = {
        'list': serializers.ContractStatusSummarySerializer,
        'retrieve': serializers.ContractStatusFullSerializer,
        'test': serializers.ContractStatusTestSerializer
    }


class PlaceOfPerformanceViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to places of performance for contracts in the Discovery universe.
    
    retrieve:
    Returns information for a single place of performance.
    
    list:
    Returns all of the places of performance that are relevant to the contracts in the Discovery universe.
    """
    queryset = contracts.PlaceOfPerformance.objects.all().distinct()
    lookup_field = 'id'
    
    action_filters = {
        'list': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter, OrderingFilter),
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.PlaceOfPerformanceFilter
    search_fields = ['country_name', 'state', 'zipcode']
    ordering_fields = ['id', 'country_code', 'country_name', 'state', 'zipcode']
    ordering = 'state'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = True
    
    action_serializers = {
        'list': serializers.PlaceOfPerformanceSummarySerializer,
        'retrieve': serializers.PlaceOfPerformanceFullSerializer,
        'test': serializers.PlaceOfPerformanceTestSerializer
    }


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
        'values': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter),
        'count': (filters.DiscoveryComplexFilterBackend, RestFrameworkFilterBackend, SearchFilter)
    }
    filter_class = filters.ContractFilter
    search_fields = ['piid', 'agency__name']
    ordering_fields = [
        'id', 'piid', 'base_piid',
        'agency__id', 'agency__name', 
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
        'place_of_performance__country_code', 'place_of_performance__country_name',
        'place_of_performance__state'
    ]
    ordering = '-date_signed'
    
    pagination_class = pagination.ResultSetPagination
    bypass_pagination = False
    
    action_serializers = {
        'list': serializers.ContractSummarySerializer,
        'retrieve': serializers.ContractFullSerializer,
        'test': serializers.ContractTestSerializer
    }


class ListMetadataView(APIView):
    """
    This endpoint returns metadata for the most recent data loads of SAM and FPDS data. It takes no parameters.
    """
    def get(self, request, format=None):
        mds = serializers.MetadataSerializer(metadata.DiscoveryMetadata())
        return Response(mds.data)
