# crm/models.py
class Lead(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='leads')
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    origen = models.CharField(max_length=50, choices=[('facebook', 'Facebook'), ('web', 'Web'), ('whatsapp', 'WhatsApp')])
    estado = models.CharField(
        max_length=50, 
        choices=[('nuevo', 'Nuevo'), ('contactado', 'Contactado'), ('interesado', 'Interesado'), ('cita', 'Cita'), ('cliente', 'Cliente'), ('perdido', 'Perdido')], 
        default='nuevo'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
