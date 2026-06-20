"""
Seed script for local development.

Creates a superuser, sample Tenant/Project, PromptTemplates,
ContentMasters, ContentVariants, and a Lead so you can immediately
interact with the API.

Usage:
    uv run python scripts/seed_dev_data.py
"""
import os
import sys

import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

# --- Imports (after django.setup()) ---
from django.contrib.auth import get_user_model
from django.db import transaction

from apps.tenants.models import Tenant, Project
from domains.content_factory.models import ContentMaster, ContentVariant, PromptTemplate
from domains.crm.models import Lead

User = get_user_model()


@transaction.atomic
def run():
    print("Seeding development data...\n")

    # ------------------------------------------------------------------
    # 1. Superuser
    # ------------------------------------------------------------------
    if User.objects.filter(username="admin").exists():
        print("  [OK] Superuser 'admin' already exists")
        admin = User.objects.get(username="admin")
    else:
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        print("  [OK] Superuser created: admin / admin123")

    # ------------------------------------------------------------------
    # 2. Tenant & Project
    # ------------------------------------------------------------------
    tenant, created = Tenant.objects.get_or_create(
        subdomain="clinica-dental",
        defaults={"name": "Clinica Dental Sonrisas"},
    )
    if created:
        print(f"  [OK] Tenant created: {tenant.name}")
    else:
        print(f"  [OK] Tenant already exists: {tenant.name}")

    project, created = Project.objects.get_or_create(
        tenant=tenant,
        name="Marketing Dental 2026",
        defaults={},
    )
    if created:
        print(f"  [OK] Project created: {project.name}")
    else:
        print(f"  [OK] Project already exists: {project.name}")

    # ------------------------------------------------------------------
    # 3. Prompt Templates
    # ------------------------------------------------------------------
    prompt_templates_data = [
        {
            "name": "Generador de Reels Educativos",
            "version": "v1.0",
            "system_prompt": (
                "Eres un odontologo experto en marketing digital. "
                "Tu tono es profesional, empatico y educativo. Responde siempre en espanol."
            ),
            "variables": ["{{tema}}", "{{duracion_segundos}}"],
            "task_type": "creative_writing",
        },
        {
            "name": "Respuesta a objecion de precio",
            "version": "v1.0",
            "system_prompt": (
                "Eres un asistente de ventas de una clinica dental de alto valor. "
                "Tu objetivo es justificar el precio mediante el valor, la tecnologia "
                "y los resultados, sin sonar defensivo."
            ),
            "variables": ["{{objecion}}", "{{tratamiento}}"],
            "task_type": "creative_writing",
        },
        {
            "name": "Post de LinkedIn Corporativo",
            "version": "v2.0",
            "system_prompt": (
                "Eres un estratega de contenido B2B. Redacta con tono profesional "
                "y datos concretos. Responde en espanol."
            ),
            "variables": ["{{topic}}", "{{audiencia}}"],
            "task_type": "creative_writing",
        },
    ]

    template_count = 0
    for tpl_data in prompt_templates_data:
        _, created = PromptTemplate.objects.get_or_create(
            name=tpl_data["name"],
            version=tpl_data["version"],
            defaults={
                "tenant": tenant,
                "system_prompt": tpl_data["system_prompt"],
                "variables": tpl_data["variables"],
                "task_type": tpl_data["task_type"],
            },
        )
        if created:
            template_count += 1

    # Generic template without tenant (tests nullable FK)
    _, created = PromptTemplate.objects.get_or_create(
        name="Plantilla Generica",
        version="v1.0",
        defaults={
            "tenant": None,
            "system_prompt": "Eres un asistente util. Responde en espanol.",
            "variables": [],
            "task_type": "general",
        },
    )
    if created:
        template_count += 1

    print(f"  [OK] {template_count} PromptTemplate(s) created")

    # ------------------------------------------------------------------
    # 4. Content Masters & Variants
    # ------------------------------------------------------------------
    masters_data = [
        {
            "title": "10 Beneficios de la Ortodoncia Invisible",
            "content": (
                "La ortodoncia invisible ha revolucionado la forma en que los pacientes "
                "corrigen sus problemas dentales. A diferencia de los brackets tradicionales, "
                "los alineadores transparentes ofrecen comodidad, estetica y resultados predecibles. "
                "En este articulo exploramos los 10 beneficios principales que han convertido "
                "a la ortodoncia invisible en la opcion preferida por adultos y jovenes."
            ),
            "status": "approved",
        },
        {
            "title": "Cada Cuanto Debo Visitar al Dentista?",
            "content": (
                "La salud bucal es fundamental para el bienestar general. Muchos pacientes "
                "se preguntan con que frecuencia deben acudir al dentista. La recomendacion "
                "general es cada 6 meses, pero esto puede variar segun factores como la edad, "
                "el historial de enfermedades dentales y habitos como el tabaquismo."
            ),
            "status": "draft",
        },
        {
            "title": "Blanqueamiento Dental: Mitos y Realidades",
            "content": (
                "El blanqueamiento dental es uno de los tratamientos esteticos mas solicitados, "
                "pero tambien uno de los que mas mitos genera. Dania el esmalte? Es doloroso? "
                "Los resultados son permanentes? Respondemos a estas preguntas con base cientifica."
            ),
            "status": "approved",
        },
    ]

    master_count = 0
    for m_data in masters_data:
        master, created = ContentMaster.objects.get_or_create(
            title=m_data["title"],
            defaults={
                "tenant": tenant,
                "project": project,
                "content": m_data["content"],
                "status": m_data["status"],
            },
        )
        if created:
            master_count += 1

            # Create a sample variant for each new master
            platforms = ["instagram", "linkedin"]
            for platform in platforms:
                ContentVariant.objects.create(
                    master=master,
                    platform=platform,
                    generated_content=(
                        f"[{platform.upper()} variant of '{master.title}']\n\n"
                        f"Contenido adaptado para {platform}. "
                        f"Manteniendo la esencia del mensaje original pero optimizado "
                        f"para la audiencia y el formato de esta plataforma."
                    ),
                )

    print(f"  [OK] {master_count} ContentMaster(s) created with variants")

    # ------------------------------------------------------------------
    # 5. Sample Lead
    # ------------------------------------------------------------------
    lead, created = Lead.objects.get_or_create(
        email="maria@example.com",
        tenant=tenant,
        project=project,
        defaults={
            "name": "Maria Garcia",
            "status": "nuevo",
        },
    )
    if created:
        print(f"  [OK] Sample Lead created: {lead.name}")
    else:
        print(f"  [OK] Sample Lead already exists: {lead.name}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n[DONE] Seeding complete!")
    print(f"   Superuser: admin / admin123")
    print(f"   Tenant:    {tenant.name} ({tenant.subdomain})")
    print(f"   Project:   {project.name}")
    print(f"\nQuick API tests:")
    print(f"   curl http://localhost:8000/api/crm/leads/")
    print(f"   curl http://localhost:8000/api/content-factory/masters/")
    print(f"   curl http://localhost:8000/api/content-factory/prompt-templates/")


if __name__ == "__main__":
    run()
