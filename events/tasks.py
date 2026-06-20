# events/tasks.py
import logging
from celery import shared_task
from django.db import transaction
from django.utils import timezone
from events.models import DomainEvent
from events import consumers

logger = logging.getLogger(__name__)

HANDLERS = {
    'lead.created': consumers.handle_lead_created,
    'ai.generation.completed': consumers.handle_ai_generation_completed,
}

@shared_task
def process_pending_events():
    with transaction.atomic():
        # select_for_update MUST be inside atomic; skip_locked lets parallel workers skip busy rows
        pending = DomainEvent.objects.select_for_update(skip_locked=True).filter(
            status='pending'
        ).order_by('created_at')[:50]

        for event in pending:
            event.status = 'processing'
            event.attempts += 1
            event.save(update_fields=['status', 'attempts'])

    # Process outside the lock so the lock isn't held during slow AI/network calls
    for event in DomainEvent.objects.filter(status='processing').order_by('created_at')[:50]:
        handler = HANDLERS.get(event.event_type)
        try:
            if handler:
                handler(event)
            else:
                logger.warning("No handler for event type: %s", event.event_type)

            event.status = 'completed'
            event.processed_at = timezone.now()
            event.save(update_fields=['status', 'processed_at'])

        except Exception as e:
            logger.exception("Failed processing event %s (attempt %d)", event.id, event.attempts)
            event.status = 'failed' if event.attempts >= 3 else 'pending'
            event.error_message = str(e)
            event.save(update_fields=['status', 'error_message'])
