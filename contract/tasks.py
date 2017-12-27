from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.exceptions import TaskError

from django.core.management import call_command
from db_mutex import DBMutexError, DBMutexTimeoutError
from db_mutex.db_mutex import db_mutex
from StringIO import StringIO

import sys


@shared_task
def update_contracts(period=520, load=520, count=500, pause=1):
    success = True
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        with db_mutex('contract.update_contracts'):
            # Commands don't return anything
            call_command('load_fpds', 
                 period=period, 
                 load=load, 
                 count=count, 
                 pause=pause
            )
    
    except DBMutexError:
        success = False
        print('update_contracts: Could not obtain lock')
        
    except DBMutexTimeoutError:
        print('update_contracts: Task completed but the lock timed out')
        
    except Exception:
        success = False
    
    sys.stdout = old_stdout
    
    if not success:
        raise TaskError(mystdout.getvalue())
        
    return { 
        "task": "update_fpds",
        "params": { 
                   "period": period, 
                   "load": load,
                   "count": count, 
                   "pause": pause
        },
        "message": mystdout.getvalue() 
    }
