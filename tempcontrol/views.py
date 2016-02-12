from django.shortcuts import render, render_to_response
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from datetime import datetime
from datetime import timedelta
import time
import json

def sumar_mins(minutos=0):
		fecha = datetime.now() + timedelta(minutes=minutos)
		nueva_fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
		return nueva_fecha


# Vista para el home
def home(request):
	grafica = [[sumar_mins(5), 25,34,10], [sumar_mins(8), 18,20,21], [sumar_mins(10), 17,19,10], [sumar_mins(17), 16,15,13], [sumar_mins(11), 15,17,10], [sumar_mins(50), 10,9,10]]
	

	fermentadoresActivos=Fermentadores.objects.values('nombre','id').filter(activo=True)
	fermentadores = {}
	for i in range(len(fermentadoresActivos)):
		temperatura =TemperaturasHistorial.objects.order_by('-fechaSensado').filter(fermentador=fermentadoresActivos[i]['id']).values('fechaSensado','fermentador','temperatura')[0]
		fermentadores[fermentadoresActivos[i]['nombre']] = str(temperatura.get('temperatura'))
	fermentadorbtn = []
	temperaturabtn = []
	
	for boton in fermentadores:
		fermentadorbtn.append(fermentadores[boton][0])
		temperaturabtn.append(fermentadores[boton][1])
	


	return render(request, 'home.html', {'values': grafica, 'fermentadorbtn':fermentadorbtn, 'temperaturabtn':temperaturabtn })

'''
fermentadorbtn = []
	temperaturabtn = []

	for boton in fermentadores:
		fermentadorbtn.append(fermentadores[boton][0])
		temperaturabtn.append(int(fermentadores[boton][1])
'''
	

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
		

# Vista para pruebas	
def pruebas(request):
	if request.POST:
		perfilForm = PerfilTempForm(request.POST)
		fermentadorForm = FermentadorForm(request.POST)
		if perfilForm.is_valid() and fermentadorForm.is_valid:
			perfilForm.save()
			fermentadorForm.save()
			return HttpResponseRedirect('/')
	else:
		perfilForm = PerfilTempForm()
		fermentadorForm = FermentadorForm()

	args = {}
	args.update(csrf(request))
	args['perfilForm'] = perfilForm
	args['fermentadorForm'] = fermentadorForm

	
	return render_to_response('pruebas.html', args)



'''
#### EJEMPLO PARA METODO POST
def contactos(request):
	if request.method == 'POST':
		form = FormularioContactos(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(cd['asunto'],cd['mensaje'],cd.get('email',
				'noreply@mtu-it.com.ar'),['siteowner@mtu-it.com.ar'])
			return render_to_response('gracias.html',{'mensaje':cd.get('mensaje'), 
				'asunto':cd.get('asunto'),'email':cd.get('email')})
	else:
		form = FormularioContactos(initial={'asunto':"que buen sitio!",
			'email':"mi@mail.com",'mensaje':"sarasaaaaaaaaaaa"})
	return render(request,'formulario-contactos.html',{'form':form})
'''

