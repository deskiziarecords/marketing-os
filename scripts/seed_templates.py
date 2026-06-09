# scripts/seed_templates.py
import os
import sys
import django

# 1. Configurar el entorno de Django para que este script funcione de forma nativa
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.tenants.models import ProjectTemplate

# 2. Definir las plantillas maestras (Datos de alta calidad)
TEMPLATES_DATA = [
    {
        "name": "Clínica Dental",
        "slug": "clinica-dental",
        "description": "Configuración optimizada para clínicas dentales, ortodoncia e implantes.",
        "config": {
            "pipelines": ["Nuevo Lead", "Evaluación Agendada", "En Tratamiento", "Seguimiento", "Paciente Perdido"],
            "prompts": [
                {
                    "name": "Generador de Reels Educativos",
                    "version": "v1.0",
                    "system_prompt": "Eres un odontólogo experto en marketing digital. Tu tono es profesional, empático y educativo. Responde siempre en español.",
                    "variables": ["{{tema}}", "{{duracion_segundos}}"],
                    "task_type": "creative_writing"
                },
                {
                    "name": "Respuesta a Objeción de Precio",
                    "version": "v1.0",
                    "system_prompt": "Eres un asistente de ventas de una clínica dental de alto valor. Tu objetivo es justificar el precio mediante el valor, la tecnología y los resultados, sin sonar defensivo.",
                    "variables": ["{{objecion}}", "{{tratamiento}}"],
                    "task_type": "creative_writing"
                }
            ],
            "automations": [
                {
                    "name": "Bienvenida y Agendamiento Automático",
                    "trigger_event": "lead.created",
                    "actions": [
                        {"type": "ai_generate", "purpose": "welcome_email", "model": "gpt-4o-mini"},
                        {"type": "wait", "duration_hours": 24},
                        {"type": "check_response", "if_no": "send_whatsapp_followup"}
                    ]
                }
            ]
        }
    },
    {
        "name": "Despacho Legal",
        "slug": "despacho-legal",
        "description": "Configuración para bufetes de abogados, derecho laboral y civil.",
        "config": {
            "pipelines": ["Consulta Inicial", "Documentación Pendiente", "En Proceso Legal", "Cierre", "Archivado"],
            "prompts": [
                {
                    "name": "Resumen de Caso Legal",
                    "version": "v1.0",
                    "system_prompt": "Eres un abogado senior experto en síntesis de casos. Tu tono es formal, preciso y objetivo. Extrae los hechos clave, la problemática legal y la posible solución.",
                    "variables": ["{{hechos}}", "{{documentos}}"],
                    "task_type": "fast_classification"
                }
            ],
            "automations": [
                {
                    "name": "Solicitud de Documentos Iniciales",
                    "trigger_event": "lead.created",
                    "actions": [
                        {"type": "ai_generate", "purpose": "document_request_email", "model": "gpt-4o"},
                        {"type": "send_email"}
                    ]
                }
            ]
        }
    }
]

def run():
    print(" Iniciando seed de Plantillas de Proyecto...")
    
    created_count = 0
    for tpl_data in TEMPLATES_DATA:
        template, created = ProjectTemplate.objects.get_or_create(
            slug=tpl_data["slug"],
            defaults={
                "name": tpl_data["name"],
                "description": tpl_data["description"],
                "config": tpl_data["config"]
            }
        )
        
        if created:
            print(f" Plantilla creada: {template.name}")
            created_count += 1
        else:
            print(f" Plantilla ya existe: {template.name}")
            
    print(f" Proceso completado. {created_count} plantillas nuevas creadas.")

if __name__ == "__main__":
    run()
