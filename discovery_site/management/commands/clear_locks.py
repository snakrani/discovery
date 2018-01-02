from django.core.management.base import BaseCommand, CommandError
from db_mutex.models import DBMutex

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
        print("-------BEGIN CLEAR_LOCKS PROCESS-------")
        
        try:
            DBMutex.objects.all().delete()

        except Exception as e:
            display_error(e)
            raise

        print("-------END CLEAR_LOCKS PROCESS-------")
