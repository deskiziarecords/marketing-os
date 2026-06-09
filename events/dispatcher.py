# events/dispatcher.py
from django.dispatch import Signal

# Definición de eventos
lead_created = Signal()
content_published = Signal()
ai_decision_made = Signal()

# Ejemplo de uso en CRM
def create_lead(name, email, tenant):
    lead = Lead.objects.create(name=name, email=email, tenant=tenant)
    # Disparar evento, no importar la app de automation
    lead_created.send(sender='crm', instance=lead)
