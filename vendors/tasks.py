from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.management import call_command


@shared_task
def update_vendors(vpp=0, tries=3, pause=1):
    call_command('load_vendors',
                 vpp=vpp,
                 tries=tries,
                 pause=pause
    )
