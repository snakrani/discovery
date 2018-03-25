from optparse import make_option
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from discovery.utils import csv_memory
from categories.models import SetAside, Pool, Zone
from vendors.models import Vendor, Manager, PoolMembership

import os
import sys
import logging
import traceback
import io

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
    line = io.StringIO()
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
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--vehicles',
            action='store',
            type=str,
            default='',
            dest='vehicles',
            help='Comma separated list of vehicles to load (lowercase)',
        )
        parser.add_argument(
            '--pools',
            action='store',
            type=str,
            default='',
            dest='pools',
            help='Comma separated list of pool numbers to load from each vehicle',
        )
        parser.add_argument(
            '--vpp',
            action='store',
            type=int,
            default=0,
            dest='vpp',
            help='Number of vendors to load per pool (useful for creating fixtures)',
        )

    def update_vendor(self, record, pool_data, options):
        logger = vendor_logger()
        
        name = record[0].strip()
        piid = record[1].strip()
        duns = format_duns(record[2].strip())
        zones = record[9].strip()
        
        # Get vendor object
        vendor, created = Vendor.objects.get_or_create(duns=duns)
         
        print("[ {} ] - Updating vendor: {} from pool {}".format(vendor.id, name, pool_data.id))
        log_memory("Starting vendor [ {} - {} ]".format(pool_data.id, vendor.id))
              
        # Update basic vendor information
        vendor.name = name
        vendor.duns_4 = duns_plus_4(duns)
        vendor.save()
        
        # Update pool membership information
        membership, ppcreated = PoolMembership.objects.get_or_create(vendor=vendor, pool=pool_data, piid=piid)
        
        if zones and zones.lower() != 'all':
            for zone_id in [x.strip() for x in zones.split(',')]:
                try:
                    zone = Zone.objects.get(id=int(zone_id))
                    if zone not in membership.zones.all():
                        membership.zones.add(zone)

                except Zone.DoesNotExist as error:
                    continue
        
        
        # Add contract manager
        cm, cm_created = membership.cms.get_or_create(name=record[3].strip())
        
        for number in filter(None, "".join(record[4].split()).split(',')):
            cm.phones.get_or_create(number=number)
        
        for address in filter(None, "".join(record[5].split()).split(',')):
            cm.emails.get_or_create(address=address)
        
        # Add project manager
        pm, pm_created = membership.pms.get_or_create(name=record[6].strip())
        
        for number in filter(None, "".join(record[7].split()).split(',')):
            pm.phones.get_or_create(number=number)
        
        for address in filter(None, "".join(record[8].split()).split(',')):
            pm.emails.get_or_create(address=address)
        
        # Add setaside information (if it exists)
        if (len(record) == 11 and len(record[10])):
            for name in filter(None, "".join(record[10].split()).split(',')):
                try:
                    sa = SetAside.objects.get(name__iexact=name)
                    if sa not in membership.setasides.all():
                        membership.setasides.add(sa)

                except SetAside.DoesNotExist as error:
                    continue
                
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
            ":".join([str(zone.pk) for zone in membership.zones.all()]),
            ":".join([str(sa.pk) for sa in membership.setasides.all()])
        )

        if created:
            logger.debug("Successfully created {}".format(vendor.name))
        else:
            logger.debug("Vendor {} already in database".format(vendor.name))


    def update_pool(self, vehicle, pool, data_path, options):
        logger = vendor_logger()
        
        data_stream = open(data_path, 'r')
        reader = csv.reader(data_stream)
        pool_count = 0
        
        # Skip header.
        next(reader)
        
        print("< {} >- Updating pool vendors".format(pool))
        log_memory("Starting pool [ {} ]".format(pool))
        
        vendors_per_pool = options['vpp']

        try:
            pool_data = Pool.objects.get(number=pool, vehicle__iexact=vehicle)
            
            for line in reader:
                self.update_vendor(line, pool_data, options)
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


    def update_vehicle(self, vehicle, options, pools):
        vehicle_dir = os.path.join(settings.BASE_DIR, 'data/pools/{0}'.format(vehicle))
        
        for pool_file in os.listdir(vehicle_dir):
            data_path = os.path.join(vehicle_dir, pool_file)
            
            try:
                pool = re.match('pool-(.*).csv', pool_file).group(1)
            except Exception:
                pool = None # Not a pool file, skip...
            
            if pool and (len(pools) == 0 or pool in pools):
                self.update_pool(vehicle, pool, data_path, options)
        

    def handle(self, *args, **options):
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
            'Zones',
            'SetAsides'
        )
        
        vehicles = [x.strip() for x in options['vehicles'].lower().split(',') if x != '']
        pools = [x.strip() for x in options['pools'].lower().split(',') if x != '']
        
        try:
            for vehicle in settings.VEHICLES:
                if len(vehicles) == 0 or vehicle in vehicles:
                    self.update_vehicle(vehicle, options, pools)

        except Exception as e:
            display_error(e)
            raise
        
        print("-------END LOAD_VENDORS PROCESS-------")
        log_memory('End')
