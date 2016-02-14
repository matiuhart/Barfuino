#!/usr/bin/python3.4
# -*- encoding: utf-8 -*-

import os
import sys
import django

sys.path.append("/home/mati/bin/django/barfuino")
os.environ["DJANGO_SETTINGS_MODULE"] = "barfuino.settings"
django.setup()

'''
Estas funciones realizan el monitoreo de las temperaturas en los fermentadores. Verifica en la base de datos si el tiempo del ultimo 
sensado de temperatura es menor a 45 minutos o si la temperatura se mantuvo por arriba de la correspondiente por mas del tiempo mencionado anterioirmente, 
de ser mayor en cualquiera de los dos casos, envia una alerta via email con el aviso de problemas de sensado
'''


from tempcontrol.models import *

# Recupero procesos activos#####################################
def buscarPorcesosActivos():
	c = ControlProcesos.objects.filter(activo='True').values('id')
	ids =[]
	for i in range(len(c)):
	    ids.append(c[i].get('id'))

	for id in ids:
		controlTemperaturaFase(id)
		
###############################################################

def controlTemperaturaFase(id):
	controlProcesoId = id
	datosProceso = ControlProcesos.objects.get(id=controlProcesoId)
	datosConfiguraciones = Configuraciones.objects.get()

	# Recupero id de fermentador, fase actual, temperaturas del perfil aplicado,
	fermentadorId = datosProceso.fermentador_id
	faseActual = datosProceso.fase
	temperaturas = datosProceso.temperaturaPerfil.temperaturas
	
	# Compruebo la fase actual y aplico las temperaturas seteadas en el perfil,
	# si no se seteó temperatura de clarificado o finalizado se toman los valores de la config general 
	temperaturaFase = 0
	if (faseActual == "fermentado1"):
		temperaturaFase = temperaturas.split(",")[0]
	elif (faseActual == "fermentado2"):
		temperaturaFase = temperaturas.split(",")[1]
	elif (faseActual == "madurado"):
		temperaturaFase = temperaturas.split(",")[2]
	elif (faseActual == "clarificado"):
		try:
			temperaturaFase = temperaturas.split(",")[3]
		except:
			print("Seteando temperatura de clarificado desde configuraciones")
			temperaturaFase = datosConfiguraciones.temperaturaClarificado
	elif (faseActual == "finalizado"):
		try:
			temperaturaFase = temperaturas.split(",")[4]
		except:
			print("Seteando temperatura de finalizado desde configuraciones")
			temperaturaFase = datosConfiguraciones.temperaturaFinalizado

	print("Temperatura: " + str(temperaturaFase) + " ProcesoId :" + str(controlProcesoId))
	#return temperaturaFase


