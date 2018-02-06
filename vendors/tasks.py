from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.exceptions import TaskError

from django.core.management import call_command
from db_mutex import DBMutexError, DBMutexTimeoutError
from db_mutex.models import DBMutex
from db_mutex.db_mutex import db_mutex
from StringIO import StringIO

import sys


@shared_task
def update_categories():
    success = True
    lock_id = 'vendors.update_categories'
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        with db_mutex(lock_id):
            # Commands don't return anything
            call_command('load_categories')
    
    except DBMutexError:
        success = False
        print('update_categories: Could not obtain lock')
        
    except DBMutexTimeoutError:
        print('update_categories: Task completed but the lock timed out')
        
    except Exception:
        DBMutex.objects.get(lock_id=lock_id).delete()
        success = False
 
    sys.stdout = old_stdout
    
    if not success:
        raise TaskError(mystdout.getvalue())
          
    return { 
        "task": "update_categories",
        "params": {},
        "message": mystdout.getvalue() 
    }


@shared_task
def update_vendors(vpp=0, tries=3, pause=1):
    success = True
    lock_id = 'vendors.update_vendors'
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        with db_mutex(lock_id):
            # Commands don't return anything
            call_command('load_vendors',
                 vpp=vpp,
                 tries=tries,
                 pause=pause
            )
    
    except DBMutexError:
        success = False
        print('update_vendors: Could not obtain lock')
        
    except DBMutexTimeoutError:
        print('update_vendors: Task completed but the lock timed out')
        
    except Exception as error:
        print(error)
        DBMutex.objects.filter(lock_id=lock_id).delete()
        success = False
   
    sys.stdout = old_stdout
    
    if not success:
        raise TaskError(mystdout.getvalue())
         
    return { 
        "task": "update_vendors",
        "params": { 
                   "vpp": vpp, 
                   "tries": tries, 
                   "pause": pause
        },
        "message": mystdout.getvalue() 
    }
