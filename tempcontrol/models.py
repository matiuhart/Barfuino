# -*- coding: UTF-8 -*-

from django.db import models
from django import forms
#from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator,MinValueValidator,validate_comma_separated_integer_list

# Clase con manager propio (Devuelve activos sin posibilidad de filtrar)
class miManager(models.Manager):
	def buscar_activos(self):
		return self.filter(activo=True)

# Clase con manager propio (Devuelve activos con posibilidad de filtrar)
class MiManagerActivos(models.Manager):
	def get_query_set(self):
		return super(MiManagerActivos,self).get_query_set().filter(activo=False)

# TABLA SENSORES
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

# TABLA FERMENTADORES
class Fermentadores(models.Model):
	nombre = models.CharField(max_length=20,unique=True)
	activo = models.BooleanField(default=False)
	sensor = models.ForeignKey(Sensores)
	arduinoId = models.IntegerField(verbose_name="Identificador en Arduino",validators=[MaxValueValidator(99),MinValueValidator(1)], default=1)
	# Defino mi manager para consultas precocinadas
	miManager = miManager()
	# Defino manager para verificar estado pasado como parametro con posibilidad de filtrado (query set)
	miManagerAct = MiManagerActivos()
	# Defino manager por defecto
	objects = models.Manager()


	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ["nombre"]
		verbose_name_plural = "Fermentadores"

# TABLA PERFILES DE TEMPERATURA
class TemperaturasPerfiles(models.Model):
	nombre = models.CharField(max_length=20)
	diasFermentado1 = models.IntegerField(verbose_name='días 1er Fermentado',validators=[MaxValueValidator(99),MinValueValidator(1)])
	diasFermentado2 = models.IntegerField(verbose_name='días 2do Fermentado',default='0',validators=[MaxValueValidator(99),MinValueValidator(0)])
	diasMadurado = models.IntegerField(verbose_name='días Madurado',validators=[MaxValueValidator(99),MinValueValidator(1)])
	diasclarificado = models.IntegerField(verbose_name='días Clarificado',validators=[MaxValueValidator(99),MinValueValidator(1)])	
	temperaturas = models.CommaSeparatedIntegerField(max_length=14)#validators=[validate_comma_separated_integer_list('0,0,0')]
	temperaturasFermentado1 = models.CommaSeparatedIntegerField(max_length=5,null=True)
	temperaturasFermentado2 = models.CommaSeparatedIntegerField(max_length=5,null=True)
	temperaturasMadurado = models.CommaSeparatedIntegerField(max_length=5,null=True)
	temperaturasClarificado = models.CommaSeparatedIntegerField(max_length=5,null=True)
	temperaturasFinalizado = models.CommaSeparatedIntegerField(max_length=5,null=True)	
	descripcion = models.CharField(max_length=200,verbose_name='descripción')

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ["nombre"]
		verbose_name_plural = "Perfiles de Temperatura"

# TABLA CONTROL DE PROCESOS
class ControlProcesos(models.Model):
	coccionNum = models.IntegerField(verbose_name='Nro. cocción',unique=True,validators=[MaxValueValidator(400),MinValueValidator(1)])
	fechaInicio = models.DateTimeField(blank=True,null=True,verbose_name='Inicio de proceso')
	fermentador = models.ForeignKey(Fermentadores)
	#sensor = models.ForeignKey(Sensores)
	temperaturaPerfil = models.ForeignKey(TemperaturasPerfiles,verbose_name='Perf. Temperatura')
	activo = models.BooleanField(default=True)
	fermentado1Fin = models.DateTimeField(verbose_name='Fermentado 1')
	fermentado2Fin = models.DateTimeField(verbose_name='Fermentado 2',blank=True,null=True,default="")
	maduradoFin = models.DateTimeField(verbose_name='Madurado')
	clarificadoFin = models.DateTimeField(verbose_name='Clarificado')
	fase = models.CharField(max_length=15,default='fermentado1')

	class Meta:
		ordering = ["fermentador"]
		verbose_name_plural = "Control de Procesos"

	
	def __str__(self):
		return "%s,%s,%s,%s,%s,%s,%s," %(self.coccionNum, self.fechaInicio, self.fermentado1Fin, 
			self.fermentado2Fin, self.maduradoFin,self.clarificadoFin, self.fase)
	

# TABLA HISTORIAL DE TEMPERATURAS
class TemperaturasHistorial(models.Model):
	fermentador = models.ForeignKey(Fermentadores,verbose_name="Fermentador")
	sensorId = models.ForeignKey(Sensores,verbose_name="sensor")
	temperatura = models.DecimalField(max_digits=3, decimal_places=1)
	fechaSensado = models.DateTimeField(verbose_name='fecha de sensado')
	coccionNumero = models.ForeignKey(ControlProcesos)
	activo = models.BooleanField(default=True)

	
	def __str__(self):
		 return "%s,%s,%s,%s,%s" %(self.coccionNumero,self.fermentador.id,self.fermentador,self.fechaSensado,self.temperatura)
	
	
	class Meta:
		ordering = ["fermentador"]
		verbose_name_plural = "Historial de Temperaturas"

class Configuraciones(models.Model):
	temperaturaClarificado = models.DecimalField("Temperatura de Clarificado por Defecto",max_digits=3, decimal_places=1,null=True)
	temperaturaFinalizado = models.DecimalField("Temperatura de Finalizado por Defecto",max_digits=3, decimal_places=1,null=True)
	brewerMail = models. EmailField(max_length=100,null=True)
