from collections import OrderedDict

from django.conf import settings
from django.core.cache import cache

from discovery import models as system

import re
import json


def page_cache_key(request):
    return "{}:{}".format(request.path, re.sub(r'[\s\{\}\(\)\"\=]', '', json.dumps(OrderedDict(request.query_params))))

def track_page_load(url):
    page, created = system.CachePage.objects.get_or_create(url=url)
    page.count += 1
    page.save()

def cached_response(request, view_op, response_cls):
    page_id = page_cache_key(request)
        
    track_page_load(request.build_absolute_uri())
    data = cache.get(page_id)
    
    if data:
        return response_cls(data)
    else:
        response = view_op()
        cache.set(page_id, response.data)
        return response
