from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from contract.models import FAPIISRecord
from vendor.models import Vendor
import csv
import os

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
       
        fapiis_reader = csv.reader(open(os.path.join(settings.BASE_DIR, 'contract/docs/fapiis/fapiis.csv'), 'r'))
        next(fapiis_reader)

        for line in fapiis_reader:
            attr_dict = {
                'piid': line[3],
                'agency_id': line[16],
                'agency_name': line[0],
                'record_type': line[1],
                'NAICS': line[15],
                'PSC': line[14],
                'record_code': line[20],
                'agency_poc_email': line[19],
                'agency_poc_phone': line[18],
                'agency_poc_name': line[17],
                'duns': line[6] 
            }

            fprec, created = FAPIISRecord.objects.get_or_create(piid=attr_dict['piid'])

            for k,v  in attr_dict.items():
                setattr(fprec, k, v)

            fprec.save()
            
        
