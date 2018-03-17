
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
