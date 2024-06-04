from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=['title', 'campana', 'description', 'important'] #son los campos que quiero ver en el formulario el resto no es necesario
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Write a title'}),
            'campana': forms.TextInput(attrs={'class': 'form-control','placeholder': 'campana'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }