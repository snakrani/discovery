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

    def handle(self, *args, **kwargs):
    
        today = datetime.now()
        ten_years = timedelta(weeks=(52*10))
        ten_years_ago = today - ten_years

        for v in Vendor.objects.all():
           
            print(self.date_format(today, ten_years_ago))
            v_con = self.contracts.get(vendor_duns=v.duns, date_signed=self.date_format(ten_years_ago, today), num_records=10**10)

            print(len(v_con))
            break
