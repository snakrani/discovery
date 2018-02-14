import os
from django.test import TestCase
from django.core.management import call_command

from discovery.fixtures import get_vendor_fixtures

class FPDSLoaderTest(TestCase):
    """Tests the load_fpds management command"""
    fixtures = get_vendor_fixtures()

    def test_load(self):
        call_command('load_fpds', id=89, period=52, load=52, pause=0, max=1)        

    #ToDO: methods to check values of certain contracts loaded from above command
