from django.conf import settings
from django.db.models.query import QuerySet

from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from test.common import normalize_list, get_nested_value

import re
import time


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
            
            if isinstance(data_value, (list, tuple, QuerySet)):
                success = False
                
                for index, data_element in enumerate(list(data_value)):
                    try:
                        _compare(op, data_element, value, **params)
                        success = True
                    
                    except AssertionError as error:
                        pass
                    
                if not success:
                    raise self._wrap_error(AssertionError("No items in value: ({}) {} ({})".format(data_value, op, value))) 
            
            elif data_value is not None:
                _compare(op, data_value, value, **params)
                
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
    
    def all(self, nested_keys, values):
        self.compare('assertAll', nested_keys, values)
        
    def all_data(self, data_values, values):
        self.compare_data('assertAll', data_values, values)
    
    def any(self, nested_keys, values):
        self.compare('assertAny', nested_keys, values)
        
    def any_data(self, data_values, values):
        self.compare_data('assertAny', data_values, values)
    
    def none(self, nested_keys, values):
        self.compare('assertNone', nested_keys, values)
        
    def none_data(self, data_values, values):
        self.compare_data('assertNone', data_values, values)


class ResponseValidator(BaseValidator):
    
    resp = None
    url  = ''

   
    def __init__(self, response, test_case, url):
        super(ResponseValidator, self).__init__(test_case)
        
        self.resp = response
        self.url = url

    
    # Utilities
    
    def _wrap_error(self, error):
        if self.url:
            error.args = ("{}\nRequestURL: {}".format(error.args[0], self.url),)
            
        raise error
    

    # Status
    
    def check_status(self, status):
        try:
            self.test.assertEqual(self.resp.status_code, status)
        
        except Exception as error:
            raise self._wrap_error(error)
        
    def success(self):
        self.check_status(200)
        
    def perm_redirect(self):
        self.check_status(301)
        
    def temp_redirect(self):
        self.check_status(302)
        
    def failure(self):
        self.check_status(400)
        
    def not_found(self):
        self.check_status(404)
        
        
    # Data
    
    def get_data(self):
        return self.resp.data
       

class APIResponseValidator(ResponseValidator):
        
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


class AcceptanceResponseValidator(BaseValidator):
    
    def __init__(self, driver, test_case, url):
        super(AcceptanceResponseValidator, self).__init__(test_case)
        
        self.driver = driver
        self.url = url
        self.locator = ''
    
        
    def __getattr__(self, name):
        def method(*args):
            components = name.split('__')
            
            if len(components) > 1 and hasattr(self, components[0]) and hasattr(self, components[1]):
                method = components[0]
                op = components[1]
                
                if args:
                    args = [op] + list(args)
                else:
                    args = [op]
                
                getattr(self, method)(*args)
            else:
                raise AttributeError("Trying to access a nonexistent method: {}".format(name))
        
        return method
    
    
    # Utilities
    
    def _wrap_error(self, error):
        if self.url:
            error.args = ("{}\nLocator: {}\nRequestURL: {}".format(error.args[0], self.locator, self.url),)
            
        raise error
    
    
    # Locators
  
    def _name(self, name):
        return (By.NAME, name)
    
    def _tag(self, name):
        return (By.TAG_NAME, name)
    
    def _id(self, path):
        return (By.ID, path)
    
    def _class(self, name):
        return (By.CLASS_NAME, name)
    
    def _xpath(self, path):
        return (By.XPATH, path)
    
    def _selector(self, name):
        return (By.CSS_SELECTOR, name)
    
    
    # Wait
    
    def default_wait(self):
        return 30
    
    
    def wait(self, test_condition):
        WebDriverWait(self.driver, self.default_wait()).until(test_condition)
        
    def wait_for(self, condition_function, vars = {}):
        start_time = time.time()
        cutoff_time = start_time + self.default_wait()
        
        while time.time() < cutoff_time:
            if condition_function(vars):
                return True
            else:
                time.sleep(0.1)
        
        raise self._wrap_error(Exception(
            'Timeout waiting for {}'.format(condition_function.__name__)
        ))
        
    
    def wait_for_name(self, name, text = None):
        if text is None:
            self.wait(EC.presence_of_all_elements_located(self._name(name)))
        else:
            self.wait(EC.text_to_be_present_in_element(self._name(name), text))
    
    def wait_for_tag(self, name, text = None):
        if text is None:
            self.wait(EC.presence_of_all_elements_located(self._tag(name)))
        else:
            self.wait(EC.text_to_be_present_in_element(self._tag(name), text))
    
    def wait_for_id(self, name, text = None):
        if text is None:
            self.wait(EC.presence_of_all_elements_located(self._id(name)))
        else:
            self.wait(EC.text_to_be_present_in_element(self._id(name), text)) 
        
    def wait_for_class(self, name, text = None):
        if text is None:
            self.wait(EC.presence_of_all_elements_located(self._class(name)))
        else:
            self.wait(EC.text_to_be_present_in_element(self._class(name), text))
     
    def wait_for_xpath(self, path, text = None):
        if text is None:
            self.wait(EC.presence_of_all_elements_located(self._xpath(path)))
        else:
            self.wait(EC.text_to_be_present_in_element(self._xpath(path), text))
            
    def wait_for_selector(self, name, text = None):
        if text is None:
            self.wait(EC.presence_of_all_elements_located(self._selector(name)))
        else:
            self.wait(EC.text_to_be_present_in_element(self._selector(name), text))
    
           
    def wait_for_enabled(self, elem, notused = None):
        def enabled(vars):
            try: 
                return self.element(elem).is_enabled()
            
            except StaleElementReferenceException: 
                return False
        
        self.wait_for(enabled)
           
    def wait_for_disabled(self, elem, notused = None):
        def disabled(vars):
            try: 
                return not self.element(elem).is_enabled()
            
            except StaleElementReferenceException: 
                return False
        
        self.wait_for(disabled)
            
    def wait_for_displayed(self, elem, notused = None):
        def displayed(vars):
            try: 
                return self.element(elem).is_displayed()
            
            except StaleElementReferenceException: 
                return False
        
        self.wait_for(displayed)
           
    def wait_for_not_displayed(self, elem, notused = None):
        def not_displayed(vars):
            try: 
                return not self.element(elem).is_displayed()
            
            except StaleElementReferenceException: 
                return False
        
        self.wait_for(not_displayed)
               
    def wait_for_nonempty(self, elem, notused = None):
        def nonempty(vars):
            try: 
                text = self.attr(elem, 'text')
                
                if text.strip():
                    return True
                else:
                    return False
            
            except StaleElementReferenceException: 
                return True
        
        self.wait_for(nonempty)
               
    def wait_for_text(self, elem, text = None):
        def elem_text(vars):
            try:
                local_text = self.attr(elem, 'text')
                
                if not text or local_text.strip() == text:
                    return True
                else:
                    return False
            
            except StaleElementReferenceException: 
                return False
        
        self.wait_for(elem_text)
        
    def wait_for_complete(self, notused = None, notused2 = None):
        self.wait_for_text('#site_status', 'complete')
        #time.sleep(0.5)
            
    def wait_for_stale(self, elem, notused = None):
        def stale(vars):
            try: 
                text = self.attr(elem, 'text')
            
            except StaleElementReferenceException: 
                return True
        
        self.wait_for(stale)
            
    def wait_for_change(self, elem, notused = None):
        vars = { 'last_text': None }
        
        def change(vars):
            try: 
                text = self.attr(elem, 'text')
                
                if vars['last_text'] is not None and text != vars['last_text']:
                    return True
                
                vars['last_text'] = text
                return False
            
            except StaleElementReferenceException: 
                return True
        
        self.wait_for(change, vars)
            
    def wait_for_has_class(self, elem, text = None):
        def no_class(vars):
            try:
                if not text or text in self.attr(elem, 'class'):
                    return True
                else:
                    return False
            
            except StaleElementReferenceException: 
                return False
        
        self.wait_for(no_class)
            
    def wait_for_no_class(self, elem, text = None):
        def no_class(vars):
            try:
                if not text or text not in self.attr(elem, 'class'):
                    return True
                else:
                    return False
            
            except StaleElementReferenceException: 
                return False
        
        self.wait_for(no_class)
                
    def wait_for_sec(self, sec, notused = None):
        time.sleep(sec)

        
    # Element access
    
    def _get_scope(self, scope = None):
        if scope is None:
            return self.driver 
        return scope
    
    def _get_element(self, elem, element_map):
        if isinstance(elem, str):
            components = elem.split('|')
            
            if len(components) > 1:
                components.pop(0)
                elem = "".join(components).strip()
            
            components = elem.split(':')
                        
            if len(components) > 1:
                if components[0] in element_map:
                    type = components[0]
                    param = ":".join(components[1:])
                else:
                    type = 'css'
                    param = ":".join(components)
            else:
                type = 'css'
                param = components[0]
            
            return element_map[type](param)
        else:
            return elem

        
    def element_wait(self, elem, scope = None):
        
        def by_css(selector):
            return self._selector(selector)
        
        def by_xpath(xpath):
            return self._xpath(xpath)
                
        return self._get_element(elem, {
            'css': by_css,
            'xpath': by_xpath
        })
        
          
    def element(self, elem, scope = None):
        
        def by_css(selector):
            return self._get_scope(scope).find_element_by_css_selector(selector)
        
        def by_xpath(xpath):
            return self._get_scope(scope).find_element_by_xpath(xpath)
        
        def by_link_text(text):
            return self._get_scope(scope).find_element_by_link_text(text)
                
        return self._get_element(elem, {
            'css': by_css,
            'xpath': by_xpath,
            'link_text': by_link_text
        })
    
    def elements(self, elems, scope = None):
        
        def by_css(selector):
            return self._get_scope(scope).find_elements_by_css_selector(selector)
        
        def by_xpath(xpath):
            return self._get_scope(scope).find_elements_by_xpath(xpath)
        
        def by_link_text(text):
            return self._get_scope(scope).find_elements_by_link_text(text)
                
        return self._get_element(elems, {
            'css': by_css,
            'xpath': by_xpath,
            'link_text': by_link_text
        })
        
        
    def attr(self, elem, name):
        if name == 'text':
            return self.element(elem).get_attribute('innerHTML')
        
        return self.element(elem).get_attribute(name)
        
    
    # Formatters
    
    def format_int(self, value):
        return int(value.replace(',', '').replace('$', ''))
    
    def format_float(self, value):
        return float(value.replace(',', '').replace('$', ''))
    
        
    # Events
    
    def execute(self, elem, event, value = None):
        
        def execute_select(elem, values):
            select = Select(elem)
            values = values if isinstance(values, (list, tuple)) else [values] 
            
            for value in values:
                select.select_by_value(value)
        
        try:        
            self.wait(EC.element_to_be_clickable(self.element_wait(elem)))
        
        except TimeoutException:
            pass
        
        if event == 'select' and value:
            execute_select(self.element(elem), value)
        else:
            getattr(self.element(elem), event)()
            
        #time.sleep(1)
    
    
    # Validation
        
    def compare_data(self, op, data_value, value = None, **params):
        
        def _compare(op, data_value, value, **params):
            if value is not None:
                getattr(self.test, op)(data_value, value, **params)
            else:
                getattr(self.test, op)(data_value, **params)
        
        try:
            if isinstance(value, (list, tuple, QuerySet)):
                value = list(value)
            
            if isinstance(data_value, (list, tuple, QuerySet)):
                _compare(op, list(data_value), value, **params)

            elif data_value is not None:
                _compare(op, data_value, value, **params)
                
        except Exception as error:
            raise self._wrap_error(error)
    
    def compare(self, op, data_value, value = None, **params):
        self.compare_data(op, data_value, value, **params)
    
      
    def title(self, text):
        self.equal(self.driver.title, text)


    def count(self, elems, count):
        self.equal(len(self.elements(elems)), count)
        
    def value__any(self, elems, values):
        selected_values = []
        
        for element in self.elements(elems):
            selected_values.append(self.attr(element, 'value'))
        
        self.any(selected_values, values)
        
    def value__all(self, elems, values):
        selected_values = []
        
        for element in self.elements(elems):
            selected_values.append(self.attr(element, 'value'))
        
        self.all(selected_values, values)
        
    def value__none(self, elems, values):
        selected_values = []
        
        for element in self.elements(elems):
            selected_values.append(self.attr(element, 'value'))
        
        self.none(selected_values, values)
       
    def text__any(self, elems, values):
        texts = []
        
        for element in self.elements(elems):
            texts.append(element.text)
        
        self.any(texts, values)
        
    def text__all(self, elems, values):
        texts = []
        
        for element in self.elements(elems):
            texts.append(element.text)
        
        self.all(texts, values)
        
    def text__none(self, elems, values):
        texts = []
        
        for element in self.elements(elems):
            texts.append(element.text)
        
        self.none(texts, values)

              
    def exists(self, elem):
        self.is_true(self.element(elem))
    
    def not_exists(self, elem):
        self.is_false(self.element(elem))
        
    def has_class(self, elem, class_name):
        self.is_true(class_name in self.attr(elem, 'class'))
        
    def no_class(self, elem, class_name):
        self.is_false(class_name in self.attr(elem, 'class'))
        
    def enabled(self, elem):
        self.is_true(self.element(elem).is_enabled())
        
    def disabled(self, elem):
        self.is_false(self.element(elem).is_enabled())
        
    def displayed(self, elem):
        self.is_true(self.element(elem).is_displayed())
        
    def not_displayed(self, elem):
        self.is_false(self.element(elem).is_displayed())
        
    def value(self, op, elem, text = None):
        if text is not None:
            getattr(self, op)(self.attr(elem, 'value'), text)
        else:
            getattr(self, op)(self.attr(elem, 'value'))
        
    def link(self, op, elem, url = None):
        if url is not None:
            getattr(self, op)(self.attr(elem, 'href'), url)
        else:
            getattr(self, op)(self.attr(elem, 'href'))
        
    def text(self, op, elem, text = None):
        if text is not None:
            match = re.match(r'^\s*\<\<(.+)\>\>\s*$', text)
            if match:
                text = self.element(match.group(1)).text
        
            getattr(self, op)(self.element(elem).text, text)
        else:
            getattr(self, op)(self.element(elem).text)
        
    def int(self, op, elem, num):
        if isinstance(num, str):
            match = re.match(r'^\s*\<\<(.+)\>\>\s*$', num)
            if match:
                num = self.format_int(self.element(match.group(1)).text)
        
        getattr(self, op)(self.format_int(self.element(elem).text), int(num))
        
    def float(self, op, elem, num):
        if isinstance(num, str):
            match = re.match(r'^\s*\<\<(.+)\>\>\s*$', num)
            if match:
                num = self.format_float(self.element(match.group(1)).text)
        
        getattr(self, op)(self.format_float(self.element(elem).text), float(num))
