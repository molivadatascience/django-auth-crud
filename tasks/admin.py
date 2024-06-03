from django.contrib import admin
from .models import Task #Para traer el modelo llamado tarea

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha_solicitud", )

# Register your models here.
admin.site.register(Task, TaskAdmin)