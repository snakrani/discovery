from django.core.management.base import BaseCommand
from django.core.cache import cache

from discovery import models as system

import urllib


class Command(BaseCommand):
    def handle(self, *args, **options):
        cache.clear()
            
        for page in system.CachePage.objects.all().order_by('-count'):
            print("[ {} ] - {}".format(page.count, page.url))
            try:
                urllib.request.urlopen(page.url).read()
            except Exception:
                page.delete()
