from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.management import call_command
from StringIO import StringIO

import sys


@shared_task
def update_fpds(years=10, weeks=520, count=500, pause=1):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    #TODO: Return some data?
    call_command('load_fpds', 
                 years=years, 
                 weeks=weeks, 
                 count=count, 
                 pause=pause
    )
    
    sys.stdout = old_stdout
        
    return { 
        "task": "update_fpds",
        "params": { 
                   "years": years, 
                   "weeks": weeks,
                   "count": count, 
                   "pause": pause
        },
        "message": mystdout.getvalue() 
    }
