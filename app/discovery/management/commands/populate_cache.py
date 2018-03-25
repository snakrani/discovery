from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

from discovery import models as system

import sys
import logging
import traceback
import warnings
import urllib


warnings.filterwarnings('ignore')


def system_logger():
    return logging.getLogger('django')


def display_error(info):
    print("MAJOR ERROR -- PROCESS ENDING EXCEPTION --  {}".format(info))
    traceback.print_tb(sys.exc_info()[2])
    system_logger().debug("MAJOR ERROR -- PROCESS ENDING EXCEPTION -- {}".format(info))


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("-------BEGIN POPULATE_CACHE PROCESS-------")
        
        try:
            cache.clear()
            
            for page in system.CachePage.objects.all().order_by('-count'):
                print("[ {} ] - {}".format(page.count, page.url))
                urllib.request.urlopen(page.url).read()

        except Exception as e:
            display_error(e)
            raise

        print("-------END POPULATE_CACHE PROCESS-------")
