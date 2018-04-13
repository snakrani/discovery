from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

import sys
import logging
import traceback
import warnings


warnings.filterwarnings('ignore')


def system_logger():
    return logging.getLogger('django')


def display_error(info):
    print("MAJOR ERROR -- PROCESS ENDING EXCEPTION --  {}".format(info))
    traceback.print_tb(sys.exc_info()[2])
    system_logger().debug("MAJOR ERROR -- PROCESS ENDING EXCEPTION -- {}".format(info))


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("-------BEGIN CLEAR_CACHE PROCESS-------")
        
        try:
            cache.clear()

        except Exception as e:
            display_error(e)
            raise

        print("-------END CLEAR_CACHE PROCESS-------")
