from django.conf import settings
from django.db.models.query import QuerySet

from test.common import normalize_list, get_nested_value

import re


VALIDATION_MAP = {
#   Lookup:   Validation method
    'isnull': 'is_none',
    'exact': 'equal',
    'iexact': 'iequal',
    'in': 'is_in',
    'contains': 'contains',
    'icontains': 'icontains',
    'startswith': 'startswith',
    'istartswith': 'istartswith',
    'endswith': 'endswith',
    'iendswith': 'iendswith',
    'regex': 'matches',
    'iregex': 'imatches',
    'date': 'startswith',
    'year': 'is_year',
    'month': 'is_month',
    'day': 'is_day',
    'week': 'is_week',
    'week_day': 'is_week_day',
    'quarter': 'is_quarter',
    'range': 'between',
    'lt': 'is_below',
    'lte': 'is_max', 
    'gt': 'is_above', 
    'gte': 'is_min',
}


class BaseValidator(object):
    
    test = None
    
    
    def __init__(self, test_case):
        self.test = test_case

    
    # Utilities
    
    def _wrap_error(self, error):
        raise error
    
    
    def check(self, validator, *args, **kwargs):
        try:
            getattr(self, validator)(*args, **kwargs)
            return True
        except AssertionError as error:
            return False
        
    
    # Data
    
    def get_data(self):
        return {}
    

    def get_data_value(self, nested_keys):
        return get_nested_value(self.get_data(), nested_keys)
    
    
    def compare_data(self, op, data_value, value = None, **params):
        
        def _compare(op, data_value, value, **params):
            if value is not None:
                getattr(self.test, op)(data_value, value, **params)
            else:
                getattr(self.test, op)(data_value, **params)
        
        try:
            if isinstance(value, (list, tuple, QuerySet)):
                value = list(value)
            elif value is not None:
                value = str(value)
            
            if isinstance(data_value, (list, tuple, QuerySet)):
                success = False
                
                for index, data_element in enumerate(list(data_value)):
                    try:
                        _compare(op, str(data_element), value, **params)
                        success = True
                    
                    except AssertionError as error:
                        pass
                    
                if not success:
                    raise self._wrap_error(AssertionError("No items in value: ({}) {} ({})".format(data_value, op, value))) 
            
            elif data_value is not None:
                _compare(op, str(data_value), value, **params)
                
        except Exception as error:
            raise self._wrap_error(error)
    
    
    def compare(self, op, nested_keys, value = None, **params):
        self.compare_data(op, self.get_data_value(nested_keys), value, **params)
    
    
    def equal(self, nested_keys, correct_value):
        self.compare('assertEqual', nested_keys, correct_value)
        
    def equal_data(self, data_value, correct_value):
        self.compare_data('assertEqual', data_value, correct_value)
        
    def not_equal(self, nested_keys, not_value):
        self.compare('assertNotEqual', nested_keys, not_value)
        
    def not_equal_data(self, data_value, not_value):
        self.compare_data('assertNotEqual', data_value, not_value)
        
    def is_a(self, nested_keys, correct_value):
        self.compare('assertIs', nested_keys, correct_value)
        
    def is_a_data(self, data_value, correct_value):
        self.compare_data('assertIs', data_value, correct_value)
        
    def is_not_a(self, nested_keys, not_value):
        self.compare('assertIsNot', nested_keys, not_value)
        
    def is_not_a_data(self, data_value, not_value):
        self.compare_data('assertIsNot', data_value, not_value)
        
    def is_in(self, nested_keys, correct_values):
        correct_values = correct_values.split(',') if isinstance(correct_values, str) else correct_values
        self.compare('assertIn', nested_keys, correct_values)
        
    def is_in_data(self, data_value, correct_values):
        correct_values = correct_values.split(',') if isinstance(correct_values, str) else correct_values
        self.compare_data('assertIn', data_value, correct_values)
        
    def is_not_in(self, nested_keys, not_values):
        not_values = not_values.split(',') if isinstance(not_values, str) else not_values
        self.compare('assertNotIn', nested_keys, not_values)
        
    def is_not_in_data(self, data_value, not_values):
        not_values = not_values.split(',') if isinstance(not_values, str) else not_values
        self.compare_data('assertNotIn', data_value, not_values)
        
    def is_instance(self, nested_keys, correct_value):
        self.compare('assertIsInstance', nested_keys, correct_value)
        
    def is_instance_data(self, data_value, correct_value):
        self.compare_data('assertIsInstance', data_value, correct_value)
        
    def is_not_instance(self, nested_keys, not_value):
        self.compare('assertNotIsInstance', nested_keys, not_value)
        
    def is_not_instance_data(self, data_value, not_value):
        self.compare_data('assertNotIsInstance', data_value, not_value)
        
    def is_true(self, nested_keys):
        self.compare('assertTrue', nested_keys)
        
    def is_true_data(self, data_value):
        self.compare_data('assertTrue', data_value)
        
    def is_false(self, nested_keys):
        self.compare('assertFalse', nested_keys)
        
    def is_false_data(self, data_value):
        self.compare_data('assertFalse', data_value)
        
    def is_none(self, nested_keys):
        self.compare('assertIsNone', nested_keys)
        
    def is_none_data(self, data_value):
        self.compare_data('assertIsNone', data_value)
        
    def is_not_none(self, nested_keys):
        self.compare('assertIsNotNone', nested_keys)
        
    def is_not_none_data(self, data_value):
        self.compare_data('assertIsNotNone', data_value)
    
    def is_empty(self, nested_keys):
        self.compare('assertIsEmpty', nested_keys)
        
    def is_empty_data(self, data_value):
        self.compare_data('assertIsEmpty', data_value)
            
    def is_not_empty(self, nested_keys):
        self.compare('assertIsNotEmpty', nested_keys)
        
    def is_not_empty_data(self, data_value):
        self.compare_data('assertIsNotEmpty', data_value)
        
    def is_int(self, nested_keys):
        self.compare('assertInteger', nested_keys)
        
    def is_int_data(self, data_value):
        self.compare_data('assertInteger', data_value)
        
    def is_float(self, nested_keys):
        self.compare('assertFloat', nested_keys)
        
    def is_float_data(self, data_value):
        self.compare_data('assertFloat', data_value)
        
    def is_max(self, nested_keys, maximum_value):
        self.compare('assertLessThanEqual', nested_keys, maximum_value)
        
    def is_max_data(self, data_value, maximum_value):
        self.compare_data('assertLessThanEqual', data_value, maximum_value)
        
    def is_below(self, nested_keys, excluded_value):
        self.compare('assertLessThan', nested_keys, excluded_value)
        
    def is_below_data(self, data_value, excluded_value):
        self.compare_data('assertLessThan', data_value, excluded_value)
        
    def between(self, nested_keys, correct_values):
        self.compare('assertBetween', nested_keys, correct_values)
        
    def between_data(self, data_value, correct_values):
        self.compare_data('assertBetween', data_value, correct_values)
    
    def is_min(self, nested_keys, minimum_value):
        self.compare('assertGreaterThanEqual', nested_keys, minimum_value)
        
    def is_min_data(self, data_value, minimum_value):
        self.compare_data('assertGreaterThanEqual', data_value, minimum_value)
        
    def is_above(self, nested_keys, excluded_value):
        self.compare('assertGreaterThan', nested_keys, excluded_value)
        
    def is_above_data(self, data_value, excluded_value):
        self.compare_data('assertGreaterThan', data_value, excluded_value)
    
    def contains(self, nested_keys, substring):
        self.compare('assertStrContains', nested_keys, substring)
        
    def contains_data(self, data_value, substring):
        self.compare_data('assertStrContains', data_value, substring)
        
    def matches(self, nested_keys, pattern):
        self.compare('assertMatch', nested_keys, pattern)
        
    def matches_data(self, data_value, pattern):
        self.compare_data('assertMatch', data_value, pattern)
        
    def startswith(self, nested_keys, text):
        self.matches(nested_keys, "^{}".format(re.escape(text)))
        
    def startswith_data(self, data_value, text):
        self.matches_data(data_value, "^{}".format(re.escape(text)))
        
    def endswith(self, nested_keys, text):
        self.matches(nested_keys, "{}$".format(re.escape(text)))
        
    def endswith_data(self, data_value, text):
        self.matches_data(data_value, "{}$".format(re.escape(text)))
        
    def icontains(self, nested_keys, substring):
        self.compare('assertIStrContains', nested_keys, substring)
        
    def icontains_data(self, data_value, substring):
        self.compare_data('assertIStrContains', data_value, substring)
        
    def imatches(self, nested_keys, pattern):
        self.compare('assertIMatch', nested_keys, pattern)
        
    def imatches_data(self, data_value, pattern):
        self.compare_data('assertIMatch', data_value, pattern)
        
    def istartswith(self, nested_keys, text):
        self.imatches(nested_keys, "^{}".format(re.escape(text)))
        
    def istartswith_data(self, data_value, text):
        self.imatches_data(data_value, "^{}".format(re.escape(text)))
        
    def iendswith(self, nested_keys, text):
        self.imatches(nested_keys, "{}$".format(re.escape(text)))
        
    def iendswith_data(self, data_value, text):
        self.imatches_data(data_value, "{}$".format(re.escape(text)))
        
    def iequal(self, nested_keys, text):
        self.imatches(nested_keys, "^{}$".format(re.escape(text)))
        
    def iequal_data(self, data_value, text):
        self.imatches_data(data_value, "^{}$".format(re.escape(text)))
    
    def is_year(self, nested_keys, year):
        self.compare('assertYear', nested_keys, year)
        
    def is_year_data(self, data_value, year):
        self.compare_data('assertYear', data_value, year)
            
    def is_month(self, nested_keys, month):
        self.compare('assertMonth', nested_keys, month)
        
    def is_month_data(self, data_value, month):
        self.compare_data('assertMonth', data_value, month)
        
    def is_day(self, nested_keys, day):
        self.compare('assertDay', nested_keys, day)
        
    def is_day_data(self, data_value, day):
        self.compare_data('assertDay', resp_value, day)
        
    def is_week(self, nested_keys, week):
        self.compare('assertWeek', nested_keys, week)
        
    def is_week_data(self, data_value, week):
        self.compare_data('assertWeek', data_value, week)
    
    def is_week_day(self, nested_keys, week_day):
        self.compare('assertWeekDay', nested_keys, week_day)
        
    def is_week_day_data(self, data_value, week_day):
        self.compare_data('assertWeekDay', data_value, week_day)
    
    def is_quarter(self, nested_keys, quarter):
        self.compare('assertQuarter', nested_keys, quarter)
        
    def is_quarter_data(self, data_value, quarter):
        self.compare_data('assertQuarter', data_value, quarter)
    

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
    
    def get_data(self):
        return self.resp.data
    
        
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

            
    def map(self, validator, base_key, lookup_keys, value, **params):
        lookup_keys = normalize_list(lookup_keys)
        data_pool = self.get_data_value(base_key)
        success = False
        
        if isinstance(data_pool, (list, QuerySet)):
            for index, element in enumerate(list(data_pool)):
                if self.map(validator, (base_key + [index]), lookup_keys, value, inner=True):
                    success = True
        
        elif isinstance(data_pool, dict):
            value_key = base_key + [lookup_keys[0]]
            
            if len(lookup_keys) == 1:
                if self.check(validator, value_key, value):
                    success = True
            else:
                if self.map(validator, value_key, lookup_keys[1:], value, inner=True):
                    success = True
        
        if not 'inner' in params and not success:
            raise self._wrap_error(AssertionError("Value ({}) {} {} keys {}".format(value, validator, base_key, lookup_keys)))
                
        return success
