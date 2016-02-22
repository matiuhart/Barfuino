#!/usr/bin/python3.4
# -*- encoding: utf-8 -*-

import os
import sys
import django
from datetime import datetime
from datetime import timedelta
import time


sys.path.append("/media/mati/cc6ff8ae-312f-44e3-b081-cca83b3f12de/mati/bin/django/barfuino")
os.environ["DJANGO_SETTINGS_MODULE"] = "barfuino.settings"
django.setup()
from tempcontrol.models import *

'''
Estas funciones realizan el monitoreo de las temperaturas en los fermentadores. Verifica en la base de datos si el tiempo del ultimo 
sensado de temperatura es menor a 45 minutos o si la temperatura se mantuvo por arriba de la correspondiente por mas del tiempo mencionado anterioirmente, 
de ser mayor en cualquiera de los dos casos, envia una alerta via email con el aviso de problemas de sensado
'''



# Resta de minutos de medicion anterior
def RestarMinutos(minutos=0):
    hora = datetime.now() - timedelta(minutes=minutos)
    nuevaHora = hora.strftime("%Y-%m-%d %H:%M:%S")
    return nuevaHora

# Recupero procesos activos#####################################
def buscarPorcesosActivos():
	c = ControlProcesos.objects.filter(activo='True').values('id')
	ids =[]
	for i in range(len(c)):
	    ids.append(c[i].get('id'))

	return ids
		
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
			temperaturaFase = datosConfiguraciones.temperaturaClarificado
	elif (faseActual == "finalizado"):
		try:
			temperaturaFase = temperaturas.split(",")[4]
		except:
			temperaturaFase = datosConfiguraciones.temperaturaFinalizado

	print("\n PROCESOID: " + str(controlProcesoId) + "\n FERMENTADOR: " + str(datosProceso.fermentador) + "\n TEMPERATURA: " + str(temperaturaFase))
	
	# Recupero temperaturas sensadas de los ultimos 45' para el fermentador actual
	ultimasTemperaturas = TemperaturasHistorial.objects.filter(fermentador=fermentadorId).filter(fechaSensado__gte=RestarMinutos(45)).values('temperatura')

	# Si encuentro valores de sensado, verifico si las ultimas 3 temperaturas son mayores que la correspondiente a la fase, si esto
	# sucede o no se encuentran valores de sensado, se envia una alerta. De lo contrario no se realiza ninguna accion
	if (ultimasTemperaturas):
		temperatura1,temperatura2,temperatura3 = ultimasTemperaturas[0].get('temperatura'), ultimasTemperaturas[1].get('temperatura'),ultimasTemperaturas[2].get('temperatura')
		CUERPO =""
		ASUNTO =""
		#si las ultimas 3 temperaturas son mayores a la de la fase envia alerta
		if ((temperatura1 > int(temperaturaFase)) & (temperatura2 > int(temperaturaFase)) & (temperatura3 > int(temperaturaFase))):
			CUERPO = 'En los ultimos 45 min las temperaturas exeden los %s° C seteados, las ultimas mediciones son %s° C'%(temperaturaFase,temperaturas)
			ASUNTO = 'Temperaturas Altas en Fermentador %s'%(datosProceso.fermentador)

			#EnviarCorreo(ASUNTO,CUERPO)
		else:
			print("\n NO HAY ALERTAS \n")
			
	else:
		CUERPO = 'En los ultimos 45 min las temperaturas no pudieron ser sensadas en el fermentador %s, por favor verifique el sistema'%(datosProceso.fermentador)
		ASUNTO = 'Problema de Sensado de Temperaturas en Fermentador %s'%(datosProceso.fermentador)

		#EnviarCorreo(ASUNTO,CUERPO)

	print("\n FASE ACTUAL: " + faseActual)
	if (CUERPO):
		print("\n CUERPO: " + CUERPO)
		print("\n ASUNTO: " + ASUNTO)
		print("------------------------------------------------------------------------------------------------------------------------------")


