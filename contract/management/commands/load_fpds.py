from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from pyfpds import Contracts
from vendor.models import Vendor
from datetime import datetime, timedelta

class Command(BaseCommand):
    
    contracts = Contracts()
   
    def date_format(self, date1, date2):
        return "[{0},{1}]".format(date1.strftime("%Y/%m/%d"), date2.strftime("%Y/%m/%d"))

    def try_key(self, obj, key):
        if key in obj:
            return obj[key]
        else:
            return "" 

    def handle(self, *args, **kwargs):
    
        today = datetime.now()
        ten_years = timedelta(weeks=(52*10))
        ten_years_ago = today - ten_years

        for v in Vendor.objects.all():
            
            by_piid = {} 
            
            v_con = self.contracts.get(vendor_duns=v.duns, date_signed=self.date_format(ten_years_ago, today), num_records='all')

            for vc in v_con:
            
                #self.contracts.pretty_print(vc)
                if 'IDV' in vc['content']:
                    continue  #skip top level idvs

                award = vc['content']['award']
                award_id = award['awardID']
                piid = ''

                if 'referencedIDVID' in award_id:
                    #part of an IDIQ
                    piid = award_id['referencedIDVID']['PIID'] + '_' 
       
                piid += award_id['awardContractID']['PIID']

                record = {
                    'mod_number': award_id['awardContractID']['modNumber'],
                    'transaction_number': award_id['awardContractID']['transactionNumber'],
                    'ultimate_completion_date': self.try_key(award['relevantContractDates'], 'ultimateCompletionDate'),
                    'current_completion_date': self.try_key(award['relevantContractDates'], 'currentCompletionDate'),
                    'signed_date': award['relevantContractDates']['signedDate'],
                    'agency_id': award_id['awardContractID']['agencyID']['#text'],
                    'agency_name': award_id['awardContractID']['agencyID']['@name'],
                    'obligated_amount': award['dollarValues']['obligatedAmount'],
                    'last_modified_by': award['transactionInformation']['lastModifiedBy'],
                    'status': award['transactionInformation']['status']['@description'],
                    'naics': self.try_key(self.try_key(award['productOrServiceInformation'], 'principalNAICSCode'), '#text'),
                    'psc': award['productOrServiceInformation']['productOrServiceCode']['#text'],
                }

                if self.try_key(award['contractData'], 'typeOfContractPricing') != '':
                    record['type_of_contract_pricing_name'] = award['contractData']['typeOfContractPricing']['@description']
                    record['type_of_contract_pricing_id'] = award['contractData']['typeOfContractPricing']['#text']
               

                if piid in by_piid:
                    by_piid[piid].append(record)
                else:
                    by_piid[piid] = [record, ]

            for piid, records in by_piid.items():
                by_piid[piid] = sorted(records, key=lambda x: (x['mod_number'], x['transaction_number']))

                print("================{0}====================\n".format(piid))
                self.contracts.pretty_print(by_piid[piid])
                #self.contracts.pretty_print(vc)
                #break
                #by_piid[
            #print(by_piid)
            #break
            #print(len(v_con))
            break
