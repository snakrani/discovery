from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('> Loading keywords')
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/keywords.json'))
        
        print('> Loading NAICS codes')
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/naics.json'))
        
        print('> Loading PSC codes')
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/psc.json'))
        
        print('> Loading vendor setasides')
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/setasides.json'))
        
        print('> Loading vendor pools')
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/pools.json'))
        
        print('> Loading zones')
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/zones.json'))
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/zonestates.json'))          
