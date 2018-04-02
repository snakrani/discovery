from django.conf import settings
from django.core.management.base import BaseCommand

from categories.models import PSC

import os
import csv


class Command(BaseCommand):    
    def handle(self, *args, **options):
        data_path = os.path.join(settings.BASE_DIR, 'data', 'psc.csv')
        
        data_stream = open(data_path, 'r')
        reader = csv.reader(data_stream)
        next(reader)
            
        for line in reader:
            psc, created = PSC.objects.get_or_create(code=line[0].strip())
            psc.description = line[1].strip()
            psc.naics_code = line[2].strip()
            psc.save()
