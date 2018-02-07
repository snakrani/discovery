from optparse import make_option
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from vendors.models import Vendor, Manager, Pool, PoolPIID, SetAside
from discovery_site.utils import csv_memory

import os
import sys
import logging
import traceback
import StringIO

import requests
import re
import xmltodict
import csv


def vendor_logger():
    return logging.getLogger('vendor')

def vendor_mem_logger():
    return logging.getLogger('vendor_memory')

def log_memory(message = "Memory"):
    vendor_mem_logger().info(csv_memory(message))

def vendor_data_logger():
    return logging.getLogger('vendor_data')

def log_data(*args):
    line = StringIO.StringIO()
    writer = csv.writer(line)
    writer.writerow(args)
    vendor_data_logger().info(line.getvalue().rstrip())


def display_error(info):
    print("MAJOR ERROR -- PROCESS ENDING EXCEPTION --  {0}".format(info))
    traceback.print_tb(sys.exc_info()[2])
    vendor_logger().debug("MAJOR ERROR -- PROCESS ENDING EXCEPTION -- {0}".format(info))


def format_duns(duns):
    return duns.replace('X', '0').replace('x', '0').zfill(9)

def duns_plus_4(duns):
    return format_duns(duns) + '0000'


class Command(BaseCommand):

    option_list = BaseCommand.option_list \
                  + (make_option('--pause', action='store', type=int, dest='pause', default=1, help="Number of seconds to pause before each query to the SAM API"), ) \
                  + (make_option('--vehicles', action='store', type=str, dest='vehicles', default='', help="Comma separated list of vehicles to load (lowercase)"), ) \
                  + (make_option('--pools', action='store', type=str, dest='pools', default='', help="Comma separated list of pool numbers to load from each vehicle"), ) \
                  + (make_option('--vpp', action='store', type=int, dest='vpp', default=0, help="Number of vendors to load per pool (useful for creating fixtures)"), ) \
                  + (make_option('--tries', action='store', type=int, dest='tries', default=3, help="Number of tries to query the SAM API before exiting"), )


    def update_vendor(self, record, pool_data, options):
        logger = vendor_logger()
        
        name = record[0].strip()
        piid = record[1].strip()
        duns = format_duns(record[2].strip())
        zone = record[9].strip()
        
        # Get vendor object
        vendor, created = Vendor.objects.get_or_create(duns=duns)
         
        print("[ {} ] - Updating vendor: {} from pool {}".format(vendor.id, name, pool_data.id))
        log_memory("Starting vendor [ {} - {} ]".format(pool_data.id, vendor.id))
              
        # Update basic vendor information
        vendor.name = name
        vendor.duns_4 = duns_plus_4(duns)
        
        # Add contract manager
        cm, cm_created = vendor.managers.get_or_create(type='CM', name=record[3].strip())
        
        for number in filter(None, "".join(record[4].split()).split(',')):
            cm.phones.get_or_create(number=number)
        
        for address in filter(None, "".join(record[5].split()).split(',')):
            cm.emails.get_or_create(address=address)
        
        # Add project manager
        pm, pm_created = vendor.managers.get_or_create(type='PM', name=record[6].strip())
        
        for number in filter(None, "".join(record[7].split()).split(',')):
            pm.phones.get_or_create(number=number)
        
        for address in filter(None, "".join(record[8].split()).split(',')):
            pm.emails.get_or_create(address=address)
        
        # Add setaside information (if it exists)
        if (len(record) == 11 and len(record[10])):
            for name in filter(None, "".join(record[10].split()).split(',')):
                try:
                    sa = SetAside.objects.get(name__iexact=name)
                    if sa not in vendor.setasides.all():
                        vendor.setasides.add(sa)

                except SetAside.DoesNotExist as error:
                    continue
        
        vendor.save()
        
        # Update pool relationship
        poolpiid, ppcreated = PoolPIID.objects.get_or_create(vendor=vendor, pool=pool_data, piid=piid, zone=zone)
        
        log_memory("Final vendor [ {} - {} ]".format(pool_data.id, vendor.id))
        log_data(
            vendor.name, 
            vendor.duns, 
            vendor.duns_4,
            cm.name,
            ":".join(cm.phone()),
            ":".join(cm.email()),
            pm.name,
            ":".join(pm.phone()),
            ":".join(pm.email()),
            zone,
            ":".join([str(sa.pk) for sa in vendor.setasides.all()])
        )
        
        if created:
            logger.debug("Successfully created {}".format(vendor.name))
            return 1
        else:
            logger.debug("Vendor {} already in database".format(vendor.name))
            return 0


    def update_pool(self, vehicle, pool, data_path, options):
        logger = vendor_logger()
        
        data_stream = open(data_path, 'r')
        reader = csv.reader(data_stream)
        new_vendor_count = 0
        pool_count = 0
        
        # Skip header.
        next(reader)
        
        print("< {} >- Updating pool vendors".format(pool))
        log_memory("Starting pool [ {} ]".format(pool))
        
        vendors_per_pool = options['vpp']

        try:
            pool_data = Pool.objects.get(number=pool, vehicle__iexact=vehicle)
            
            for line in reader:
                new_vendor_count += self.update_vendor(line, pool_data, options)
                pool_count += 1
                
                if vendors_per_pool > 0 and pool_count == vendors_per_pool:
                    break

        except Pool.DoesNotExist as e:
            logger.debug("Pool {} not found for spreadsheet".format(pool))
            data_stream.close()
            raise(e)

        except Pool.MultipleObjectsReturned as e:
            logger.debug("More than one pool matched {}. Integrity error!".format(pool))
            data_stream.close()
            raise(e)
        
        print(" --- completed pool {} with: {} vendor(s) processed".format(pool, pool_count))
        log_memory("Final pool [ {} ]".format(pool))
        data_stream.close()
        
        return new_vendor_count


    def update_vehicle(self, vehicle, options, pools):
        vehicle_dir = os.path.join(settings.BASE_DIR, 'vendors/data/{0}'.format(vehicle))
        new_vendor_count = 0
        
        for pool_file in os.listdir(vehicle_dir):
            data_path = os.path.join(vehicle_dir, pool_file)
            
            try:
                pool = re.match('pool-(.*).csv', pool_file).group(1)
            except Exception:
                pool = None # Not a pool file, skip...
            
            if pool and (len(pools) == 0 or pool in pools):
                new_vendor_count += self.update_pool(vehicle, pool, data_path, options)
        
        return new_vendor_count
        

    def handle(self, *args, **options):
        new_vendor_count = 0
        
        print("-------BEGIN LOAD_VENDORS PROCESS-------")
        log_memory('Start')        
        log_data('Name', 
            'DUNS', 
            'DUNS+4', 
            'CM Name', 
            'CM Phones', 
            'CM Emails', 
            'PM Name', 
            'PM Phones', 
            'PM Emails',
            'Zone',
            'SetAsides'
        )
        
        vehicles = filter(None, "".join(options['vehicles'].lower().split()).split(','))
        pools = filter(None, "".join(options['pools'].split()).split(','))
        
        try:
            for vehicle in settings.VEHICLES:
                if len(vehicles) == 0 or vehicle in vehicles:
                    new_vendor_count += self.update_vehicle(vehicle, options, pools)

            #load extra SAM fields
            call_command('load_sam', **options)

        except Exception as e:
            display_error(e)
            raise
        
        print("New vendors: {}".format(new_vendor_count))
        print("-------END LOAD_VENDORS PROCESS-------")
        log_memory('End')
