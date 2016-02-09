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


def procesosActivos(request):
	activos = ControlProcesos.objects.filter(activo=True)
	return render(request, 'activos.html', {'activos':activos})


