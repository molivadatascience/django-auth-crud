from django import forms
from .models import Task, hijos

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=['title', 'fecha_solicitud', 'nombre_cliente', 'campana', 'kam', 'valor_oportunidad', 'margen','tipo_importacion', 'pais_origen', 'fecha_entrega_propuesta', 'fecha_entrega_productos', 'solicitud_muestra', 'description', 'fecha_cotizacion', 'cotizacion_aceptada', 'nombre_contacto', 'email_contacto', 'cotización_valida_dias', 'tiempo_muestra_fisica_dias', 'tiempo_produccion_dias', 'important'] #son los campos que quiero ver en el formulario el resto no es necesario
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Write a title'}),
            'fecha_solicitud':forms.DateInput(attrs={'type': 'date'}),
            'nombre_cliente':forms.TextInput(attrs={'class': 'form-control','placeholder': 'nombre_cliente'}),
            'campana': forms.TextInput(attrs={'class': 'form-control','placeholder': 'campana'}),
            'kam':forms.TextInput(attrs={'class': 'form-control','placeholder': 'kam'}),
            'valor_oportunidad':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa valor'}),
            'margen':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa valor'}),
            'tipo_importacion':forms.TextInput(attrs={'class': 'form-control','placeholder': 'tipo_importacion'}),
            'pais_origen':forms.TextInput(attrs={'class': 'form-control','placeholder': 'pais_origen'}),
            'fecha_entrega_propuesta':forms.DateInput(attrs={'type': 'date'}),
            'fecha_entrega_productos':forms.DateInput(attrs={'type': 'date'}),
            'solicitud_muestra': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Write a description'}),
            'fecha_cotizacion':forms.DateInput(attrs={'type': 'date'}),
            'cotizacion_aceptada':forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
            'nombre_contacto': forms.TextInput(attrs={'class': 'form-control','placeholder': 'nombre_contacto'}),
            'email_contacto': forms.TextInput(attrs={'class': 'form-control','placeholder': 'email_contacto'}),
            'cotización_valida_dias':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese días'}),
            'tiempo_muestra_fisica_dias':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese días'}),
            'tiempo_produccion_dias':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese días'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }


class hijosForm(forms.ModelForm):
    class Meta:
        model = hijos
        fields = ['nombre_producto', 'origen', 'id']