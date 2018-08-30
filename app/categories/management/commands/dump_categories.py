from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('> Dumping keywords')
        call_command('dumpdata', 'categories.keyword', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/keywords.json'))
        
        print('> Dumping SIN codes')
        call_command('dumpdata', 'categories.sin', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/sin.json'))
        
        print('> Dumping NAICS codes')
        call_command('dumpdata', 'categories.naics', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/naics.json'))
        
        print('> Dumping PSC codes')
        call_command('dumpdata', 'categories.psc', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/psc.json'))
        
        print('> Dumping vendor setasides')
        call_command('dumpdata', 'categories.setaside', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/setasides.json'))
        
        print('> Dumping vendor vehicles')
        call_command('dumpdata', 'categories.vehicle', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/vehicles.json'))
        
        print('> Dumping vendor pools')
        call_command('dumpdata', 'categories.pool', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/pools.json'))
        
        print('> Dumping zones')
        call_command('dumpdata', 'categories.state', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/states.json'))
        call_command('dumpdata', 'categories.zone', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/zones.json'))
                  
