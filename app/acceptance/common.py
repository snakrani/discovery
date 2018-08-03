from test.common import normalize_list

import copy
import json


def add_naics_tests(schema, code, option_count, enabled = True, displayed = True):
    schema['n1|#naics-code'] = ('value__equal', code)
    schema['n2|#naics-code option'] = ('count', option_count)
    schema['n3|#naics-code'] = 'enabled' if enabled else 'disabled'
    schema['n4|#naics-code'] = 'displayed' if displayed else 'not_displayed'


def add_vehicle_tests(schema, id, option_count, enabled = True, displayed = True):
    schema['v1|#vehicle-id'] = ('value__equal', id)
    schema['v2|#vehicle-id option'] = ('count', option_count)
    schema['v3|#vehicle-id'] = 'enabled' if enabled else 'disabled'
    schema['v4|#vehicle-id'] = 'displayed' if displayed else 'not_displayed'

def add_pool_tests(schema, ids, option_count, display_count, enabled = True, displayed = True):
    if isinstance(ids, (list, tuple)):
        schema['p1|#pool-id'] = ('select__all', ids)
    else:
        schema['p2|#pool-id'] = ('value__equal', ids)
    
    schema['p3|#pool-id option'] = ('count', option_count)
    schema['p4|#pool-id'] = 'enabled' if enabled else 'disabled'
    schema['p5|#pool-id'] = 'displayed' if displayed else 'not_displayed'
    schema['p6|div.pool'] = ('count', display_count)

def add_zone_tests(schema, ids, option_count, enabled = True, displayed = True):
    if isinstance(ids, (list, tuple)):
        schema['z1|#zone-id'] = ('select__all', ids)
    else:
        schema['z2|#zone-id'] = ('value__equal', ids)
    
    schema['z3|#zone-id option'] = ('count', option_count)
    schema['z4|#zone-id'] = 'enabled' if enabled else 'disabled'
    schema['z5|#zone-id'] = 'displayed' if displayed else 'not_displayed'

def add_setaside_filter_tests(schema, values, selection_count, enabled = True, displayed = True):
    if values:
        values = values if isinstance(values, (list, tuple)) else [values]
        
        if selection_count == len(values):
            comparison = 'value__all'
        else:
            comparison = 'value__any'
        
        schema['s1|#setaside-filters input:checked'] = (comparison, values)
        
    schema['s2|#setaside-filters input:checked'] = ('count', selection_count)
    schema['s3|.se_filter'] = 'enabled' if enabled else 'disabled'
    schema['s4|#setaside-filters'] = 'displayed' if displayed else 'not_displayed'

def add_vendor_result_info_tests(schema, result_count, csv_path):
    schema['r1|#download_data_results'] = ('link__equal', "http://localhost:8080/{}".format(csv_path))
    schema['r2|span.matching_your_search'] = ('text__equal', "{} vendors match your search".format(result_count))

def add_vendor_table_tests(schema, result_count, sort_field, sort_direction, pagination_current = None, pagination_last_page = None):
    direction = 'arrow-up' if sort_direction == 'asc' else 'arrow-down'
    
    schema['t1|tr.table_row_data'] = ('count', result_count)
    schema["t2|th.{}".format(sort_field)] = ('has_class', direction)
    
    if pagination_current:
        schema['t3|#pagination_container .current'] = ('text__all', pagination_current);
        
        if pagination_last_page:
            schema['t4|#pagination_container li'] = ('text__any', pagination_last_page)
    else:
        schema['t5|#pagination_container'] = 'not_displayed'


def add_membership_filter_tests(schema, values, option_count, selection_count, capability_statement_link_count, contacts = {}, setasides = {}):
    if values:
        values = values if isinstance(values, (list, tuple)) else [values]
        
        if selection_count == len(values):
            comparison = 'value__all'
        else:
            comparison = 'value__any'
        
        schema['m1|#contract_filters input:checked'] = (comparison, values)
    
    schema['m2|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr'] = ('count', (option_count + 1))
    schema['m3|#contract_filters input:checked'] = ('count', selection_count)
    schema['m4|div.capability_statement_link'] = ('count', capability_statement_link_count)
    
    for index, contact_info in contacts.items():
        schema['m5|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[3]'.format(index + 1)] = ('text__equal', contact_info[0])
        schema['m6|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[4]'.format(index + 1)] = ('text__equal', contact_info[1])
        schema['m7|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[5]'.format(index + 1)] = ('text__equal', contact_info[2])
     
    for index, setaside_names in setasides.items():   
        for name in setaside_names:
            if name == 'SB':
                schema['m8|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[6]/img'.format(index + 1)] = 'exists'
            elif name == 'SDB':
                schema['m9|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[7]/img'.format(index + 1)] = 'exists'
            elif name == '8(a)':
                schema['m10|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[8]/img'.format(index + 1)] = 'exists'
            elif name == '8(a) exp':
                schema['m11|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[9]'.format(index + 1)] = 'text__is_not_empty'
            elif name == 'HubZ':
                schema['m12|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[10]/img'.format(index + 1)] = 'exists'
            elif name == 'WO':
                schema['m13|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[11]/img'.format(index + 1)] = 'exists'
            elif name == 'VO':
                schema['m14|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[12]/img'.format(index + 1)] = 'exists'
            elif name == 'SDVO':
                schema['m15|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[13]/img'.format(index + 1)] = 'exists'
            elif name == 'VA VIP':
                schema['m16|xpath://*[@id="vendor_contract_filter_table"]/tbody/tr[{}]/td[14]/img'.format(index + 1)] = 'exists'

def add_vendor_sam_tests(schema, sam_expiration, expired_displayed = False, debarred_displayed = False):
    schema['s1|span.vendor_sam_expiration_date'] = ('text__equal', sam_expiration)
    schema['s2|span.vendor_sam_expiration_notice'] = 'displayed' if expired_displayed else 'not_displayed'
    schema['s3|div.debarred_status'] = 'displayed' if debarred_displayed else 'not_displayed'

def add_vendor_info_tests(schema, title, duns, cage, employees, revenue):
    schema['i1|div.vendor_title'] = ('text__equal', title)   
    schema['i2|span.duns_number'] = ('text__equal', duns)
    schema['i3|span.cage_code'] = ('text__equal', cage)
    schema['i4|span.number_of_employees'] = ('text__equal', employees)
    schema['i5|span.annual_revenue'] = ('text__equal', revenue)

def add_vendor_address_tests(schema, address_1, address_2, website = False):    
    schema['a1|span.vendor_address1'] = ('text__equal', address_1)
    schema['a2|span.vendor_address2'] = ('text__equal', address_2)
    schema['a3|#vendor_site_link'] = 'displayed' if website else 'not_displayed'

def add_vendor_badge_tests(schema, small_business = False):
    schema['b1|#sb_badge'] = 'displayed' if small_business else 'not_displayed'

def add_contract_result_info_tests(schema, csv_path):
    schema['r1|#download_data'] = ('link__equal', "http://localhost:8080/{}".format(csv_path))
    
def add_contract_table_tests(schema, result_count, sort_field, sort_direction, pagination_current = None, pagination_last_page = None):
    direction = 'arrow-up' if sort_direction == 'asc' else 'arrow-down'
    
    schema['t1|tr.table_row_data'] = ('count', result_count)
    schema["t2|th.{}".format(sort_field)] = ('has_class', direction)
    
    if pagination_current:
        schema['t3|#pagination_container .current'] = ('text__all', pagination_current);
        
        if pagination_last_page:
            schema['t4|#pagination_container li'] = ('text__any', pagination_last_page)
    else:
        schema['t5|#pagination_container'] = 'not_displayed'


def generate_test(config, create_tags = True):
    schema = {}
    config = copy.deepcopy(config)  
    tags = normalize_list(config.pop('tags', []))
    
    if create_tags:
        tags.append('url')
        schema['tags'] = tags
    
    if 'params' in config:
        schema['params'] = config.pop('params')
    
    if 'wait' in config:
        schema['wait'] = config.pop('wait')
    else:
        schema['wait'] = 'complete'
        
    if 'naics' in config:
        add_naics_tests(schema, *config.pop('naics'))
    
        
    if 'vehicle' in config:
        add_vehicle_tests(schema, *config.pop('vehicle'))
        
    if 'pool' in config:
        add_pool_tests(schema, *config.pop('pool'))
        
    if 'zone' in config:
        add_zone_tests(schema, *config.pop('zone'))
        
    if 'setaside_filters' in config:
        add_setaside_filter_tests(schema, *config.pop('setaside_filters'))
        
    if 'vendor_result_info' in config:
        add_vendor_result_info_tests(schema, *config.pop('vendor_result_info'))
        
    if 'vendor_table' in config:
        add_vendor_table_tests(schema, *config.pop('vendor_table'))
    
        
    if 'membership_filters' in config:
        add_membership_filter_tests(schema, *config.pop('membership_filters'))
        
    if 'vendor_sam' in config:
        add_vendor_sam_tests(schema, *config.pop('vendor_sam'))    
    
    if 'vendor_info' in config:
        add_vendor_info_tests(schema, *config.pop('vendor_info'))
        
    if 'vendor_address' in config:
        add_vendor_address_tests(schema, *config.pop('vendor_address'))
        
    if 'vendor_badges' in config:
        add_vendor_badge_tests(schema, *config.pop('vendor_badges'))
        
    if 'contract_result_info' in config:
        add_contract_result_info_tests(schema, *config.pop('contract_result_info'))
        
    if 'contract_table' in config:
        add_contract_table_tests(schema, *config.pop('contract_table'))
    
    for name, test_config in config.items():
        if name != 'action':
            schema[name] = test_config
        
    return schema

def generate_action_test(config):
    schema = {'wait': 'complete'}
    
    def add_actions(actions, local_config, index = 1):
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
            schema['wait'] = 'complete'
        
        if len(actions) > 0:
            schema[event_name] = {}
            schema[event_name]['actions'] = add_actions(actions, local_config, (index + 1))
        else:
            schema[event_name] = generate_test(local_config, False)
            
            if 'wait' not in local_config:
                schema[event_name]['wait'] = 'complete'
        
        return schema
    
    tags = normalize_list(config.pop('tags', []))
    tags.append('action')
    schema['tags'] = tags
    
    params = config.pop('params', {})
    schema['params'] = {}
    
    if 'args' in params:
        schema['params']['args'] = params['args']
    
    if 'test' in params:
        schema['params']['test'] = params['test']
       
    if 'action' in config:
        schema['actions'] = add_actions(config.pop('action'), config)
    
    return schema


def generate_action_tests(schema, type, name, config):
    if (not type or type == 'url') and 'params' in config:
        schema["filter_{}_url".format(name)] = generate_test(config)
    
    if (not type or type == 'action') and 'action' in config:
        schema["filter_{}_action".format(name)] = generate_action_test(config)


def generate_schema(config, type = None):
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
            generate_action_tests(schema, type, name, action_config)
    
    if not type or type == 'test':        
        for name, test_config in config.items():
            schema[name] = test_config             
    
    return schema
