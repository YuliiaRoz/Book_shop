from celery import shared_task
from django.core.management import call_command
import time

@shared_task
def send_order_email(user_email, order_id):
    time.sleep(2)
    return f"Email sent to {user_email} for order #{order_id}"

@shared_task
def clear_sessions():
    call_command('clear_sessions')
    return "Expired sessions cleared successfully"

@shared_task
def generate_reports():
    return "Daily reports generated"