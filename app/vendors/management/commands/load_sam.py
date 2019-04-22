from optparse import make_option
from time import sleep
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from discovery.utils import csv_memory
from categories.models import SetAside, Pool
from vendors.models import Vendor, Location, SamLoad

import os
import sys
import logging
import traceback
import warnings
import io

import requests
import json
import csv
import re


warnings.filterwarnings('ignore')
successCount = 0
failuresCount = 0

def vendor_logger():
    return logging.getLogger('vendor')

def vendor_mem_logger():
    return logging.getLogger('vendor_memory')

def log_memory(message = "Memory"):
    vendor_mem_logger().info(csv_memory(message))

def sam_data_logger():
    return logging.getLogger('sam_data')

def log_data(*args):
    line = io.StringIO()
    writer = csv.writer(line)
    writer.writerow([str(s).encode("utf-8") for s in args])
    sam_data_logger().info(line.getvalue().rstrip())


def display_error(info):
    print("MAJOR ERROR -- PROCESS ENDING EXCEPTION --  {}".format(info))
    traceback.print_tb(sys.exc_info()[2])
    vendor_logger().debug("MAJOR ERROR -- PROCESS ENDING EXCEPTION -- {}".format(info))


def get_value(obj, key, vendor, default=None):
    try:
        return obj[key]

    except KeyError as e:
        vendor_logger().debug("There was a key error on {}: {}".format(vendor.duns, e))
        return default


def get_root_sam_url(duns_4):
    return settings.SAM_API_URL + duns_4

def get_sam_url(duns_4):
    return get_root_sam_url(duns_4) + '?api_key=' + settings.SAM_API_KEY


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--pause',
            action='store',
            type=int,
            default=1,
            dest='pause',
            help='Number of seconds to pause before each query to the SAM API',
        )
        parser.add_argument(
            '--tries',
            action='store',
            type=int,
            default=3,
            dest='tries',
            help='Number of tries to query the SAM API before exiting',
        )
    
    
    def get_vendor_ids(self):
        vendor_list = Vendor.objects.all().order_by('id').values_list('id', flat=True)
        vendors = {}
        order = []
        
        for update in SamLoad.objects.all():
            if update.load_time:
                vendors[update.vendor.id] = update.load_time
            
        # Load all unloaded vendors first
        for vid in vendor_list:
            if vid not in vendors:
                order.append(vid)
        
        # Load vendors by oldest first
        for vid in sorted(vendors, key=vendors.get):
            order.append(vid)
        
        return order
    
    
    def load_sam_data(self, duns_4, options):
        logger = vendor_logger()
        
        sam_data = {}
        loaded = True
        
        sam_url = get_sam_url(duns_4)
        log_url = get_root_sam_url(duns_4)
        
        #don't kill the api
        if options['pause'] > 0:
            sleep(options['pause'])
        
        #request data
        logger.info("Fetching vendor at {}".format(log_url))
        request = requests.get(sam_url)

        #catch and log key problems
        if request.status_code == 403:
            if 'Message' in request.json():
                logger.error("There was a 403 error on {}. Registration information forbidden".format(log_url))
            else:
                raise Exception('Data.gov API key is invalid')
        
        try:
            sam_data = request.json()

        except ValueError:
            #the api did not return anything. Sleep and try again? (recursive goodness!)
            if options['tries'] > 0:
                options['tries'] -= 1
                options['pause'] = 5
                sam_data, loaded = self.load_sam_data(duns_4, options)
                
        if 'sam_data' in sam_data:
            sam_data = sam_data['sam_data']
        
        elif 'Error' in sam_data:
            logger.error("SAM API returned an error for {}, and duns {}".format(log_url, duns_4))
            loaded = False
        else:
            logger.error("Could not load data from {} for unknown reason".format(log_url))
            loaded = False
                
        return sam_data, loaded


    def update_vendor(self, vendor, options):
        logger = vendor_logger()
        sam_data, sam_loaded = self.load_sam_data(vendor.duns_4, options)
        global successCount
        global failuresCount

        if 'registration' in sam_data:
            
            print("[ {} ] - Updating SAM vendor: {}".format(vendor.id, vendor.name))
            log_memory("Starting vendor [ {} | {} ]".format(vendor.id, vendor.name))
        
            reg = sam_data['registration']
            
            vendor.sam_status = get_value(reg, 'status', vendor)
            vendor.sam_activation_date = get_value(reg, 'activationDate', vendor)
            vendor.sam_expiration_date = get_value(reg, 'expirationDate', vendor)
            vendor.sam_exclusion = get_value(reg, 'hasKnownExclusion', vendor)
            vendor.cage = get_value(reg, 'cage', vendor)
            
            addr = get_value(reg, 'samAddress', vendor)
            if addr:
                location, created = Location.objects.get_or_create(
                    address = get_value(addr, 'line1', vendor, '').strip().title(),
                    city = get_value(addr, 'city', vendor, '').strip().title(),
                    state = get_value(addr, 'stateorProvince', vendor, '').strip().upper(),
                    zipcode = get_value(addr, 'zip', vendor).strip(),
                    congressional_district = re.sub(r'[^\d]+', '', get_value(reg, 'congressionalDistrict', vendor, ''))
                )                
                vendor.sam_location = location

            vendor.sam_url = get_value(reg, 'corporateUrl', vendor)
            if vendor.sam_url and vendor.sam_url[:3].lower() == "www" :
                vendor.sam_url = 'http://' + vendor.sam_url

            vendor.save()

            logger.error("record saved for {}".format(vendor.duns_4))
            logger.error("{}".format(vendor.duns_4))

            successCount = successCount + 1
            sam_load, created = SamLoad.objects.get_or_create(vendor = vendor)
            sam_load.load_time = datetime.now()
            sam_load.save()
                      
            log_memory("Final vendor [ {} | {} ]".format(vendor.id, vendor.name))
            logger.error("SuccessCountInsideSuccess {}".format(successCount))
            log_data(vendor.name,
                vendor.duns,
                vendor.duns_4,
                vendor.sam_status,
                vendor.sam_activation_date,
                vendor.sam_expiration_date,
                vendor.sam_exclusion,
                vendor.cage,
                vendor.sam_location.address,
                vendor.sam_location.city,
                vendor.sam_location.state,
                vendor.sam_location.zipcode,
                vendor.sam_location.congressional_district,
                vendor.sam_url
            )
        else:
            failuresCount = failuresCount + 1
            logger.error("'registration' key is missing for {} / {}".format(vendor.id, vendor.duns_4))
            logger.error("FailureCount {}".format(failuresCount))
            logger.error("SuccessCount {}".format(successCount))

        

    def handle(self, *args, **options):
        print("-------BEGIN LOAD_SAM PROCESS-------")
        global successCount
        global failuresCount
        logger = vendor_logger()
        log_memory('Start')        
        log_data('Name', 
            'DUNS', 
            'DUNS+4', 
            'SAM Status', 
            'SAM Activation Date', 
            'SAM Expiration Date', 
            'SAM Exclusion', 
            'Cage Code', 
            'SAM Address', 
            'SAM City',
            'SAM State',
            'SAM Zipcode',
            'SAM Congressional District', 
            'SAM URL'
        )

        try:
            vendor_ids = self.get_vendor_ids()
            
            for vid in vendor_ids:
                vendor = Vendor.objects.get(id=vid)
                
                if vendor:
                    self.update_vendor(vendor, options)

        except Exception as e:
            display_error(e)
            raise
        
        finally:
            logger.error("FailureCountLast {}".format(failuresCount))
            logger.error("SuccessCountLast {}".format(successCount))

        print("-------END LOAD_SAM PROCESS-------")
        log_memory('End')
