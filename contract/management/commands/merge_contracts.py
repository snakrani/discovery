import pytz
from datetime import datetime
from django.conf import settings
from vendor.models import Vendor
from contract.models import FPDSContract, Contract #FAPIISRecord
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        #get all fpds contracts
        for contract in FPDSContract.objects.all():
        
            merged_con, created = Contract.objects.get_or_create(piid=contract.piid, vendor=contract.vendor)
            for field in ('agency_name',
                          'agency_id', 
                          'NAICS',
                          'PSC',
                          'date_signed',
                          'completion_date',
                          'vendor', 
                          'pricing_type',
                          'obligated_amount',):
   
                try:
                    setattr(merged_con, field, getattr(contract, field))
                except AttributeError:
                    pass

            #Calculate status
            today = datetime.now(pytz.utc)
            if contract.completion_date and contract.completion_date > today:
                merged_con.status = 'Current'

            elif contract.completion_date and contract.completion_date < today:
                merged_con.status = 'Completed'

            #fapiis status can overwrite above, goes here

            if contract.last_modified_by:
                merged_con.point_of_contact = contract.last_modified_by

            #fapiis POC data can overwrite above, goes here

            merged_con.save()

        #match with fapiis records

        #create merged record 

            #create status based on dates/fapiis

