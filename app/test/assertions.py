from datetime import datetime
from django.db.models.query import QuerySet

from test.common import normalize_list, get_nested_value

import re
import math


class TestAssertions(object):
   
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
        if number is None:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_int(number):
            raise AssertionError("Value ({}) given is not an integer value".format(number))
             
    def assertFloat(self, number, **params):
        if number is None:
            raise AssertionError("Value must be passed as a decimal or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not an decimal value".format(number))

              
    def assertLessThanEqual(self, number, maximum_value, **params):
        if number is None:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) > float(maximum_value):
            raise AssertionError("Value ({}) given is greater than the maximum allowed ({})".format(number, maximum_value))
        
    def assertLessThan(self, number, excluded_value, **params):
        if number is None:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) >= float(excluded_value):
            raise AssertionError("Value ({}) given is not less than ({})".format(number, excluded_value))
              
    def assertGreaterThanEqual(self, number, minimum_value, **params):
        if number is None:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) < float(minimum_value):
            raise AssertionError("Value ({}) given is less than the minimum allowed ({})".format(number, minimum_value))
        
    def assertGreaterThan(self, number, excluded_value, **params):
        if number is None:
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
    
    
    def _convert_date(self, date):
        if not date or not isinstance(date, str) or not re.search('^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$', date):
            raise AssertionError("Value ({}) must be passed as a date string".format(date))
        
        try:
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        
        except Exception as e:
            date = datetime.strptime(date, '%Y-%m-%d')
        
        return date        
        
        
    def assertYear(self, date, year, **params):
        date = self._convert_date(date)
        
        if date.year != int(year):
            raise AssertionError("Value ({}) given does not match year {}".format(year, date.year))
        
    def assertMonth(self, date, month, **params):
        date = self._convert_date(date)
        
        if date.month != int(month):
            raise AssertionError("Value ({}) given does not match month {}".format(month, date.month))
        
    def assertDay(self, date, day, **params):
        date = self._convert_date(date)
        
        if date.day != int(day):
            raise AssertionError("Value ({}) given does not match day {}".format(day, date.day))
        
    def assertWeek(self, date, week, **params):
        date = self._convert_date(date)
        date_week = date.isocalendar()[1]
        
        if date_week != int(week):
            raise AssertionError("Value ({}) given does not match week {}".format(week, date_week))
        
    def assertWeekDay(self, date, week_day, **params):
        date = self._convert_date(date)
        date_week_day = max((date.isoweekday() + 1) % 8, 1)
        
        if date_week_day != int(week_day):
            raise AssertionError("Value ({}) given does not match week day {}".format(week_day, date_week_day))
        
    def assertQuarter(self, date, quarter, **params):
        date = self._convert_date(date)
        date_quarter = math.ceil(date.month / 3)
        
        if date_quarter != int(quarter):
            raise AssertionError("Value ({}) given does not match quarter {}".format(quarter, date_quarter))
