# ai/providers/service.py
import time
import hashlib
from django.conf import settings
from litellm import completion, completion_cost
from ai.audits.models import AIAuditLog
from events.services import publish_event

class AIRouter:
    """Decide qué modelo usar según la necesidad, ocultando la complejidad al dominio."""
    
    @staticmethod
    def get_model_for_task(task_type: str) -> str:
        routing_map = {
            'creative_writing': 'claude-3-5-sonnet-20240620',
            'fast_classification': 'gpt-4o-mini',
            'rag_qa': 'gpt-4o',
            'default': 'gpt-4o'
        }
        return routing_map.get(task_type, routing_map['default'])

def generate_ai_content(
    prompt: str, 
    system_prompt: str, 
    task_type: str, 
    tenant, 
    project=None, 
    user=None
) -> str:
    start_time = time.time()
    model = AIRouter.get_model_for_task(task_type)
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    
    try:
        # 1. Llamada unificada a LiteLLM
        response = completion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        # 2. Cálculo de métricas
        latency_ms = int((time.time() - start_time) * 1000)
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = completion_cost(completion_response=response)
        
        # 3. Auditoría (Guardado en BD)
        audit_log = AIAuditLog.objects.create(
            tenant=tenant,
            project=project,
            user=user,
            provider=response.model.split('-')[0], # Simplificación
            model=model,
            purpose=task_type,
            prompt_hash=prompt_hash,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            latency_ms=latency_ms,
            success=True
        )
        
        # 4. Disparar Evento (Outbox)
        publish_event(
            event_type='ai.generation.completed',
            payload={
                'audit_log_id': str(audit_log.id),
                'model': model,
                'tokens': input_tokens + output_tokens,
                'cost_usd': float(cost)
            },
            tenant_id=str(tenant.id),
            project_id=str(project.id) if project else None
        )
        
        return response.choices[0].message.content

    except Exception as e:
        # Auditoría de fallos (crítico para debugging)
        AIAuditLog.objects.create(
            tenant=tenant,
            project=project,
            user=user,
            provider='unknown',
            model=model,
            purpose=task_type,
            prompt_hash=prompt_hash,
            input_tokens=0,
            output_tokens=0,
            cost_usd=0.0,
            latency_ms=int((time.time() - start_time) * 1000),
            success=False,
            error_detail=str(e)
        )
        raise
