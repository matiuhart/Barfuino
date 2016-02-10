from django.db import models
from django import forms
from datetime import datetime

class Sensores(models.Model):
	nombre = models.CharField(max_length=10)
	#fermentador = models.ForeignKey(Fermentadores,default='1')
	mac = models.CharField(max_length=20,blank=True)
	activo = models.BooleanField(default=False)

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ["nombre"]
		verbose_name_plural = "Sensores"

class Fermentadores(models.Model):
	nombre = models.CharField(max_length=20,unique=True)
	activo = models.BooleanField(default=False)
	sensor = models.ForeignKey(Sensores,default='1')


	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ["nombre"]
		verbose_name_plural = "Fermentadores"


class TemperaturasPerfiles(models.Model):
	nombre = models.CharField(max_length=20)
	diasFermentado1 = models.IntegerField(verbose_name='días 1er Fermentado')
	diasFermentado2 = models.IntegerField(verbose_name='días 2do Fermentado',default='0')
	diasMadurado = models.IntegerField(verbose_name='días Madurado')
	diasclarificado = models.IntegerField(verbose_name='días Clarificado')	
	temperaturas = models.CommaSeparatedIntegerField(max_length=9)
	descripcion = models.CharField(max_length=200,verbose_name='descripción')

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ["nombre"]
		verbose_name_plural = "Perfiles de Temperatura"


class ControlProcesos(models.Model):
	coccionNum = models.IntegerField(verbose_name='Nro. cocción',unique=True,blank=True,null=True)
	fechaInicio = models.DateTimeField(blank=True,null=True,verbose_name='Inicio de proceso')
	fermentador = models.ForeignKey(Fermentadores)
	sensor = models.ForeignKey(Sensores)
	temperaturaPerfil = models.ForeignKey(TemperaturasPerfiles,verbose_name='Perf. Temperatura')
	activo = models.BooleanField(default=True)
	fermentado1Fin = models.DateTimeField(verbose_name='Fermentado 1',blank=True, null=True)
	fermentado2Fin = models.DateTimeField(verbose_name='Fermentado 2',blank=True, null=True)
	maduradoFin = models.DateTimeField(verbose_name='Madurado',blank=True, null=True)
	clarificadoFin = models.DateTimeField(verbose_name='Clarificado',blank=True, null=True)


	def __unicode__(self):
		return "%s" %(self.coccionNum)

	class Meta:
		ordering = ["coccionNum"]
		verbose_name_plural = "Control de Procesos"


class TemperaturasHistorial(models.Model):
	fermentador = models.ForeignKey(Fermentadores,verbose_name="Fermentador")
	sensorId = models.ForeignKey(Sensores,verbose_name="sensor")
	temperatura = models.DecimalField(verbose_name=None, name=None, max_digits=4, decimal_places=2)
	fechaSensado = models.DateTimeField(verbose_name='fecha de sensado',blank=True, null=True)
	coccionNumero = models.ForeignKey(ControlProcesos,default='1')
	
	class Meta:
		ordering = ["fermentador"]
		verbose_name_plural = "Historial de Temperaturas"





