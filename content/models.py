# content/models.py
class IdeaContenido(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='ideas')
    tema = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.CharField(max_length=50, choices=[('borrador', 'Borrador'), ('aprobada', 'Aprobada')], default='borrador')
    popularidad = models.IntegerField(default=0)

class CalendarioEditorial(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='calendario')
    idea = models.ForeignKey(IdeaContenido, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_programada = models.DateTimeField()
    red_social = models.CharField(max_length=50, choices=[('instagram', 'Instagram'), ('linkedin', 'LinkedIn'), ('tiktok', 'TikTok')])
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('programado', 'Programado'), ('publicado', 'Publicado')])
    contenido_final = models.TextField(blank=True, null=True)
