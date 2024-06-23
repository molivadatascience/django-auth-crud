from django import forms
from .models import Task, DetalleOportunidad
from django.utils import timezone
class NumberInputWithThousandsSeparator(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value is not None:
            try:
                value = "{:,}".format(int(value)).replace(",", ".")
            except ValueError:
                pass
        return super().render(name, value, attrs, renderer)
    
    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if value:
            value = value.replace('.', '')
            if value.isdigit():
                return int(value)
        return value

class PercentageInput(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value is not None:
            try:
                value = f"{float(value)}%"
            except ValueError:
                pass
        return super().render(name, value, attrs, renderer)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if value:
            value = value.replace('%', '').replace(',', '.').strip()
            try:
                return float(value)
            except ValueError:
                raise forms.ValidationError("Enter a valid percentage.")
        return value

    def format_value(self, value):
        if value is None:
            return ''
        try:
            value = float(value)
        except ValueError:
            return value
        return f"{value}%"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=['title', 'fecha_solicitud', 'nombre_cliente', 'kam', 'valor_oportunidad', 'margen','tipo_importacion', 'pais_destino', 'fecha_entrega_propuesta', 'fecha_entrega_productos', 'solicitud_muestra_materialidad', 'descripcion'] #son los campos que quiero ver en el formulario el resto no es necesario
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Write a title'}),
            'fecha_solicitud':forms.DateInput(attrs={'type': 'date'}),
            'nombre_cliente':forms.Select(attrs={'class': 'form-control','placeholder': 'nombre_cliente'}),
            #'campana': forms.TextInput(attrs={'class': 'form-control','placeholder': 'campana'}),
            'kam':forms.Select(attrs={'class': 'form-control'}),
            #'valor_oportunidad':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa valor'}),
            'valor_oportunidad': NumberInputWithThousandsSeparator(attrs={'class': 'form-control', 'placeholder': 'Ingresa valor'}),
            #'margen':forms.TextInput(attrs={'class': 'form-control'}),
            'margen': PercentageInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa margen'}),
            'tipo_importacion':forms.Select(attrs={'class': 'form-control','placeholder': 'tipo_importacion'}),
            'pais_destino':forms.Select(attrs={'class': 'form-control'}),
            'fecha_entrega_propuesta':forms.DateInput(attrs={'type': 'date'}),
            'fecha_entrega_productos':forms.DateInput(attrs={'type': 'date'}),
            'solicitud_muestra_materialidad': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description', 'rows': 2}),  # Actualiza a Textarea con filas
            #'precio_unitario':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa precio en CLP'}),
            #'fecha_cotizacion':forms.DateInput(attrs={'type': 'date'}),
            #'cotizacion_aceptada':forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
            #'nombre_contacto': forms.TextInput(attrs={'class': 'form-control','placeholder': 'nombre_contacto'}),
            #'email_contacto': forms.TextInput(attrs={'class': 'form-control','placeholder': 'email_contacto'}),
            #'cotización_valida_dias':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese días'}),
            #'tiempo_muestra_fisica_dias':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese días'}),
            #'tiempo_produccion_dias':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese días'}),
            #'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }
  
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['fecha_solicitud'].initial = timezone.now().date()  # Fecha actual por defecto
        self.fields['pais_destino'].initial = 'Chile'
        self.fields['margen'].initial = 30.0

    def clean_valor_oportunidad(self):
        data = self.cleaned_data.get('valor_oportunidad')
        if data:
            data = str(data).replace('.', '')
            if data.isdigit():
                return int(data)
            raise forms.ValidationError("Enter a whole number.")
        return data

    #def clean_margen(self):
    #    data = self.cleaned_data.get('margen')
    #    if isinstance(data, str):
    #        data = data.replace('%', '').replace(',', '.').strip()
    #        try:
    #            return float(data)
    #        except ValueError:
    #            raise forms.ValidationError("Enter a valid percentage.")
    #    return data
    def clean_margen(self):
        data = self.cleaned_data.get('margen', 30.0)
        if isinstance(data, str):
            data = data.replace('%', '')
        return float(data)


class DetalleOportunidadForm(forms.ModelForm):
    class Meta:
        model = DetalleOportunidad
        fields = [
            'categoria_a_cotizar','producto', 'margen_producto', 'precio_objetivo',
            'unidades', 'tamano', 'color', 'branding', 'cantidad_de_disenos',
            'muestra_materialidad', 'muestra_pps', 'observaciones', 'precio_unitario','packaging_master_unidades',
            'packaging_inner_unidades', 'packaging_unitario_unidades', 'packaging_master_tipo',
            'packaging_inner_tipo', 'packaging_diseno_tipo', 'packaging_master_diseno',
            'packaging_inner_diseno', 'packaging_unitario_diseno', 'archivos_adjuntos'
        ]
        widgets = {
           # 'id_requerimiento_comercial': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria_a_cotizar': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.TextInput(attrs={'class': 'form-control'}),
            #'margen': forms.NumberInput(attrs={'class': 'form-control'}),
            'margen_producto': PercentageInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa margen'}),
            #'precio_objetivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_objetivo': NumberInputWithThousandsSeparator(attrs={'class': 'form-control', 'placeholder': 'Ingresa precio'}),
            #'unidades': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidades': NumberInputWithThousandsSeparator(attrs={'class': 'form-control', 'placeholder': 'Ingresa unidades'}),
            'tamano': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'branding': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_de_disenos': forms.NumberInput(attrs={'class': 'form-control'}),
            'muestra_materialidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'muestra_pps': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_unitario':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa precio en CLP'}),
            'packaging_master_unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_inner_unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_unitario_unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_master_tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_inner_tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_diseno_tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_master_diseno': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_inner_diseno': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_unitario_diseno': forms.TextInput(attrs={'class': 'form-control'}),
            'archivos_adjuntos': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
    def __init__(self, *args, **kwargs):
        super(DetalleOportunidadForm, self).__init__(*args, **kwargs)
        self.fields['margen_producto'].initial = 30.0
    def clean_precio_objetivo(self):
        data = self.cleaned_data.get('precio_objetivo')
        if data:
            data = str(data).replace('.', '')
            if data.isdigit():
                return int(data)
            raise forms.ValidationError("Enter a whole number.")
        return data

    def clean_unidades(self):
        data = self.cleaned_data.get('unidades')
        if data:
            data = str(data).replace('.', '')
            if data.isdigit():
                return int(data)
            raise forms.ValidationError("Enter a whole number.")
        return data

    #def clean_margen_producto(self):
    #    data = self.cleaned_data.get('margen_producto')
    #    if isinstance(data, str):
    #        data = data.replace('%', '').replace(',', '.').strip()
    #        try:
    #            return float(data)
    #        except ValueError:
    #            raise forms.ValidationError("Enter a valid percentage.")
    #    return data
    def clean_margen_producto(self):
        data = self.cleaned_data.get('margen_producto', 30.0)
        if isinstance(data, str):
            data = data.replace('%', '')
        return float(data)
