from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=['nombre_cliente','fecha_solicitud', 'observaciones', 'important',] #son los campos que quiero ver en el formulario el resto no es necesario
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control','placeholder': 'nombre_cliente'}),
            'fecha_solicitud': forms.DateField(attrs={'class': 'form-control','placeholder': 'fecha_solicitud'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Observaciones'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }