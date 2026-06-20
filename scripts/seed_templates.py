# scripts/seed_templates.py
import os
import sys

import django

# 1. Configurar el entorno de Django para que este script funcione de forma nativa
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from apps.tenants.models import ProjectTemplate

# 2. Definir las plantillas maestras (Datos de alta calidad)
TEMPLATES_DATA = [
    {
        "name": "Clinica Dental",
        "slug": "clinica-dental",
        "description": "Configuracion optimizada para clinicas dentales, ortodoncia e implantes.",
        "config": {
            "pipelines": ["Nuevo Lead", "Evaluacion Agendada", "En Tratamiento", "Seguimiento", "Paciente Perdido"],
            "prompts": [
                {
                    "name": "Generador de Reels Educativos",
                    "version": "v1.0",
                    "system_prompt": "Eres un odontologo experto en marketing digital. Tu tono es profesional, empatico y educativo. Responde siempre en espanol.",
                    "variables": ["{{tema}}", "{{duracion_segundos}}"],
                    "task_type": "creative_writing",
                },
                {
                    "name": "Respuesta a objecion de precio",
                    "version": "v1.0",
                    "system_prompt": "Eres un asistente de ventas de una clinica dental de alto valor. Tu objetivo es justificar el precio mediante el valor, la tecnologia y los resultados, sin sonar defensivo.",
                    "variables": ["{{objecion}}", "{{tratamiento}}"],
                    "task_type": "creative_writing",
                },
            ],
            "automations": [
                {
                    "name": "Bienvenida y Agendamiento Automatico",
                    "trigger_event": "lead.created",
                    "actions": [
                        {"type": "ai_generate", "purpose": "welcome_email", "model": "gpt-4o-mini"},
                        {"type": "wait", "duration_hours": 24},
                        {"type": "check_response", "if_no": "send_whatsapp_followup"},
                    ],
                },
            ],
        },
    },
    {
        "name": "Despacho Legal (General)",
        "slug": "despacho-legal",
        "description": "Configuracion para bufetes de abogados, derecho laboral y civil.",
        "config": {
            "pipelines": ["Consulta Inicial", "Documentacion Pendiente", "En Proceso Legal", "Cierre", "Archivado"],
            "prompts": [
                {
                    "name": "Resumen de Caso Legal",
                    "version": "v1.0",
                    "system_prompt": "Eres un abogado senior experto en sintesis de casos. Tu tono es formal, preciso y objetivo. Extrae los hechos clave, la problematica legal y la posible solucion.",
                    "variables": ["{{hechos}}", "{{documentos}}"],
                    "task_type": "fast_classification",
                },
            ],
            "automations": [
                {
                    "name": "Solicitud de Documentos Iniciales",
                    "trigger_event": "lead.created",
                    "actions": [
                        {"type": "ai_generate", "purpose": "document_request_email", "model": "gpt-4o"},
                        {"type": "send_email"},
                    ],
                },
            ],
        },
    },
    # ------------------------------------------------------------------
    # PLANTILLA: DESPACHO LABORAL (Conciliacion y Litigio)
    # ------------------------------------------------------------------
    {
        "name": "Despacho Laboral (Conciliacion y Litigio)",
        "slug": "despacho-laboral",
        "description": (
            "Plantilla especializada para despachos de derecho laboral. "
            "Incluye prompts de IA para contenido educativo en redes sociales, "
            "automacion de bienvenida para leads laborales, y pipeline de "
            "conciliacion y litigio."
        ),
        "config": {
            "pipelines": [
                "Lead Recibido",
                "Consulta Inicial",
                "Evaluacion de Caso",
                "Documentacion",
                "Conciliacion",
                "Litigio",
                "Cierre",
                "Archivado",
            ],
            "prompts": [
                # ------------------------------------------------------------------
                # Prompts para REDES SOCIALES (contenido educativo)
                # ------------------------------------------------------------------
                {
                    "name": "Post Educativo - Despidos",
                    "version": "v1.0",
                    "system_prompt": (
                        "Eres un abogado laboral con 15 anos de experiencia en "
                        "despidos injustificados. Tu tono es claro, directo y "
                        "empatico. Traduce conceptos legales complejos a un "
                        "lenguaje que cualquier trabajador entienda. "
                        "Responde siempre en espanol."
                    ),
                    "variables": ["{{tema}}", "{{plataforma}}"],
                    "task_type": "creative_writing",
                },
                {
                    "name": "Video Script - Liquidaciones",
                    "version": "v1.0",
                    "system_prompt": (
                        "Eres un abogado laboral especializado en calculo de "
                        "liquidaciones y finiquitos. Explica de forma clara "
                        "y paso a paso. Usa ejemplos concretos con numeros. "
                        "Tu tono es profesional pero accesible. "
                        "Responde en espanol."
                    ),
                    "variables": ["{{tema}}", "{{duracion_segundos}}"],
                    "task_type": "creative_writing",
                },
                {
                    "name": "Carrusel Instagram - Derechos Laborales",
                    "version": "v1.0",
                    "system_prompt": (
                        "Eres un abogado laboral que crea contenido para "
                        "Instagram. Genera un carrusel educativo de 7-10 "
                        "diapositivas. Cada slide debe tener un titular "
                        "corto y 1-2 frases de apoyo. El tono es directo "
                        "y visual. No uses jerga legal. Responde en espanol."
                    ),
                    "variables": ["{{tema}}", "{{slides}}"],
                    "task_type": "creative_writing",
                },
                {
                    "name": "Reel TikTok - Casos Reales",
                    "version": "v1.0",
                    "system_prompt": (
                        "Eres un abogado laboral que cuenta casos reales "
                        "en TikTok. El tono es conversational, como si "
                        "estuvieras hablando con un amigo. Usa un gancho "
                        "fuerte en los primeros 3 segundos. Explica el caso "
                        "en 30-45 segundos. Termina con un CTA claro. "
                        "Responde en espanol."
                    ),
                    "variables": ["{{caso}}", "{{leccion}}"],
                    "task_type": "creative_writing",
                },
                {
                    "name": "Respuesta a Consulta de Lead",
                    "version": "v1.0",
                    "system_prompt": (
                        "Eres el asistente virtual de un despacho laboral. "
                        "Responde a las consultas de potenciales clientes "
                        "de forma clara, empatica y profesional. No des "
                        "asesoria legal vinculante, pero explica conceptos "
                        "generales y recomienda agendar una consulta. "
                        "Responde en espanol."
                    ),
                    "variables": ["{{consulta}}", "{{nombre_cliente}}"],
                    "task_type": "creative_writing",
                },
                {
                    "name": "Email de Bienvenida y Solicitud de Docs",
                    "version": "v1.0",
                    "system_prompt": (
                        "Eres el asistente de un despacho laboral. Redacta "
                        "un email de bienvenida para un nuevo cliente que "
                        "acaba de contactarnos por un caso laboral. "
                        "El tono debe ser profesional, empatico y tranquilizador. "
                        "Incluye una lista de documentos que debe reunir "
                        "(contrato, recibos de nomina, identificacion, etc.). "
                        "Responde en espanol."
                    ),
                    "variables": ["{{nombre}}", "{{tipo_caso}}"],
                    "task_type": "creative_writing",
                },
                # ------------------------------------------------------------------
                # Prompts de SISTEMA (clasificacion, analisis)
                # ------------------------------------------------------------------
                {
                    "name": "Clasificador de Caso Laboral",
                    "version": "v1.0",
                    "system_prompt": (
                        "Eres un abogado laboral senior. Clasifica el caso "
                        "del cliente en una de estas categorias: DESPIDO, "
                        "LIQUIDACION, SALARIOS, ACOSO, PRESTACIONES, "
                        "CONTRATO, CONCILIACION, OTRO. "
                        "Responde SOLO con el nombre de la categoria."
                    ),
                    "variables": ["{{descripcion_caso}}"],
                    "task_type": "fast_classification",
                },
            ],
            "automations": [
                {
                    "name": "Bienvenida y Solicitud de Documentos",
                    "trigger_event": "lead.created",
                    "actions": [
                        {
                            "type": "ai_generate",
                            "purpose": "welcome_and_docs_request",
                            "model": "gpt-4o-mini",
                            "prompt_template": "Email de Bienvenida y Solicitud de Docs",
                        },
                        {"type": "send_email"},
                        {
                            "type": "wait",
                            "duration_hours": 48,
                        },
                        {
                            "type": "check_response",
                            "if_no": "send_whatsapp_followup",
                        },
                    ],
                },
                {
                    "name": "Clasificacion Automatica de Caso",
                    "trigger_event": "lead.created",
                    "actions": [
                        {
                            "type": "ai_generate",
                            "purpose": "case_classification",
                            "model": "gpt-4o-mini",
                            "prompt_template": "Clasificador de Caso Laboral",
                        },
                        {"type": "update_lead_category"},
                    ],
                },
                {
                    "name": "Generacion de Contenido Semanal",
                    "trigger_event": "schedule.weekly",
                    "actions": [
                        {
                            "type": "ai_generate",
                            "purpose": "weekly_social_content",
                            "model": "gpt-4o-mini",
                            "prompt_template": "Post Educativo - Despidos",
                        },
                        {
                            "type": "create_variants",
                            "platforms": ["instagram", "tiktok", "facebook", "linkedin"],
                        },
                        {"type": "schedule_posts"},
                    ],
                },
            ],
        },
    },
]


def run():
    print("Iniciando seed de Plantillas de Proyecto...")

    created_count = 0
    for tpl_data in TEMPLATES_DATA:
        template, created = ProjectTemplate.objects.get_or_create(
            slug=tpl_data["slug"],
            defaults={
                "name": tpl_data["name"],
                "description": tpl_data["description"],
                "config": tpl_data["config"],
            },
        )

        if created:
            print(f"  [OK] Plantilla creada: {template.name}")
            created_count += 1
        else:
            print(f"  [OK] Plantilla ya existe: {template.name}")

    print(f"\nProceso completado. {created_count} plantilla(s) nueva(s) creada(s).")


if __name__ == "__main__":
    run()
