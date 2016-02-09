from django import forms
from tempcontrol.models import *
from django.contrib.admin import widgets 

#

class ControlPocesosCrearForm(forms.ModelForm):
	fechaInicio = forms.DateField(widget=forms.SelectDateWidget())
	fermentado1Fin = forms.DateField(widget=forms.SelectDateWidget())
	fermentado2Fin = forms.DateField(widget=forms.SelectDateWidget())
	maduradoFin = forms.DateField(widget=forms.SelectDateWidget())
	clarificadoFin = forms.DateField(widget=forms.SelectDateWidget())
	class Meta:
		model = ControlProcesos
		fields = ('fechaInicio','fermentador','sensor',
			'temperaturaPerfil','activo','fermentado1Fin','fermentado2Fin','maduradoFin','clarificadoFin')



class SensoresCrearFormm(forms.ModelForm):
	class Meta:
		model = Sensores
		fields = ('nombre','fermentador','mac','activo')



class PerfilesTempCrearForm(forms.ModelForm):
	class Meta:
		model = TemperaturasPerfiles
		fields = ('nombre','diasFermentado1','diasFermentado2',
			'diasMadurado','diasclarificado','temperaturas','descripcion')




	