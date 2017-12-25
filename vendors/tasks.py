from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.exceptions import TaskError

from django.core.management import call_command
from db_mutex import DBMutexError, DBMutexTimeoutError
from db_mutex.db_mutex import db_mutex
from StringIO import StringIO

import sys


@shared_task
def update_categories():
    success = True
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        with db_mutex('vendors.update_categories'):
            # Commands don't return anything
            call_command('load_categories')
    
    except DBMutexError:
        success = False
        print('update_categories: Could not obtain lock')
        
    except DBMutexTimeoutError:
        print('update_categories: Task completed but the lock timed out')
        
    except Exception:
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
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        with db_mutex('vendors.update_vendors'):
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
        
    except Exception:
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
