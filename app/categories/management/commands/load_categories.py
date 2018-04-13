from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

import os
import sys
import logging
import traceback
import warnings


warnings.filterwarnings('ignore')


def vendor_logger():
    return logging.getLogger('vendor')

def display_error(info):
    print("MAJOR ERROR -- PROCESS ENDING EXCEPTION --  {}".format(info))
    traceback.print_tb(sys.exc_info()[2])
    vendor_logger().debug("MAJOR ERROR -- PROCESS ENDING EXCEPTION -- {}".format(info))


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("-------BEGIN LOAD_CATEGORIES PROCESS-------")
        
        try:
            print('> Loading NAICS codes')
            call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/naics.json'))
            
            print('> Loading PSC codes')
            call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/psc.json'))
            
            print('> Loading vendor setaside categories')
            call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/setasides.json'))
            
            print('> Loading vendor pools')
            call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/pools.json'))
            
            print('> Loading zones')
            call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/zones.json'))
            call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/zonestates.json'))          

        except Exception as e:
            display_error(e)
            raise

        print("-------END LOAD_CATEGORIES PROCESS-------")
