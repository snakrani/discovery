import os
import json


def cloud_config(name, default=None, types='user-provided'):
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
                data = service['credentials']
                
                if name in data:
                    value = data[name]        
    
    except Exception:
        pass # return what we've got

    return value