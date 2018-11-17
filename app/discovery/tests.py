from test import cases as case
from test import fixtures as data


class SmokeTest(case.RequestTestCase):
    
    fixtures = data.get_vendor_fixtures()


    def test_home_found(self):
        self.validated_path('/')

    def test_docs_found_1(self):
        self.validated_path('/api/')
        
    def test_docs_found_2(self):
        self.validated_temp_redirect('/docs/')
        
    def test_docs_found_3(self):
        self.validated_temp_redirect('/developer/')
        
    def test_docs_found_4(self):
        self.validated_temp_redirect('/developers/')
