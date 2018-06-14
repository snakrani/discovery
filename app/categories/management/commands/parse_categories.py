from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

import pandas as pd
from xlrd import open_workbook

from categories.models import Keyword, SetAside, Pool, SIN, Naics, PSC

import os
import logging
import re
import math
import datetime
import pytz
import json


def category_logger():
    return logging.getLogger('category')

def format_sin(text):
    return re.sub(r'\s+', '-', text)

def format_label(text):
    description = text.strip().title() # Get somewhat normalized version of string
    description = re.sub(r'\s+', ' ', description) # Condense whitespace
    description = re.sub(r'\s*,+\s*', ' , ', description) # Separate comma from words
    description = re.sub(r'\s*:+\s*', ' : ', description) # Separate colons from words
    description = re.sub(r'\s*;+\s*', ' ; ', description) # Separate semicolons from words
    description = re.sub(r'\s*\(+\s*', ' ( ', description) # Separate parenthesis from words
    description = re.sub(r'\s*\)+\s*', ' ) ', description) # Separate parenthesis from words
    description = re.sub(r'\s*-+\s*', ' - ', description) # Normalize dashes
    description = re.sub(r'\s*/+\s*', ' / ', description) # Normalize slashes
    
    # Correct some words
    description = re.sub(r'(^|\s+)Svc\s+', ' Service ', description)
    description = re.sub(r'(^|\s+)Svcs\s+', ' Services ', description)
    description = re.sub(r'(^|\s+)Maint\s+', ' Maintenance ', description)
    description = re.sub(r'(^|\s+)Equip\s+', ' Equipment ', description)
    description = re.sub(r'(^|\s+)Ac\s+', ' AC ', description)
    description = re.sub(r'(^|\s+)Alt\s+', ' Alteration ', description)
    description = re.sub(r'(^|\s+)Alter\s+', ' Alteration ', description)
    description = re.sub(r'(^|\s+)Tr\.?\s+', ' Training ', description)
    description = re.sub(r'(^|\s+)Educ\.?\s+', ' Education ', description)
    description = re.sub(r'(^|\s+)Info\.?\s+', ' Information ', description)
    description = re.sub(r'(^|\s+)Tech\.?\s+', ' Technology ', description)
    description = re.sub(r'(^|\s+)Sci\.?\s+', ' Science ', description)
    description = re.sub(r'(^|\s+)Telecomm\.?\s+', ' Telecommunications ', description)
    description = re.sub(r'(^|\s+)Develop\.?\s+', ' Development ', description)
    description = re.sub(r'\s*SUBJECT TO COOPERATIVE PURCHASING\s*', '', description)
            
    description = re.sub(r'\s,\s', ', ', description) # Normalize comma
    description = re.sub(r'\s:\s', ': ', description) # Normalize colons
    description = re.sub(r'\s;\s', '; ', description) # Normalize semicolons
    description = re.sub(r'\s\(\s', ' (', description) # Normalize parenthesis
    description = re.sub(r'\s\)\s', ') ', description) # Normalize parenthesis
    description = re.sub(r'\s*-+\s*', '-', description) # Normalize dashes
    description = re.sub(r'\s*\-\s*$', '', description) # Strip ending dash
    
    return description


class Command(BaseCommand):

    def parse_mapping(self, schedule_data, processor_method):
        process = False
        last_sin = None
        last_sin_label = None
        
        for row in range(schedule_data.nrows):
            sin = str(schedule_data.cell(row, 0).value)
                    
            if process:
                # SIN
                if not sin:
                    sin = last_sin
                else:
                    last_sin = sin
                        
                # SIN label
                sin_label = str(schedule_data.cell(row, 1).value)
                       
                if not sin_label:
                    sin_label = last_sin_label
                else:
                    last_sin_label = sin_label
                        
                # Classification
                code = str(schedule_data.cell(row, 2).value)
                        
                # Record mapping
                getattr(self, processor_method)(format_sin(sin), format_label(sin_label), code)
                    
            elif sin == 'SIN':
                process = True

    
    def load_naics_codes(self):
        mapping_file = os.path.join(settings.BASE_DIR, 'data/naics.xlsx')
        wb = open_workbook(mapping_file)
        
        print("Loading NAICS codes")
        for listing in wb.sheets():
            for row in range(listing.nrows):
                try:
                    code = int(listing.cell(row, 0).value)
                    title = str(listing.cell(row, 1).value)
                    
                    # Save NAICS object
                    naics, created = Naics.objects.get_or_create(code=code)
                    naics.description = title
                    naics.save()
                    
                except Exception as e:
                    pass
    
    def map_naics_code(self, sin, sin_label, naics_code):
        sin_obj, created = SIN.objects.get_or_create(code=sin)
        keyword, created = Keyword.objects.get_or_create(name=sin_label)
        
        # Ensure SIN label
        if sin_label not in list(sin_obj.keywords.all().values_list('name')):
            sin_obj.keywords.add(keyword)
                
        # Include SIN, keyword, and NAICS codes
        try:
            naics = Naics.objects.get(code=naics_code)
            
            if sin not in naics.sin.all():
                naics.sin.add(sin)
                
            if sin_label not in list(naics.keywords.all().values_list('name')):
                naics.keywords.add(keyword)
                
            # Include NAICS code
            for psc in PSC.objects.filter(sin=sin):
                if naics.code not in list(psc.naics.all().values_list('code')):
                    psc.naics.add(naics)

        except Naics.DoesNotExist as error:
            pass    
    
    def map_naics_codes(self):
        mapping_file = os.path.join(settings.BASE_DIR, 'data/mappings/sin_naics.xlsx')
        wb = open_workbook(mapping_file)
        
        print("Processing NAICS mappings")
        for schedule in wb.sheets():
            print("Schedule: {}".format(schedule.name))
            self.parse_mapping(schedule, 'map_naics_code')

 
    def load_psc_codes(self):
        mapping_file = os.path.join(settings.BASE_DIR, 'data/psc.xls')
        wb = open_workbook(mapping_file)
        
        print("Loading PSC codes")
        for listing in wb.sheets():
            process = False
            
            for row in range(listing.nrows):
                code = str(listing.cell(row, 0).value)
                
                if process:
                    if code:
                        title = str(listing.cell(row, 4).value)
                        
                        if not title:
                            title = str(listing.cell(row, 1).value)
                        
                        title = format_label(title)
                        
                        # Save PSC object
                        psc, created = PSC.objects.get_or_create(code=code)
                        psc.description = title
                        psc.save()
                
                elif re.match(r'PSC', code, re.IGNORECASE):
                    process = True
    
    def map_psc_code(self, sin, sin_label, psc_code):
        sin_obj, created = SIN.objects.get_or_create(code=sin)
        keyword, created = Keyword.objects.get_or_create(name=sin_label)
        
        # Ensure SIN label
        if sin_label not in list(sin_obj.keywords.all().values_list('name')):
            sin_obj.keywords.add(keyword)
                
        # Include SIN and keyword
        try:
            psc = PSC.objects.get(code=psc_code)
            
            if sin not in psc.sin.all():
                psc.sin.add(sin)
                
            if sin_label not in list(psc.keywords.all().values_list('name')):
                psc.keywords.add(keyword)

        except PSC.DoesNotExist as error:
            pass
            
    def map_psc_codes(self):
        mapping_file = os.path.join(settings.BASE_DIR, 'data/mappings/sin_psc.xlsx')
        wb = open_workbook(mapping_file)
        
        print("Processing PSC mappings")
        for schedule in wb.sheets():
            if re.match(r'\d+', schedule.name, re.IGNORECASE):
                print("Schedule: {}".format(schedule.name))
                self.parse_mapping(schedule, 'map_psc_code')


    def handle(self, *args, **options):
        # Code definitions
        self.load_naics_codes()
        self.load_psc_codes()
        
        # Code mappings
        self.map_psc_codes()
        self.map_naics_codes()
        
        # Other imports
        print("Loading vendor setasides")
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/setasides.json'))
        
        print("Loading vendor pools")
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/pools.json'))
        
        print("Loading zones")
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/zones.json'))
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/zonestates.json'))
