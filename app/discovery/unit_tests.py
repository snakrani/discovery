from django.conf import settings
from django.db.models.query import QuerySet
from django.test import Client, TestCase

from discovery import fixtures as data

from urllib.parse import urlencode, quote

import re


ASSERTION_MAP = {
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
    'date': 'equal',
    'year': 'equal',
    'month': 'equal',
    'day': 'equal',
    'week': 'equal',
    'week_day': 'equal',
    'quarter': 'equal',
    'range': 'between',
    'lt': 'is_below',
    'lte': 'is_max', 
    'gt': 'is_above', 
    'gte': 'is_min',
}


def normalize_list(input_value):
    if isinstance(input_value, (str, int, float)):
        return [input_value]
    elif isinstance(input_value, tuple):
        return list(input_value)
    return input_value


def get_nested_value(data, keys):
    
    def _nested_value(data, keys):
        try:
            if keys and data:
                element = keys[0]
                
                if element is not None:
                    if isinstance(data, dict):
                        value = data.get(element)
                    elif isinstance(data, list):
                        value = data[element]
                    
                    return value if len(keys) == 1 else _nested_value(value, keys[1:])
    
        except Exception as error:
            pass
    
        return None

    return _nested_value(data, normalize_list(keys))


class ResponseValidator(object):
    
    resp = None
    test = None
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
    
    def compare_data(self, op, data_value, correct_value = None, **params):
        try:
            if correct_value is not None:
                getattr(self.test, op)(data_value, correct_value, **params)
            else:
                getattr(self.test, op)(data_value, **params)
                
        except Exception as error:
            raise self._wrap_error(error)
    
    
    def compare(self, op, resp_value, correct_value = None, **params):
        if isinstance(resp_value, (str, list)):
            data_value = get_nested_value(self.resp.data, resp_value)
        else:
            data_value = resp_value
                
        self.compare_data(op, data_value, correct_value, **params)
    
    
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
    
        
    def includes(self, resp_value, items, validator = None):
        self.compare('assertIncludes', resp_value, items, resp = self, validator = validator)

        
    # Count
    
    def count(self, correct_value):
        self.equal('count', correct_value)
        
    def countMax(self, maximum_value):
        self.is_max('count', maximum_value)
        
    def countMin(self, minimum_value):
        self.is_min('count', minimum_value)
        
    
    # Ordering
    
    def validate_ordering(self, resp_value, dir = 'asc'):
        prev_value = None
        
        if not dir in ['asc', 'desc']:
            raise Exception("Ordering direction ({}) not supported".format(dir))
        
        for i in range(0, len(self.resp.data['results']) - 1):
            data_value = get_nested_value(self.resp.data['results'][i], resp_value)
            
            if isinstance(data_value, str):
                data_value = data_value.lower()
            
            if i > 0:
                if dir == 'asc':
                    if data_value < prev_value:
                        raise self._wrap_error(AssertionError("Data value ({}) is less than previous ({}) - Expected greater or equal".format(data_value, prev_value)))
                else:
                    if data_value > prev_value:
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



class DiscoveryAssertions(object):
   
    def assertIsEmpty(self, value, **params):
        if isinstance(value, QuerySet):
            value = list(value)
        
        if not isinstance(value, (str, list, dict)):
            raise AssertionError("Value passed ({}) is not a string, list, or dictionary value".format(str(value)))
        
        if (isinstance(value, (str, list)) and len(value) > 0) or (isinstance(value, dict) and len(value.keys()) > 0):
            raise AssertionError("Value should be empty")
                
    
    def assertIsNotEmpty(self, value, **params):
        if isinstance(value, QuerySet):
            value = list(value)
            
        if not isinstance(value, (str, list, dict)):
            raise AssertionError("Value passed ({}) is not a string, list, or dictionary value".format(str(value)))
        
        if (isinstance(value, (str, list)) and len(value) == 0) or (isinstance(value, dict) and len(value.keys()) == 0):
            raise AssertionError("Value should not be empty")
    
    
    def _check_int(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False
    
    def _check_float(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False
              
    def assertInteger(self, number, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_int(number):
            raise AssertionError("Value ({}) given is not an integer value".format(number))
             
    def assertFloat(self, number, **params):
        if not number:
            raise AssertionError("Value must be passed as a decimal or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not an decimal value".format(number))

              
    def assertLessThanEqual(self, number, maximum_value, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) > float(maximum_value):
            raise AssertionError("Value ({}) given is greater than the maximum allowed ({})".format(number, maximum_value))
        
    def assertLessThan(self, number, excluded_value, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) >= float(excluded_value):
            raise AssertionError("Value ({}) given is not less than ({})".format(number, excluded_value))
              
    def assertGreaterThanEqual(self, number, minimum_value, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) < float(minimum_value):
            raise AssertionError("Value ({}) given is less than the minimum allowed ({})".format(number, minimum_value))
        
    def assertGreaterThan(self, number, excluded_value, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) <= float(excluded_value):
            raise AssertionError("Value ({}) given is not greater than ({})".format(number, excluded_value))
   
    def assertBetween(self, number, correct_values, **params):
        if isinstance(correct_values, str): 
            if ',' in correct_values:
                components = correct_values.split(',')
                minimum_value = components[0]
                maximum_value = components[1]
            else:
                AssertionError("Betwen needs multiple values, one ({}) given".format(correct_values))
        else:
            minimum_value = correct_values[0]
            maximum_value = correct_values[1]
        
        self.assertGreaterThanEqual(number, minimum_value)    
        self.assertLessThanEqual(number, maximum_value)


    def assertStrContains(self, value, substring, **params):
        if not value or not isinstance(value, str):
            raise AssertionError("Value must be passed as an alpha-numeric string")
        
        if value.find(substring) == -1:
            raise AssertionError("Value ({}) given does not contain {}".format(value, substring))
        
    def assertIStrContains(self, value, substring, **params):
        if not value or not isinstance(value, str):
            raise AssertionError("Value must be passed as an alpha-numeric string")
        
        if value.lower().find(substring.lower()) == -1:
            raise AssertionError("Value ({}) given does not contain {}".format(value, substring))
    
    
    def assertMatch(self, value, pattern, **params):
        if not value or not isinstance(value, str):
            raise AssertionError("Value must be passed as a alpha-numeric string")
        
        if not re.search(pattern, value):
            raise AssertionError("Value ({}) given does not match pattern {}".format(value, pattern))
        
    def assertIMatch(self, value, pattern, **params):
        if not value or not isinstance(value, str):
            raise AssertionError("Value must be passed as a alpha-numeric string")
        
        if not re.search(pattern, value, re.IGNORECASE):
            raise AssertionError("Value ({}) given does not match pattern {}".format(value, pattern))
    
    
    def assertIncludes(self, value, items, **params):
        failed = True
        
        resp = params['resp']
        validator = params['validator']
        
        if isinstance(value, QuerySet):
            value = list(value)
            
        if not value or not isinstance(value, (list, dict)):
            raise AssertionError("Value must be passed as a list or dictionary")
        
        
        def _check_value(data, keys, item):
            try:
                getattr(resp, "{}_data".format(validator))(get_nested_value(data, keys), item)
                return True
            
            except Exception:
                return None        
        
        if isinstance(items, dict):
            keys = next(iter(items))
            items = items[keys]
            
            keys = keys.split('|') if '|' in keys else [keys]
            items = normalize_list(items)
            
            for item in items:
                if isinstance(value, list):
                    for element in value:
                        if _check_value(element, keys, item):
                            failed = False
                else:
                    if _check_value(value, keys, item):
                        failed = False
                
        else:
            if isinstance(items, (str, int, float)):
                items = [items]
        
            for item in items:
                if (isinstance(value, list) and item in value) or (isinstance(value, dict) and value.get(item, None)):
                    failed = False
        
        if failed:    
            raise AssertionError("Value passed ({}) does not include item ({})".format(str(value), item))
    

class DiscoveryAPITestCase(TestCase, DiscoveryAssertions):
    
    client = None
    path = None
    router = None
    
    
    # Initialization
    
    def setUp(self):
        self.client = Client()
        self.initialize()
        
        if self.router:
            self.router = self.router.lower()
        
        if not self.path and self.router:
            self.path = "/api/{}/".format(self.router)
    
        
    def initialize(self):
        # Override in subclass
        pass

    
    # Request
    
    def encode(self, params):
        return urlencode(params)
    
    def encode_str(self, string):
        return quote(string)
    
    def _get_object_path(self, id):
        return self.path + str(id)
    
    def _get_object_url(self, id, params = {}):
        return "{}{}?{}".format(settings.API_HOST, self._get_object_path(id), self.encode(params))
    
    def _get_list_url(self, params = {}):
        return "{}{}?{}".format(settings.API_HOST, self.path, self.encode(params))
    
    
    def fetch_object(self, id, **params):
        return ResponseValidator(
            self.client.get(self._get_object_path(id), params), 
            self, 
            self._get_object_url(id, params)
        )
    
    def fetch_objects(self, **params):
        return ResponseValidator(
            self.client.get(self.path, params), 
            self, 
            self._get_list_url(params)
        )

    
    # Validation
    
    def validated_list(self, list_count = None, **params):
        resp = self.fetch_objects(**params)
        resp.success()
        
        if list_count is not None:
            resp.count(list_count)
        else:
            resp.countMin(1)
        resp.validate_list()
        return resp
    
    def validated_single_list(self, **params):
        return self.validated_list(1, **params)
    
    def validated_multi_list(self, **params):
        return self.validated_list(None, **params)
    
    def empty_list(self, **params):
        resp = self.fetch_objects(**params)
        resp.success()
        resp.count(0)
        return resp
    
    def invalid_list(self, **params):
        resp = self.fetch_objects(**params)
        resp.not_found()
        return resp
    
    def validated_object(self, id, **params):
        resp = self.fetch_object(id, **params)
        resp.success()
        resp.validate_object()
        return resp

    def invalid_object(self, id, **params):
        resp = self.fetch_object(id, **params)
        resp.not_found()
        return resp
    
    
    def validate_object(self, resp, base_key = []):
        # Override in subclass
        pass

    
    # Testing
    
    def test_schema(self):
        schema = self.schema()
        object = schema.get('object', None)
        
        if object:
            self._test_schema_object(object)
        else:
            with self.subTest(all = "schema"):
                self.validated_multi_list()
            
            self._test_schema_ordering(schema.get('ordering', None))
            self._test_schema_pagination(schema.get('pagination', None))
            self._test_schema_search(schema.get('search', None))
            self._test_schema_fields(schema.get('fields', None))
    
    
    def _test_schema_ordering(self, ordering):
        if ordering:
            for field in normalize_list(ordering):
                with self.subTest(ordering = "{} [asc]".format(field)):
                    resp = self.validated_multi_list(ordering = field)
                    resp.validate_ordering(field, 'asc')
                    
                with self.subTest(ordering = "{} [desc]".format(field)):
                    resp = self.validated_multi_list(ordering = "-{}".format(field))
                    resp.validate_ordering(field, 'desc')                
    
    
    def _test_schema_pagination(self, pagination):
        if pagination:
            for name, params in pagination.items():
                validation = self._validation_info(name, '@')
                
                page = params.get('page', None)
                count = params.get('count', None)
                
                with self.subTest(pagination = "{} [{}]".format(validation['lookup'], validation['type'])):
                    page_options = {}
                    
                    if page:
                        page_options['page'] = page
                    if count:
                        page_options['count'] = count
                        
                    page = 1 if page is None else page   
                    resp = getattr(self, validation['method'])(**page_options)
                    
                    if self._check_valid(validation):
                        resp.validate_pagination(page, count)
    
    
    def _test_schema_search(self, search):
        if search:
            for name, params in search.items():
                validation = self._validation_info(name, '@')
                
                field = params[0]
                validator = params[1]
                search_value = params[2]
                
                with self.subTest(search = "{} [{}]".format(validation['lookup'], validation['type'])):
                    resp = getattr(self, validation['method'])(**{'q': search_value})
                    
                    if self._check_valid(validation):
                        resp.validate(lambda resp, base_key: getattr(resp, validator)(base_key + [field], search_value))
     
        
    def _test_schema_fields(self, fields):   
        if fields:
            for field, lookups in fields.items():
                field_info = self._field_info(field)
                
                for lookup, params in lookups.items():
                    params = normalize_list(params)
                    
                    validation = self._validation_info(lookup, '@')
                    validator = ASSERTION_MAP[validation['lookup']]
                    
                    field_lookup = field if validation['lookup'] == 'exact' else "{}__{}".format(field, validation['lookup'])
                    search_value = params[0]
                        
                    if not search_value:
                        raise Exception("Search value (string/integer) must be first parameter to lookup")
                        
                    check_value = params[1] if len(params) > 1 else search_value
                        
                    with self.subTest(field = "{} [{}]".format(field_lookup, validation['type'])):
                        if field_info['relation']:
                            resp = getattr(self, validation['method'])(**{"{}".format(field_lookup): search_value})
                            
                            if self._check_valid(validation):
                                resp.validate(lambda resp, base_key: resp.includes((base_key + [field_info['base_field']]), {"{}".format(field_info['relation']): search_value}, validator))         
                        else:                    
                            resp = getattr(self, validation['method'])(**{"{}".format(field_lookup): search_value})
                            
                            if self._check_valid(validation):
                                resp.validate(lambda resp, base_key: getattr(resp, validator)(base_key + [field], check_value))
    
    
    def _test_schema_object(self, object):
        if object:
            for id, params in object.items():
                validation = self._validation_info(id, '&')
                
                with self.subTest(object = "{} [{}]".format(validation['lookup'], validation['type'])):
                    resp = getattr(self, validation['method'])(validation['lookup'])
                    
                    if self._check_valid(validation) and len(params) == 3:
                        field = params[0]
                        validator = params[1]
                        search_value = params[2]
                    
                        getattr(resp, validator)(field, search_value)
                
    
    def schema(self):
        # Override in subclass
        return {}

     
    def _field_info(self, field):
        if field.find('__') != -1:
            components = field.split('__')
            
            base_field = components[0]
            relation = components[1]
        else:
            base_field = field
            relation = None
            
        return { 'base_field': base_field, 'relation': relation }

    
    def _validation_info(self, lookup, default_type = '@'):
        count_specifier = default_type
                    
        if re.search('^[\-\*\@\!\&\#]', lookup):
            count_specifier = lookup[0]
            lookup = lookup[1:]
            
        if count_specifier == '*':
            validation_method = 'validated_single_list'
        elif count_specifier == '-':
            validation_method = 'empty_list'
        elif count_specifier == '!':
            validation_method = 'invalid_list'
        elif count_specifier == '&':
            validation_method = 'validated_object'
        elif count_specifier == '#':
            validation_method = 'invalid_object'
        else:
            validation_method = 'validated_multi_list'
        
        return { 'lookup': lookup, 'method': validation_method, 'type': count_specifier }
    
    
    def _check_valid(self, validation_info):
        if not re.search('^[\-\!\#]', validation_info['type']):
            return True
        return False
    

class CategoryAPITestCase(DiscoveryAPITestCase):
    fixtures = data.get_category_fixtures()


class VendorAPITestCase(DiscoveryAPITestCase):
    fixtures = data.get_vendor_fixtures()
     