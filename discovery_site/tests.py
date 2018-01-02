from django.test import Client, TestCase

class SmokeTest(TestCase):
    """smoke tests for discovery site"""

    fixtures = ['naics.json', 'vendors.json', 'setasides.json', 'pools.json']

    def setUp(self):
        self.c = Client()

    def test_index_page_loads(self):
        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 200)
