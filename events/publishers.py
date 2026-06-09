# events/publishers.py
from events.models import DomainEvent

def publish_event(event_type: str, payload: dict, tenant_id: str = None, project_id: str = None):
    """
    Outbox Pattern: Guarda el evento en la BD. 
    Un worker de Celery lo leerá después, garantizando consistencia.
    """
    DomainEvent.objects.create(
        event_type=event_type,
        tenant_id=tenant_id,
        project_id=project_id,
        payload=payload,
        status='pending'
    )
