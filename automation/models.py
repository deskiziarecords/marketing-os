# automation/models.py
class ReglaAutomatizacion(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='reglas')
    nombre = models.CharField(max_length=255)
    desencadenante = models.CharField(max_length=100, help_text="Ej: 'lead_creado'")
    # Ejemplo de acciones: [{"tipo": "enviar_whatsapp", "delay_minutos": 0}, {"tipo": "esperar", "delay_horas": 24}, {"tipo": "enviar_email"}]
    acciones = models.JSONField() 
    activa = models.BooleanField(default=True)
