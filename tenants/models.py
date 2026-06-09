# tenants/models.py
class ProjectTemplate(models.Model):
    nombre = models.CharField(max_length=100) # "Clínica Dental"
    configuracion_inicial = models.JSONField() 
    # Ej: {"pipelines": ["Nuevo", "Agendado", "Tratamiento"], "prompts": [...], "faq": [...]}

class Tenant(models.Model):
    nombre = models.CharField(max_length=255)
    plantilla = models.ForeignKey(ProjectTemplate, on_delete=models.SET_NULL, null=True)
    # ... campos de white label (logo, colores, dominio)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.plantilla:
            self._aplicar_plantilla()

    def _aplicar_plantilla(self):
        # Lógica para clonar pipelines, prompts y FAQs desde el JSON de la plantilla
        pass
