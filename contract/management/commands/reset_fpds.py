from django.core.management.base import BaseCommand, CommandError
from contract.models import FPDSLoad

import sys
import logging
import traceback
import warnings


warnings.filterwarnings('ignore')


def fpds_logger():
    return logging.getLogger('fpds')


def display_error(info):
    print("MAJOR ERROR -- PROCESS ENDING EXCEPTION --  {0}".format(info))
    traceback.print_tb(sys.exc_info()[2])
    fpds_logger().debug("MAJOR ERROR -- PROCESS ENDING EXCEPTION -- {0}".format(info))
    

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("-------BEGIN RESET_FPDS PROCESS-------")
        
        try:
            FPDSLoad.objects.all().delete()
            
        except Exception as e:
            display_error(e)
            raise
        
        print("-------END RESET_FPDS PROCESS-------")
