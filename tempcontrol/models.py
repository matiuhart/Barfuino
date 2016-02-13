from django.db import models
from django import forms
#from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator,MinValueValidator,validate_comma_separated_integer_list

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
	temperaturas = models.CommaSeparatedIntegerField(max_length=9)#validators=[validate_comma_separated_integer_list('0,0,0')]
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
	sensor = models.ForeignKey(Sensores)
	temperaturaPerfil = models.ForeignKey(TemperaturasPerfiles,verbose_name='Perf. Temperatura')
	activo = models.BooleanField(default=True)
	fermentado1Fin = models.DateTimeField(verbose_name='Fermentado 1')
	fermentado2Fin = models.DateTimeField(verbose_name='Fermentado 2')
	maduradoFin = models.DateTimeField(verbose_name='Madurado')
	clarificadoFin = models.DateTimeField(verbose_name='Clarificado')
	fase = models.CharField(max_length=15,default='fermentacion1')


	def __unicode__(self):
		return "%s" %(self.coccionNum)

	class Meta:
		ordering = ["fermentador"]
		verbose_name_plural = "Control de Procesos"

# TABLA HISTORIAL DE TEMPERATURAS
class TemperaturasHistorial(models.Model):
	fermentador = models.ForeignKey(Fermentadores,verbose_name="Fermentador")
	sensorId = models.ForeignKey(Sensores,verbose_name="sensor")
	temperatura = models.DecimalField(max_digits=3, decimal_places=1)
	fechaSensado = models.DateTimeField(verbose_name='fecha de sensado')
	coccionNumero = models.ForeignKey(ControlProcesos)
	activo = models.BooleanField(default=True)

	def __str__(self):
		 return "%s,%s,%s,%s" %(self.fermentador.id,self.fermentador,self.fechaSensado,self.temperatura)

	
	class Meta:
		ordering = ["fermentador"]
		verbose_name_plural = "Historial de Temperaturas"

class Configuraciones(models.Model):
	temperaturaClarificado = models.DecimalField("Temperatura de Clarificado por Defecto",max_digits=3, decimal_places=1,null=True)
	temperaturaFinalizado = models.DecimalField("Temperatura de Finalizado por Defecto",max_digits=3, decimal_places=1,null=True)
	brewerMail = models. EmailField(max_length=100,null=True)








