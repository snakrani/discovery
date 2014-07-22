from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from vendor.models import Vendor, Pool
import csv
from django.conf import settings
import os
import re
import requests
import logging
import xmltodict

class Command(BaseCommand):
    
    logger = logging.getLogger('vendors')
   
    def get_contract(piid):
        
        resp = requests.get(USASPENDING_API_URL + "?piid=" + piid)
        data = xmltodict.parse(resp.text)
        try:
            doc = data['usaspendingSearchResults']['result']['doc']
            return doc

        except KeyError:
            self.logger.debug("PIID {0} did not return any results from USASpending".format(piid))
            return None
        
    def replace_x(self, duns):
        return duns.replace('X', '0').replace('x', '0')

    def duns_plus_4(self, duns):
        return self.replace_x(duns) + '0000'

    def handle(self, *args, **kwargs):
        #read in setasides from yaml file

        #read in vendors from csv files 
        
        for vehicle in settings.VEHICLES:
            #cycle through predefined set of vehicles
            doc_dir = os.path.join(settings.BASE_DIR, 'vendor/docs/{0}/pools'.format(vehicle))
            
            for f in os.listdir(doc_dir):
                datafile = open(os.path.join(doc_dir, f), 'r')
                pool = re.match('Pool (.*)-Table.*', f).group(1) 
                reader = csv.reader(datafile)

                try:
                    pool_obj = Pool.objects.get(number=pool, vehicle__iexact=vehicle)
                    for idx, line in enumerate(reader): 
                        #skip header rows
                        if idx < 2: continue
                        #emtpy row
                        if line[1] == '' or line[3] == '': continue
                        
                        #relevant columns
                        data = line[1:11]

                        piid = data[1]

                        attr_dict = {
                            'name': data[0],
                            'duns': self.replace_x(data[2]),
                            'duns_4': self.duns_plus_4(data[2]),                            
                            'cm_name': data[4],
                            'cm_phone': data[5],
                            'cm_email': data[6],
                            'pm_name': data[7],
                            'pm_phone': data[8],
                            'pm_email': data[9]
                        }
                        new_obj, created = Vendor.objects.get_or_create(**attr_dict)
                
                        if created:
                            print("Successfully created {}".format(new_obj.name))
                        else:
                            print("Vendor {} already in database".format(new_obj.name))

                                        #Next Steps
                #        contract = self.get_contract(piid)
                        
                        #create contract record with piid, using fpds API
                        #use sam API to get addresses
                        #pre load setasides? 
                        #use SAM API to get setaside statuses for a vendor

                        #Need to document:
                        #API key will need rate limiting restrictions removed probably
        

                except Pool.DoesNotExist:
                    print("Pool {} not found for spreadsheet".format(pool))

                except Pool.MultipleObjectsReturned:
                    print("More than one pool matched {}. Integrity error!".format(pool))

            #call the sam check to fill in extra fields
            call_command('check_sam')


