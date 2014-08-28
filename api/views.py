from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from rest_framework.response import Response
from rest_framework.views import APIView

from contract.models import Contract
from vendor.models import Vendor, Naics, SetAside, SamLoad, Pool
from api.serializers import VendorSerializer, NaicsSerializer, PoolSerializer, ShortVendorSerializer, ContractSerializer


def filter_vendors(obj):
    vendors = Vendor.objects.all()
    naics = obj.request.QUERY_PARAMS.get('naics', None)
    setasides = obj.request.QUERY_PARAMS.get('setasides', None)
    
    if naics == "all":
        naics = None
    naics_obj = None

    if naics:
        try:
            naics_obj = Naics.objects.get(short_code=naics)
            vendors = vendors.filter(pools__naics=naics_obj)
        except:
            #return an empty list if no naics match
            return (Vendor.objects.none(), None)

    if setasides:
        setasides = setasides.split(',')
        for sa in SetAside.objects.filter(code__in=setasides):
            vendors = vendors.filter(setasides=sa)                
    
    return (vendors, naics_obj)

def create_or_add_to_pool(pool_array, pool, vendor):

    for p in pool_array:
        if p['id'] == pool.id:
            #add vendor and return
            p['vendors'].append(ShortVendorSerializer(vendor).data)
            return

    #didn't return, pool not in there, need to add it
    serial_pool = PoolSerializer(pool).data
    serial_pool['vendors'] = [ShortVendorSerializer(vendor).data]
    pool_array.append(serial_pool)

class GetVendor(APIView):

    def get(self, request, duns, format=None):
        vendor = Vendor.objects.get(duns=duns) 
        return Response(VendorSerializer(vendor).data) 



class ListVendors(APIView):
    
    def get(self, request, format=None):

        group =  request.QUERY_PARAMS.get('group', None)
        pool_id = request.QUERY_PARAMS.get('pool', None)

        #check if request is limited by a pool (only used if naics not supplied)
        if pool_id: 
            pool_id = pool_id.upper()
         
        try:
            pool_filter = Pool.objects.get(id=pool_id)
        except Pool.DoesNotExist as e:
            pool_id = None
            pass #invalid pool id

        sam_load_results = SamLoad.objects.all().order_by('-sam_load')[:1]
        sam_load = sam_load_results[0].sam_load if sam_load_results else None

        if group and group == 'pool':
            vendors, naics = filter_vendors(self)
            resp_json = { 'results': [] }
            
            for v in vendors:
                v_pools = v.pools.all()
                for p in v_pools:
                    #if there is a naics code, only return pools relevant to that naics
                    if naics: 
                        if naics in p.naics.all():
                            create_or_add_to_pool(resp_json['results'], p, v)
                    elif pool_id:
                        if p == pool_filter:
                            create_or_add_to_pool(resp_json['results'], p, v)
                    else:
                        create_or_add_to_pool(resp_json['results'], p, v)
            
            resp_json['results'] = sorted(resp_json['results'], key=lambda k: k['number'])
            resp_json['num_results'] = vendors.count()
            resp_json['sam_load'] = sam_load
            return Response(resp_json)

        else:
            serializer = VendorSerializer(self.get_queryset(), many=True)
            return  Response({ 'num_results': len(serializer.data), 'sam_load':sam_load, 'results': serializer.data } )

    def get_queryset(self):
        vendors, naics = filter_vendors(self)
        return vendors


class ListNaics(APIView):

    def get(self, request, format=None):
        serializer = NaicsSerializer(self.get_queryset(), many=True)
        return Response({'num_results': len(serializer.data), 'results': serializer.data})

    def get_queryset(self):
        codes = Naics.objects.all()

        #filters
        q = self.request.QUERY_PARAMS.get('q', None)

        if q:
            codes = Naics.objects.filter(description__icontains=q)
        else:
            codes = Naics.objects.all()

        return codes

class ListContracts(APIView):
    
    def get(self, request, format=None):
        contracts = self.get_queryset()

        if contracts == 1:
            return HttpResponseBadRequest("You must provide a vendor DUNS to retrieve contracts.")

        elif not contracts:
            return Response({'num_results': 0, 'results': []})

        else:
            serializer = ContractSerializer(contracts)
            return Response({'num_results': len(serializer.data), 'results': serializer.data})

    def get_queryset(self):
        
        duns = self.request.QUERY_PARAMS.get('duns', None)
        naics = self.request.QUERY_PARAMS.get('naics', None)

        if not duns:
            return 1

        vendor = Vendor.objects.get(duns=duns)
        contracts = Contract.objects.filter(vendor=vendor)

        if naics:
            #contracts = contracts.filter(NAICS=Naics.objects.filter(code=naics)[0])
            contracts = contracts.filter(NAICS=naics)  #change to above when naics loaded right

        return contracts



