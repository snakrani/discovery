from django.core.management.base import BaseCommand, CommandError
from vendor.models import Vendor, Pool
from django.conf import settings
import requests
import logging


class Command(BaseCommand):

    logger = logging.getLogger('sam')

    def handle(self, *args, **kwargs):

        vendors = Vendor.objects.all()
        for v in vendors:
            #get SAM.gov API response for this vendor
            uri = settings.SAM_API_URL + v.duns_4 + '?api_key=' + settings.SAM_API_KEY
            sam_data = requests.get(uri).json()
   
            try:
                if 'sam_data' in sam_data:
                    if 'registration' in sam_data['sam_data']:
                        reg = sam_data['sam_data']['registration']
                        v.sam_status = reg['status']
                        v.sam_exclusion = reg['hasKnownExclusion']
                        v.oasis_address = reg['samAddress']['Line1']
                        v.oasis_citystate = "{0}, {1} {2}".format(reg['samAddress']['City'], reg['samAddress']['stateorProvince'], reg['samAddress']['Zip'])

                        v.sam_url = reg['corporateUrl']
                        

                        v.save()

                        # fill out setasides

                    else:
                        self.logger.debug("'registration' key is missing for {}".format(uri))

                elif 'Error' in sam_data:
                    self.logger.debug("SAM API returned an error for {0}, and duns {1}".format(uri, v.duns ))    
                else:
                    self.logger.debug("Could not load data from {} for unknown reason".format(uri))

            except KeyError as k:
                self.logger.debug("There was a key error on {0}: {1}".format(v.duns, k))

