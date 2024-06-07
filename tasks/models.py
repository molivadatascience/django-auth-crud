from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Vamos a crear una tabla
# from tkinter import CASCADE
class Task(models.Model):
    title = models.CharField(max_length=100)
    fecha_solicitud = models.DateTimeField(null=True, blank=True)
    nombre_cliente = models.CharField(max_length=100)
    campana = models.CharField(max_length=100)
    kam = models.CharField(max_length=100)
    valor_oportunidad = models.IntegerField()
    margen= models.DecimalField(max_digits=5, decimal_places=2)
    tipo_importacion= models.CharField(max_length=100)
    pais_origen = models.CharField(max_length=100)
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

class hijos(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=150)
    origen = models.CharField(max_length=100)
    