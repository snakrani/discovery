from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import os
import io
import re
import csv


def is_ascii(text):
    if isinstance(text, str):
        try:
            text.encode('ascii')
        
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
            
        except UnicodeDecodeError:
            return False
    
    return True


class Command(BaseCommand):

    def check_pool(self, vehicle, pool, data_path, options):
        data_stream = open(data_path, 'r')
        reader = csv.reader(data_stream)
        
        print("< {}_{} >- Check pool vendors".format(vehicle, pool))
        for line in reader:
            for item in line:
                if not is_ascii(item):
                    print('WARNING: NON ASCII FOUND')
                    print(line[0])
                    print(item)

        data_stream.close()


    def check_vehicle(self, vehicle, options):
        vehicle_dir = os.path.join(settings.BASE_DIR, 'data/pools/{0}'.format(vehicle))
        
        for pool_file in os.listdir(vehicle_dir):
            data_path = os.path.join(vehicle_dir, pool_file)
            
            try:
                pool = re.match('pool-(.*).csv', pool_file).group(1)
            except Exception:
                pool = None # Not a pool file, skip...
            
            if pool:
                self.check_pool(vehicle, pool, data_path, options)
        

    def handle(self, *args, **options):
        print("-------BEGIN FIX_VENDORS PROCESS-------")
        
        for vehicle in settings.VEHICLES:
            self.check_vehicle(vehicle, options)

        print("-------END LOAD_VENDORS PROCESS-------")
