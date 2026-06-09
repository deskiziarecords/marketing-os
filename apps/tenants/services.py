# apps/tenants/services.py
from ai.prompts.models import PromptTemplate
from domains.automation.models import AutomationRule

def apply_template_to_project(project, template):
    """
    Clona la configuración de una ProjectTemplate a un Project específico.
    """
    config = template.config
    
    # 1. Clonar Prompts
    prompts_to_create = []
    for p_data in config.get("prompts", []):
        prompts_to_create.append(
            PromptTemplate(
                project=project,
                name=p_data["name"],
                version=p_data["version"],
                system_prompt=p_data["system_prompt"],
                variables=p_data["variables"],
                task_type=p_data["task_type"]
            )
        )
    # bulk_create es mucho más rápido que crear uno por uno
    PromptTemplate.objects.bulk_create(prompts_to_create)
    
    # 2. Clonar Reglas de Automatización
    automations_to_create = []
    for a_data in config.get("automations", []):
        automations_to_create.append(
            AutomationRule(
                project=project,
                name=a_data["name"],
                trigger_event=a_data["trigger_event"],
                actions=a_data["actions"],
                is_active=True
            )
        )
    AutomationRule.objects.bulk_create(automations_to_create)
    
    return True
