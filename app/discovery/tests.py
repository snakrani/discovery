from django.test import Client, TestCase

from discovery.fixtures import get_vendor_fixtures


class SmokeTest(TestCase):
    """smoke tests for discovery site"""
    fixtures = get_vendor_fixtures()

    def setUp(self):
        self.c = Client()

    def test_index_page_loads(self):
        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 200)
