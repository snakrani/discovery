
import copy
import json


def add_naics_tests(schema, code, option_count, enabled, displayed = True):
    schema['n1|#naics-code'] = ('value__equal', code)
    schema['n2|#naics-code option'] = ('count', option_count)
    schema['n3|#naics-code'] = 'enabled' if enabled else 'disabled'
    schema['n4|#naics-code'] = 'displayed' if displayed else 'not_displayed'

def add_vehicle_tests(schema, id, option_count, enabled, displayed = True):
    schema['v1|#vehicle-id'] = ('value__equal', id)
    schema['v2|#vehicle-id option'] = ('count', option_count)
    schema['v3|#vehicle-id'] = 'enabled' if enabled else 'disabled'
    schema['v4|#vehicle-id'] = 'displayed' if displayed else 'not_displayed'

def add_pool_tests(schema, id, option_count, display_count, enabled, displayed = True):
    schema['p1|#pool-id'] = ('value__equal', id)
    schema['p2|#pool-id option'] = ('count', option_count)
    schema['p3|#pool-id'] = 'enabled' if enabled else 'disabled'
    schema['p4|#pool-id'] = 'displayed' if displayed else 'not_displayed'
    schema['p5|div.pool'] = ('count', display_count)

def add_zone_tests(schema, id, option_count, enabled, displayed = True):
    schema['z1|#zone-id'] = ('value__equal', id)
    schema['z2|#zone-id option'] = ('count', option_count)
    schema['z3|#zone-id'] = 'enabled' if enabled else 'disabled'
    schema['z4|#zone-id'] = 'displayed' if displayed else 'not_displayed'

def add_filter_tests(schema, values, selection_count, enabled, displayed = True):
    if values:
        values = values if isinstance(values, (list, tuple)) else [values]
        
        if selection_count == len(values):
            comparison = 'value__all'
        else:
            comparison = 'value__any'
        
        schema['s1|#setaside-filters input:checked'] = (comparison, values)
        
    schema['s2|#setaside-filters input:checked'] = ('count', selection_count)
    schema['s3|#setaside-filters'] = 'enabled' if enabled else 'disabled'
    schema['s4|#setaside-filters'] = 'displayed' if displayed else 'not_displayed'

def add_result_info_tests(schema, result_count, csv_path):
    schema['r1|#download_data_results'] = ('link__equal', "http://localhost:8080/{}".format(csv_path))
    schema['r2|span.matching_your_search'] = ('text__equal', "{} vendors match your search".format(result_count))

def add_table_tests(schema, result_count, sort_field, sort_direction, pagination_current = None, pagination_last_page = None):
    direction = 'arrow-up' if sort_direction == 'asc' else 'arrow-down'
    
    schema['t1|tr.table_row_data'] = ('count', result_count)
    schema["t2|th.{}".format(sort_field)] = ('has_class', direction)
    
    if pagination_current:
        schema['t3|#pagination_container .current'] = ('text__all', pagination_current);
        
        if pagination_last_page:
            schema['t4|#pagination_container li'] = ('text__any', pagination_last_page)
    else:
        schema['t5|#pagination_container'] = 'not_displayed'


def generate_test(config):
    schema = {}
    
    config = copy.deepcopy(config)
    
    if 'params' in config:
        schema['params'] = config.pop('params')
    
    if 'wait' in config:
        schema['wait'] = config.pop('wait')
    else:
        schema['wait'] = ('text', '#site_status', 'complete')
        
    if 'naics' in config:
        add_naics_tests(schema, *config.pop('naics'))
        
    if 'vehicle' in config:
        add_vehicle_tests(schema, *config.pop('vehicle'))
        
    if 'pool' in config:
        add_pool_tests(schema, *config.pop('pool'))
        
    if 'zone' in config:
        add_zone_tests(schema, *config.pop('zone'))
        
    if 'filters' in config:
        add_filter_tests(schema, *config.pop('filters'))
        
    if 'results' in config:
        add_result_info_tests(schema, *config.pop('results'))
        
    if 'table' in config:
        add_table_tests(schema, *config.pop('table'))
    
    for name, test_config in config.items():
        if name != 'action':
            schema[name] = test_config
        
    return schema

def generate_action_test(config):
    schema = {'wait': ('text', '#site_status', 'complete')}
    
    def add_actions(actions, params, config, index = 1):
        if not isinstance(actions[0], (list, tuple)):
            actions = [actions]
        else:
            actions = list(actions)
        
        action = actions.pop(0)
        schema = {}
        
        filter_selector = action[0]
        filter_event = action[1]
        event_name = "{}<>{}".format(filter_selector, filter_event)
            
        if len(action) == 3:
            schema['wait'] = action[2]
        else:
            schema['wait'] = ('text', '#site_status', 'complete')
        
        if len(actions) > 0:
            schema[event_name] = {}
            schema[event_name]['actions'] = add_actions(actions, params, config, (index + 1))
        else:
            schema[event_name] = generate_test(config)
            
            if 'wait' not in config:
                schema[event_name]['wait'] = ('text', '#site_status', 'complete')
        
        return schema
    
    params = config.pop('params', {})
        
    if 'action' in config:
        schema['actions'] = add_actions(config.pop('action'), params, config)
    
    return schema


def generate_action_tests(schema, name, config):
    if 'params' in config:
        schema["filter_{}_url".format(name)] = generate_test(config)
    
    if 'action' in config:
        schema["filter_{}_action".format(name)] = generate_action_test(config)


def generate_schema(config):
    schema = {}
        
    if 'includes' in config:
        included_tests = config.pop('includes')
        for name, included_config in included_tests.items():
            for test_name, test_config in included_config.items():
                if test_name == 'actions':
                    if not 'actions' in config:
                        config['actions'] = {}
                
                    for action_name, action_config in test_config.items():
                        config['actions'][action_name] = action_config
                else:
                    config[test_name] = test_config
    
    if 'actions' in config:
        action_tests = config.pop('actions')
        for name, action_config in action_tests.items():
            generate_action_tests(schema, name, action_config)
            
    for name, test_config in config.items():
        schema[name] = test_config             
    
    return schema
