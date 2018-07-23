from titlecase import titlecase

from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView

from categories.models import VEHICLE_CHOICES, Naics, PSC, SetAside, Pool
from vendors.models import Vendor, ContractManager
from contracts.models import Contract

import csv
import time
import json


def format_duns(text):
    return str(text).zfill(9)


def get_vehicle_name(id):
    for vehicle_info in VEHICLE_CHOICES:
        if vehicle_info[0] == id:
            return vehicle_info[1];
    return ''


def get_memberships(vendor):
    membership_map = {}
    
    for membership in vendor.pools.all():
        piid = membership.piid
        vehicle_id = membership.pool.vehicle
        vehicle_name = get_vehicle_name(vehicle_id)
        pool_id = membership.pool.id
        pool_number = membership.pool.number
        
        cms = membership.cms.all()
        contact_name = cms[0].name
        contact_phone = ",".join(cms[0].phone())
        contact_email = ",".join(cms[0].email())
        
        if piid not in membership_map:
            membership_map[piid] = {
                'vehicle_ids': [],
                'vehicle_names': [],
                'pool_ids': [],
                'pool_numbers': [],
                'zones': [],
                'contacts': [],
                'phones': [],
                'emails': [],
                'setasides': [],
                'reference': membership
            }
            
        if vehicle_id not in membership_map[piid]['vehicle_ids']:
            membership_map[piid]['vehicle_ids'].append(vehicle_id)
            membership_map[piid]['vehicle_names'].append(vehicle_name)
            
        if pool_id not in membership_map[piid]['pool_ids']:
            membership_map[piid]['pool_ids'].append(pool_id)
            membership_map[piid]['pool_numbers'].append(pool_number)
        
        for zone in membership.zones.all():    
            if str(zone.id) not in membership_map[piid]['zones']:
                membership_map[piid]['zones'].append(str(zone.id))
            
        if contact_name not in membership_map[piid]['contacts']:
            membership_map[piid]['contacts'].append(contact_name)
            
        if contact_phone not in membership_map[piid]['phones']:
            membership_map[piid]['phones'].append(contact_phone)
            
        if contact_email not in membership_map[piid]['emails']:
            membership_map[piid]['emails'].append(contact_email)
            
        for setaside in membership.setasides.all():
            if setaside.code not in membership_map[piid]['setasides']:
                membership_map[piid]['setasides'].append(setaside.code)
            
    return membership_map
 
 
def get_membership_name(membership_map, piid):
    info = membership_map[piid]
    vehicles = sorted(info['vehicle_names'])
    
    def sort_key(name):
        try:
            return int(name)
        except Exception:
            return name
    
    pools = sorted(info['pool_numbers'], key=sort_key)
    zones = sorted(info['zones'], key=sort_key)
    
    name = ",".join(vehicles) + ' (Service categories: ' + ",".join(pools) + ') '

    if len(info['zones']):
        name += ' (Zones: ' + ",".join(zones) + ')'
    
    return name.strip()


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
    
    if 'naics' in request.GET:
        naics = Naics.objects.get(code=request.GET['naics'])
    
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
        name = "{} {}: {}".format(" ".join(pool.vehicle.split('_')), pool.number, pool.name)
        writer.writerow(('', name))
    
    if len(setasides):
        writer.writerow(('', ))
        writer.writerow(('Setasides', ", ".join(setasides)))
    
    writer.writerow(('',))
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
            if v_pool.pool.vehicle not in vehicleMap:
                vendor_vehicles.append(" ".join(v_pool.pool.vehicle.split('_')))
                vehicleMap[v_pool.pool.vehicle] = True      
        
        v_row = [format_duns(v.duns), v.name, location, contract_list.count(), ", ".join(vendor_vehicles)]
        v_row.extend(setaside_list)
        lines.append(v_row)

    lines.sort(key=lambda x: x[3], reverse=True)
    for line in lines:
        writer.writerow(line)

    return response


def VendorCSV(request, vendor_duns):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
    writer = csv.writer(response)

    # Vendor loading
    vendor = Vendor.objects.get(duns=vendor_duns)
    membership_map = get_memberships(vendor)
    membership_rows = []
    
    naics = None    
    memberships = []
    
    setasides_all = SetAside.objects.all().order_by('far_order')
    
    if 'naics' in request.GET:
        naics = Naics.objects.get(code=request.GET['naics'])
   
    if 'memberships' in request.GET:
        memberships = request.GET['memberships'].split(',')
        
    for piid, info in membership_map.items():
        row = {}
        setasides = []
        
        row['filter'] = piid in memberships
        row['piid'] = piid
        row['name'] = get_membership_name(membership_map, piid)
        row['contact_name'] = ",".join(info['contacts'])
        row['contact_phone'] = ",".join(info['phones'])
        row['contact_email'] = ",".join(info['emails'])
        
        for sa in setasides_all:
            if sa.code in info['setasides']:
                setasides.append('X')
            else:
                setasides.append('')
        
        row['setasides'] = setasides
        
        membership_rows.append(row)
                    
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
    
    if len(memberships) > 0:
        contracts = contracts.filter(base_piid__in = memberships) 
        
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
    
    filter_labels = ['Filter', 'Contract PIID', 'Name', 'Contact name', 'Contact phone', 'Contact email']
    filter_labels.extend([sa_obj.name for sa_obj in setasides_all])
    
    writer.writerow(filter_labels)
    for filter_row in membership_rows:
        filter_data = [
            'X' if filter_row['filter'] else '',
            filter_row['piid'],
            filter_row['name'],
            filter_row['contact_name'],
            filter_row['contact_phone'],
            filter_row['contact_email']
        ]
        filter_data.extend(filter_row['setasides'])
        writer.writerow(filter_data)

    writer.writerow(('', ))
    
    if naics:
        writer.writerow(('Showing vendor contract history for PSCs related to {}'.format(naics.code), ))
        writer.writerow(('NAICS: ', "{} - {}".format(naics.code, naics.description),))
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
