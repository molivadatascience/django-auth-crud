from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Vamos a crear una tabla
# from tkinter import CASCADE
class Task(models.Model):
    KAM_CHOICES = [
        ('Francisca', 'Francisca'),
        ('María Jesús', 'María Jesús'),
        ('Rolando', 'Rolando'),
    ]
    TIPOIMPORTACION_CHOICES = [
        ('Marítimo', 'Marítimo'),
        ('Aéreo', 'Aéreo'),
    ]

    PAISORIGEN_CHOICES = [
        ('Chile', 'Chile'),
        ('China', 'China'),
    ]

    title = models.CharField(max_length=100)
    fecha_solicitud = models.DateTimeField(null=True, blank=True)
    nombre_cliente = models.CharField(max_length=100)
    campana = models.CharField(max_length=100)
    kam = models.CharField(max_length=100,choices=KAM_CHOICES)
    valor_oportunidad = models.IntegerField()
    margen= models.DecimalField(max_digits=5, decimal_places=2)
    tipo_importacion= models.CharField(max_length=100,choices=TIPOIMPORTACION_CHOICES)
    pais_origen = models.CharField(max_length=100,choices=PAISORIGEN_CHOICES)
    fecha_entrega_propuesta = models.DateTimeField(null=True, blank=True)
    fecha_entrega_productos = models.DateTimeField(null=True, blank=True)
    solicitud_muestra = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    fecha_cotizacion = models.DateTimeField(null=True, blank=True)
    cotizacion_aceptada = models.BooleanField(default=False)
    nombre_contacto = models.CharField(max_length=100)
    email_contacto = models.CharField(max_length=100)
    cotización_valida_dias = models.IntegerField()
    tiempo_muestra_fisica_dias = models.IntegerField()
    tiempo_produccion_dias = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True) # el automaticamente guarda la fecha
    datecompleted = models.DateTimeField(null=True, blank=True) #permite valores nulos
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title+ '- by '+ self.user.username

class Hijos(models.Model):
    task = models.ForeignKey(Task, related_name='hijos', on_delete=models.CASCADE)
    nota_1 = models.TextField()
    nota_2 = models.DecimalField(max_digits=5, decimal_places=2)
    
    #def __str__(self):
    #   return f"Hijo de {self.task.nombre}"

class DetalleOportunidad(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    id_requerimiento_comercial = models.IntegerField()
    producto = models.CharField(max_length=100)
    origen = models.CharField(max_length=100)
    margen = models.FloatField()
    precio_objetivo = models.FloatField()
    destino = models.CharField(max_length=100)
    categoria_a_cotizar = models.CharField(max_length=100)
    unidades = models.IntegerField()
    tamaño = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    branding = models.CharField(max_length=100)
    cantidad_de_diseños = models.IntegerField()
    muestra_materialidad = models.BooleanField()
    muestra_pps = models.CharField(max_length=100)
    observaciones = models.CharField(max_length=100)
    packaging_master_unidades = models.CharField(max_length=100)
    packaging_inner_unidades = models.CharField(max_length=100)
    packaging_unitario_unidades = models.CharField(max_length=100)
    packaging_master_tipo = models.CharField(max_length=100)
    packaging_inner_tipo = models.CharField(max_length=100)
    packaging_diseño_tipo = models.CharField(max_length=100)
    packaging_master_diseño = models.CharField(max_length=100)
    packaging_inner_diseño = models.CharField(max_length=100)
    packaging_unitario_diseño = models.CharField(max_length=100)
    archivos_adjuntos = models.FileField(upload_to='archivos_adjuntos/')

    def __str__(self):
        return f"Detalle {self.id_detalle_venta}"
