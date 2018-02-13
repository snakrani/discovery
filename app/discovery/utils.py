from inspect import getframeinfo, stack

import psutil
import os
import json


def config_value(name, default=None, types='user-provided', instance=None):
    # Order of precedence
    # 1. Cloud configurations coming in through VCAP_SERVICES
    # 2. Local environment variable if it exists
    # 3. Default value provided

    value = default
    
    # Check for an existing environment variable
    # TODO: Need to do anything with the types?
    try:
        value = os.environ[name]
    except:
        pass
    
    # Check for a cloud foundry service configuration
    #TODO SOON: Cache this JSON object
    try:
        services = json.loads(os.environ['VCAP_SERVICES'])
        
        # Ensure we are dealing with an iterable list
        if not isinstance(types, list): 
            types = [ types ]
        
        # We are in a cloud foundry instance
        for type in types:
            if type not in services.keys():
                continue
            
            for service in services[type]:
                if instance and service['name'] != instance:
                    continue
                
                data = service['credentials']
                
                if name in data:
                    value = data[name]        
    
    except Exception:
        pass # return what we've got

    return value


def memory_in_mb(mem):
    #documentation on memory fields: http://psutil.readthedocs.io/en/latest/#id1
    unit = 1024 * 1024 # MB
    return {
        'total': mem.total / unit,
        'available': mem.available / unit, #*
        'used': mem.used / unit, #*
        'free': mem.free / unit,
        'active': mem.active / unit,
        'inactive': mem.inactive / unit,
        'buffers': mem.buffers / unit,
        'cached': mem.cached / unit,
        'shared': mem.shared / unit,
    }


def print_memory(message = "Max Memory"):
    caller = getframeinfo(stack()[1][0])
    mem = memory_in_mb(psutil.virtual_memory())   
    
    
    print("{}/{} | {}: {:.2f}MB {:.2f}MB".format(caller.filename, caller.lineno, message, mem['available'], mem['used']))


def csv_memory(message = "Memory"):
    caller = getframeinfo(stack()[1][0])
    mem = memory_in_mb(psutil.virtual_memory())
    
    return('"{}","{}",{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}'.format(caller.filename, message, mem['total'], mem['available'], mem['used'], mem['free'], mem['active'], mem['inactive'], mem['buffers'], mem['cached'], mem['shared']))
