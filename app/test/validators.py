from django.conf import settings

from test.common import get_nested_value

import re


class BaseValidator(object):
    
    test = None
    
    
    def __init__(self, test_case):
        self.test = test_case

    
    # Utilities
    
    def check(self, validator, *args, **kwargs):
        try:
            getattr(self, validator)(*args, **kwargs)
            return True
        except AssertionError as error:
            return False
        
    
    # Data
    
    def compare_data(self, op, data_value, correct_value = None, **params):
        try:
            if correct_value is not None:
                getattr(self.test, op)(data_value, correct_value, **params)
            else:
                getattr(self.test, op)(data_value, **params)
                
        except Exception as error:
            raise self._wrap_error(error)
    
    def compare(self, op, resp_value, correct_value = None, **params):
        self.compare_data(op, resp_value, correct_value, **params)
    
    
    def equal(self, resp_value, correct_value):
        self.compare('assertEqual', resp_value, correct_value)
        
    def equal_data(self, data_value, correct_value):
        self.compare_data('assertEqual', data_value, correct_value)
        
    def not_equal(self, resp_value, not_value):
        self.compare('assertNotEqual', resp_value, not_value)
        
    def not_equal_data(self, data_value, not_value):
        self.compare_data('assertNotEqual', data_value, not_value)
        
    def is_a(self, resp_value, correct_value):
        self.compare('assertIs', resp_value, correct_value)
        
    def is_a_data(self, data_value, correct_value):
        self.compare_data('assertIs', data_value, correct_value)
        
    def is_not_a(self, resp_value, not_value):
        self.compare('assertIsNot', resp_value, not_value)
        
    def is_not_a_data(self, data_value, not_value):
        self.compare_data('assertIsNot', data_value, not_value)
        
    def is_in(self, resp_value, correct_values):
        correct_values = correct_values.split(',') if isinstance(correct_values, str) else correct_values
        self.compare('assertIn', resp_value, correct_values)
        
    def is_in_data(self, data_value, correct_values):
        correct_values = correct_values.split(',') if isinstance(correct_values, str) else correct_values
        self.compare_data('assertIn', data_value, correct_values)
        
    def is_not_in(self, resp_value, not_values):
        not_values = not_values.split(',') if isinstance(not_values, str) else not_values
        self.compare('assertNotIn', resp_value, not_values)
        
    def is_not_in_data(self, data_value, not_values):
        not_values = not_values.split(',') if isinstance(not_values, str) else not_values
        self.compare_data('assertNotIn', data_value, not_values)
        
    def is_instance(self, resp_value, correct_value):
        self.compare('assertIsInstance', resp_value, correct_value)
        
    def is_instance_data(self, data_value, correct_value):
        self.compare_data('assertIsInstance', data_value, correct_value)
        
    def is_not_instance(self, resp_value, not_value):
        self.compare('assertNotIsInstance', resp_value, not_value)
        
    def is_not_instance_data(self, data_value, not_value):
        self.compare_data('assertNotIsInstance', data_value, not_value)
        
    def is_true(self, resp_value):
        self.compare('assertTrue', resp_value)
        
    def is_true_data(self, data_value):
        self.compare_data('assertTrue', data_value)
        
    def is_false(self, resp_value):
        self.compare('assertFalse', resp_value)
        
    def is_false_data(self, data_value):
        self.compare_data('assertFalse', data_value)
        
    def is_none(self, resp_value):
        self.compare('assertIsNone', resp_value)
        
    def is_none_data(self, data_value):
        self.compare_data('assertIsNone', data_value)
        
    def is_not_none(self, resp_value):
        self.compare('assertIsNotNone', resp_value)
        
    def is_not_none_data(self, data_value):
        self.compare_data('assertIsNotNone', data_value)
    
    def is_empty(self, resp_value):
        self.compare('assertIsEmpty', resp_value)
        
    def is_empty_data(self, data_value):
        self.compare_data('assertIsEmpty', data_value)
            
    def is_not_empty(self, resp_value):
        self.compare('assertIsNotEmpty', resp_value)
        
    def is_not_empty_data(self, data_value):
        self.compare_data('assertIsNotEmpty', data_value)
        
    def is_int(self, resp_value):
        self.compare('assertInteger', resp_value)
        
    def is_int_data(self, data_value):
        self.compare_data('assertInteger', data_value)
        
    def is_float(self, resp_value):
        self.compare('assertFloat', resp_value)
        
    def is_float_data(self, data_value):
        self.compare_data('assertFloat', data_value)
        
    def is_max(self, resp_value, maximum_value):
        self.compare('assertLessThanEqual', resp_value, maximum_value)
        
    def is_max_data(self, data_value, maximum_value):
        self.compare_data('assertLessThanEqual', data_value, maximum_value)
        
    def is_below(self, resp_value, excluded_value):
        self.compare('assertLessThan', resp_value, excluded_value)
        
    def is_below_data(self, data_value, excluded_value):
        self.compare_data('assertLessThan', data_value, excluded_value)
        
    def between(self, resp_value, correct_values):
        self.compare('assertBetween', resp_value, correct_values)
        
    def between_data(self, data_value, correct_values):
        self.compare_data('assertBetween', data_value, correct_values)
    
    def is_min(self, resp_value, minimum_value):
        self.compare('assertGreaterThanEqual', resp_value, minimum_value)
        
    def is_min_data(self, data_value, minimum_value):
        self.compare_data('assertGreaterThanEqual', data_value, minimum_value)
        
    def is_above(self, resp_value, excluded_value):
        self.compare('assertGreaterThan', resp_value, excluded_value)
        
    def is_above_data(self, data_value, excluded_value):
        self.compare_data('assertGreaterThan', data_value, excluded_value)
    
    def contains(self, resp_value, substring):
        self.compare('assertStrContains', resp_value, substring)
        
    def contains_data(self, data_value, substring):
        self.compare_data('assertStrContains', data_value, substring)
        
    def matches(self, resp_value, pattern):
        self.compare('assertMatch', resp_value, pattern)
        
    def matches_data(self, data_value, pattern):
        self.compare_data('assertMatch', data_value, pattern)
        
    def startswith(self, resp_value, text):
        self.matches(resp_value, "^{}".format(re.escape(text)))
        
    def startswith_data(self, data_value, text):
        self.matches_data(data_value, "^{}".format(re.escape(text)))
        
    def endswith(self, resp_value, text):
        self.matches(resp_value, "{}$".format(re.escape(text)))
        
    def endswith_data(self, data_value, text):
        self.matches_data(data_value, "{}$".format(re.escape(text)))
        
    def icontains(self, resp_value, substring):
        self.compare('assertIStrContains', resp_value, substring)
        
    def icontains_data(self, data_value, substring):
        self.compare_data('assertIStrContains', data_value, substring)
        
    def imatches(self, resp_value, pattern):
        self.compare('assertIMatch', resp_value, pattern)
        
    def imatches_data(self, data_value, pattern):
        self.compare_data('assertIMatch', data_value, pattern)
        
    def istartswith(self, resp_value, text):
        self.imatches(resp_value, "^{}".format(re.escape(text)))
        
    def istartswith_data(self, data_value, text):
        self.imatches_data(data_value, "^{}".format(re.escape(text)))
        
    def iendswith(self, resp_value, text):
        self.imatches(resp_value, "{}$".format(re.escape(text)))
        
    def iendswith_data(self, data_value, text):
        self.imatches_data(data_value, "{}$".format(re.escape(text)))
        
    def iequal(self, resp_value, text):
        self.imatches(resp_value, "^{}$".format(re.escape(text)))
        
    def iequal_data(self, data_value, text):
        self.imatches_data(data_value, "^{}$".format(re.escape(text)))
    
    def is_year(self, resp_value, year):
        self.compare('assertYear', resp_value, year)
        
    def is_year_data(self, data_value, year):
        self.compare_data('assertYear', data_value, year)
            
    def is_month(self, resp_value, month):
        self.compare('assertMonth', resp_value, month)
        
    def is_month_data(self, data_value, month):
        self.compare_data('assertMonth', data_value, month)
        
    def is_day(self, resp_value, day):
        self.compare('assertDay', resp_value, day)
        
    def is_day_data(self, data_value, day):
        self.compare_data('assertDay', resp_value, day)
        
    def is_week(self, resp_value, week):
        self.compare('assertWeek', resp_value, week)
        
    def is_week_data(self, data_value, week):
        self.compare_data('assertWeek', data_value, week)
    
    def is_week_day(self, resp_value, week_day):
        self.compare('assertWeekDay', resp_value, week_day)
        
    def is_week_day_data(self, data_value, week_day):
        self.compare_data('assertWeekDay', data_value, week_day)
    
    def is_quarter(self, resp_value, quarter):
        self.compare('assertQuarter', resp_value, quarter)
        
    def is_quarter_data(self, data_value, quarter):
        self.compare_data('assertQuarter', data_value, quarter)
    
        
    def includes(self, resp_value, items, validator = None):
        self.compare('assertIncludes', resp_value, items, resp = self, validator = validator)


class APIResponseValidator(BaseValidator):
    
    resp = None
    url  = ''
    
    
    def __init__(self, response, test_case, url):
        self.resp = response
        self.test = test_case
        self.url = url


    # Utilities
    
    def _wrap_error(self, error):
        if self.url:
            error.args = ("{}\nRequestURL: {}".format(error.args[0], self.url),)
            
        raise error
    

    # Status
    
    def check_status(self, status):
        self.test.assertEqual(self.resp.status_code, status)
        
    def success(self):
        self.check_status(200)
        
    def failure(self):
        self.check_status(400)
        
    def not_found(self):
        self.check_status(404)
        
        
    # Data
    
    def compare(self, op, resp_value, correct_value = None, **params):
        if isinstance(resp_value, (str, list)):
            data_value = get_nested_value(self.resp.data, resp_value)
        else:
            data_value = resp_value
                
        self.compare_data(op, data_value, correct_value, **params)
    
        
    # Count
    
    def count(self, correct_value):
        self.equal('count', correct_value)
        
    def countMax(self, maximum_value):
        self.is_max('count', maximum_value)
        
    def countMin(self, minimum_value):
        self.is_min('count', minimum_value)
        
    
    # Ordering
    
    def _order_value(self, value):
        if isinstance(value, str):
            return re.sub('[^a-z0-9]+', '', value.lower())
        else:
            return value


    def validate_ordering(self, resp_value, dir = 'asc'):
        prev_value = None
        
        if not dir in ['asc', 'desc']:
            raise Exception("Ordering direction ({}) not supported".format(dir))
        
        for i in range(0, len(self.resp.data['results']) - 1):
            data_value = get_nested_value(self.resp.data['results'][i], resp_value)
            
            if data_value is not None:
                if prev_value is not None:
                    if dir == 'asc':
                        if self._order_value(data_value) < self._order_value(prev_value):
                            raise self._wrap_error(AssertionError("Data value ({}) is less than previous ({}) - Expected greater or equal".format(data_value, prev_value)))
                    else:
                        if self._order_value(data_value) > self._order_value(prev_value):
                            raise self._wrap_error(AssertionError("Data value ({}) is greater than previous ({}) - Expected less than or equal".format(data_value, prev_value)))
                
                prev_value = data_value
    
    
    # Pagination
    
    def validate_pagination(self, page = 1, page_count = None):
        page_size = settings.REST_PAGE_COUNT
        result_count = len(self.resp.data['results'])
        
        if page_count:
            if result_count < page_count:
                raise self._wrap_error(AssertionError("Data results returned fewer results ({}) than expected ({})".format(result_count, page_count)))
        
        if page_count or result_count > page_size:
            if page == 1:
                self.is_none('previous')
            
                self.matches('next', '^https?://')
                self.matches('next', 'page=2')
        
            else:
                self.matches('previous', '^https?://')
                
                if page > 2:
                    self.matches('previous', "page={}".format(page - 1))
            
                self.matches('next', '^https?://')
                self.matches('next', "page={}".format(page + 1))

            
    # Validation
    
    def validate(self, validate_function):
        for i in range(0, len(self.resp.data['results']) - 1):
            validate_function(self, ['results', i])
    
    def validate_list(self):
        self.validate(lambda resp, base_key: self.test.validate_object(resp, base_key))
            
    def validate_object(self):
        self.test.validate_object(self)
