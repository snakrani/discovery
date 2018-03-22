from test import cases as case


class MetadataListTest(case.MetadataAPITestCase):
  
    def initialize(self):
        self.router = 'metadata'
    

    def validate_object(self, resp):
        resp.is_not_empty('sam_load_date')
        resp.is_not_empty('fpds_load_date')
    
    
    def test_mixed_request_found_1(self):
        resp = self.validated_data()
        resp.validate_object()
