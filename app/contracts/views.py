from titlecase import titlecase

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from discovery.csv import get_memberships, get_membership_name, BaseCSVView
from discovery.cache import track_page_load

from categories import models as categories
from vendors import models as vendors
from contracts import models as contracts

import csv
import time


# Filters:
# 
#     naics={CODE},...
#     memberships={PIID},...
#     countries={CODE},...
#     states={CODE},...
#


class ContractCSV(BaseCSVView):
    
    def __init__(self, **kwargs):
        super(ContractCSV, self).__init__(**kwargs)
        
        # Filters
        self.vendor = None
        
        self.naics_param = 'naics'
        self.naics = []
        
        self.memberships_param = 'memberships'
        self.memberships = []
        
        self.countries_param = 'countries'
        self.countries = []
        
        self.states_param = 'states'
        self.states = []
        
        # Queries
        self.setaside_data = categories.SetAside.objects.all().order_by('far_order')
        self.contract_data = contracts.Contract.objects.all().order_by('-date_signed')


    def _render_vendor(self, writer):
        writer.writerow((self.vendor.name,))
        writer.writerow(('SAM registration expires: ', self.vendor.sam_expiration_date.strftime("%m/%d/%Y")))
        writer.writerow(('', ))
        writer.writerow(('DUNS', self.vendor.duns))
        writer.writerow(('CAGE Code', self.vendor.cage))
        writer.writerow(('', ))
        writer.writerow(('Address',))
        writer.writerow((titlecase(self.vendor.sam_location.address),))
        writer.writerow((titlecase(self.vendor.sam_location.city) + ', ' + self.vendor.sam_location.state.upper() + ', ' + self.vendor.sam_location.zipcode,))
        
        writer.writerow(('', ))

    def _process_vendor(self, writer, duns):
        self.vendor = vendors.Vendor.objects.get(duns=duns)
        self.contract_data = self.contract_data.filter(vendor=self.vendor)
        self._render_vendor(writer)

    
    def _render_naics(self, writer):
        naics_data = categories.Naics.objects.filter(code__in=self.naics)
        
        writer.writerow(('Contract NAICS codes:', 'Code', 'Description'))
        
        for naics in naics_data:
            writer.writerow(('', naics.code, naics.description))
        
        writer.writerow(('', ))       
    
    def _process_naics(self, writer):
        self.naics = self.get_params(self.naics_param)
        
        if len(self.naics) > 0:
            naics_data = categories.Naics.objects.filter(code__in=self.naics)
            sin_codes = {}
                
            for naics in naics_data:
                for sin_code in list(naics.sin.all().values_list('code', flat=True)):
                    sin_codes[sin_code] = True
                
            psc_codes = list(categories.PSC.objects.filter(sin__code__in=sin_codes.keys()).distinct().values_list('code', flat=True))
            
            self.contract_data = self.contract_data.filter(Q(PSC__in=psc_codes) | Q(NAICS__in=self.naics))
            self._render_naics(writer)

  
    def _render_memberships(self, writer):
        membership_map = get_memberships(self.vendor)
        membership_rows = []
        
        labels = ['Vendor vehicle memberships:', 'Filter', 'Contract PIID', 'Name', 'Contact name', 'Contact phone', 'Contact email']
        labels.extend([sa_obj.name for sa_obj in self.setaside_data])
        writer.writerow(labels)
        
        for piid, info in membership_map.items():
            setasides = []
            
            for sa in self.setaside_data:
                if sa.code in info['setasides']:
                    setasides.append('X')
                else:
                    setasides.append('')
            
            filter_data = [
                '',
                'X' if piid in self.memberships else '',
                piid,
                get_membership_name(membership_map, piid),
                ",".join(info['contacts']),
                ",".join(info['phones']),
                ",".join(info['emails'])
            ]
            filter_data.extend(setasides)
            writer.writerow(filter_data)
        
        writer.writerow(('', ))       
    
    def _process_memberships(self, writer):
        self.memberships = self.get_params(self.memberships_param)
        
        if len(self.memberships) > 0:
            self.contract_data = self.contract_data.filter(base_piid__in = self.memberships)
            self._render_memberships(writer)

  
    def _render_countries(self, writer):
        writer.writerow(('Contract place of performance countries:', 'Code'))
        
        for country in self.countries:
            writer.writerow(('', country))
        
        writer.writerow(('', ))       
    
    def _process_countries(self, writer):
        self.countries = self.get_params(self.countries_param)
        
        if len(self.countries) > 0:
            self.contract_data = self.contract_data.filter(place_of_performance__country_code__in=self.countries)
            self._render_countries(writer)

  
    def _render_states(self, writer):
        writer.writerow(('Contract place of performance states:', 'Code'))
        
        for state in self.states:
            writer.writerow(('', state))
        
        writer.writerow(('', ))       
    
    def _process_states(self, writer):
        self.states = self.get_params(self.states_param)
        
        if len(self.states) > 0:
            self.contract_data = self.contract_data.filter(place_of_performance__state__in=self.states)
            self._render_states(writer)


    def _render_contracts(self, writer):
        writer.writerow(("Work performed by a vendor is often reported under a different NAICS code due to FPDS restrictions.",))
        writer.writerow(('', ))
      
        writer.writerow(('Date Signed', 'PIID', 'Agency', 'Type', 'Value ($)', 'Email POC', 'Place of Performance', 'NAIC', 'PSC', 'Status'))
    
        for contract in self.contract_data.iterator():
            pricing_type = ''
            status = ''
            
            if contract.pricing_type:
                pricing_type = contract.pricing_type.name
            
            if contract.status:
                status = contract.status.name
                    
            writer.writerow((contract.date_signed.strftime("%m/%d/%Y"), contract.piid, titlecase(contract.agency.name), pricing_type, contract.obligated_amount, (contract.point_of_contact or "").lower(), contract.place_of_performance, contract.NAICS, contract.PSC, status))
    
        writer.writerow(('', ))


    @method_decorator(cache_page(settings.PAGE_CACHE_LIFETIME, cache='page_cache')) 
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vendor_contracts.csv"'
        
        writer = csv.writer(response)    
        writer.writerow(('GSA Discovery vendor contract research results',))
        writer.writerow(('URL: ' + self.request.build_absolute_uri(),))
        writer.writerow(('Time: ' + time.strftime('%b %d, %Y %l:%M%p %Z'),))
        writer.writerow(('', ))
        
        self._process_vendor(writer, kwargs['vendor_duns'])
        self._process_naics(writer)
        self._process_memberships(writer)
        self._process_countries(writer)
        self._process_states(writer)
        
        self._render_contracts(writer)
        
        track_page_load(request)
        return response
