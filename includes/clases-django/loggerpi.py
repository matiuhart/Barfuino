#!/usr/bin/python3.4
# -*- encoding: utf-8 -*-

import os
import sys
import django
from datetime import datetime
from datetime import timedelta
import time
from tempcontrol.models import *
from seriecom import *
from time import sleep
from datetime import datetime, timedelta
import glob
from estadoarduino import buscarPorcesosActivos
from django.utils import timezone


ahora = timezone.make_aware(datetime.now())
#fecha=now.strftime('%Y-%m-%d %H:%M:%S')

procesosActivos = buscarPorcesosActivos()

# FUNCION PARA CONSULTA E INSERSION DE TEMPERATURAS
def grabarTemperatura(procesoId,coccionId,fermentadorArduinoId,fermentadorId,sensorId):
	procesosTablas = ControlProcesos.objects.get(id=procesoId)
	fermentadoresTablas = Fermentadores.objects.get(id=fermentadorId)
	sensoresTablas = Sensores.objects.get(id=sensorId)

	# Instacio para insersion
	fermentadorId = Fermentadores.objects.get(id=fermentadoresTablas.id)
	fermentadorArduinoId = Fermentadores.objects.get(id=fermentadoresTablas.id)
	coccionId = ControlProcesos.objects.get(id=procesosTablas.id)
	sensorId= Sensores.objects.get(id=sensoresTablas.id)
	
	serieout = serial_w('g',str(fermentadorArduinoId))
	time.sleep(2.5)
	#print serieout
	temp = int(serieout)
	print(temp)
	#print fermentadorId[0][0]
	if (temp > 0 and temp < 35 and temp != ""):
		TemperaturasHistorial.objects.create(fermentador=fermentadorId, sensorId=sensorId,
			temperatura=temp,fechaSensado=ahora,coccionNumero=coccionId)
	else:
		temp_hist(fermentador)


for proceso in procesosActivos:
	datosProceso = ControlProcesos.objects.get(id=controlProcesoId)

	procesoId = datosProceso.id
	coccionId = datosProceso.coccionNum
	sensorId= datosProceso.sensor_id
	fermentadorArduinoId = datosProceso.fermentador.arduinoId	

	grabarTemperatura(procesoId,coccionId, fermentadorArduinoId, fermentadorId, sensorId)





