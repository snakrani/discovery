from titlecase import titlecase

from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest

from categories.models import Naics, PSC, SetAside
from vendors.models import Vendor, Contact
from contracts.models import Contract

from discovery.csv import get_memberships, get_membership_name

import csv
import time


def ContractCSV(request, vendor_duns):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vendor_contracts.csv"'
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

    for contract in contracts.iterator():
        pricing_type = ''
        status = ''
        
        if contract.pricing_type:
            pricing_type = contract.pricing_type.name
        
        if contract.status:
            status = contract.status.name
                
        writer.writerow((contract.date_signed.strftime("%m/%d/%Y"), contract.piid, titlecase(contract.agency_name), pricing_type, contract.obligated_amount, (contract.point_of_contact or "").lower(), status))

    return response
