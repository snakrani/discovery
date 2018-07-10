from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from contracts.models import Contract

import sys
import logging
import traceback
import warnings
import pytz


warnings.filterwarnings('ignore')


def fpds_logger():
    return logging.getLogger('fpds')


def display_error(info):
    print("MAJOR ERROR -- PROCESS ENDING EXCEPTION --  {0}".format(info))
    traceback.print_tb(sys.exc_info()[2])
    fpds_logger().debug("MAJOR ERROR -- PROCESS ENDING EXCEPTION -- {0}".format(info))
    

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--period',
            action='store',
            type=int,
            default=260,
            dest='period',
            help='Number of weeks back to populate database (default 5 years)',
        )

    def handle(self, *args, **options):
        print("-------BEGIN PRUNE_CONTRACTS PROCESS-------")
        
        try:
            first_date = pytz.UTC.localize(datetime.now() - timedelta(weeks=(options['period'])))
            
            print("First date: {}".format(first_date))
            print('------------------------------')
            
            for contract in Contract.objects.all().iterator():
                if contract.completion_date: 
                    if contract.completion_date < first_date:
                        print("Deleting contract {} completed at {}".format(contract.id, contract.completion_date))
                        contract.delete() 
            
        except Exception as e:
            display_error(e)
            raise
        
        print("-------END PRUNE_CONTRACTS PROCESS-------")
