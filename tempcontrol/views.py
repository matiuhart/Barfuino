# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from datetime import datetime
from datetime import timedelta
import time
from django.utils import timezone


def sumar_mins(minutos=0):
		fecha = datetime.now() + timedelta(minutes=minutos)
		nueva_fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
		return nueva_fecha

def restart_mins(minutos=0):
		fecha = datetime.now() - timedelta(minutes=minutos)
		nueva_fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
		return nueva_fecha

# Vista para el home
def home(request):
	start_date = restart_mins(4320)
	end_date = datetime.now()
	
	registrosTemperaturas = TemperaturasHistorial.objects.order_by('id').filter(fermentador__activo__exact=True).filter(fechaSensado__range=(start_date,end_date)).values()
	
	fermentadorbtn = {}

	grafica = []
	# Armo array para grafica
	for i in range(len(registrosTemperaturas)):
		valores=[]
		fecha = registrosTemperaturas[i]['fechaSensado'].astimezone(timezone.get_current_timezone())
		valores.append(fecha.strftime("%Y-%m-%d %H:%M:%S"))
		valores.append(str(registrosTemperaturas[i]['temperatura']))
		grafica.append(valores)
	
	# Recupero fermentadores activos y su ultima temperatura para botones
	try:
		cocciones=[]

		for coccion in range(len(registrosTemperaturas)):
		    cocciones.append(registrosTemperaturas[coccion]['coccionNumero_id'])
		    cocciones = list(set(cocciones))
		
		for coccion in cocciones:
			data = {}
			ultimo = TemperaturasHistorial.objects.filter(coccionNumero_id=coccion).latest('fechaSensado')
			data.update({ultimo.fermentador.nombre:str(ultimo.temperatura)})
			fermentadorbtn.update(data)
	except:
		fermentadorbtn = ""
	return render(request, 'home.html', {'values': grafica, 'fermentadorbtn':fermentadorbtn})


# Vista para crear perfil de temperatura
def crearPerfTemp(request):
	if request.POST:
		form = PerfilesTempCrearForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('home.html')
	else:
		form = PerfilesTempCrearForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render_to_response('perfilesTemp.html', args)


# Vista para visualizar procesos en curso
def procesosActivos(request):
	activos = ControlProcesos.objects.filter(activo=True)
	return render(request, 'activos.html', {'activos':activos})


def pruebas(request):
	# Funcion para calculo de dias
	def sumar_dias(dias=0):
		fecha = datetime.now() + timedelta(days=dias)
		nueva_fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
		return nueva_fecha

	if request.POST:
		form = ControlPocesosCrearForm(request.POST)
		if form.is_valid():
			perfilNombre = request.GET['temperaturaPerfil']
			fermentadorNombre = request.GET['fermentador']
			coccionNumero = request.GET['coccionNum']

			
			perfilTablas = TemperaturasPerfiles.objects.get(nombre=perfilNombre)
			fermentadorTablas = Fermentadores.objects.get(nombre=fermentadorNombre)
			
			# Calculo las fechas de finalizado de cada fase en base a dias especificados en TemperaturasPerfiles
			finFermentado1 = sumar_dias(perfilTablas.diasFermentado1)
			finFermentado2 = sumar_dias(perfilTablas.diasFermentado1 + perfilTablas.diasFermentado2)
			finMadurado = sumar_dias(perfilTablas.diasFermentado1 + perfilTablas.diasFermentado2 + perfilTablas.diasMadurado)
			finClarificado = sumar_dias(perfilTablas.diasFermentado1 + perfilTablas.diasFermentado2 + 
				perfilTablas.diasMadurado + perfilTablas.diasclarificado)

			#Instancio para insersion en ControlProcesos
			s=Sensores.objects.get(id=fermentadorTablas.sensor.id)
			f=Fermentadores.objects.get(id=fermentadorTablas.id)
			p=TemperaturasPerfiles.objects.get(id=perfilTablas.id)

			#Actualizo Fermentadores.activo a True para que no sea mostrado nuevamente
			Fermentadores.objects.filter(id=fermentadorTablas.id).update(activo=True)
			
			# Inserto los datos para nuevo proceso en ControlProcesos
			ControlProcesos.objects.create(coccionNum=coccionNumero,fechaInicio=datetime.now(),fermentador=f,
				sensor=s,temperaturaPerfil=p,activo=True,fermentado1Fin=finFermentado1,
				fermentado2Fin=finFermentado2,maduradoFin=finMadurado,clarificadoFin=finClarificado)

			form.save()
			return HttpResponseRedirect('home.html')
	

	else:
		form = ControlPocesosCrearForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render_to_response('pruebas.html', args)

###############################################################################################################

# Vista para aplicar perfil de temperatura
def aplicarPerfilTemp(request):
	
	# Funcion para calculo de dias
	def sumar_dias(dias=0):
		fecha = datetime.now() + timedelta(days=dias)
		nueva_fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
		return nueva_fecha
	
	perfiles = TemperaturasPerfiles.objects.all()
	fermentadores = Fermentadores.objects.filter(activo=False)
	error = ""
	# Siel metodo es GET y contiene datos, los recupero y realizo la insersion a BD
	if request.method == 'GET':
		
		if 'perfil' in request.GET and 'fermentador' in request.GET and 'coccion' in request.GET:
			perfilNombre = request.GET['perfil']
			fermentadorNombre = request.GET['fermentador']
			coccionNumero = request.GET['coccion']
			
			if (not fermentadorNombre) and (not fermentadorNombre) and (not coccionNumero):
				error = "Error!!Verificá que no falten datos a ingresar"
			else:
				perfilTablas = TemperaturasPerfiles.objects.get(nombre=perfilNombre)
				fermentadorTablas = Fermentadores.objects.get(nombre=fermentadorNombre)
				
				# Calculo las fechas de finalizado de cada fase en base a dias especificados en TemperaturasPerfiles
				finFermentado1 = sumar_dias(perfilTablas.diasFermentado1)
				finFermentado2 = sumar_dias(perfilTablas.diasFermentado1 + perfilTablas.diasFermentado2)
				finMadurado = sumar_dias(perfilTablas.diasFermentado1 + perfilTablas.diasFermentado2 + perfilTablas.diasMadurado)
				finClarificado = sumar_dias(perfilTablas.diasFermentado1 + perfilTablas.diasFermentado2 + 
					perfilTablas.diasMadurado + perfilTablas.diasclarificado)

				#Instancio para insersion en ControlProcesos
				s=Sensores.objects.get(id=fermentadorTablas.sensor.id)
				f=Fermentadores.objects.get(id=fermentadorTablas.id)
				p=TemperaturasPerfiles.objects.get(id=perfilTablas.id)

				#Actualizo Fermentadores.activo a True para que no sea mostrado nuevamente
				Fermentadores.objects.filter(id=fermentadorTablas.id).update(activo=True)
				
				# Inserto los datos para nuevo proceso en ControlProcesos
				ControlProcesos.objects.create(coccionNum=coccionNumero,fechaInicio=datetime.now(),fermentador=f,
					sensor=s,temperaturaPerfil=p,activo=True,fermentado1Fin=finFermentado1,
					fermentado2Fin=finFermentado2,maduradoFin=finMadurado,clarificadoFin=finClarificado)

				return HttpResponseRedirect('/')
							
		else:
			args = {}
			args['perfiles'] = perfiles
			args['fermentadores'] = fermentadores
			
			return render_to_response('aplicarperfil.html', args)

'''
# GRAFICA PYGAL

import pygal
# Vista para pruebas	
from pygal.style import DefaultStyle
from pygal.style import NeonStyle
from pygal.style import LightGreenStyle
from datetime import datetime, timedelta

def pruebas(request):
	start_date = restart_mins(4320)
	end_date = datetime.now()

	registrosTemperaturas = TemperaturasHistorial.objects.order_by('id').filter(fermentador__activo__exact=True).filter(fechaSensado__range=(start_date,end_date)).values()

	datetimeline = pygal.DateTimeLine(
		tooltip_border_radius=10,
		height=300,
		style=LightGreenStyle,
		x_label_rotation=10, truncate_label=-1,
		x_value_formatter=lambda dt: dt.strftime('%d/%M/%Y %I:%M:%S'))

	grafica = []
	# Armo array para grafica
	for i in range(len(registrosTemperaturas)):
		valores=[]
		fecha = registrosTemperaturas[i]['fechaSensado'].astimezone(timezone.get_current_timezone())
		valores.append(fecha.strftime("%Y-%m-%d %H:%M:%S"))
		valores.append(str(registrosTemperaturas[i]['temperatura']))
		grafica.append(valores)

	datetimeline.add(
		"Serie", [
    	(datetime(2013, 1, 2, 12, 0), 20),
    	(datetime(2013, 1, 12, 14, 30, 45), 30),
    	(datetime(2013, 2, 2, 6), 18),
    	(datetime(2013, 2, 22, 9, 45), 21)])
	datetimeline.add(
    	"prueba",[
    	(datetime(2013, 2,3, 10, 0),10),
    	(datetime(2013, 1, 10, 14, 30, 45), 11),
    	(datetime(2013, 2, 2, 6), 10),
    	(datetime(2013, 2, 22, 9, 45), 9)])

	return render_to_response('pruebas.html', {'line_chart':datetimeline.render()})
'''

