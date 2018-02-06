import os
from django.test import TestCase
from django.core.management import call_command

class FPDSLoaderTest(TestCase):
    """Tests the load_fpds management command"""
    fixtures = ['naics.json', 'setasides.json', 'locations.json', 'fpds_vendor.json']

    def test_load(self):
        call_command('load_fpds', period=52, load=52, pause=0, max=1)        


    #ToDO: methods to check values of certain contracts loaded from above command
