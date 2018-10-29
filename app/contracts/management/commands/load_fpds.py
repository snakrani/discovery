from optparse import make_option
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from pyfpds import Contracts

from discovery.utils import csv_memory
from vendors.models import Vendor, Location
from contracts import catch_key_error
from contracts.models import Agency, Contract, PlaceOfPerformance, FPDSLoad

import os
import sys
import signal
import logging
import traceback
import io

import re
import pytz
import json
import csv


def fpds_logger():
    return logging.getLogger('fpds')

def fpds_mem_logger():
    return logging.getLogger('fpds_memory')

def log_memory(message = "Memory"):
    fpds_mem_logger().info(csv_memory(message))

def fpds_data_logger():
    return logging.getLogger('fpds_data')

def log_data(*args):
    line = io.StringIO()
    writer = csv.writer(line)
    writer.writerow(args)
    fpds_data_logger().info(line.getvalue().rstrip())


def display_error(info):
    print("MAJOR ERROR -- PROCESS ENDING EXCEPTION --  {0}".format(info))
    traceback.print_tb(sys.exc_info()[2])
    fpds_logger().debug("MAJOR ERROR -- PROCESS ENDING EXCEPTION -- {0}".format(info))
    
    
def crash_handler(signum, frame):
    if signum == 2: #user exit
        print("SHUTDOWN -- USER TERMINATED PROCESS --")
    else:
        fpds_mem_logger().info("System Crash: {}".format(signum))
        display_error(frame)
    
    sys.exit(1)


@catch_key_error
def get_award_id_obj(award):
    if 'https://www.fpds.gov/FPDS:awardID' in award: 
        return award['https://www.fpds.gov/FPDS:awardID']
    else:
        return award['https://www.fpds.gov/FPDS:OtherTransactionAwardID']['https://www.fpds.gov/FPDS:OtherTransactionAwardContractID']


def get_piid(award_id):
    piid = ''
    if 'https://www.fpds.gov/FPDS:referencedIDVID' in award_id:
        #part of an IDIQ
        piid = award_id['https://www.fpds.gov/FPDS:referencedIDVID']['https://www.fpds.gov/FPDS:PIID'] + '_' 
    elif 'https://www.fpds.gov/FPDS:PIID' in award_id:
        return award_id['https://www.fpds.gov/FPDS:PIID']

    piid += award_id['https://www.fpds.gov/FPDS:awardContractID']['https://www.fpds.gov/FPDS:PIID']

    return piid


def get_mod(award_id):
    if 'https://www.fpds.gov/FPDS:modNumber' in award_id:
        return award_id['https://www.fpds.gov/FPDS:modNumber']
    return award_id['https://www.fpds.gov/FPDS:awardContractID']['https://www.fpds.gov/FPDS:modNumber']


def get_agency_id(award_id):
    if 'https://www.fpds.gov/FPDS:awardContractID' in award_id:
        return award_id['https://www.fpds.gov/FPDS:awardContractID']['https://www.fpds.gov/FPDS:agencyID']['#text']
    else:
        return award_id['https://www.fpds.gov/FPDS:agencyID']['#text']


def get_agency_name(award_id):
    if 'https://www.fpds.gov/FPDS:awardContractID' in award_id:
        return award_id['https://www.fpds.gov/FPDS:awardContractID']['https://www.fpds.gov/FPDS:agencyID']['@name']
    else:
        return award_id['https://www.fpds.gov/FPDS:agencyID']['@name'] 


@catch_key_error
def get_transaction_number(award_id):
    return award_id['https://www.fpds.gov/FPDS:awardContractID']['https://www.fpds.gov/FPDS:transactionNumber']


@catch_key_error
def get_ultimate_completion_date(award):
    return award['https://www.fpds.gov/FPDS:relevantContractDates']['https://www.fpds.gov/FPDS:ultimateCompletionDate']


@catch_key_error
def get_current_completion_date(award):
    return award['https://www.fpds.gov/FPDS:relevantContractDates']['https://www.fpds.gov/FPDS:currentCompletionDate']


@catch_key_error
def get_annual_revenue(award):
    return award['https://www.fpds.gov/FPDS:vendor']['https://www.fpds.gov/FPDS:vendorSiteDetails']['https://www.fpds.gov/FPDS:vendorOrganizationFactors']['https://www.fpds.gov/FPDS:annualRevenue']


@catch_key_error
def get_number_of_employees(award):
    return award['https://www.fpds.gov/FPDS:vendor']['https://www.fpds.gov/FPDS:vendorSiteDetails']['https://www.fpds.gov/FPDS:vendorOrganizationFactors']['https://www.fpds.gov/FPDS:numberOfEmployees']


@catch_key_error
def get_last_modified_by(award):
    return award['https://www.fpds.gov/FPDS:transactionInformation']['https://www.fpds.gov/FPDS:lastModifiedBy']

@catch_key_error
def get_created_by(award):
    return award['https://www.fpds.gov/FPDS:transactionInformation']['https://www.fpds.gov/FPDS:createdBy']

def poc_is_email(text):
    if text and re.search('@', text):
        return text
    return None
    
def get_point_of_contact(award):
    poc = get_last_modified_by(award)
    if poc is None:
        poc = get_created_by(award)
        
    return poc_is_email(poc)


def get_contract_pricing_name(award):
    
    @catch_key_error
    def get_name(award):
        return award['https://www.fpds.gov/FPDS:contractData']['https://www.fpds.gov/FPDS:typeOfContractPricing']

    name = get_name(award) 
    if name and isinstance(name, str):
        return name

    elif name: 
        return award['https://www.fpds.gov/FPDS:contractData']['https://www.fpds.gov/FPDS:typeOfContractPricing']['@description']


@catch_key_error
def get_contract_pricing_id(award):
    return award['https://www.fpds.gov/FPDS:contractData']['https://www.fpds.gov/FPDS:typeOfContractPricing']['#text']


@catch_key_error
def get_reason_for_modification(award):
    return award['https://www.fpds.gov/FPDS:contractData']['https://www.fpds.gov/FPDS:reasonForModification']['#text']


def get_naics(award):
    
    @catch_key_error
    def get_name(award):
        return award['https://www.fpds.gov/FPDS:productOrServiceInformation']['https://www.fpds.gov/FPDS:principalNAICSCode']
    
    name = get_name(award)
    
    if name and isinstance(name, str):
        return name
    elif name:
        return award['https://www.fpds.gov/FPDS:productOrServiceInformation']['https://www.fpds.gov/FPDS:principalNAICSCode']['#text']


@catch_key_error
def get_psc(award):
    return award['https://www.fpds.gov/FPDS:productOrServiceInformation']['https://www.fpds.gov/FPDS:productOrServiceCode']['#text']


@catch_key_error
def get_phone(award):
    return "{}-{}-{}".format(
        award['https://www.fpds.gov/FPDS:vendor']['https://www.fpds.gov/FPDS:vendorSiteDetails']['https://www.fpds.gov/FPDS:vendorLocation']['https://www.fpds.gov/FPDS:phoneNo'][:3],
        award['https://www.fpds.gov/FPDS:vendor']['https://www.fpds.gov/FPDS:vendorSiteDetails']['https://www.fpds.gov/FPDS:vendorLocation']['https://www.fpds.gov/FPDS:phoneNo'][3:6],
        award['https://www.fpds.gov/FPDS:vendor']['https://www.fpds.gov/FPDS:vendorSiteDetails']['https://www.fpds.gov/FPDS:vendorLocation']['https://www.fpds.gov/FPDS:phoneNo'][6:]
    )


@catch_key_error
def get_location(award):
    loc = award['https://www.fpds.gov/FPDS:vendor']['https://www.fpds.gov/FPDS:vendorSiteDetails']['https://www.fpds.gov/FPDS:vendorLocation']
    return {
        'address': loc['https://www.fpds.gov/FPDS:streetAddress'].strip().title(),
        'city': loc['https://www.fpds.gov/FPDS:city'].strip().title(),
        'state': loc['https://www.fpds.gov/FPDS:state']['#text'].strip().upper(),
        'zipcode': loc['https://www.fpds.gov/FPDS:ZIPCode'].strip()[:5],
        'congressional_district': '{:02d}'.format(int(loc['https://www.fpds.gov/FPDS:congressionalDistrictCode']))
    }


@catch_key_error
def get_place_of_performance(award):
    pop = award['https://www.fpds.gov/FPDS:placeOfPerformance']['https://www.fpds.gov/FPDS:principalPlaceOfPerformance']
    info = {
        'country_code': pop['https://www.fpds.gov/FPDS:countryCode']['#text'].strip().upper(),
        'country_name': pop['https://www.fpds.gov/FPDS:countryCode']['@name'].strip().title(),
        'state': None,
        'zipcode': None
    }
    
    if 'https://www.fpds.gov/FPDS:stateCode' in pop:
        info['state'] = pop['https://www.fpds.gov/FPDS:stateCode']['#text'].strip().upper()
        
    if 'https://www.fpds.gov/FPDS:placeOfPerformanceZIPCode' in award['https://www.fpds.gov/FPDS:placeOfPerformance']:
        info['zipcode'] = award['https://www.fpds.gov/FPDS:placeOfPerformance']['https://www.fpds.gov/FPDS:placeOfPerformanceZIPCode']['#text'].strip()[:5]
        
    return info


def init_load(options):
    if options['reinit']:
        if options['id']:
            FPDSLoad.objects.filter(vendor=options['id']).delete()
            Contract.objects.filter(vendor=options['id']).delete()
        else:
            FPDSLoad.objects.all().delete()
            Contract.objects.all().delete()
        

def last_load(vendor, options):
    first_date = datetime.now() - timedelta(weeks=(options['period']))
    
    if len(options['starting_date']) == 0:
        try:
            load = FPDSLoad.objects.get(vendor_id=vendor.id)
            return load.load_date
        
        except FPDSLoad.DoesNotExist:
            pass
    else:
        first_date = datetime.strptime(options['starting_date'], "%Y-%m-%d")
    
    return first_date.date()


def create_load(vendor, load_date):
    try:
        load = FPDSLoad.objects.get(vendor_id=vendor.id)
        load.load_date = load_date
        load.save()

    except FPDSLoad.DoesNotExist:
        FPDSLoad.objects.create(vendor_id=vendor.id, load_date=load_date)


class Command(BaseCommand):

    date_now = datetime.now().date()
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--pause',
            action='store',
            type=int,
            default=1,
            dest='pause',
            help='Number of seconds to pause before each query to the FPDS-NG ATOM feed',
        )
        parser.add_argument(
            '--starting_id',
            action='store',
            type=int,
            default=1,
            dest='starting_id',
            help='Start loading contracts for vendors greater or equal to this id',
        )
        parser.add_argument(
            '--id',
            action='store',
            type=int,
            default=0,
            dest='id',
            help='Load contracts for only this vendor id',
        )
        parser.add_argument(
            '--starting_date',
            action='store',
            type=str,
            default='',
            dest='starting_date',
            help='Start loading contracts starting from a specific date',
        )
        parser.add_argument(
            '--reinit',
            action='store_true',
            default=False,
            dest='reinit',
            help='Reinitialize all vendor contract data',
        )
        parser.add_argument(
            '--period',
            action='store',
            type=int,
            default=260,
            dest='period',
            help='Number of weeks back to populate database (default 5 years)',
        )
        parser.add_argument(
            '--load',
            action='store',
            type=int,
            default=260,
            dest='load',
            help='Weekly interval to process incoming data (default 5 years)',
        )
        parser.add_argument(
            '--count',
            action='store',
            type=int,
            default=500,
            dest='count',
            help='Number of records to return from each load of the FPDS_NG ATOM feed',
        )
        parser.add_argument(
            '--max',
            action='store',
            type=int,
            default=0,
            dest='max',
            help='Maximum number of records to collect from each vendor (for generating fixtures)',
        )


    def init_contract(self, raw_entry):
        fpds_contract = raw_entry['content']
        
        #get contract award information
        if 'https://www.fpds.gov/FPDS:IDV' in fpds_contract:
            return None, {} # don't get IDV records

        try:
            award = fpds_contract['https://www.fpds.gov/FPDS:award']
                    
        except KeyError:
            try:
                award = fpds_contract['https://www.fpds.gov/FPDS:OtherTransactionAward']
            except KeyError:
                return None, {}
                        
        if 'https://www.fpds.gov/FPDS:contractDetail' in award:
            award = award['https://www.fpds.gov/FPDS:contractDetail'] # for OtherTransactionAward, details are nested one more level
    
        award_id = get_award_id_obj(award)
        if award_id is None:
            return None, {}
        
        piid = get_piid(award_id)
        location = get_location(award)
        pop = get_place_of_performance(award)
        
        record = {
            'mod_number': get_mod(award_id), 
            'transaction_number': get_transaction_number(award_id),
            'ultimate_completion_date': get_ultimate_completion_date(award), 
            'current_completion_date': get_current_completion_date(award), 
            'signed_date': award['https://www.fpds.gov/FPDS:relevantContractDates']['https://www.fpds.gov/FPDS:signedDate'],
            'agency_id': get_agency_id(award_id),
            'agency_name': get_agency_name(award_id),
            'obligated_amount': award['https://www.fpds.gov/FPDS:dollarValues']['https://www.fpds.gov/FPDS:obligatedAmount'],
            'annual_revenue': get_annual_revenue(award),
            'number_of_employees': get_number_of_employees(award),
            'last_modified_by': get_last_modified_by(award),
            'point_of_contact': get_point_of_contact(award),
            'reason_for_modification': get_reason_for_modification(award),
            'type_of_contract_pricing_name': get_contract_pricing_name(award),
            'type_of_contract_pricing_id': get_contract_pricing_id(award),
            'naics' : get_naics(award),
            'psc': get_psc(award),
            'vendor_phone': get_phone(award)
        }
        if location:
            record['vendor_address'] = location['address']
            record['vendor_city'] = location['city']
            record['vendor_state'] = location['state']
            record['vendor_zipcode'] = location['zipcode']
            record['vendor_congressional_district'] = location['congressional_district']
        
        if pop:
            record['pop_country_code'] = pop['country_code']
            record['pop_country_name'] = pop['country_name']
            record['pop_state'] = pop['state']
            record['pop_zipcode'] = pop['zipcode']
        
        return piid, record
    
    
    def update_contract(self, piid, records, v):
        records = sorted(records, key=lambda x: (x['mod_number'], x['transaction_number']))
        con, created = Contract.objects.get_or_create(piid=piid, vendor=v)
        total = 0 # amount obligated
        
        con.base_piid = piid.split('_')[0]
        
        for mod in records:
            total += float(mod.get('obligated_amount'))
            
            con.date_signed = mod.get('signed_date') 
            con.completion_date = mod.get('current_completion_date') or mod.get('ultimate_completion_date')
            
            agency_id = mod.get('agency_id')
            if agency_id:
                agency, created = Agency.objects.get_or_create(id = agency_id)
                agency.name = mod.get('agency_name')
                agency.save()
                
            con.agency_id = agency_id
            
            con.pricing_type_id = mod.get('type_of_contract_pricing_id')
            
            if mod.get('reason_for_modification') in ['X', 'E', 'F']:
                con.status_id = mod.get('reason_for_modification')
            else:
                if con.completion_date:
                    date_obj = datetime.strptime(con.completion_date, '%Y-%m-%d %H:%M:%S')
                    today = datetime.utcnow()
                    if date_obj:
                        if date_obj > today:
                            con.status_id = 'C2'
                        else:
                            con.status_id = 'C1'
            
            if mod.get('last_modified_by') and '@' in mod['last_modified_by'].lower():
                #only add if it's an actual email, make this a better regex
                con.last_modified_by = mod['last_modified_by']
            
            poc = poc_is_email(mod.get('point_of_contact'))    
            if poc:
                con.point_of_contact = poc
            
            con.vendor_phone = mod.get('vendor_phone')
            
            if mod.get('vendor_address'):
                location, created = Location.objects.get_or_create(
                    address = mod.get('vendor_address'),
                    city = mod.get('vendor_city'),
                    state = mod.get('vendor_state'),
                    zipcode = mod.get('vendor_zipcode'),
                    congressional_district = mod.get('vendor_congressional_district')
                )                
                con.vendor_location = location
            
            if mod.get('pop_country_code'):
                pop, created = PlaceOfPerformance.objects.get_or_create(
                    country_code = mod.get('pop_country_code'),
                    country_name = mod.get('pop_country_name'),
                    state = mod.get('pop_state'),
                    zipcode = mod.get('pop_zipcode')
                )
                con.place_of_performance = pop
            
            #ADD NAICS -- need to add other naics as objects to use foreignkey
            con.PSC = mod.get('psc')
            con.NAICS = mod.get('naics')

            ar = mod.get('annual_revenue') or None
            ne = mod.get('number_of_employees') or None
            
            if ar:
                con.annual_revenue = int(ar)
            if ne:
                con.number_of_employees = int(ne)
        
        con.obligated_amount = total
        con.save()  
    
    
    def get_vendor_ids(self, starting_id=1):
        return Vendor.objects.filter(id__gte=starting_id).order_by('id').values_list('id', flat=True)
        
    
    def update_vendor(self, vid, load_to, options):
        logger = fpds_logger()
        
        vendor = Vendor.objects.get(id=vid)
        contracts = Contracts(logger=logger.debug)      
        load_date = last_load(vendor, options)
        
        if load_to <= load_date: #already loaded more data than requested
            load_to = load_date + timedelta(weeks = options['load'])
        if load_to > self.date_now: #load_to can't be in the future
            load_to = self.date_now
        if load_date == self.date_now: #need to request at least one day
            load_date = load_date - timedelta(days = 1)
            
        print("[ {} ] - Updating vendor {} ({}) from {} to {}".format(vid, vendor.name, vendor.duns, load_date, load_to))
        log_memory("Starting [ {} ] {} - {}".format(vid, vendor.name, vendor.duns))
            
        by_piid = {}
            
        v_index = 0
        contracts_processed = 0
        missing_modified = 0
            
        while True:
            v_con, v_index = contracts.get_page(v_index, options['count'], vendor_duns=vendor.duns, last_modified_date=[load_date, load_to], _sleep=options['pause'])
            
            log_memory("Loading [ {} ] {} - {}".format(vid, vendor.name, vendor.duns))
            
            for vc in v_con:
                piid, contract_record = self.init_contract(vc)
                   
                if piid is None:
                    continue
                    
                contracts_processed += 1
                    
                if piid in by_piid:
                    by_piid[piid].append(contract_record)
                else:
                    by_piid[piid] = [contract_record, ]
                    
                if options['max'] > 0 and len(by_piid.keys()) >= options['max']:
                    v_index = 0
                    break
                                
            if v_index == 0:
                break
        
        for piid, records in by_piid.items():
            logger.debug("================{0}===Vendor {1}=================\n".format(piid, vendor.duns))
            logger.debug(contracts.pretty_print(by_piid[piid]))
        
            self.update_contract(piid, records, vendor)
                
        #save load time
        create_load(vendor, load_to)
            
        print(" --- completed with: {} PIID(s), {} contract(s) processed".format(len(by_piid.keys()), contracts_processed))
        log_memory("Final [ {} ] {} - {}".format(vid, vendor.name, vendor.duns))
        log_data(vid, vendor.duns, vendor.name, load_date, load_to, contracts_processed, len(by_piid.keys()))

    
    def update_vendors(self, vendor_ids, load_to, options):
        success = True
        
        log_data("Vendor ID", 
            "DUNS", 
            "Name", 
            "Start Date", 
            "End Date", 
            "Contracts", 
            "PIIDs", 
        )
        
        for vid in vendor_ids:
            self.update_vendor(vid, load_to, options)
            
        return success
       

    def handle(self, *args, **options):
        print("-------BEGIN LOAD_FPDS PROCESS-------")
        log_memory('Start')
        
        signal.signal(signal.SIGSEGV, crash_handler) #catch segmentation faults
        
        try:
            init_load(options)
            
            print('> Loading contract status codes')
            call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'contracts/fixtures/contractstatuses.json'))
            
            print('> Loading contract pricing structure codes')
            call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'contracts/fixtures/pricingstructures.json'))
            
            if options['id'] > 0:
                try:
                    FPDSLoad.objects.get(id=options['id']).delete()
                except Exception:
                    pass

                self.update_vendor(options['id'], self.date_now, options)
            else:
                #allow to start from a certain vendor
                vid = options['starting_id']
            
                vendor_ids = self.get_vendor_ids(vid)
                all_vendor_ids = self.get_vendor_ids() if vid > 1 else vendor_ids
            
                #repeat every incrementally until end
                first_date = self.date_now - timedelta(weeks = options['period'])
                load_to = first_date
                
                while self.date_now > load_to: #while load_to is in the past
                    load_to = load_to + timedelta(weeks = options['load'])
                    if self.date_now < load_to: #load_to can't be in the future
                        load_to = self.date_now
                    
                    self.update_vendors(vendor_ids, load_to, options)
                    
                    #reset vendor ids so we start processing at the beginning again
                    vendor_ids = all_vendor_ids
            
        except Exception as e:
            display_error(e)
            raise
        
        print("-------END LOAD_FPDS PROCESS-------")
        log_memory('End')
