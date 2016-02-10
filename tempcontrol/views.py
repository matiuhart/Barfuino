from django.shortcuts import render, render_to_response
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf


# Create your views here.
def hola(request):
	return render(request,'base.html')

def home(request):
	activos = ControlProcesos.objects.filter(activo=True)
	return render(request, 'home.html', {'activos':activos,'values': [['foo', 32], ['bar', 64], ['baz', 96]]})

def pruebas(request):
	if request.POST:
		form = ControlPocesosCrearForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = ControlPocesosCrearForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render_to_response('pruebas.html', args)



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


def aplicarPerfilTemp(request):
	perfiles = TemperaturasPerfiles.objects.all()
	fermentadores = Fermentadores.objects.filter(activo=False)
	error = ""
	if request.method == 'GET':
		if 'perfil' in request.GET and 'fermentador' in request.GET:
			perfilNombre = request.GET['perfil']
			fermentadorNombre = request.GET['fermentador']
			if (not fermentadorNombre) and (not fermentadorNombre):
				error = "Faltan valores en la peticion"
			else:
				perfilTablas = TemperaturasPerfiles.objects.get(nombre=perfilNombre)
				fermentadorTablas = Fermentadores.objects.get(nombre=fermentadorNombre)

				return render_to_response('aplicarperfil.html', {'pTablas':perfilTablas,'fTablas':fermentadorTablas,
					'perfil':perfilNombre,'fermentador':fermentadorNombre,'error':error})

				#return render_to_response('aplicarperfil.html', {'perfil':perfilNombre,'fermentador':fermentadorNombre,'error':error})
		else:
			return render_to_response('aplicarperfil.html', {'perfiles':perfiles, 'fermentadores':fermentadores})
		
	#return render_to_response('aplicarperfil.html')

def procesosActivos(request):
	activos = ControlProcesos.objects.filter(activo=True)
	return render(request, 'activos.html', {'activos':activos})


	


'''
def aplicarPerfilTemp(request):
	perfiles = TemperaturasPerfiles.objects.all()
	fermentadores = Fermentadores.objects.filter(activo=False)
	if request.POST:
		form = PerfilesTempCrearForm(request.POST)
		if form.is_valid():
			#insertar en bd
	else:
		return render_to_response('aplicarperfil.html', {'perfiles':perfiles, 'fermentadores':fermentadores})
	
	return render_to_response('aplicarperfil.html')




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

