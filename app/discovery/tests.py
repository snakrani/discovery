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
        
    def test_admin_found(self):
        self.validated_temp_redirect('/admin/')
        
    def test_results_found(self):
        self.validated_path('/results/')
    
    def test_results_csv_found_1(self):
        self.validated_path('/results/csv/')
    
    def test_results_csv_found_2(self):
        self.validated_path('/results/csv/', **{'vehicle': 'HCATS_SB', 'naics': 611710})
    
    def test_results_csv_found_3(self):
        self.validated_path('/results/csv/', **{'vehicle': 'PSS', 'pool': 'PSS_874', 'setasides': 'A6'})
        
    def test_vendor_found(self):
        self.validated_path('/vendor/079939977/')
    
    def test_vendor_csv_found(self):
        self.validated_path('/vendor/079939977/csv/')
