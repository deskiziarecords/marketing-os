# core/models.py
from django.db import models
from django.conf import settings

class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    industria = models.CharField(max_length=255)
    subindustria = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField()
    
    # Branding (Capa 1)
    logo = models.ImageField(upload_to='branding/logos/', blank=True, null=True)
    paleta_colores = models.JSONField(default=list, help_text="Ej: ['#FF0000', '#000000']")
    tipografias = models.JSONField(default=dict, help_text="Ej: {'titulo': 'Roboto', 'cuerpo': 'Open Sans'}")
    tono = models.CharField(max_length=255, blank=True, null=True)
    
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
