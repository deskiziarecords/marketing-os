# events/consumers.py
import logging
from apps.billing.services import record_ai_usage
from apps.analytics.services import update_ai_dashboard

logger = logging.getLogger(__name__)

def handle_ai_generation_completed(event: 'DomainEvent'):
    """
    Este consumidor no sabe NADA de cómo se generó el contenido.
    Solo sabe que ocurrió, y actualiza sus propios dominios.
    """
    payload = event.payload
    
    # 1. Billing: Cobra al cliente por el uso (Metered Billing)
    record_ai_usage(
        tenant_id=event.tenant_id,
        cost_usd=payload['cost_usd'],
        tokens=payload['tokens']
    )
    
    # 2. Analytics: Actualiza el dashboard de gasto de IA
    update_ai_dashboard(
        tenant_id=event.tenant_id,
        model=payload['model'],
        cost=payload['cost_usd']
    )
    
    logger.info(f"Evento ai.generation.completed procesado para Tenant {event.tenant_id}")
