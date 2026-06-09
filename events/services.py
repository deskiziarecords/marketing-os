# events/services.py
from django.db import transaction
from .models import DomainEvent

def publish_event(event_type: str, payload: dict, tenant_id: str = None, project_id: str = None):
    """
    Implementación del Outbox Pattern.
    Guarda el evento en la BD dentro de la misma transacción que la lógica de negocio.
    """
    DomainEvent.objects.create(
        event_type=event_type,
        tenant_id=tenant_id,
        project_id=project_id,
        payload=payload,
        status='pending'
    )
    # Nota: No llamamos a Celery aquí directamente. 
    # Un worker de Celery Beat hará polling de eventos 'pending' para garantizar 
    # que la transacción principal ya haya hecho commit.
