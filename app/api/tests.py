from django.test import Client, TestCase
from django.utils import timezone
import json
import datetime

from discovery.fixtures import get_category_fixtures, get_vendor_fixtures, get_contract_fixtures, get_metadata_fixtures
from vendors.models import SamLoad


class NaicsTest(TestCase):
    """tests for NAICS API endpoint"""
    fixtures = get_category_fixtures()

    def setUp(self):
        self.c = Client()
        self.path = '/api/naics/'

    def test_request_no_params(self):
        resp = self.c.get(self.path, {'format': 'json'})
        
        self.assertEqual(resp.data['count'], 55)
        self.assertEqual(resp.status_code, 200)

    def test_request_q_param(self):
        resp = self.c.get(self.path, {'q': 'test'})
        
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.status_code, 200)


class PoolsTest(TestCase):
    """tests for Pools API endpoint"""
    fixtures = get_category_fixtures()

    def setUp(self):
        self.c = Client()
        self.path = '/api/pools/'

    def test_request_no_params(self):
        resp = self.c.get(self.path, {'format': 'json'})
        
        self.assertEqual(resp.data['count'], 18)
        self.assertEqual(resp.status_code, 200)

    def test_request_vehicle_param(self):
        resp = self.c.get(self.path, {'vehicle': 'HCATS_SB'})
        
        self.assertEqual(resp.data['count'], 2)
        self.assertEqual(resp.status_code, 200)

    def test_request_naics_param(self):
        resp = self.c.get(self.path, {'naics__code': 541611})
        
        self.assertEqual(resp.data['count'], 4)
        self.assertEqual(resp.status_code, 200)


class ZonesTest(TestCase):
    """tests for Zones API endpoint"""
    fixtures = get_category_fixtures()

    def setUp(self):
        self.c = Client()
        self.path = '/api/zones/'

    def test_request_no_params(self):
        resp = self.c.get(self.path, {'format': 'json'})
        
        self.assertEqual(resp.data['count'], 6)
        self.assertEqual(resp.status_code, 200)

    def test_request_state_param(self):
        resp = self.c.get(self.path, {'state': 'NC'})
        
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.status_code, 200)


class VendorsTest(TestCase):
    """test for vendor API endpoint"""
    fixtures = get_contract_fixtures()
 
    def setUp(self):
        self.c = Client()
        self.path = '/api/vendors/'
        sl = SamLoad(sam_load=timezone.now())
        sl.save()

    def test_request_no_params(self):
        resp = self.c.get(self.path, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)

    def test_request_valid_vehicle(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__vehicle__iexact': 'oasis_sb'})
        self.assertEqual(resp.status_code, 200)

    def test_request_invalid_vehicle_returns_empty(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__vehicle__iexact': 'dlasfjosdf'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 0)
 
    def test_request_valid_naics(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__naics__code': '541330'})
        self.assertEqual(resp.status_code, 200)

    def test_request_invalid_naics_returns_empty(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__naics__code': 'dlasfjosdf'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 0)
   
    def test_request_valid_setasides(self):
        resp = self.c.get(self.path, {'format': 'json', 'setasides__code': 'A6'})
        self.assertEqual(resp.status_code, 200)
   
    def test_request_invalid_setasides_returns_empty(self):
        resp = self.c.get(self.path, {'format': 'json', 'setasides__code': 'A25,27'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 0)

    def test_default_pagination(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__vehicle__iexact': 'oasis_sb'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['results']), 100)
        self.assertEqual(resp.data['previous'], None)
        self.assertTrue('page=2' in resp.data['next'])
        self.assertEqual(resp.data['count'], 130)
        
    def test_custom_pagination(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__vehicle__iexact': 'oasis', 'count': 15})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['results']), 15)
        self.assertEqual(resp.data['previous'], None)
        self.assertTrue('page=2' in resp.data['next'])
        self.assertEqual(resp.data['count'], 77)
   
    def test_request_num_results(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__naics__code': '541330'})
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(resp.data['count'], 0)

    def test_request_results(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__naics__code': '541330'})
        self.assertEqual(resp.status_code, 200)
        assert 'results' in resp.data

    def test_result_length_pool_group(self):
        resp = self.c.get(self.path, {'format': 'json', 'setasides__code': 'A2', 'pools__vehicle__iexact': 'oasis_sb', 'pools__naics__code': '541330'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['results']), resp.data['count'])

    def test_default_sort(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__vehicle__iexact': 'oasis'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['results'][0]['number_of_contracts'], 500)

    def test_sort_with_all_params(self):
        resp = self.c.get(self.path, {'format': 'json', 'pools__vehicle__iexact': 'oasis', 'ordering': 'name'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['results'][0]['name'] , "Accenture Federal Services LLC")
        
        resp = self.c.get(self.path, {'format': 'json', 'pools__vehicle__iexact': 'oasis', 'ordering': '-name'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['results'][0]['name'] , "Wyle Laboratories, Inc.")


class VendorTest(TestCase):
    """ tests single vendor endpoint """
    fixtures = get_vendor_fixtures()

    def setUp(self):
        self.c = Client()
        self.path = '/api/vendors/118498067/'

    def test_vendor_exists(self):
        resp = self.c.get(self.path)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['name'] , 'Advanced C4 Solutions, Inc. dba AC4S')


class ContractsTest(TestCase):
    """tests for Contracts API endpoint"""
    fixtures = get_contract_fixtures()

    def setUp(self):
        self.c = Client()
        self.path = '/api/contracts/'

    def test_default_pagination(self):
        resp = self.c.get(self.path, {'vendor__duns': '926451519'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['results']), 100)
        self.assertEqual(resp.data['previous'], None)
        self.assertTrue('page=2' in resp.data['next'])
        self.assertEqual(resp.data['count'], 500)
    
    def test_custom_pagination(self):
        resp = self.c.get(self.path, {'vendor__duns': '926451519', 'count': 25})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['results']), 25)
        self.assertEqual(resp.data['previous'], None)
        self.assertTrue('page=2' in resp.data['next'])
        self.assertEqual(resp.data['count'], 500)

    def test_naics_filter(self):
        resp = self.c.get(self.path, {'vendor__duns': '807990382', 'NAICS': '541611'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 1)

    def test_default_sort(self):
        resp = self.c.get(self.path, {'vendor__duns': '807990382'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['results'][0]['date_signed'], "2017-11-17T00:00:00Z")

    def test_sort_with_all_params(self):
        resp = self.c.get(self.path, {'vendor__duns': '807990382', 'ordering': 'status__name'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['results'][0]['status']['name'], 'Completed')
        
        resp = self.c.get(self.path, {'vendor__duns': '807990382', 'ordering': '-status__name'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['results'][0]['status']['name'], 'Terminated for Convenience')


class MetadataTest(TestCase):
    """ Tests the metadata endpoint """
    fixtures = get_metadata_fixtures()

    def setUp(self):
        self.c = Client()
        self.path = '/api/metadata/'

    def test_metadata(self):
        resp = self.c.get(self.path)
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(None, resp.data['sam_load_date'])
        self.assertNotEqual(None, resp.data['fpds_load_date'])
