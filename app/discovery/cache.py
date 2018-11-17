from django.conf import settings

from discovery import models as system


def track_page_load(request):
    page, created = system.CachePage.objects.get_or_create(url=request.build_absolute_uri())
    page.count += 1
    page.save()
