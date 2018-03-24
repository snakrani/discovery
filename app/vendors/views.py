from titlecase import titlecase

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView

from categories.models import Naics, SetAside, Pool
from vendors.models import Vendor, ProjectManager
from contracts.models import Contract

import csv
import os.path


class VendorView(TemplateView):
    pdf_dir = 'static/discovery_site/capability_statements/'
    static_pdf_dir = 'discovery_site/capability_statements/'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        duns = context['vendor_duns']
        capability_statement = self.has_statement(duns)
        context['has_capability_statement'] = capability_statement
        if capability_statement:
            context['capability_statement_url'] = self.get_pdf_path(duns, self.static_pdf_dir)
        return context

    def has_statement(self, duns):
        if os.path.isfile(self.get_pdf_path(duns, self.pdf_dir)):
            return True
        return False

    def get_pdf_path(self, duns, path):
        pdf_path = path
        pdf_path += duns
        pdf_path += '.pdf'
        return pdf_path


def PoolCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
    writer = csv.writer(response)
    #write results
    vendors = Vendor.objects.all()
    setasides_all = SetAside.objects.all().order_by('far_order')
    filter_text = []
    #naics
    naics = Naics.objects.get(code=request.GET['naics-code'])
    vehicle = request.GET['vehicle'].upper()
    pool = Pool.objects.get(naics=naics, vehicle=vehicle)
    vendors = vendors.filter(pools__pool=pool).distinct()
    filter_text.append("NAICS code {0}".format(naics))

    #setasides
    if 'setasides' in request.GET:
        setasides = request.GET.getlist('setasides')[0].split(',')
        setaside_objs = SetAside.objects.filter(code__in=setasides)
        for sobj in setaside_objs:
            vendors = vendors.filter(pools__setasides=sobj)

        filter_text.append("Set Aside filters: {0}".format(", ".join(setasides)))

    writer.writerow(("Vehicle: " + vehicle,))
    writer.writerow(("Search Results: {0} Vendors".format(len(vendors)),))
    writer.writerow(filter_text)

    writer.writerow(('',))
    header_row = ['Vendor', 'Location', 'No. of Contracts',]
    header_row.extend([sa_obj.name for sa_obj in setasides_all])
    writer.writerow(header_row)

    lines = []

    for v in vendors:
        setaside_list = []
        for sa in setasides_all:
            if sa.id in v.pools.filter(pool__id=pool.id).values_list('setasides', flat=True):
                setaside_list.append('X')
            else:
                setaside_list.append('')
                
        if v.sam_location:
            location = "{}, {} {}".format(v.sam_location.city, v.sam_location.state, v.sam_location.zipcode)
        else:
            location = 'NA'

        v_row = [v.name, location, Contract.objects.filter(NAICS=naics.code, vendor=v).count()]
        v_row.extend(setaside_list)
        lines.append(v_row)

    lines.sort(key=lambda x: x[2], reverse=True)
    for line in lines:
        writer.writerow(line)

    return response


def VendorCSV(request, vendor_duns):
    vendor = Vendor.objects.get(duns=vendor_duns)
    setasides = SetAside.objects.all().order_by('far_order')
    
    vendor_sa = []
    pm_names = []
    pm_phones = []
    pm_emails = []

    vehicle = request.GET.get('vehicle', 'None')
    naics = request.GET.get('naics-code', None)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
    writer = csv.writer(response)

    writer.writerow((vendor.name,))
    writer.writerow(('SAM registration expires: ', vendor.sam_expiration_date.strftime("%m/%d/%Y")))
    writer.writerow(('', ))
    writer.writerow([''] + [sa_obj.name for sa_obj in setasides])
    
    if vehicle and naics:
        naics = Naics.objects.get(code=naics)
        pool = Pool.objects.get(naics=naics, vehicle=vehicle.upper())
        membership = None
        
        for mem in vendor.pools.all():
            if pool.id == mem.pool.id:
                membership = mem
                break
        
        if membership:
            for sa in setasides:
                if sa.id in membership.setasides.values_list('id', flat=True):
                    vendor_sa.append('X')
                else:
                    vendor_sa.append('')
            
            if membership.pms.count():
                for pm in membership.pms.all():
                    pm_names.append(pm.name)
                    pm_phones.append(",".join(pm.phone()))
                    pm_emails.append(",".join(pm.email()))
            else:
                pm_names = ['NA']
                pm_phones = ['NA']
                pm_emails = ['NA']
    else:
        for sa in setasides:
            if sa.id in vendor.pools.values_list('setasides', flat=True):
                vendor_sa.append('X')
            else:
                vendor_sa.append('')
    
        if vendor.pools.count():
            for id in vendor.pools.all().values_list('pms', flat=True):
                pm = ProjectManager.objects.get(manager_ptr_id=id)
            
                pm_names.append(pm.name)
                pm_phones.append(",".join(pm.phone()))
                pm_emails.append(",".join(pm.email()))
        else:
            pm_names = ['NA']
            pm_phones = ['NA']
            pm_emails = ['NA']
    
    contracts = Contract.objects.filter(vendor=vendor).order_by('-date_signed')[:1]
    
    if contracts.count() > 0:
        latest_contract = contracts[0]
        number_of_employees = latest_contract.number_of_employees    
        annual_revenue = latest_contract.annual_revenue
    else:
        number_of_employees = 'NA'
        annual_revenue = 'NA'
        

    writer.writerow([''] + vendor_sa)
    writer.writerow(('', ))
    writer.writerow(('DUNS', vendor.duns, '', 'Address:', titlecase(vendor.sam_location.address)))
    writer.writerow(('CAGE Code', vendor.cage, '', '',  titlecase(vendor.sam_location.state) + ', ' + vendor.sam_location.zipcode))
    writer.writerow(['Employees', number_of_employees, '', 'POC:'] + pm_names)
    writer.writerow(['Annual Revenue', annual_revenue, '', ''] + pm_phones)
    writer.writerow(['', '', '', ''] + pm_emails)
    writer.writerow(('', ))
    
    if naics:
        writer.writerow(('This vendor\'s contract history for NAICS {0}'.format(naics.code), ))
        writer.writerow(('{0}'.format(naics.description), ))
    else:
        writer.writerow(('This vendor\'s contract history for all contracts', ))

    writer.writerow(('Date Signed', 'PIID', 'Agency', 'Type', 'Value ($)', 'Email POC', 'Status'))

    if naics:
        contracts = Contract.objects.filter(vendor=vendor, NAICS=naics.root_code).order_by('-date_signed')
    else:
        contracts = Contract.objects.filter(vendor=vendor).order_by('-date_signed')

    for c in contracts:
        writer.writerow((c.date_signed.strftime("%m/%d/%Y"), c.piid, titlecase(c.agency_name), c.pricing_type.name, c.obligated_amount, (c.point_of_contact or "").lower(), c.status.name))

    return response
