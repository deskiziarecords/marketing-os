# apps/tenants/services.py
from django.db import transaction

from domains.content_factory.models import PromptTemplate as ContentPromptTemplate


def apply_template_to_project(project, template):
    """
    Clona la configuracion de una ProjectTemplate a un Project especifico.
    Crea los PromptTemplates pre-configurados para el proyecto.
    """
    config = template.config

    # 1. Clonar Prompts de IA
    prompts_to_create = []
    for p_data in config.get("prompts", []):
        prompts_to_create.append(
            ContentPromptTemplate(
                tenant=project.tenant,
                name=p_data["name"],
                version=p_data.get("version", "v1.0"),
                system_prompt=p_data["system_prompt"],
                variables=p_data.get("variables", []),
                task_type=p_data.get("task_type", "creative_writing"),
            )
        )

    with transaction.atomic():
        ContentPromptTemplate.objects.bulk_create(prompts_to_create)

    return True
