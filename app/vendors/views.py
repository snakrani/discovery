from titlecase import titlecase

from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest

from categories.models import Naics, PSC, SetAside, Vehicle, Pool, Zone
from vendors.models import Vendor, Contact
from contracts.models import Contract

from discovery.csv import format_duns

import csv
import time


def VendorCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vendors.csv"'
    writer = csv.writer(response)
        
    # Vendor filtering
    setasides_all = SetAside.objects.all().order_by('far_order')
    vendors = Vendor.objects.all().distinct()
    
    naics = None
    vehicle = None
    pools = []
    zones = []
    setasides = []
    
    if 'naics' in request.GET:
        naics = Naics.objects.get(code=request.GET['naics'])
    
    if 'vehicle' in request.GET:
        vehicle = request.GET['vehicle'].upper()
        
    if 'pools' in request.GET:
        pools = Pool.objects.filter(id__in=request.GET.getlist('pools')[0].split(','))
    else:
        if vehicle:
            pools = Pool.objects.filter(vehicle__id=vehicle)
        elif naics:
            pools = Pool.objects.filter(naics=naics.code)
        else:
            pools = Pool.objects.all()
            
    vendors = vendors.filter(pools__pool__id__in=pools.values_list('id', flat=True))
        
    if 'zones' in request.GET:
        zones = Zone.objects.filter(id__in=request.GET.getlist('zones')[0].split(','))
        vendors = vendors.filter(pools__zones__id__in=zones.values_list('id', flat=True))
    
    if 'setasides' in request.GET:
        setasides = request.GET.getlist('setasides')[0].split(',')
        setaside_objs = SetAside.objects.filter(code__in=setasides)
        
        for sobj in setaside_objs:
            vendors = vendors.filter(pools__setasides=sobj)

    # CSV generation
    writer.writerow(('GSA Discovery research results',))
    writer.writerow(('URL: ' + request.build_absolute_uri(),))
    writer.writerow(('Time: ' + time.strftime('%b %d, %Y %l:%M%p %Z'),))
    writer.writerow(('', ))
    
    if naics:
        writer.writerow(('NAICS code', "{}: {}".format(naics.code, naics.description)))
    
    if len(setasides):
        writer.writerow(('Setasides', ", ".join(setaside_objs.values_list('name', flat=True))))
    
    writer.writerow(('', ))
    writer.writerow(('Included zones:',))
    for zone in zones:
        name = "Zone {}: {}".format(zone.id, ", ".join(zone.states.all().values_list('code', flat=True)))
        writer.writerow(('', name))
    
    writer.writerow(('', ))
    writer.writerow(('Included pools:',))
    for pool in pools:
        name = "{} {}: {}".format(" ".join(pool.vehicle.id.split('_')), pool.number, pool.name)
        writer.writerow(('', name))
    
    writer.writerow(('',))
    writer.writerow(("Search Results: {0} Vendors".format(len(vendors)),))
    
    writer.writerow(('',))
    header_row = ['Vendor DUNS', 'Vendor Name', 'Location', 'No. of Contracts', 'Vehicles']
    header_row.extend([sa_obj.name for sa_obj in setasides_all])
    writer.writerow(header_row)

    lines = []

    for v in vendors:
        setaside_list = []
        for sa in setasides_all:
            if sa.id in v.pools.all().values_list('setasides', flat=True):
                setaside_list.append('X')
            else:
                setaside_list.append('')
                
        if v.sam_location:
            location = "{}, {} {}".format(v.sam_location.city, v.sam_location.state, v.sam_location.zipcode)
        else:
            location = 'NA'
        
        if naics:    
            psc_codes = list(PSC.objects.filter(naics__code=naics.code).distinct().values_list('code', flat=True))
            contract_list = Contract.objects.filter(Q(PSC__in=psc_codes) | Q(NAICS=naics.code), vendor=v)
        else:
            contract_list = Contract.objects.filter(vendor=v)
        
        vehicleMap = {}
        vendor_vehicles = []  
        for v_pool in v.pools.all():
            if v_pool.pool.vehicle.id not in vehicleMap:
                vendor_vehicles.append(" ".join(v_pool.pool.vehicle.id.split('_')))
                vehicleMap[v_pool.pool.vehicle.id] = True      
        
        v_row = [format_duns(v.duns), v.name, location, contract_list.count(), ", ".join(vendor_vehicles)]
        v_row.extend(setaside_list)
        lines.append(v_row)

    lines.sort(key=lambda x: x[3], reverse=True)
    for line in lines:
        writer.writerow(line)

    return response
