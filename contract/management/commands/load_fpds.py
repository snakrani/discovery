from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from pyfpds import Contracts
from vendor.models import Vendor
from contract.models import FPDSContract
from datetime import datetime, timedelta

class Command(BaseCommand):
    
    contracts = Contracts()
   
    def date_format(self, date1, date2):
        return "[{0},{1}]".format(date1.strftime("%Y/%m/%d"), date2.strftime("%Y/%m/%d"))

    def try_key(self, obj, key):
        if key in obj:
            return obj[key]
        else:
            return None 

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
                }

                if award.get('transactionInformation'):
                    record['last_modified_by'] = award.get('transactionInformation').get('lastModifiedBy')
                    record['status'] = award.get('transactionInformation').get('status').get('@description')

                if award.get('contractData') and award.get('contractData').get('typeOfContractPricing'):
                    if type(award.get('contractData').get('typeOfContractPricing')) == str:
                        record['type_of_contract_pricing_name'] = award['contractData']['typeOfContractPricing']
                    else: 
                        record['type_of_contract_pricing_name'] = award['contractData']['typeOfContractPricing'].get('@description')
                        record['type_of_contract_pricing_id'] = award['contractData']['typeOfContractPricing'].get('#text')
               
                if award.get('productOrServiceInformation'):
                    
                    if type(award.get('productOrServiceInformation').get('principalNAICSCode')) == str:
                        record['naics'] = award['productOrServiceInformation']['principalNAICSCode']
                    elif award.get('productOrServiceInformation').get('principalNAICSCode'):
                        record['naics'] = award['productOrServiceInformation']['principalNAICSCode'].get('#text')
                    
                    if award.get('productOrServiceInformation').get('productOrServiceCode'):
                        record['psc'] = award['productOrServiceInformation']['productOrServiceCode'].get('#text')

                if piid in by_piid:
                    by_piid[piid].append(record)
                else:
                    by_piid[piid] = [record, ]

            for piid, records in by_piid.items():
                by_piid[piid] = sorted(records, key=lambda x: (x['mod_number'], x['transaction_number']))

               # try: 
                total = 0 # amount obligated
                
                print("================{0}===Vendor {1}=================\n".format(piid, v.duns))
                self.contracts.pretty_print(by_piid[piid])
                
                con, created = FPDSContract.objects.get_or_create(piid=piid, vendor=v)

                for mod in by_piid[piid]:
                    total += float(mod.get('obligated_amount'))
                    con.date_signed = mod.get('signed_date') 
                    con.completion_date = mod.get('current_completion_date') or mod.get('ultimate_completion_date')
                    con.agency_id = mod.get('agency_id')
                    con.agency_name = mod.get('agency_name')
                    con.pricing_type = mod.get('type_of_contract_pricing_id')

                    if mod.get('last_modified_by') and '@' in mod['last_modified_by'].lower():
                        #only add if it's an actual email, make this a better regex
                        con.last_modified_by = mod['last_modified_by']
                    
                    #ADD NAICS -- need to add other naics as objects to use foreignkey
                    con.PSC = mod.get('psc')
                    con.NAICS = mod.get('naics')

                con.obligated_amount = total
                
                #debug
               
                con.save()

            #except Exception as e:
            #self.contracts.pretty_print(vc)
                #break
                #by_piid[
            #print(by_piid)
            #break
            #print(len(v_con))
