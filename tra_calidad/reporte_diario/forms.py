from django import forms
from .models import ReporteDiario, Funda, Defecto, PorcentajeDefecto # Asegúrate de importar los modelos necesarios
from django.forms import modelformset_factory

# class ReporteDiarioForm(forms.ModelForm):
#     class Meta:
#         model = ReporteDiario
#         fields = '__all__'

#     marca_funda = forms.ModelChoiceField(queryset=Funda.objects.all(), empty_label=None)



class ReporteDiarioForm(forms.ModelForm):
    defectos = forms.ModelMultipleChoiceField(
        queryset=Defecto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = ReporteDiario
        fields = ['nombre_analista','turno','presentacion','lote','hora', 'fecha','clasificacion', 'cuenta_lbs', 'total_camaron','peso_neto', 'camarones_grandes', 'camarones_pequenos', 'marca_funda_manual', 'peso_bruto', 'peso_sin_funda_manual','porcentaje_glaseo','uniformidad','observaciones','correctivos']

    def __init__(self, *args, **kwargs):
        super(ReporteDiarioForm, self).__init__(*args, **kwargs)
        # Configura los campos como no requeridos
        self.fields['total_camaron'].required = False
        self.fields['camarones_grandes'].required = False
        self.fields['camarones_pequenos'].required = False
        self.fields['porcentaje_glaseo'].required = False
        self.fields['uniformidad'].required = False



 
class FundaForm(forms.ModelForm):
    class Meta:
        model = Funda
        fields = ['marca', 'peso_funda']



class PorcentajeDefectoForm(forms.ModelForm):
    defectos = [
        ("Rosado leve", "Rosado leve"),
        ("Deshidratado", "Deshidratado"),
        ("Picado", "Picado"),
        ("Dañados o piezas", "Dañados o piezas"),
        ("Mudado", "Mudado"),
        ("Suave o quebrado", "Suave o quebrado"),
        ("Mal descabezado", "Mal descabezado"),
        ("Sin telson", "Sin telson"),
        ("Cascara", "Cascara"),
        ("Corte profundo", "Corte profundo"),
        ("Falta de corte", "Falta de corte"),
        ("Intestino / vena", "Intestino / vena"),
        ("Semi crudo", "Semi crudo"),
        ("Pequeño", "Pequeño"),
        ("Otros", "Otros"),
    ]

    defecto = forms.ChoiceField(
        choices=defectos,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = PorcentajeDefecto
        fields = ['defecto', 'cantidad', 'porcentaje']


