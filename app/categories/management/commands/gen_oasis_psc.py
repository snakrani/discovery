from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

from categories import models as categories

import os
import csv
import re


class Command(BaseCommand):    
    def handle(self, *args, **options):
        output_path = os.path.join(settings.BASE_DIR, 'data', 'oasis_output_psc.csv')
        output_stream = open(output_path, 'w')
        writer = csv.writer(output_stream, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        input_path = os.path.join(settings.BASE_DIR, 'data', 'oasis_psc.csv')
        input_stream = open(input_path, 'r')
        reader = csv.reader(input_stream)
        next(reader)
            
        for line in reader:
            psc_code = line[1].strip()
            sb_pool_id = line[2].strip()
            unr_pool_id = line[3].strip()
            
            description = line[4].strip().title() # Get somewhat normalized version of string
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
            
            sb_naics = list(categories.Pool.objects.get(id = sb_pool_id).naics.values_list('root_code', flat=True))
            unr_naics = list(categories.Pool.objects.get(id = unr_pool_id).naics.values_list('root_code', flat=True))
            naics_codes = ",".join(set(sb_naics + unr_naics))
            
            print("[{}]: {} | {}".format(psc_code, description, naics_codes))
            writer.writerow([psc_code, description, naics_codes])
            