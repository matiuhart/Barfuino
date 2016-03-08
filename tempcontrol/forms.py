from django import forms
from tempcontrol.models import *
from django.contrib.admin import widgets
from django.forms import BaseModelFormSet

# Formulario de creacion de Control Proceso nuevo
class ControlPocesosCrearForm(forms.ModelForm):
	#fechaInicio = forms.DateField(widget=forms.SelectDateWidget())
	#fermentado1Fin = forms.DateField(widget=forms.SelectDateWidget())
	#fermentado2Fin = forms.DateField(widget=forms.SelectDateWidget())
	#maduradoFin = forms.DateField(widget=forms.SelectDateWidget())
	#clarificadoFin = forms.DateField(widget=forms.SelectDateWidget())
	
	class Meta:
		model = ControlProcesos
		fields = ('coccionNum','fermentador','temperaturaPerfil')
		#fields = ('fechaInicio','fermentador','sensor','temperaturaPerfil','activo','fermentado1Fin','fermentado2Fin','maduradoFin','clarificadoFin')


class ControlPocesosForm(forms.ModelForm):
    class Meta:
        model = ControlProcesos
        fields = ('coccionNum','fechaInicio','fermentador','temperaturaPerfil','activo','fermentado1Fin','fermentado2Fin','maduradoFin','clarificadoFin')
    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        hide_condition = kwargs.pop('hide_condition',None)
        super(ControlPocesosForm, self).__init__(*args, **kwargs)
        if hide_condition:
            self.fields['fechaInicio'].widget = HiddenInput()
            self.fields['fermentado1Fin'].widget = HiddenInput()
            self.fields['fermentado2Fin'].widget = HiddenInput()
            self.fields['maduradoFin'].widget = HiddenInput()
            self.fields['clarificadoFin'].widget = HiddenInput()
            #self.fields['sensor'].widget = HiddenInput()
            # or alternately:  del self.fields['fieldname']  to remove it from the form altogether.
    class BaseAuthorFormSet(BaseModelFormSet):
	    def __init__(self, *args, **kwargs):
	    	super(BaseAuthorFormSet, self).__init__(*args, **kwargs)
	    	self.queryset = Fermentadores.objects.filter(activo=True)




class SensoresCrearFormm(forms.ModelForm):
	class Meta:
		model = Sensores
		fields = ('nombre','mac','activo')

class PerfilesTempCrearForm(forms.ModelForm):
	class Meta:
		model = TemperaturasPerfiles
		fields = ('nombre','diasFermentado1','diasFermentado2',
			'diasMadurado','diasclarificado','temperaturas','descripcion')


class PerfilTempForm(forms.ModelForm):
	class Meta:
		model = TemperaturasPerfiles
		fields = ('nombre','diasclarificado')

class FermentadorForm(forms.ModelForm):
	class Meta:
		model = Fermentadores
		fields = ('id','nombre',)


	