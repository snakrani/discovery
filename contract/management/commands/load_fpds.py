from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from pyfpds import Contracts
from vendor.models import Vendor
from contract.models import FPDSContract
from contract import catch_key_error
from datetime import datetime, timedelta

def get_award_id_obj(award):
    return award['awardID']

def get_piid(award_id):
    piid = ''
    if 'referencedIDVID' in award_id:
        #part of an IDIQ
        piid = award_id['referencedIDVID']['PIID'] + '_' 
    piid += award_id['awardContractID']['PIID']

    return piid

def get_mod(award_id):
    return award_id['awardContractID']['modNumber']

def get_transaction_number(award_id):
    return award_id['awardContractID']['transactionNumber']

@catch_key_error
def get_ultimate_completion_date(award):
    return award['relevantContractDates']['ultimateCompletionDate']

@catch_key_error
def get_current_completion_date(award):
    return award['relevantContractDates']['currentCompletionDate']

@catch_key_error
def get_annual_revenue(award):
    print (award['vendor']['vendorSiteDetails']['vendorOrganizationFactors']['annualRevenue'])
    return award['vendor']['vendorSiteDetails']['vendorOrganizationFactors']['annualRevenue']

@catch_key_error
def get_number_of_employees(award):
    return award['vendor']['vendorSiteDetails']['vendorOrganizationFactors']['numberOfEmployees']

@catch_key_error
def get_last_modified_by(award):
    return award['transactionInformation']['lastModifiedBy']

@catch_key_error
def get_status(award):
    return award['transactionInformation']['status']['@description']

def get_contract_pricing_name(award):
    
    @catch_key_error
    def get_name(award):
        return award['contractData']['typeOfContractPricing']

    name = get_name(award) 
    if name and type(name) == str:
        return name

    elif name: 
        return award['contractData']['typeOfContractPricing']['@description']

@catch_key_error
def get_contract_pricing_id(award):
    return award['contractData']['typeOfContractPricing']['#text']
 
def get_naics(award):
    
    @catch_key_error
    def get_name(award):
        return award['productOrServiceInformation']['principalNAICSCode']

    name = get_name(award) 
    if name and type(name) == str:
        return name

    elif name: 
        return award['productOrServiceInformation']['principalNAICSCode']['#text']

@catch_key_error
def get_psc(award):
    return award['productOrServiceInformation']['productOrServiceCode']['#text']


class Command(BaseCommand):
    
    contracts = Contracts()
   
    def date_format(self, date1, date2):
        return "[{0},{1}]".format(date1.strftime("%Y/%m/%d"), date2.strftime("%Y/%m/%d"))

    def handle(self, *args, **kwargs):
   
        #TO DO make this smarter -- keep track of last load, only load modified since that date
        today = datetime.now()
        ten_years = timedelta(weeks=(52*10))
        ten_years_ago = today - ten_years

        #for v in Vendor.objects.filter(duns='127222466'):
        for v in Vendor.objects.all():

            by_piid = {} 
            v_con = self.contracts.get(vendor_duns=v.duns, date_signed=self.date_format(ten_years_ago, today), num_records='all')

            #find some way to order by date so that ANNUAL REVENUT AND NUMBER OF EMPLOYEES IS CORRECT
            
            for vc in v_con:
                
                con_type = ''
                #self.contracts.pretty_print(vc)
                if 'IDV' in vc['content']:
                    continue # don't get IDV records

                award = vc['content']['award']
                award_id = get_award_id_obj(award)
                piid = get_piid(award_id)

                record = {
                    'mod_number': get_mod(award_id), 
                    'transaction_number': get_transaction_number(award_id),
                    'ultimate_completion_date': get_ultimate_completion_date(award), 
                    'current_completion_date': get_current_completion_date(award), 
                    'signed_date': award['relevantContractDates']['signedDate'],
                    'agency_id': award_id['awardContractID']['agencyID']['#text'],
                    'agency_name': award_id['awardContractID']['agencyID']['@name'],
                    'obligated_amount': award['dollarValues']['obligatedAmount'],
                    'annual_revenue': get_annual_revenue(award),
                    'number_of_employees': get_number_of_employees(award),
                    'last_modified_by': get_last_modified_by(award),
                    'status': get_status(award),
                    'type_of_contract_pricing_name': get_contract_pricing_name(award),
                    'type_of_contract_pricing_id': get_contract_pricing_id(award),
                    'naics' : get_naics(award),
                    'psc': get_psc(award),
                }

                
                if piid in by_piid:
                    by_piid[piid].append(record)
                else:
                    by_piid[piid] = [record, ]

            for piid, records in by_piid.items():
                by_piid[piid] = sorted(records, key=lambda x: (x['mod_number'], x['transaction_number']))

               # try: 
                total = 0 # amount obligated
                
                print("================{0}===Vendor {1}=================\n".format(piid, v.duns))
                print(v.duns)
                print(v.id)

                self.contracts.pretty_print(by_piid[piid])
                
                con, created = FPDSContract.objects.get_or_create(piid=piid, vendor=v)

                for mod in by_piid[piid]:
                    total += float(mod.get('obligated_amount'))
                    con.date_signed = mod.get('signed_date') 
                    con.completion_date = mod.get('current_completion_date') or mod.get('ultimate_completion_date')
                    con.agency_id = mod.get('agency_id')
                    con.agency_name = mod.get('agency_name')
                    con.pricing_type = mod.get('type_of_contract_pricing_id')
                    con.pricing_type_name = mod.get('type_of_contract_pricing_name')

                    if mod.get('last_modified_by') and '@' in mod['last_modified_by'].lower():
                        #only add if it's an actual email, make this a better regex
                        con.last_modified_by = mod['last_modified_by']
                    
                    #ADD NAICS -- need to add other naics as objects to use foreignkey
                    con.PSC = mod.get('psc')
                    con.NAICS = mod.get('naics')

                    if mod.get('annual_revenue'):
                        v.annual_revenue = mod.get('annual_revenue')

                    if mod.get('number_of_employees'):
                        v.number_of_employees = mod.get('number_of_employees')

                con.obligated_amount = total
                con.save()

            #save updates to annual revenue, number of employees
            v.save()
