# ai/providers/service.py
import hashlib
import time

from ai.audits.models import AIAuditLog
from events.publishers import publish_event


def generate_ai_content(prompt: str, system_prompt: str, purpose: str, tenant, project=None):
    # Lazy-import litellm so its heavy dependencies (aiohttp, etc.) are only loaded
    # when an actual AI call is made — not at module import time.
    from litellm import completion, completion_cost  # noqa: PLC0415

    start_time = time.time()
    model = "gpt-4o-mini"
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()

    try:
        response = completion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )

        latency_ms = int((time.time() - start_time) * 1000)
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = completion_cost(completion_response=response)

        audit_log = AIAuditLog.objects.create(
            tenant=tenant,
            project=project,
            model=model,
            purpose=purpose,
            prompt_hash=prompt_hash,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            latency_ms=latency_ms,
            success=True,
        )

        publish_event(
            event_type="ai.generation.completed",
            payload={
                "audit_log_id": str(audit_log.id),
                "model": model,
                "tokens": input_tokens + output_tokens,
                "cost_usd": float(cost),
            },
            tenant_id=str(tenant.id),
            project_id=str(project.id) if project else None,
        )

        return response.choices[0].message.content

    except Exception as e:
        AIAuditLog.objects.create(
            tenant=tenant,
            project=project,
            model=model,
            purpose=purpose,
            prompt_hash=prompt_hash,
            input_tokens=0,
            output_tokens=0,
            cost_usd=0.0,
            latency_ms=int((time.time() - start_time) * 1000),
            success=False,
            error_detail=str(e),
        )
        raise
