from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import Naics, SetAside, Pool, Zone
from vendors.models import Vendor, SamLoad
from contracts.models import Contract, FPDSLoad
from api.serializers import VendorSerializer, NaicsSerializer, ZoneSerializer, PoolSerializer, ShortVendorSerializer, ContractSerializer, Metadata, MetadataSerializer, ShortPoolSerializer
from api.pagination import PaginationSerializer

import json


def get_nested_value(data, keys):
    try:
        if keys and data:
            element  = keys[0]
            if element:
                value = data.get(element)
                return value if len(keys) == 1 else get_nested_value(value, keys[1:])
    
    except Exception:
        pass
    
    return None


def get_page(items, request):
    paginator = Paginator(items, min(int(request.QUERY_PARAMS.get('count', 100)), 100))
    items = paginator.page(request.QUERY_PARAMS.get('page', 1))
           
    serializer = PaginationSerializer(items, context={'request': request})       
    serializer.data['num_results'] = serializer.data['count']       
    del serializer.data['count']
    
    return serializer


def get_naics(request):
    naics = request.QUERY_PARAMS.get('naics', None)
    
    if naics and naics != 'all':
        return Naics.objects.get(code=naics)
    
    return None


def get_pools(request, naics=None):
    vehicle = request.QUERY_PARAMS.get('vehicle', None)
    
    if vehicle and vehicle.lower() not in settings.VEHICLES:
        raise Exception("Acquisition vehicle {} not found".format(vehicle))
    
    if vehicle and naics:
        return [Pool.objects.get(naics=naics, vehicle=vehicle.upper())]
    elif vehicle:
        return Pool.objects.filter(vehicle=vehicle.upper())
    elif naics:
        return Pool.objects.filter(naics=naics)
    else:
        return Pool.objects.all()


def get_setasides(request):
    setaside_str = request.QUERY_PARAMS.get('setasides', None)
    
    if setaside_str:
        setasides = [sa.strip() for sa in setaside_str.split(',')]
        results = SetAside.objects.filter(code__in=setasides)
        
        if len(setasides) != len(results):
            raise Exception("Invalid setasides specified: {}".format(setaside_str))
        
        return results
    
    return None


def get_ordered_results(queryset, request, serializer_class, context = {}):
    descending = False if serializer_class.sort_direction() == 'asc' else True
    
    context.update({'request': request})
    
    if request.QUERY_PARAMS.get('direction', None):
        descending = False if request.QUERY_PARAMS.get('direction', 'desc') == 'asc' else True
    
    sort = serializer_class.sort_field(request.QUERY_PARAMS.get('sort', None))
 
    items = serializer_class(queryset, context=context)
    items.data.sort(key=lambda k: get_nested_value(k, sort), reverse=descending)
    return items.data


class ListNaics(APIView):
    """
    This endpoint lists all of the NAICS codes that are relevant to the OASIS family of vehicles.

    ---
    GET:
        parameters:
          - name: q
            paramType: query
            description: Text to search within NAICS description
            required: false
            type: string
    """
    def get(self, request, format=None):
        try:
            serializer = NaicsSerializer(self.get_results(request.QUERY_PARAMS.get('q', None)), many=True)
        
        except Exception as error:
            return HttpResponseBadRequest(error)
        
        return Response({
            'num_results': len(serializer.data), 
            'results': serializer.data
        })

    def get_results(self, query):
        codes = Naics.objects.all().order_by('description')

        if query:
            codes = codes.filter(description__icontains=query)

        return codes


class ListPools(APIView):
    """
    This endpoint lists all of the acquisition vehicle pools.

    ---
    GET:
        parameters:
          - name: vehicle
            paramType: query
            description: Filter pools by vehicle.  Choices are; oasis, oasis_sb, hcats, hcats_sb. Will filter vendors by their presence in either the OASIS unrestricted vehicle or the OASIS Small Business vehicle.
            required: false
            type: string
          - name: naics
            paramType: query
            description: NAICS code that pool services
            required: false
            type: string
    """
    def get(self, request, format=None):
        try:
            serializer = PoolSerializer(self.get_results(
                request.QUERY_PARAMS.get('vehicle', None),
                get_naics(request)
            ), many=True)
        
        except Exception as error:
            return HttpResponseBadRequest(error)
        
        return Response({
            'num_results': len(serializer.data), 
            'results': serializer.data
        })

    def get_results(self, vehicle, naics):
        pools = Pool.objects.all().order_by('id')

        if vehicle:
            pools = pools.filter(vehicle=vehicle.upper())

        if naics:
            pools = pools.filter(naics__code=naics.code)

        return pools


class ListZones(APIView):
    """
    This endpoint lists all of the acquisition vehicle zones.

    ---
    GET:
        parameters:
          - name: state
            paramType: query
            description: State code within zone
            required: false
            type: string
    """
    def get(self, request, format=None):
        try:
            serializer = ZoneSerializer(self.get_results(request.QUERY_PARAMS.get('state', None)), many=True)
        
        except Exception as error:
            return HttpResponseBadRequest(error)
        
        return Response({
            'num_results': len(serializer.data), 
            'results': serializer.data
        })

    def get_results(self, state):
        zones = Zone.objects.all().order_by('id')

        if state:
            zones = zones.filter(state__state=state)

        return zones


class GetVendor(APIView):
    """
    This endpoint returns a single vendor by their 9 digit DUNS number. DUNS numbers can be looked up in the [System for Award Management](https://www.sam.gov) by vendor name.
    
    ---
    GET:
        parameters:
          - name: duns
            description: a nine digit DUNS number that uniquely identifies the vendor (required)
            required: true
            type: string
            paramType: path
    """
    def get(self, request, duns, format=None):
        try:
            serializer = VendorSerializer(Vendor.objects.get(duns=duns)) 
        
        except Exception as error:
            return HttpResponseBadRequest(error)
        
        return Response(serializer.data) 


class ListVendors(APIView):
    """
    This endpoint returns a list of vendors potentially filtered by a NAICS code. The NAICS code maps to an OASIS pool and is used to retrieve vendors in that pool only.

    OASIS pools are groupings of NAICS codes that have the same small business size standard. Because contracts solicited to OASIS vendors can only be issued to one pool, much of the data is presented as part of a pool grouping. Using the NAICS code is a shortcut, so that you don't have to explicitly map the NAICS code to a pool in OASIS yourself.
    
    Vendors can also be filtered by a particular setaside. Valid values for the setasides are short codes which include:

    * 8(A) (8(a))
    * HubZ (Hubzone)
    * SDVO (service disabled veteran owned)
    * WO (women owned)
    * VO (veteran owned)
    * SDB (small disadvantaged business).

    ---
    GET:
        parameters:
          - name: vehicle
            paramType: query
            description: Choices are; oasis, oasis_sb, hacts, hcats_sb. Will filter vendors by their presence in either the OASIS unrestricted vehicle or the OASIS Small Business vehicle.
            required: false
            type: string
          - name: naics
            paramType: query
            description: a six digit NAICS code
            required: false
            type: string
          - name: setasides  
            paramType: query
            allowMultiple: true
            description: a comma delimited list of two character setaside identifiers to filter by.  Ex. setasides=8(A),VO will filter by 8a and veteran owned businesses.
            required: false
            type: string
          - name: sort
            paramType: query
            required: false
            description: A field to sort on. Can sort by any result field.  Nested fields can be sorted with keys separated by a comma.
            type: string
          - name: direction
            paramType: query
            description: The sort direction of the results. Choices are asc or desc.
            type: string
            required: false
          - name: page
            paramType: query
            description: The page (starting from 1) to access. Results are paginated in default increments of 100.
            type: string
            required: false
          - name: count
            paramType: query
            description: The number of vendors to return per page (default/max 100)
            type: string
            required: false
    """
    def get(self, request, format=None):  
        try:
            naics = get_naics(request)
            pools = get_pools(request, naics)
            
            pool_serializer = ShortPoolSerializer(pools)
            vendor_serializer = get_page(self.get_results(pools, get_setasides(request), naics), request)
            
            sam_load_results = SamLoad.objects.all().order_by('-sam_load')[:1]
            last_updated = sam_load_results[0].sam_load if sam_load_results else None
        
        except Exception as error:
            return HttpResponseBadRequest(error)
        
        return Response({ 
            'num_results': vendor_serializer.data['num_results'],
            'last_updated': last_updated,
            'pools' : pool_serializer.data,  
            'page': vendor_serializer.data
        })
                 
    def get_results(self, pools, setasides, naics):
        vendors = Vendor.objects.filter(pools__in=pools).distinct()
        
        if setasides:
            for sa in setasides:
                vendors = vendors.filter(setasides=sa)

        return get_ordered_results(vendors, self.request, ShortVendorSerializer, {'naics': naics})


class ListContracts(APIView):
    """   
    This endpoint returns contract history from FPDS for a specific vendor. The vendor's DUNS number is a required parameter. You can also filter contracts by their NAICS code to find contracts relevant to a particular category. 
    
    ---
    GET:
        parameters:
          - name: duns
            description: A 9-digit DUNS number that uniquely identifies a vendor (required).
            required: true
            type: string
            paramType: query
          - name: naics
            description: A six digit NAICS code used to filter by contracts with a certain NAICS
            type: string
            required: false
            paramType: query
          - name: sort
            paramType: query
            required: false
            description: A field to sort on. Can sort by any result field.  Nested fields can be sorted with keys separated by a comma.
            type: string
          - name: direction
            paramType: query
            description: The sort direction of the results. Choices are asc or desc.
            type: string
            required: false
          - name: page
            paramType: query
            description: The page (starting from 1) to access. Results are paginated in default increments of 100.
            type: string
            required: false
          - name: count
            paramType: query
            description: The number of vendors to return per page (default/max 100)
            type: string
            required: false
    """
    def get(self, request, format=None):
        try:
            duns = self.request.QUERY_PARAMS.get('duns', None)
            if not duns:
                raise Exception("Vendor DUNS required to retrieve contracts")
            
            vendor = Vendor.objects.get(duns=duns)
            contract_serializer = get_page(self.get_results(vendor, 
                                                            get_naics(request)), 
                                           request)
            
            fpds_load_results = FPDSLoad.objects.filter(vendor=vendor)
            last_updated = fpds_load_results[0].load_date if fpds_load_results else None
        
        except Exception as error:
            return HttpResponseBadRequest(error)
        
        return Response({ 
            'num_results': contract_serializer.data['num_results'],
            'last_updated': last_updated,
            'page': contract_serializer.data
        })

    def get_results(self, vendor, naics):
        contracts = Contract.objects.filter(vendor=vendor)
        
        if naics:
            contracts = contracts.filter(NAICS=naics.root_code)
        
        return get_ordered_results(contracts, self.request, ContractSerializer)


class MetadataView(APIView):
    """
    This endpoint returns metadata for the most recent data loads of SAM and FPDS data. It takes no parameters.
    """
    def get(self, request, format=None):
        try:
            mds = MetadataSerializer(Metadata())
        
        except Exception as error:
            return HttpResponseBadRequest(error)
        
        return Response(mds.data)
