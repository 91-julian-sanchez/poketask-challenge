from django.dispatch import receiver
from .tasks import fetch_and_create_pokemon
from celery import signals
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@receiver(signals.task_postrun)
def task_postrun_handler(sender, task_id, task, args, retval, state, **kwargs):
    if retval and ("error" not in retval):
        send_email_notification(retval)
    if retval.get("error") == 'DUP_ENTRY':
        log_duplicate_pokemon(retval)
        fetch_and_create_pokemon.delay()

def send_email_notification(pokemon_data):
    subject = 'New Pokemon Created'
    message = f"A new Pokemon has been created {pokemon_data}"
    from_email = '91.julian.sanchez@gmail.com'
    recipient_list = ['julian.sanchez91@hotmail.com']
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def log_duplicate_pokemon(pokemon_data):
    logger.warning(f"A duplicate Pokemon has been found", pokemon_data)
