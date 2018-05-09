from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

from categories.models import Keyword, Naics, PSC

import os
import csv
import re


class Command(BaseCommand):    
    def handle(self, *args, **options):
        data_path = os.path.join(settings.BASE_DIR, 'data', 'keywords.csv')
        
        data_stream = open(data_path, 'r')
        reader = csv.reader(data_stream)
        next(reader)
            
        for line in reader:
            keyword, created = Keyword.objects.get_or_create(id=line[0].strip())
            
            name = line[1].strip().capitalize() # Get somewhat normalized version of string
            name = re.sub(r'\s+', ' ', name) # Condense whitespace
            name = re.sub(r'\s*,+\s*', ', ', name) # Separate comma from words
            name = re.sub(r'\s*:+\s*', ': ', name) # Separate colons from words
            name = re.sub(r'\s*;+\s*', '; ', name) # Separate semicolons from words
            name = re.sub(r'\s*\(+\s*', ' (', name) # Separate parenthesis from words
            name = re.sub(r'\s*\)+\s*', ') ', name) # Separate parenthesis from words
            name = re.sub(r'\s*-+\s*', ' - ', name) # Normalize dashes
            name = re.sub(r'\s*/+\s*', ' / ', name) # Normalize slashes
            name = name.strip()
            
            keyword.name = name
            
            print("Updating keyword: {} ({})".format(keyword.name, keyword.id))
            keyword.save()
            
            for naics_code in filter(None, "".join(line[2].split()).split(',')):
                for naics in Naics.objects.filter(root_code=naics_code):
                    if keyword not in naics.keywords.all():
                        print(" > Adding NAICS code: [ {} ]".format(naics_code))
                        naics.keywords.add(keyword)
                
            for psc_code in filter(None, "".join(line[3].split()).split(',')):
                for psc in PSC.objects.filter(code=psc_code):
                    if keyword not in psc.keywords.all():
                        print(" > Adding PSC code: [ {} ]".format(psc_code))
                        psc.keywords.add(keyword)
                
        call_command('dumpdata', 'categories.keyword', indent=2, output="{}/{}".format(settings.BASE_DIR, 'categories/fixtures/keywords.json'))
