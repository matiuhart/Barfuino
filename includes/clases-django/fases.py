#!/usr/bin/python3.4
# -*- encoding: utf-8 -*-

import os
import sys
import django
from datetime import datetime
from datetime import timedelta
import time
from django.utils import timezone
from tempcontrol.models import *
from seriecom import *
from notificaciones import *
from estadoarduino import *

sys.path.append("/home/mati/bin/django/barfuino")
os.environ["DJANGO_SETTINGS_MODULE"] = "barfuino.settings"
django.setup()


# Clase para comprobacion de fase actual
class ComprobarFase(object):
    fase = ""
    def __init__(self,ControlProcesosId):
        self.estadoId=ControlProcesosId
        ComprobarFase.datosProceso = ControlProcesos.objects.get(id=self.estadoId)

    def faseActual(self):
        faseActual = ComprobarFase.datosProceso.fase
        return faseActual
        

##### CLASE DE CAMBIO
class CambiarFase(object):
    ahora = timezone.make_aware(datetime.now())
    temperaturas = ['']

    def __init__(self,produccionEstadoId):
        self.estadoId = produccionEstadoId
        CambiarFase.datosProceso = ControlProcesos.objects.get(id=self.estadoId)
        CambiarFase.datosConfiguraciones = Configuraciones.objects.get()

        CambiarFase.fermentadorId = self.datosProceso.fermentador_id
        CambiarFase.fermentadorNombre = self.datosProceso.fermentador
        CambiarFase.arduinoId = self.datosProceso.fermentador.arduinoId
        CambiarFase.temperaturas = self.datosProceso.temperaturaPerfil.temperaturas
        CambiarFase.fase = self.datosProceso.fase
        CambiarFase.fermentado1 = self.datosProceso.fermentado1Fin
        CambiarFase.fermentado2 = self.datosProceso.fermentado2Fin
        CambiarFase.madurado = self.datosProceso.maduradoFin
        CambiarFase.clarificado = self.datosProceso.clarificadoFin
        
    def fermentado_1_(self):

        if CambiarFase.ahora > CambiarFase.fermentado1:
            if (CambiarFase.fermentado2 is None):
                #Actualizo la fase del proceso
                ControlProcesos.objects.filter(id=self.estadoId).update(fase="madurado")

                # Escribo la nueva temperatura en el puerto serie de arduino                
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
                return "madurado"
            # Cambio a fermentado 2
            else:
                ControlProcesos.objects.filter(id=self.estadoId).update(fase="fermentado2")

                # Escribo la nueva temperatura en el puerto serie de arduino                
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[1]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[1]))
            return "fermentado2"
        #Mantengo fermentado 1
        else:
            #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[0]))
            print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[0]))
            return "fermentado1"

    def fermentado_2_(self):
        # Cambio a madurado
        if CambiarFase.fermentado2:
            if CambiarFase.ahora > CambiarFase.fermentado2:
                ControlProcesos.objects.filter(id=self.estadoId).update(fase="madurado")

                # Escribo la nueva temperatura en el puerto serie de arduino   
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
                return "madurado"
            # Mantengo fermentado 2
            else:
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[1]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[1]))
                return "fermentado2"
        return "sin fermentado 2"

    def madurado_(self):
        # Cambia a clarificado
        if CambiarFase.ahora > CambiarFase.madurado:
            ControlProcesos.objects.filter(id=self.estadoId).update(fase="clarificado")
            try:
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[3]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[3]))
            except:
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaClarificado))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaClarificado))
            return "clarificado"
        # Sigue en madurado
        else:
            #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
            print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
            return "madurado"

    def clarificado_(self):
        # Cambia a finalizado
        if CambiarFase.ahora > CambiarFase.clarificado:
            ControlProcesos.objects.filter(id=self.estadoId).update(fase="finalizado")
            try:
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[4]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[4]))
            except:
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaFinalizado))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaFinalizado))
            return "finalizado"
        # Sigue en clarificado
        else:
            try:
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[3]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[3]))
            except:
                #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaClarificado))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaClarificado))
            return "clarificado"

    def finalizado_(self):
        try:
            serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[4]))
            print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[4]))

        except:
            #serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaFinalizado))
            print('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaFinalizado))
        return "finalizado"


            
            


'''            
0 ferm1
1 ferm2
2 Mad
3 clar
4 final
'''
# FUNCION PARA MONITOREO
def MonitorEstados(ControlProcesosId):
    estadoid = ControlProcesosId
    faseEstado = ComprobarFase(ControlProcesosId)
    faseCambio = CambiarFase(ControlProcesosId)
    faseActual = faseEstado.faseActual()

    print ("Fase actual: " + str(faseActual))

    if (faseActual == 2):
        fermentacion1 = faseCambio.fermentacion_1()

        print ("Cambio de fase?: " + str(fermentacion1))

        if (fermentacion1 == 0):
            print("Esta en fermentacion_1 y se mantiene fase en estadoid %s"%(estadoid))
        elif (fermentacion1 == 1):
            print ("Se realiza cambio a fase fermentacion_2 en estadoid %s"%(estadoid))
        elif (fermentacion1 == 2):
            print ("Se realiza cambio a fase maduracion en estadoid %s"%(estadoid))
        else:
            print ("No es posible determinar el fin de la fermentacion 1 en estadoid %s"%(estadoid))

    elif (faseActual == 3):
        fermentacion2 = faseCambio.fermentacion_2()
        print ("Cambio de fase?: " + str(fermentacion2))

        if (fermentacion2 == 0):
            print ("Esta en fermentacion_2 y se mantiene fase en estadoid %s"%(estadoid))
        elif (fermentacion2 == 1):
            print ("Se realiza cambio a fase maduracion en estadoid %s"%(estadoid))
        else:
            print ("No es posible determinar el fin de la fermentacion 2 en estadoid %s"%(estadoid))

    elif (faseActual == 4):
        maduracion = faseCambio.maduracion()
        print ("Cambio de fase?: " + str(maduracion))

        if (maduracion == 0):
            print ("Esta en maduracion y se mantiene fase en estadoid %s"%(estadoid))
        elif (maduracion == 1):
            print ("Fin de maduracion")
        else:
            print ("No es posible determinar el fin de la maduracion en estadoid %s"%(estadoid))

    elif (faseActual == 5):
        print ("Proceso finalizado, se mantiene la temperatura de proceso finalizado en estadoid %s"%(estadoid))

# FUNCION DE PRUEBAS
def BuscarActivos():
    query ="SELECT id FROM ControlProcesos WHERE activo = 'T'"
    consulta = MysqlQuery(query)
    activas = consulta.runQueryAsBasic()
    for row in activas:
        MonitorEstados(row)

BuscarActivos()
