from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

from categories.models import Naics, PSC

import os
import csv
import re


class Command(BaseCommand):    
    def handle(self, *args, **options):
        data_path = os.path.join(settings.BASE_DIR, 'data', 'psc.csv')
        
        data_stream = open(data_path, 'r')
        reader = csv.reader(data_stream)
        next(reader)
            
        for line in reader:
            psc, created = PSC.objects.get_or_create(code=line[0].strip())
            
            description = line[1].strip().title() # Get somewhat normalized version of string
            description = re.sub(r'\s+', ' ', description) # Condense whitespace
            description = re.sub(r'\s*,+\s*', ' , ', description) # Separate comma from words
            description = re.sub(r'\s*:+\s*', ' : ', description) # Separate colons from words
            description = re.sub(r'\s*;+\s*', ' ; ', description) # Separate semicolons from words
            description = re.sub(r'\s*\(+\s*', ' ( ', description) # Separate parenthesis from words
            description = re.sub(r'\s*\)+\s*', ' ) ', description) # Separate parenthesis from words
            description = re.sub(r'\s*-+\s*', ' - ', description) # Normalize dashes
            description = re.sub(r'\s*/+\s*', ' / ', description) # Normalize slashes
            
            # Correct some words
            description = re.sub(r'\s+Svc\s+', ' Service ', description)
            description = re.sub(r'\s+Svcs\s+', ' Services ', description)
            description = re.sub(r'\s+Maint\s+', ' Maintenance ', description)
            description = re.sub(r'\s+Equip\s+', ' Equipment ', description)
            description = re.sub(r'\s+Ac\s+', ' AC ', description)
            description = re.sub(r'\s+Alt\s+', ' Alteration ', description)
            description = re.sub(r'\s+Tr\.?\s+', ' Training ', description)
            description = re.sub(r'\s+Educ\.?\s+', ' Education ', description)
            description = re.sub(r'\s+Info\.?\s+', ' Information ', description)
            description = re.sub(r'\s+Tech\.?\s+', ' Technology ', description)
            description = re.sub(r'\s+Sci\.?\s+', ' Science ', description)
            description = re.sub(r'\s+Telecomm\.?\s+', ' Telecommunications ', description)
            description = re.sub(r'\s+Develop\.?\s+', ' Development ', description)
            
            description = re.sub(r'\s,\s', ', ', description) # Normalize comma
            description = re.sub(r'\s:\s', ': ', description) # Normalize colons
            description = re.sub(r'\s;\s', '; ', description) # Normalize semicolons
            description = re.sub(r'\s\(\s', ' (', description) # Normalize parenthesis
            description = re.sub(r'\s\)\s', ') ', description) # Normalize parenthesis
            
            psc.description = description
            
            print("Updating PSC: [ {} ] - {}".format(psc.code, psc.description))
            psc.save()
            
            for naics_code in filter(None, "".join(line[2].split()).split(',')):
                try:
                    for naics in Naics.objects.filter(root_code=naics_code):
                        if naics not in psc.naics.all():
                            print(" > Adding NAICS code: [ {} ]".format(naics_code))
                            psc.naics.add(naics)

                except Naics.DoesNotExist as error:
                    continue
                
        call_command('dumpdata', 'categories.psc', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/psc.json'))
