#!/usr/bin/python3.4
# -*- encoding: utf-8 -*-

import os
import sys
import django
from datetime import datetime
from datetime import timedelta
import time
from seriecom import serial_w
from time import sleep
from datetime import datetime, timedelta
import glob
#from estadoarduino import buscarPorcesosActivos
from django.utils import timezone
from djangoPath import *


ahora = timezone.make_aware(datetime.now())
#ahora = datetime.now()
#fecha=now.strftime('%Y-%m-%d %H:%M:%S')

# Recupero procesos activos#####################################
def buscarPorcesosActivos():
    c = ControlProcesos.objects.filter(activo='True').values('id')
    ids =[]
    for i in range(len(c)):
        ids.append(c[i].get('id'))
    return ids

procesosActivos = buscarPorcesosActivos()

# FUNCION PARA CONSULTA E INSERSION DE TEMPERATURAS
def grabarTemperatura(procesoId,coccionId,fermentadorArduinoId,fermentadorId,sensorId):
	procesosTablas = ControlProcesos.objects.get(id=procesoId)
	fermentadoresTablas = Fermentadores.objects.get(id=fermentadorId)
	sensoresTablas = Sensores.objects.get(id=sensorId)

	# Instacio para insersion
	fermentadorId = Fermentadores.objects.get(id=fermentadoresTablas.id)
	arduinoId = Fermentadores.objects.get(id=fermentadoresTablas.id)
	coccionId = ControlProcesos.objects.get(id=procesosTablas.id)
	sensorId= Sensores.objects.get(id=sensoresTablas.id)
	
	arduinoid = str(fermentadorArduinoId - 1)
	

	try:
		serieout = serial_w('g',arduinoid)
		temp = serieout
		print(temp)

		if temp:
			if (int(temp == -127)):
				print("El sensor no está conectado")
			elif (int(temp) > 0 and int(temp) < 35):
				TemperaturasHistorial.objects.create(fermentador=fermentadorId, sensorId=sensorId,
					temperatura=temp,fechaSensado=ahora,coccionNumero=coccionId)
				print("Seguardaron los datos de sensado")
		else:
			print("El valor de temperatura es nulo, se vuelve a consultar a arduino")
			grabarTemperatura(procesoId,coccionId, fermentadorArduinoId, fermentadorId, sensorId)
	except:
		print("Ha ocurrido una excepcion, no se pudo recuperar el valor de temperatura")
	#print serieout
	


for procesoId in procesosActivos:
	datosProceso = ControlProcesos.objects.get(id=procesoId)

	coccionId = datosProceso.coccionNum
	sensorId= datosProceso.sensor_id
	fermentadorArduinoId = datosProceso.fermentador.arduinoId
	fermentadorId = datosProceso.fermentador_id	

	grabarTemperatura(procesoId,coccionId, fermentadorArduinoId, fermentadorId, sensorId)






