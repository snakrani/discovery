from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from vendor.models import Vendor, Naics, SetAside, SamLoad
from api.serializers import VendorSerializer, NaicsSerializer, PoolSerializer, ShortVendorSerializer


def filter_vendors(obj):
    vendors = Vendor.objects.all()
    naics = obj.request.QUERY_PARAMS.get('naics', None)
    setasides = obj.request.QUERY_PARAMS.get('setasides', None)
    
    if naics:
        try:
            naics_obj = Naics.objects.get(short_code=naics)
            vendors = vendors.filter(pools__naics=naics_obj)
        except:
            #return an empty list if no naics match
            return Vendor.objects.none()

    if setasides:
        setasides = setasides.split(',')
        for sa in SetAside.objects.filter(code__in=setasides):
            vendors = vendors.filter(setasides=sa)                
    
    return vendors

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


class ListVendors(APIView):
    
    def get(self, request, format=None):

        group =  request.QUERY_PARAMS.get('group', None)
        sam_load = SamLoad.objects.all().order_by('-sam_load')[:1]
        if group and group == 'pool':
            vendors = filter_vendors(self)
            resp_json = { 'results': [] }
            
            for v in vendors:
                v_pools = v.pools.all()
                for p in v_pools:
                    create_or_add_to_pool(resp_json['results'], p, v)
           
            resp_json['num_results'] = vendors.count()
            resp_json['sam_load'] = sam_load
            return Response(resp_json)

        else:
            serializer = VendorSerializer(self.get_queryset(), many=True)
            return  Response({ 'num_results': len(serializer.data), 'sam_load':sam_load[0].sam_load, 'results': serializer.data } )

    def get_queryset(self):
        return filter_vendors(self)


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
