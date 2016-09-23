from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from vendor.models import Vendor, Pool, PoolPIID, SetAside
import csv
from django.conf import settings
import os
import re
import requests
import logging
import xmltodict
import csv

class Command(BaseCommand):
    
    logger = logging.getLogger('vendors')
   
    def replace_x(self, duns):
        return duns.replace('X', '0').replace('x', '0')

    def duns_plus_4(self, duns):
        return self.replace_x(duns) + '0000'

    def load_temp_setasides(self):
        reader = csv.reader(open(os.path.join(settings.BASE_DIR, 'vendor/docs/temp_8a_hubzone.csv')))
        for line in reader:
            try:
                v = Vendor.objects.get(duns=line[1])
            except Vendor.DoesNotExist:
                print 'Could not find the specified vendor.'

            try:
                sa = SetAside.objects.get(code=line[2])
            except SetAside.DoesNotExist:
                print 'Could not find the specified setaside.'

            if sa not in v.setasides.all():
                v.setasides.add(sa)

    def handle(self, *args, **kwargs):
        #read in setasides from yaml file

        #read in vendors from csv files 
        
        for vehicle in settings.VEHICLES:
            #cycle through predefined set of vehicles
            doc_dir = os.path.join(settings.BASE_DIR, 'vendor/docs/{0}/pools'.format(vehicle))
            
            for f in os.listdir(doc_dir):
                datafile = open(os.path.join(doc_dir, f), 'r')
                pool = re.match('Pool (.*).csv', f).group(1)
                reader = csv.reader(datafile)

                # Skip header.
                reader.next()

                try:
                    pool_obj = Pool.objects.get(number=pool, vehicle__iexact=vehicle)
                    for line in reader:
                        #relevant columns
                        piid = line[1]
                        duns = self.replace_x(line[2])

                        new_obj, created = Vendor.objects.get_or_create(duns=duns)

                        attr_dict = {
                            'name': line[0],
                            'duns': self.replace_x(line[2]),
                            'duns_4': self.duns_plus_4(duns),                            
                            'cm_name': line[3],
                            'cm_phone': line[4],
                            'cm_email': line[5],
                            'pm_name': line[6],
                            'pm_phone': line[7],
                            'pm_email': line[8]
                        }
                        
                        for k, v in attr_dict.items(): 
                            if v and v != '' and v != ' ':
                                setattr(new_obj, k, v)

                        new_obj.save()

                        #add pool relationship
                        poolpiid, ppcreated = PoolPIID.objects.get_or_create(vendor=new_obj, pool=pool_obj, piid=piid)

                        if created:
                            self.logger.debug("Successfully created {}".format(new_obj.name))
                        else:
                            self.logger.debug("Vendor {} already in database".format(new_obj.name))
                        

                        #Need to document:
                        #API key will need rate limiting restrictions removed probably
        

                except Pool.DoesNotExist:
                    self.logger.debug("Pool {} not found for spreadsheet".format(pool))
                    print("Pool {0} not found. Did you load the pools fixture?".format(pool))

                except Pool.MultipleObjectsReturned:
                    self.logger.debug("More than one pool matched {}. Integrity error!".format(pool))

        #call the sam check to fill in extra fields
        call_command('check_sam')
        #self.load_temp_setasides()