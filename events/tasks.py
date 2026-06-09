# events/tasks.py
from celery import shared_task
from django.db import transaction
from django.utils import timezone
from events.models import DomainEvent
from events import consumers

@shared_task
def process_pending_events():
    # select_for_update(skip_locked=True) evita que dos workers procesen el mismo evento
    events = DomainEvent.objects.select_for_update(skip_locked=True).filter(
        status='pending'
    ).order_by('created_at')[:50]

    for event in events:
        with transaction.atomic():
            event.status = 'processing'
            event.attempts += 1
            event.save()

        try:
            if event.event_type == 'lead.created':
                consumers.handle_lead_created(event)
            elif event.event_type == 'ai.generation.completed':
                consumers.handle_ai_generation_completed(event)
            
            event.status = 'completed'
            event.processed_at = timezone.now()
            event.save()
            
        except Exception as e:
            event.status = 'failed' if event.attempts >= 3 else 'pending'
            event.error_message = str(e)
            event.save()
