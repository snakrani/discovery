import os
from django.test import TestCase
from django.core.management import call_command

class FPDSLoaderTest(TestCase):
    """Tests the load_fpds management command with limited vendor set"""
    fixtures = ['naics.json', 'setasides.json', 'fpds_test_vendor.json']

    def test_load(self):
        call_command('load_fpds')        


    #ToDO: methods to check values of certain contracts loaded from above command
