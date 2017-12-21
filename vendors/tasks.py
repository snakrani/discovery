from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.management import call_command
from StringIO import StringIO

import sys


@shared_task
def update_vendors(vpp=0, tries=3, pause=1):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    call_command('load_vendors',
                 vpp=vpp,
                 tries=tries,
                 pause=pause
    )
    
    sys.stdout = old_stdout
        
    return { 
        "task": "update_vendors",
        "params": { 
                   "vpp": vpp, 
                   "tries": tries, 
                   "pause": pause
        },
        "message": mystdout.getvalue() 
    }
