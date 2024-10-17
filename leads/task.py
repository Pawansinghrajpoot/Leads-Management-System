# leads/tasks.py

from celery import shared_task
from datetime import datetime
from .models import Lead

@shared_task
def check_due_calls():
    today = datetime.now().date()
    leads_due_for_call = Lead.objects.filter(last_call_date=today)
    
    for lead in leads_due_for_call:
        # Here you can send a notification, email, or log the alert
        print(f"Reminder: You need to call {lead.name} today!")
