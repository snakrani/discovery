from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.exceptions import TaskError

from django.core.management import call_command
from db_mutex import DBMutexError, DBMutexTimeoutError
from db_mutex.models import DBMutex
from db_mutex.db_mutex import db_mutex

import sys
import io


@shared_task
def update_contracts(period=260, load=260, count=500, pause=1):
    success = True
    lock_id = 'contracts.update_contracts'
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    
    try:
        with db_mutex(lock_id):
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
        
    except Exception as error:
        print(error)
        
        DBMutex.objects.filter(lock_id=lock_id).delete()
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


@shared_task
def prune_contracts(period=260):
    success = True
    lock_id = 'contracts.prune_contracts'
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    
    try:
        with db_mutex(lock_id):
            # Commands don't return anything
            call_command('prune_contracts', 
                 period=period
            )
    
    except DBMutexError:
        success = False
        print('prune_contracts: Could not obtain lock')
        
    except DBMutexTimeoutError:
        print('prune_contracts: Task completed but the lock timed out')
        
    except Exception as error:
        print(error)
        
        DBMutex.objects.filter(lock_id=lock_id).delete()
        success = False
    
    sys.stdout = old_stdout
    
    if not success:
        raise TaskError(mystdout.getvalue())
        
    return { 
        "task": "prune_contracts",
        "params": { 
                   "period": period
        },
        "message": mystdout.getvalue() 
    }
