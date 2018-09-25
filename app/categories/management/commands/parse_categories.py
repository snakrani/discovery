from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

import pandas as pd
from xlrd import open_workbook

from categories.models import Keyword, SetAside, Tier, Vehicle, Pool, SIN, Naics, PSC

import os
import logging
import re
import math
import datetime
import pytz
import json


def category_logger():
    return logging.getLogger('category')


def format_bool(text):
    if isinstance(text, str) and re.match(r'\s*x\s*', text, re.IGNORECASE):
        return True
    return False

def format_text(text):
    if isinstance(text, str) or (isinstance(text, (int, float)) and not math.isnan(text)):
        return text
    return ''

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
        mapping_files = [
            os.path.join(settings.BASE_DIR, 'data/naics_2012.xls'),
            os.path.join(settings.BASE_DIR, 'data/naics_2017.xlsx')
        ]
        
        print("Loading NAICS codes")
        for file in mapping_files:
            wb = open_workbook(file)
        
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


    def load_vehicle_tiers(self, data):
        print('Loading vehicle tiers')
        for index, record in data.iterrows():
            tier, created = Tier.objects.get_or_create(number=record['number'])
            tier.name = format_text(record['name'])
            tier.save()

    def load_vehicles(self, data):
        print('Loading vehicles')
        for index, record in data.iterrows():
            vehicle, created = Vehicle.objects.get_or_create(id=record['id'])
            vehicle.name = format_text(record['name'])
            vehicle.tier_id = format_text(record['tier'])
            vehicle.poc = format_text(record['poc'])
            vehicle.ordering_guide = format_text(record['ordering_guide'])
            vehicle.small_business = format_bool(record['small_business'])
            vehicle.numeric_pool = format_bool(record['numeric_pool'])
            vehicle.display_number = format_bool(record['display_number'])
            vehicle.save()

    def load_pools(self, data):
        print('Loading pools')
        for index, record in data.iterrows():
            pool, created = Pool.objects.get_or_create(id="{}_{}".format(record['vehicle'], record['number']))
            pool.name = format_text(record['name'])
            pool.vehicle_id = format_text(record['vehicle'])
            pool.number = format_text(record['number'])
            pool.threshold = format_text(record['threshold'])
            pool.save()        

    def load_pool_naics(self, pool_ids, data):
        print('Loading pool NAICS')
        for id in pool_ids:
            pool = Pool.objects.get(id=id)
            pool.naics.clear()
            
            for index, record in data.iterrows():
                if format_bool(record[id]):
                    pool.naics.add(record['NAICS'])

    def load_pool_psc(self, pool_ids, data):
        print('Loading pool PSC')
        for id in pool_ids:
            pool = Pool.objects.get(id=id)
            pool.psc.clear()
            
            for index, record in data.iterrows():
                if format_bool(record[id]):
                    pool.psc.add(record['PSC'])

    def load_pool_info(self):
        index_file = os.path.join(settings.BASE_DIR, 'data/pool_index.xlsx')
        wb = pd.ExcelFile(index_file)

        self.load_vehicle_tiers(wb.parse('Tiers'))
        self.load_vehicles(wb.parse('Vehicles'))
        self.load_pools(wb.parse('Pools'))

        pool_ids = list(Pool.objects.all().values_list('id', flat=True))
        self.load_pool_naics(pool_ids, wb.parse('NAICS'))
        self.load_pool_psc(pool_ids, wb.parse('PSC'))


    def handle(self, *args, **options):
        # Code definitions
        self.load_naics_codes()
        self.load_psc_codes()
        
        # Code mappings
        self.map_psc_codes()
        self.map_naics_codes()

        # Vehicle/pool information
        self.load_pool_info()
        
        # Other imports
        print("Loading vendor setasides")
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/setasides.json'))
                
        print("Loading zones")
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/states.json'))
        call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/zones.json'))
