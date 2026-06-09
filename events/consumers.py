# events/consumers.py
import logging
from ai.providers.service import generate_ai_content
from apps.tenants.models import Tenant, Project

logger = logging.getLogger(__name__)

def handle_lead_created(event):
    """
    Consumidor del evento 'lead.created'.
    Aquí es donde la magia sucede: IA y Billing reaccionan sin que el CRM lo sepa.
    """
    payload = event.payload
    tenant = Tenant.objects.get(id=event.tenant_id)
    project = Project.objects.get(id=event.project_id)
    
    logger.info(f"Procesando lead creado: {payload['name']}")
    
    # 1. La IA genera un mensaje de bienvenida personalizado
    system_prompt = f"Eres el asistente virtual de {tenant.name}. Tono: profesional y cercano."
    prompt = f"Redacta un correo de bienvenida corto para {payload['name']} ({payload['email']}) que acaba de registrarse."
    
    try:
        welcome_email = generate_ai_content(
            prompt=prompt,
            system_prompt=system_prompt,
            purpose='welcome_email_generation',
            tenant=tenant,
            project=project
        )
        logger.info(f"Email generado con éxito. Costo: ver AIAuditLog")
        
        # Aquí iría la lógica para enviar el email real (integrations/sendgrid, etc.)
        
    except Exception as e:
        logger.error(f"Fallo al generar email con IA: {e}")

def handle_ai_generation_completed(event):
    """
    Consumidor del evento de IA. Actualiza el Billing.
    """
    payload = event.payload
    logger.info(f"Registrando consumo de IA: {payload['cost_usd']} USD para Tenant {event.tenant_id}")
    
    # Aquí llamarías a: apps.billing.services.record_usage(event.tenant_id, payload['cost_usd'])
