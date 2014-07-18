from django.core.management.base import BaseCommand, CommandError
from vendor.models import Vendor, Pool
import csv
from django.conf import settings
import os


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        #read in setasides from yaml file

        #read in vendors from csv files 
        
        for vehicle in settings.VEHICLES:
            #cycle through predefined set of vehicles
            doc_dir = os.path.join(settings.BASE_DIR, 'vendor/docs/{0}/pools'.format(vehicle))
            for f in os.listdir(doc_dir):
                datafile = open(os.path.join(doc_dir, f), 'r')
                reader = csv.reader(datafile)
                print(f) 
                for line in reader: print(line)

        #step 2
        #determine pool, vehicle, piid from file name and contents

        #step 3
        #Query the FPDS API to get the DUNS, for the vendor

        #step 4 
        #use SAM API to get setaside statuses for a vendor

        #2
        return
