from django import template


register = template.Library()


@register.filter
def process_docs_fields(input_fields):
    field_map = {}
    fields = []
    
    for field in input_fields:
        if not field_map.get(field.name, None):
            fields.append(field)
            field_map[field.name] = True
        
    return fields