from titlecase import titlecase

from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView

from categories.models import Naics, PSC, SetAside, Pool
from vendors.models import Vendor, ContractManager
from contracts.models import Contract

import csv
import time


def PoolCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
    writer = csv.writer(response)
        
    # Vendor filtering
    setasides_all = SetAside.objects.all().order_by('far_order')
    vendors = Vendor.objects.all().distinct()
    
    naics = None
    vehicle = None
    pools = []
    zone = None
    setasides = []
    
    if 'naics-code' in request.GET:
        naics = Naics.objects.get(code=request.GET['naics-code'])
    
    if 'vehicle' in request.GET:
        vehicle = request.GET['vehicle'].upper()
        
    if 'pool' in request.GET:
        pools = [request.GET['pool'].upper()]
        vendors = vendors.filter(pools__pool__id=pools[0])
    else:
        if vehicle:
            pools = Pool.objects.filter(vehicle=vehicle)
        elif naics:
            pools = Pool.objects.filter(naics=naics.code)
        else:
            pools = Pool.objects.all()
            
        vendors = vendors.filter(pools__pool__id__in=pools.values_list('id', flat=True))
        
    if 'zone' in request.GET:
        zone = request.GET['zone']
        vendors = vendors.filter(pools__zone__id=zone)
    
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
    
    if zone:
        writer.writerow(('Zone', zone))
    
    writer.writerow(('', ))
    writer.writerow(('Included pools',))
    for pool in pools:
        name = "{} pool {}: {}".format(" ".join(pool.vehicle.split('_')), pool.number, pool.name)
        writer.writerow(('', name))
    
    if len(setasides):
        writer.writerow(('', ))
        writer.writerow(('Setasides', ", ".join(setasides)))
    
    writer.writerow(('',))
    writer.writerow(('',))
    writer.writerow(("Search Results: {0} Vendors".format(len(vendors)),))
    
    writer.writerow(('',))
    header_row = ['Vendor', 'Location', 'No. of Contracts', 'Vehicles']
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
            if v_pool.pool.vehicle not in vehicleMap:
                vendor_vehicles.append(" ".join(v_pool.pool.vehicle.split('_')))
                vehicleMap[v_pool.pool.vehicle] = True      
        
        v_row = [v.name, location, contract_list.count(), ", ".join(vendor_vehicles)]
        v_row.extend(setaside_list)
        lines.append(v_row)

    lines.sort(key=lambda x: x[2], reverse=True)
    for line in lines:
        writer.writerow(line)

    return response


def VendorCSV(request, vendor_duns):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
    writer = csv.writer(response)

    # Vendor loading
    vendor = Vendor.objects.get(duns=vendor_duns)
    
    vehicle = None
    naics = None
    
    pools = []
    selected_pools = []
    pool_piids = []
    vendor_pools = {}
    
    setasides = SetAside.objects.all().order_by('far_order')
    vendor_setasides = []
       
    pool_contacts = {}
    
    if 'naics-code' in request.GET:
        naics = Naics.objects.get(code=request.GET['naics-code'])

    if 'vehicle' in request.GET:
        vehicle = request.GET['vehicle'].upper()
        
    if 'pool' in request.GET:
        selected_pools = request.GET['pool'].upper().split(',')
    
    if vehicle:
        pools = Pool.objects.filter(vehicle=vehicle)
    elif naics:
        pools = Pool.objects.filter(naics=naics.code)
    else:
        pools = Pool.objects.all()
            
    pools = pools.values_list('id', flat=True)    
    
    if vendor.pools.count():
        vendor_setaside_ids = vendor.pools.values_list('setasides', flat=True)
        
        for membership in vendor.pools.all():
            pool_id = membership.pool.id
            
            if pool_id in pools:
                pool_name = "{} pool {}: {}".format(" ".join(membership.pool.vehicle.split('_')), membership.pool.number, membership.pool.name)
            
                vendor_pools[pool_id] = {'name': pool_name}
            
                if pool_id in selected_pools:
                    vendor_pools[pool_id]['filter'] = 'X'
                    pool_piids.append(membership.piid)
                else:
                    vendor_pools[pool_id]['filter'] = ''
            
                if membership.cms.count():
                    cm = membership.cms.all()[:1].get()   
                    vendor_pools[pool_id]['contact_name'] = cm.name
                    vendor_pools[pool_id]['contact_phone'] = ",".join(cm.phone())
                    vendor_pools[pool_id]['contact_email'] = ",".join(cm.email())
        
        for sa in setasides:
            if sa.id in vendor_setaside_ids:
                vendor_setasides.append('X')
            else:
                vendor_setasides.append('')
                    
    contracts = Contract.objects.filter(vendor=vendor).order_by('-date_signed')[:1]
    
    if contracts.count() > 0:
        latest_contract = contracts[0]
        number_of_employees = latest_contract.number_of_employees    
        annual_revenue = latest_contract.annual_revenue
    else:
        number_of_employees = 'NA'
        annual_revenue = 'NA'
    
    # Contract filtering
    if naics:
        psc_codes = list(PSC.objects.filter(naics__code=naics.code).distinct().values_list('code', flat=True))    
        contracts = Contract.objects.filter(Q(PSC__in=psc_codes) | Q(NAICS=naics.code), vendor=vendor).order_by('-date_signed')
    else:
        contracts = Contract.objects.filter(vendor=vendor).order_by('-date_signed')
    
    if len(pool_piids) > 0:
        contracts = contracts.filter(base_piid__in = pool_piids) 
        
    # CSV generation
    writer.writerow(('GSA Discovery research results',))
    writer.writerow(('URL: ' + request.build_absolute_uri(),))
    writer.writerow(('Time: ' + time.strftime('%b %d, %Y %l:%M%p %Z'),))
    writer.writerow(('', ))
    
    writer.writerow((vendor.name,))
    writer.writerow(('SAM registration expires: ', vendor.sam_expiration_date.strftime("%m/%d/%Y")))
    writer.writerow(('', ))
    writer.writerow(('DUNS', vendor.duns))
    writer.writerow(('CAGE Code', vendor.cage))
    writer.writerow(('Employees', number_of_employees))
    writer.writerow(('Annual Revenue', annual_revenue))
    writer.writerow(('', ))
    writer.writerow(('Address',))
    writer.writerow((titlecase(vendor.sam_location.address),))
    writer.writerow((titlecase(vendor.sam_location.city) + ', ' + vendor.sam_location.state.upper() + ', ' + vendor.sam_location.zipcode,))
    
    writer.writerow(('', ))
    writer.writerow([''] + [sa_obj.name for sa_obj in setasides])
    writer.writerow([''] + vendor_setasides)
    writer.writerow(('', ))
    
    writer.writerow(('Filter', 'Pool name', 'Contact name', 'Contact phone', 'Contact email'))
    for pool_id, pool_data in vendor_pools.items():
        writer.writerow((
            pool_data['filter'], 
            pool_data['name'],
            pool_data['contact_name'],
            pool_data['contact_phone'],
            pool_data['contact_email']
        ))
    writer.writerow(('', ))
    
    if naics:
        writer.writerow(('Showing vendor contract history for PSCs related to {}'.format(naics.code), ))
        writer.writerow(('NAICS: ', naics.description,))
    else:
        writer.writerow(("Showing this vendor's indexed contract history", ))

    writer.writerow(('', ))
    writer.writerow(("Work performed by a vendor is often reported under a different NAICS code due to FPDS restrictions.",))
    writer.writerow(('', ))
    
    writer.writerow(('Date Signed', 'PIID', 'Agency', 'Type', 'Value ($)', 'Email POC', 'Status'))

    for contract in contracts:
        pricing_type = ''
        status = ''
        
        if contract.pricing_type:
            pricing_type = contract.pricing_type.name
        
        if contract.status:
            status = contract.status.name
                
        writer.writerow((contract.date_signed.strftime("%m/%d/%Y"), contract.piid, titlecase(contract.agency_name), pricing_type, contract.obligated_amount, (contract.point_of_contact or "").lower(), status))

    return response
