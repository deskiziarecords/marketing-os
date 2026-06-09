# domains/crm/services.py
from django.db import transaction
from domains.crm.models import Lead
from events.publishers import publish_event

def create_lead(name: str, email: str, tenant, project):
    """
    Crea el lead y publica el evento en la MISMA transacción (Outbox).
    """
    with transaction.atomic():
        lead = Lead.objects.create(
            tenant=tenant, project=project, name=name, email=email, status='nuevo'
        )
        
        publish_event(
            event_type='lead.created',
            payload={'lead_id': str(lead.id), 'name': name, 'email': email},
            tenant_id=str(tenant.id),
            project_id=str(project.id)
        )
        
    return lead
