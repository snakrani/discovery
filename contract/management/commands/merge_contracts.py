import pytz
from datetime import datetime
from django.conf import settings
from vendor.models import Vendor
from contract.models import FPDSContract, Contract, FAPIISRecord
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


            if contract.last_modified_by:
                merged_con.point_of_contact = contract.last_modified_by

            if '_' in contract.piid: 
                base_piid = contract.piid.split('_')[1]
            else:
                base_piid = contract.piid

            try:
                if len(base_piid) > 4:
                    #want to bypass short piids that won't match
                    fapiis_rec = FAPIISRecord.objects.get(piid=base_piid)
                    #cross check against vendor since some piids are duplicated across agencies
                    if contract.vendor.duns == fapiis_rec.duns or contract.vendor.duns_4 == fapiis_rec.duns:
                        print ("found one!")
                        if fapiis_rec.agency_poc_email: 
                            merged_con.point_of_contact = fapiis_rec.agency_poc_email
                        elif fapiis_rec.agency_poc_phone:
                            if fapiis_rec.agency_poc_name:
                                merged_con.point_of_contact = "{0} ({1})".format(fapiis_rec.agency_poc_name, fapiis_rec.agency_poc_phone)
                            else:
                                merged_con.point_of_contact = fapiis_rec.agency_poc_phone


                    #fapiis status can overwrite above, goes here
                    merged_con.status = fapiis_rec.record_type


            except FAPIISRecord.DoesNotExist as e:
                pass

            merged_con.save()

        #match with fapiis records

        #create merged record 

            #create status based on dates/fapiis

