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
def populate_cache():
    success = True
    lock_id = 'discovery.populate_cache'
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    
    try:
        with db_mutex(lock_id):
            # Commands don't return anything
            call_command('populate_cache')
    
    except DBMutexError:
        success = False
        print('populate_cache: Could not obtain lock')
        
    except DBMutexTimeoutError:
        print('populate_cache: Task completed but the lock timed out')
        
    except Exception as error:
        print(error)
        
        DBMutex.objects.filter(lock_id=lock_id).delete()
        success = False
 
    sys.stdout = old_stdout
    
    if not success:
        raise TaskError(mystdout.getvalue())
          
    return { 
        "task": "populate_cache",
        "params": {},
        "message": mystdout.getvalue() 
    }
