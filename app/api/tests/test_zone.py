from discovery import unit_tests as test
from api import filters


class BaseZoneTest(test.CategoryAPITestCase):
    def initialize(self):
        self.router = 'zones'
        
    def validate_object(self, resp, base_key = []):
        resp.is_int(base_key + ['id'])
        resp.is_not_empty(base_key + ['states'])


class ZoneListTest(BaseZoneTest):
    
    def test_no_args(self):
        self.validated_list(6)
        
    
    def test_filter_id_exact_found(self):
        resp = self.validated_list(1, id = 2)
        resp.validate(lambda resp, base_key: resp.equal(base_key + ['id'], 2))
    
    def test_filter_id_lt_found(self):
        resp = self.validated_list(3, id__lt = 4)
        resp.validate(lambda resp, base_key: resp.is_max(base_key + ['id'], 3))
    
    def test_filter_id_lte_found(self):
        resp = self.validated_list(4, id__lte = 4)
        resp.validate(lambda resp, base_key: resp.is_max(base_key + ['id'], 4))
    
    def test_filter_id_gt_found(self):
        resp = self.validated_list(4, id__gt = 2)
        resp.validate(lambda resp, base_key: resp.is_min(base_key + ['id'], 3))
    
    def test_filter_id_gte_found(self):
        resp = self.validated_list(4, id__gte = 3)
        resp.validate(lambda resp, base_key: resp.is_min(base_key + ['id'], 3))
    
    def test_filter_id_range_found(self):
        resp = self.validated_list(4, id__range = "2,5")
        resp.validate(lambda resp, base_key: resp.is_in(base_key + ['id'], [2, 3, 4, 5]))
    
    def test_filter_id_in_found(self):
        resp = self.validated_list(3, id__in = "2,3,5")
        resp.validate(lambda resp, base_key: resp.is_in(base_key + ['id'], [2, 3, 5]))
             
    def test_filter_id_exact_not_found(self):
        self.empty_list(id = 75)
      
    def test_filter_id_lt_not_found(self):
        self.empty_list(id__lt = 0)
        
    def test_filter_id_lte_not_found(self):
        self.empty_list(id__lte = -2)        
        
    def test_filter_id_gt_not_found(self):
        self.empty_list(id__gt = 75)        
       
    def test_filter_id_gte_not_found(self):
        self.empty_list(id__gte = 75)        
       
    def test_filter_id_range_not_found(self):
        self.empty_list(id__range = "75,120")    
       
    def test_filter_id_in_not_found(self):
        self.empty_list(id__in = "75,82,21")    
    
    
    def test_filter_state_exact_found(self):
        resp = self.validated_list(1, state = 'PA')
        resp.validate(lambda resp, base_key: resp.includes(base_key + ['states'], 'PA'))
    
    def test_filter_state_iexact_found(self):
        resp = self.validated_list(1, state__iexact = 'mE')
        resp.validate(lambda resp, base_key: resp.includes(base_key + ['states'], 'ME'))
    
    def test_filter_state_in_found(self):
        resp = self.validated_list(3, state__in = "PA,NC,TX,NY")
        resp.validate(lambda resp, base_key: resp.includes(base_key + ['states'], ['PA', 'NC', 'TX', 'NY']))
    
    def test_filter_state_exact_not_found(self):
        self.empty_list(state = "ABCD")
    
    def test_filter_state_iexact_not_found(self):
        self.empty_list(state__iexact = "ABCD")
    
    def test_filter_state_in_not_found(self):
        self.empty_list(state__in = "ABCD,EFGH")
    
       
    def test_ordering_id(self):
        resp = self.validated_list(6, ordering = '-id')
        resp.validate_ordering('id', 'desc')
    
    
    def test_mixed_request_found_1(self):
        resp = self.validated_list(1, id = 1, state__iexact = 'md')
        resp.validate(lambda resp, base_key: resp.equal(base_key + ['id'], 1))
        resp.validate(lambda resp, base_key: resp.includes(base_key + ['states'], 'MD'))
    
    def test_mixed_request_found_2(self):
        resp = self.validated_list(1, filters = self.encode_str('(state__iexact=ct)&(state__iexact=nH)'))
        resp.validate(lambda resp, base_key: resp.includes(base_key + ['states'], ['CT', 'NH']))
    
    def test_mixed_request_not_found_1(self):
        self.empty_list(id = 625, state = 'NC')
    
    def test_mixed_request_not_found_2(self):
        self.empty_list(filters = self.encode_str('(state=GA)&(state=IA)'))
    

    def test_pagination_no_args(self):
        resp = self.validated_list(6)
        resp.validate_pagination(1)    
    
    def test_pagination_page_requested(self):
        self.invalid_list(page = 2)
    
    def test_pagination_count_requested(self):
        resp = self.validated_list(6, count = 2)
        resp.validate_pagination(1, 2)
    
    def test_pagination_page_count_requested(self):
        resp = self.validated_list(6, page = 2, count = 2)
        resp.validate_pagination(2, 2)


class ZoneRetrieveTest(BaseZoneTest):
    
    def test_found_1(self):
        resp = self.validated_object(1)
        resp.includes('states', 'DE')
    
    def test_found_2(self):
        resp = self.validated_object(3)
        resp.includes('states', 'FL')
    
    def test_found_3(self):
        resp = self.validated_object(6)
        resp.includes('states', 'KS')
    
    def test_not_found_1(self):
        self.invalid_object(345)
    
    def test_not_found_2(self):
        self.invalid_object('ABCDEFG')
