from test import cases as case
from test import fixtures as data

from django.core.management import call_command


class FPDSLoaderTest(case.BaseTestCase):

    fixtures = data.get_vendor_fixtures()


    def test_load(self):
        call_command('load_fpds', id=89, period=52, load=52, pause=0, max=1)
