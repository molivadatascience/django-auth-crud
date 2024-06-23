from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Vamos a crear una tabla
# from tkinter import CASCADE
class Task(models.Model):
    NOMBRE_CLIENTES_CHOICES = [
        ('CCU', 'CCU'),
        ('AGROSUPER', 'AGROSUPER'),
        ('COCA-COLA', 'COCA-COLA'),
    ]
    KAM_CHOICES = [
        ('Francisca', 'Francisca'),
        ('María Jesús', 'María Jesús'),
        ('Rolando', 'Rolando'),
    ]
    TIPOIMPORTACION_CHOICES = [
        ('Aéreo', 'Aéreo'),
        ('Ambas', 'Ambas'),
        ('Marítimo', 'Marítimo'),
    ]

    PAISDESTINO_CHOICES = [
        ('Chile', 'Chile'),
        ('Colombia', 'Colombia'),
        ('México', 'México'),
        ('Perú', 'Perú'),
    ]

    title = models.CharField(max_length=100)
    fecha_solicitud = models.DateTimeField(null=True, blank=True)
    nombre_cliente = models.CharField(max_length=100,choices=NOMBRE_CLIENTES_CHOICES)
    #campana = models.CharField(max_length=100)
    kam = models.CharField(max_length=100,choices=KAM_CHOICES)
    valor_oportunidad = models.IntegerField()
    margen= models.DecimalField(max_digits=5, decimal_places=2)
    tipo_importacion= models.CharField(max_length=100,choices=TIPOIMPORTACION_CHOICES)
    pais_destino = models.CharField(max_length=100,choices=PAISDESTINO_CHOICES)
    fecha_entrega_propuesta = models.DateTimeField(null=True, blank=True)
    fecha_entrega_productos = models.DateTimeField(null=True, blank=True)
    solicitud_muestra = models.BooleanField(default=False)
    descripcion = models.CharField(blank=True)
    #fecha_cotizacion = models.DateTimeField(null=True, blank=True)
    #cotizacion_aceptada = models.BooleanField(default=False)
    #nombre_contacto = models.CharField(max_length=100)
    #email_contacto = models.CharField(max_length=100)
    #cotización_valida_dias = models.IntegerField()
    #tiempo_muestra_fisica_dias = models.IntegerField()
    #tiempo_produccion_dias = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True) # el automaticamente guarda la fecha
    datecompleted = models.DateTimeField(null=True, blank=True) #permite valores nulos
   # important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title+ '- by '+ self.user.username



class DetalleOportunidad(models.Model):
    ORIGEN_CHOICES = [
        ('Internacional', 'Internacional'),
        ('Nacional', 'Nacional'),
    ]
    DESTINO_CHOICES = [
        ('Chile', 'Chile'),
        ('Perú', 'Perú'),
    ]
    CATEGORIA_A_COTIZAR_CHOICES = [
        ('Durables', 'Durables'),
        ('Merch', 'Merch'),
        ('Visibilidad', 'Visibilidad')
    ]
    MUESTRA_PPS_CHOICES = [
        ('Digital', 'Digital'),
        ('Física', 'Física'),
    ]
    task = models.ForeignKey(Task, related_name='detalles', on_delete=models.CASCADE)
    id_detalle_venta = models.AutoField(primary_key=True)
   # id_requerimiento_comercial = models.IntegerField()
    producto = models.CharField(max_length=100)
    origen = models.CharField(max_length=100,choices=ORIGEN_CHOICES)
    margen_producto = models.DecimalField(max_digits=5, decimal_places=2)
    precio_objetivo = models.IntegerField()
    destino = models.CharField(max_length=100,choices=DESTINO_CHOICES)
    categoria_a_cotizar = models.CharField(max_length=100,choices=CATEGORIA_A_COTIZAR_CHOICES)
    unidades = models.IntegerField()
    tamano = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    branding = models.CharField(max_length=100)
    cantidad_de_disenos = models.IntegerField()
    muestra_materialidad = models.BooleanField()
    muestra_pps = models.CharField(max_length=100,choices=MUESTRA_PPS_CHOICES)
    observaciones = models.CharField(max_length=100)
    precio_unitario = models.IntegerField()
    packaging_master_unidades = models.CharField(max_length=100)
    packaging_inner_unidades = models.CharField(max_length=100)
    packaging_unitario_unidades = models.CharField(max_length=100)
    packaging_master_tipo = models.CharField(max_length=100)
    packaging_inner_tipo = models.CharField(max_length=100)
    packaging_diseno_tipo = models.CharField(max_length=100)
    packaging_master_diseno = models.CharField(max_length=100)
    packaging_inner_diseno = models.CharField(max_length=100)
    packaging_unitario_diseno = models.CharField(max_length=100)
    archivos_adjuntos = models.FileField(upload_to='archivos_adjuntos/')

    #def __str__(self):
    #    return f"Detalle {self.id_detalle_venta}"
