
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Vamos a crear una tabla
# from tkinter import CASCADE
class Task(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    
    observaciones = models.TextField(blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True) # el automaticamente guarda la fecha
    datecompleted = models.DateTimeField(null=True, blank=True) #permite valores nulos
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title+ '- by '+ self.user.username
