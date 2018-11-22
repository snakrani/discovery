from test.common import normalize_list

import copy
import json


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
