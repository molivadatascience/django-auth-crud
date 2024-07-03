from django import forms
from .models import Task, DetalleOportunidad,Costeo
from django.utils import timezone
#from .widgets import MultiFileInput
from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe
from django.forms import inlineformset_factory

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
        fields=['campaña', 'fecha_solicitud', 'nombre_cliente', 'kam', 'valor_oportunidad', 'margen','tipo_importacion', 'pais_destino', 'fecha_entrega_propuesta', 'fecha_entrega_productos', 'descripcion'] #son los campos que quiero ver en el formulario el resto no es necesario
        widgets = {
            
            'campaña': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre Campaña'}),
            'fecha_solicitud':forms.DateInput(attrs={'type': 'date'}),
            'nombre_cliente':forms.Select(attrs={'class': 'form-control','placeholder': 'nombre_cliente'}),
            'kam':forms.Select(attrs={'class': 'form-control'}),
            'valor_oportunidad': NumberInputWithThousandsSeparator(attrs={'class': 'form-control', 'placeholder': 'Ingresa valor'}),
            'margen': PercentageInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa margen'}),
            'tipo_importacion':forms.Select(attrs={'class': 'form-control','placeholder': 'tipo_importacion'}),
            'pais_destino':forms.Select(attrs={'class': 'form-control'}),
            'fecha_entrega_propuesta':forms.DateInput(attrs={'type': 'date'}),
            'fecha_entrega_productos':forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese descripción', 'rows': 2}),  # Actualiza a Textarea con filas
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
            'unidades', 'unidades_2','unidades_3','unidades_4','tamano', 'color', 'branding', 'cantidad_de_disenos',
            'muestra_materialidad', 'aprobacion_muestra_pps', 'observaciones', 'precio_unitario','packaging_master_unidades',
            'packaging_master_diseno', 'packaging_master_tipo', 'packaging_inner_unidades', 'packaging_inner_diseno', 'packaging_inner_tipo',
            'packaging_unitario_unidades','packaging_unitario_diseno','packaging_diseno_tipo','archivos_adjuntos'
        ]
        widgets = {
            'categoria_a_cotizar': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.TextInput(attrs={'class': 'form-control'}),
            'margen_producto': PercentageInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa margen'}),
            'precio_objetivo': NumberInputWithThousandsSeparator(attrs={'class': 'form-control', 'placeholder': 'Ingresa precio'}),
            'unidades': NumberInputWithThousandsSeparator(attrs={'class': 'form-control', 'placeholder': 'Ingresa unidades'}),
            'unidades_2': NumberInputWithThousandsSeparator(attrs={'class': 'form-control', 'placeholder': 'Ingresa unidades'}),
            'unidades_3': NumberInputWithThousandsSeparator(attrs={'class': 'form-control', 'placeholder': 'Ingresa unidades'}),
            'unidades_4': NumberInputWithThousandsSeparator(attrs={'class': 'form-control', 'placeholder': 'Ingresa unidades'}),
            'tamano': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'branding': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_de_disenos': forms.NumberInput(attrs={'class': 'form-control'}),
            'muestra_materialidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aprobacion_muestra_pps': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_unitario':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa precio en CLP'}),
            'packaging_master_unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_master_diseno': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'packaging_master_tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_inner_unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_inner_diseno': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'packaging_inner_tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_unitario_unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'packaging_unitario_diseno': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'packaging_diseno_tipo': forms.TextInput(attrs={'class': 'form-control'}),
            #'archivos_adjuntos': forms.ClearableFileInput(attrs={'multiple': True}),
            'archivos_adjuntos': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            #'archivos_adjuntos': MultiFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(DetalleOportunidadForm, self).__init__(*args, **kwargs)
        self.fields['margen_producto'].initial = 30.0
        self.fields['packaging_master_unidades'].initial = 'Sin requerimiento'
        self.fields['packaging_inner_unidades'].initial = 'Sin requerimiento'
        self.fields['packaging_unitario_unidades'].initial = 'Sin requerimiento'
        self.fields['packaging_master_tipo'].initial = 'Sin requerimiento'
        self.fields['packaging_inner_tipo'].initial = 'Sin requerimiento'
        self.fields['packaging_diseno_tipo'].initial = 'Sin requerimiento'
        self.fields['aprobacion_muestra_pps'].initial = 'Física'

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

    def clean_unidades_2(self):
        data = self.cleaned_data.get('unidades_2')
        if data:
            data = str(data).replace('.', '')
            if data.isdigit():
                return int(data)
            raise forms.ValidationError("Enter a whole number.")
        return data

    def clean_unidades_3(self):
        data = self.cleaned_data.get('unidades_3')
        if data:
            data = str(data).replace('.', '')
            if data.isdigit():
                return int(data)
            raise forms.ValidationError("Enter a whole number.")
        return data

    def clean_unidades_4(self):
        data = self.cleaned_data.get('unidades_4')
        if data:
            data = str(data).replace('.', '')
            if data.isdigit():
                return int(data)
            raise forms.ValidationError("Enter a whole number.")
        return data

    def clean_margen_producto(self):
        data = self.cleaned_data.get('margen_producto', 30.0)
        if isinstance(data, str):
            data = data.replace('%', '')
        return float(data)


#class ArchivoAdjuntoForm(forms.ModelForm):
#    class Meta:
#        model = ArchivoAdjunto
#        fields = ('archivo',)
#
#    def __init__(self, *args, **kwargs):
#        super(ArchivoAdjuntoForm, self).__init__(*args, **kwargs)
#        self.fields['archivo'].widget.attrs.update({'class': 'form-control-file', 'multiple': True, 'accept': '.pdf,.doc,.docx,.xls,.xlsx'})

#ArchivoAdjuntoFormSet = inlineformset_factory(DetalleOportunidad, ArchivoAdjunto, form=ArchivoAdjuntoForm, extra=1)


class CosteoForm(forms.ModelForm):
    class Meta:
        model = Costeo
        exclude = ['id_detalle_venta']  # Excluir el campo id_detalle_venta del formulario

        widgets = {
            'prov_elegido': forms.Select(choices=Costeo.SI_NO_CHOICES),
            'responsable': forms.Select(choices=Costeo.RESPONSABLE_CHOICES),
            'proveedor': forms.Select(choices=Costeo.PROVEEDOR_CHOICES),
            'tipo_importacion': forms.Select(choices=Costeo.IMPORTACION_COSTEO_CHOICES),
            'pais': forms.Select(choices=Costeo.PAIS_CHOICES),
            'puerto': forms.Select(choices=Costeo.PUERTO_CHOICES),
            'tamaño_muestra': forms.Select(choices=Costeo.TAMAÑO_MUESTRA_CHOICES),
            'portal_licitaciones': forms.Select(choices=Costeo.PORTAL_LICITACIONES_CHOICES),
            'fecha_costeo': forms.DateInput(attrs={'type': 'date'}),
             # Widget de fecha para desplegar un calendario
        }