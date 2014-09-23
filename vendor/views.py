from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from vendor.models import Vendor, Pool, Naics, SetAside
from contract.models import Contract
import csv

def pool_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
    writer = csv.writer(response)
    #write results
    vendors = Vendor.objects.all()
    setasides_all = SetAside.objects.all().order_by('far_order')
    filter_text = []
    #naics
    if 'naics-code' in request.GET:
        naics = request.GET['naics-code']
        naics_obj = Naics.objects.get(short_code=naics)
        vendors = vendors.filter(pools__naics=naics_obj)
        filter_text.append("NAICS code {0}".format(naics))
    #setasides
    if 'setasides' in request.GET:
        setasides = request.GET.getlist('setasides')[0].split(',')
        setaside_objs = SetAside.objects.filter(code__in=setasides)
        for sobj in setaside_objs:
            vendors = vendors.filter(setasides=sobj)

        filter_text.append("Set Aside filters: {0}".format(", ".join(setasides)))

    writer.writerow(("Search Results: {0} Vendors".format(len(vendors)),))
    writer.writerow(filter_text)

    writer.writerow(('',))
    header_row = ['Vendor', 'Location']
    header_row.extend([sa_obj.short_name for sa_obj in setasides_all])
    writer.writerow(header_row)

    for v in vendors: 
        setaside_list = []
        for sa in setasides_all:
            if sa in v.setasides.all():
                setaside_list.append('X')
            else:
                setaside_list.append('')

        v_row = [v.name, v.sam_citystate]
        v_row.extend(setaside_list)
        writer.writerow(v_row)

    return response


def vendor_csv(request, vendor_duns):
    vendor = Vendor.objects.get(duns=vendor_duns)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
    writer = csv.writer(response)

    writer.writerow((vendor.name,))
    writer.writerow(('SAM registration expires: ', vendor.sam_expiration_date))
    writer.writerow(('', ))
    writer.writerow(('8(a)', 'HubZ', 'SDVO', 'WO', 'VO', 'SDB'))
    
    vendor_sa = []
    for sa in  SetAside.objects.all().order_by('far_order'):
        if sa in vendor.setasides.all():
            vendor_sa.append('X')
        else:
            vendor_sa.append('')

    writer.writerow(vendor_sa)
    writer.writerow(('', ))
    writer.writerow(('DUNS', vendor.duns, '', 'Address:', vendor.sam_address))
    writer.writerow(('CAGE Code', vendor.cage, '', '', vendor.sam_citystate))
    writer.writerow(('Employees', vendor.number_of_employees, '', 'OASIS POC:', vendor.pm_name))
    writer.writerow(('Annual Revenue', vendor.annual_revenue, '', '', vendor.pm_phone))
    writer.writerow(('', '', '', '', vendor.pm_email))
    writer.writerow(('', ))
    writer.writerow(('This vendor\'s contract history', ))
    writer.writerow(('Date Signed', 'PIID', 'Agency', 'Type', 'Value ($)', 'Email POC', 'Status'))

    for c in Contract.objects.filter(vendor=vendor).order_by('-date_signed'):
        if '_' in c.piid:
            piid = c.piid.split('_')[1]
        else:
            piid = c.piid
        writer.writerow((c.date_signed, piid, c.agency_name, c.get_pricing_type_display(), c.obligated_amount, c.point_of_contact, c.status))

    return response


