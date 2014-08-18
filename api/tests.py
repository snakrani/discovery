from django.test import Client, TestCase
from django.utils import timezone

from vendor.models import SamLoad

class NaicsTest(TestCase):
    """tests for NAICS API endpoint"""
    fixtures = ['naics.json']

    def setUp(self):
        self.c = Client()
        self.path = '/api/naics/'

    def test_request_no_params(self):
        resp = self.c.get(self.path, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)

    def test_request_q_param(self):
        resp = self.c.get(self.path, {'q': 'test'})
        self.assertEqual(resp.status_code, 200)


class VendorsTest(TestCase):
    """test for vendor API endpoint"""
    fixtures = ['vendors.json']
 
    def setUp(self):
        self.c = Client()
        self.path = '/api/vendors/'
        sl = SamLoad(sam_load=timezone.now())
        sl.save()

    def test_request_no_params(self):
        resp = self.c.get(self.path, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)

    def test_request_valid_naics(self):
        resp = self.c.get(self.path, {'format': 'json', 'naics': '541330'})
        self.assertEqual(resp.status_code, 200)

    def test_request_invalid_naics_returns_empty_list(self):
        resp = self.c.get(self.path, {'format': 'json', 'naics': 'dlasfjosdf'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['num_results'], 0)
    
    def test_request_num_results(self):
        resp = self.c.get(self.path, {'format': 'json', 'naics': '541330'})
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(resp.data['num_results'], 0)

    def test_request_results(self):
        resp = self.c.get(self.path, {'format': 'json', 'naics': '541330'})
        self.assertEqual(resp.status_code, 200)
        assert 'results' in resp.data

    def test_latest_sam_load_with_data(self):
        resp = self.c.get(self.path, {'format': 'json', 'naics': '541330'})
        self.assertEqual(resp.status_code, 200)
        assert 'sam_load' in resp.data

    def test_sam_load_with_no_data(self):
        SamLoad.objects.all().delete()
        resp = self.c.get(self.path, {'format': 'json', 'naics': '541330'})
        self.assertEqual(resp.status_code, 200)
        assert 'sam_load' in resp.data

    def test_no_naics_returns_all(self):
        resp = self.c.get(self.path, {'format': 'json', 'naics': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['num_results'] > 0)

    def test_all_naics_returns_all(self):
        resp = self.c.get(self.path, {'format': 'json', 'naics': "all"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['num_results'] > 0)

    def test_group_by_pool(self):
        resp = self.c.get(self.path, {'format': 'json', 'group': 'pool', 'naics': '541330'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('number' in resp.data['results'][0])
        self.assertTrue('vehicle' in resp.data['results'][0])

    def test_one_pool_returned(self):
        resp = self.c.get(self.path, {'format': 'json', 'naics': 'all', 'pool': '1_SB', 'group': 'pool' })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data['results']) == 1)
        self.assertTrue(resp.data['results'][0]['id'] == '1_SB')





