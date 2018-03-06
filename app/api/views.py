from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Concat, Coalesce

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from discovery import query
from discovery import metadata
from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts
from api import mixins, filters, serializers, pagination


class DiscoveryReadOnlyModelViewSet(
    mixins.FilterViewSetMixin, 
    mixins.SerializerViewSetMixin, 
    ReadOnlyModelViewSet
): pass
    

class NaicsViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related NAICS code information.
    
    retrieve:
    Returns information for a single NAICS code.
    
    list:
    Returns all of the NAICS codes that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.Naics.objects.all()
    lookup_field = 'code'
    
    action_filters = {
        'list': (SearchFilter, OrderingFilter),
    }
    search_fields = ['code', 'description']
    ordering_fields = ['code', 'root_code', 'description']
    ordering = 'description'
    
    pagination_class = pagination.ResultSetPagination
    serializer_class = serializers.NaicsSerializer


class SetAsideViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related business setaside information.
    
    retrieve:
    Returns information for a single business setaside code.
    
    list:
    Returns all of the business setasides that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.SetAside.objects.all()
    lookup_field = 'code'
    
    action_filters = {
        'list': (SearchFilter, OrderingFilter),
    }
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['code', 'name', 'description']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    serializer_class = serializers.SetAsideSerializer


class PoolViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery related vendor pool information.
    
    retrieve:
    Returns information for a single vendor pool.
    
    list:
    Returns all of the vendor pools that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.Pool.objects.all()
    lookup_field = 'id'
    
    action_filters = {
        'list': (DjangoFilterBackend, SearchFilter, OrderingFilter),
    }
    filter_class = filters.PoolFilter
    search_fields = ['id', 'name', 'number', 'vehicle']
    ordering_fields = ['id', 'name', 'number', 'vehicle']
    ordering = 'name'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers =  { 
        'list': serializers.ShortPoolSerializer, 
        'retrieve': serializers.PoolSerializer 
    }


class ZoneViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to Discovery vendor pool zone information.
    
    retrieve:
    Returns information for a single vendor pool zone.
    
    list:
    Returns all of the vendor pool zones that are relevant to the acquisition vehicles in the Discovery universe.
    """
    queryset = categories.Zone.objects.all()
    lookup_field = 'id'
    
    action_filters = {
        'list': (DjangoFilterBackend, OrderingFilter),
    }
    filter_class = filters.ZoneFilter
    ordering_fields = ['id']
    ordering = 'id'
    
    pagination_class = pagination.ResultSetPagination
    serializer_class = serializers.ZoneSerializer


class VendorViewSet(DiscoveryReadOnlyModelViewSet):
    """
    API endpoint that allows for access to vendor information in the Discovery universe.
    
    retrieve:
    Returns information for a single vendor.
    
    list:
    Returns all of the vendors that contract through the acquisition vehicles in the Discovery universe.
    """
    queryset = vendors.Vendor.objects.all()
    lookup_field = 'duns'
    
    action_filters = {
        'list': (DjangoFilterBackend, SearchFilter, OrderingFilter),
    }
    filter_class = filters.VendorFilter
    search_fields = ['id', 'name', 'duns']
    ordering_fields = [
        'id', 'name', 'duns', 'sam_status', 'sam_exclusion', 'sam_url',
        'sam_location__address', 'sam_location__city', 'sam_location__state', 
        'sam_location__zipcode', 'sam_location__congressional_district',
        'annual_revenue', 'number_of_employees', 'number_of_contracts'
    ]
    ordering = '-number_of_contracts'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers =  { 
        'list': serializers.ShortVendorSerializer, 
        'retrieve': serializers.VendorSerializer 
    }
    
    def get_queryset(self):
        naics_param_name = 'pool_naics_code'
        
        queryset = self.queryset.annotate(
            annual_revenue=Subquery(
                contracts.Contract.objects.filter(vendor=OuterRef('pk')).order_by('-date_signed').values('annual_revenue')[:1]
            ),
            number_of_employees=Subquery(
                contracts.Contract.objects.filter(vendor=OuterRef('pk')).order_by('-date_signed').values('number_of_employees')[:1]
            )
        )
        if naics_param_name in self.request.query_params and self.request.query_params[naics_param_name]:
            contract_list = contracts.Contract.objects.filter(NAICS=self.request.query_params[naics_param_name], vendor=OuterRef('pk')).values('pk')
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
    queryset = contracts.Contract.objects.all()
    lookup_field = 'id'
    
    action_filters = {
        'list': (DjangoFilterBackend, SearchFilter, OrderingFilter),
    }
    filter_class = filters.ContractFilter
    search_fields = ['id', 'name', 'duns']
    ordering_fields = [
        'id', 'piid', 'agency_id', 'agency_name', 'NAICS', 'PSC',
        'date_signed', 'completion_date', 'obligated_amount' 
        'point_of_contact', 'status__name', 'pricing_type__name',
        'place_of_performance_location'
    ]
    ordering = '-date_signed'
    
    pagination_class = pagination.ResultSetPagination
    action_serializers =  { 
        'list': serializers.ShortContractSerializer, 
        'retrieve': serializers.ContractSerializer 
    }
    
    def get_queryset(self):
        return self.queryset.annotate(
            place_of_performance_location = Concat('place_of_performance__country_name', Value(' '), Coalesce('place_of_performance__state', Value('')))
        )


class ListMetadataView(APIView):
    """
    This endpoint returns metadata for the most recent data loads of SAM and FPDS data. It takes no parameters.
    """
    def get(self, request, format=None):
        mds = serializers.MetadataSerializer(metadata.DiscoveryMetadata())
        return Response(mds.data)
