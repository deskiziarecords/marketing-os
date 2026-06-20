# domains/content_factory/services.py
from django.db import transaction

from ai.providers.service import generate_ai_content
from apps.tenants.models import Project, Tenant
from domains.content_factory.models import ContentMaster, ContentVariant, PromptTemplate
from events.publishers import publish_event


def create_content_master(
    title: str,
    content: str,
    tenant: Tenant,
    project: Project,
    status: str = "draft",
) -> ContentMaster:
    """Create a new ContentMaster and publish an event."""
    with transaction.atomic():
        master = ContentMaster.objects.create(
            tenant=tenant,
            project=project,
            title=title,
            content=content,
            status=status,
        )

        publish_event(
            event_type="content.master.created",
            payload={
                "master_id": str(master.id),
                "title": title,
            },
            tenant_id=str(tenant.id),
            project_id=str(project.id),
        )

    return master


def generate_variant(
    master: ContentMaster,
    platform: str,
    tenant: Tenant,
    project: Project,
    prompt_template: PromptTemplate | None = None,
) -> ContentVariant:
    """
    Generate an AI-powered platform variant for a ContentMaster.

    Uses the AI provider service, logs the audit trail, publishes an
    Outbox event for billing, and saves the result as a ContentVariant.
    """
    # Build prompts
    platform_descriptions = {
        "instagram": "Instagram (visual + caption)",
        "linkedin": "LinkedIn (professional network)",
        "tiktok": "TikTok (short-form video script)",
        "twitter": "Twitter / X (short text)",
        "facebook": "Facebook (social post)",
        "blog": "Blog article",
        "email": "Email newsletter",
    }
    platform_label = platform_descriptions.get(platform, platform)

    if prompt_template:
        system_prompt = prompt_template.system_prompt
    else:
        system_prompt = (
            f"Eres un experto en marketing de contenidos para {platform_label}. "
            f"Adapta el contenido manteniendo la esencia pero optimizando para el formato y "
            f"la audiencia de {platform_label}. Tono: profesional y cercano. Responde en español."
        )

    prompt = (
        f"Genera una variante para {platform_label} a partir del siguiente contenido base:\n\n"
        f"---\n{master.content}\n---\n\n"
        f"Título: {master.title}"
    )

    # Call AI provider (logs audit, publishes ai.generation.completed event)
    generated_content = generate_ai_content(
        prompt=prompt,
        system_prompt=system_prompt,
        purpose="content_variant_generation",
        tenant=tenant,
        project=project,
    )

    # Save the variant
    with transaction.atomic():
        variant = ContentVariant.objects.create(
            master=master,
            platform=platform,
            generated_content=generated_content,
            prompt_used=prompt_template,
        )

        publish_event(
            event_type="content.variant.generated",
            payload={
                "variant_id": str(variant.id),
                "master_id": str(master.id),
                "platform": platform,
            },
            tenant_id=str(tenant.id),
            project_id=str(project.id),
        )

    return variant
