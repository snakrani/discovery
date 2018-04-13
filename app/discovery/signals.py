from django.dispatch import receiver
from django.core.signals import request_finished
from django.contrib.admin.models import LogEntry
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save

import logging


@receiver(user_logged_in)
def on_logged_in(sender, user, request, **kwargs):
    logging.getLogger('authentication').info("User login as: {}".format(user))

@receiver(user_logged_out)
def on_logged_out(sender, user, request, **kwargs):
    logging.getLogger('authentication').info("User logout as: {}".format(user))

@receiver(user_login_failed)
def on_login_failed(sender, user, request, **kwargs):
    logging.getLogger('authentication').info("User login failed for: {}".format(user))


@receiver(post_save)
def on_admin_log_save(sender, instance, created, raw, using, update_fields, **kwargs):
    if isinstance(instance, LogEntry):
        
        if instance.is_addition():
            action = 'Creating'
        elif instance.is_change():
            action = 'Updating'
        elif instance.is_deletion():
            action = 'Deleting'
        else:
            action = 'Entry: '
        
        logging.getLogger('admin').info("User {}: {} {} {} - {}".format(
            instance.user,
            action,
            instance.content_type,
            instance.object_repr, 
            instance.get_change_message().lower()
        ))
