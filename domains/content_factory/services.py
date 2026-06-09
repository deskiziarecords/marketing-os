# domains/content_factory/services.py
from ai.providers.service import generate_ai_content
from events.services import publish_event

def generar_variante_red_social(idea, plataforma, tenant, user):
    system_prompt = f"Eres un experto en {plataforma}. Tono: {tenant.marca.tono}."
    prompt = f"Crea un post sobre: {idea.tema_central}"
    
    # 1. Llamada al wrapper de IA (esto guarda el AuditLog y dispara el evento Outbox)
    contenido_generado = generate_ai_content(
        prompt=prompt,
        system_prompt=system_prompt,
        task_type='creative_writing',
        tenant=tenant,
        project=idea.project,
        user=user
    )
    
    # 2. Guardar el resultado en el dominio de contenido
    variante = ContentVariant.objects.create(
        master=idea,
        plataforma=plataforma,
        contenido_generado=contenido_generado
    )
    
    # 3. Disparar evento de dominio (Outbox)
    publish_event(
        event_type='content.variant.generated',
        payload={'variant_id': str(variante.id), 'platform': plataforma},
        tenant_id=str(tenant.id),
        project_id=str(idea.project.id)
    )
    
    return variante
