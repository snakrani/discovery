from django.test import tag

from test import cases as case
from test import fixtures as data


@tag('metadata')
class MetadataTest(case.APITestCase):
    
    fixtures = data.get_metadata_fixtures()
    
    
    def initialize(self):
        self.router = 'metadata'
    
    
    @tag('info', 'date')
    def test_found(self):
        resp = self.validated_data()
        resp.matches('sam_load_date', '^\d{4}-\d{2}-\d{2}$')
        resp.matches('fpds_load_date', '^\d{4}-\d{2}-\d{2}$')
