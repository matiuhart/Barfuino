#!/usr/bin/python3.4
# -*- encoding: utf-8 -*-

import os
import sys
import django
from datetime import datetime
from datetime import timedelta
import time
from django.utils import timezone
from seriecom import *
from notificaciones import *
#from estadoarduino import *
from djangoPath import *


# Recupero procesos activos#####################################
def buscarPorcesosActivos():
    c = ControlProcesos.objects.filter(activo='True').values('id')
    ids =[]
    for i in range(len(c)):
        ids.append(c[i].get('id'))
    return ids


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
    #ahora = datetime.now()
    temperaturas = ['']

    def __init__(self,produccionEstadoId):
        self.estadoId = produccionEstadoId
        CambiarFase.datosProceso = ControlProcesos.objects.get(id=self.estadoId)
        CambiarFase.datosConfiguraciones = Configuraciones.objects.get()

        CambiarFase.fermentadorId = self.datosProceso.fermentador_id
        CambiarFase.fermentadorNombre = self.datosProceso.fermentador
        CambiarFase.arduinoId = self.datosProceso.fermentador.arduinoId - 1
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
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
                return "madurado"
            # Cambio a fermentado 2
            else:
                ControlProcesos.objects.filter(id=self.estadoId).update(fase="fermentado2")

                # Escribo la nueva temperatura en el puerto serie de arduino                
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[1]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[1]))
            return "fermentado2"
        #Mantengo fermentado 1
        else:
            serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[0]))
            print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[0]))
            return "fermentado1"

    def fermentado_2_(self):
        # Cambio a madurado
        if CambiarFase.fermentado2:
            if CambiarFase.ahora > CambiarFase.fermentado2:
                ControlProcesos.objects.filter(id=self.estadoId).update(fase="madurado")

                # Escribo la nueva temperatura en el puerto serie de arduino   
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
                return "madurado"
            # Mantengo fermentado 2
            else:
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[1]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[1]))
                return "fermentado2"
        return "sin fermentado 2"

    def madurado_(self):
        # Cambia a clarificado
        if CambiarFase.ahora > CambiarFase.madurado:
            ControlProcesos.objects.filter(id=self.estadoId).update(fase="clarificado")
            try:
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[3]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[3]))
            except:
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaClarificado))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaClarificado))
            return "clarificado"
        # Sigue en madurado
        else:
            serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
            print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[2]))
            return "madurado"

    def clarificado_(self):
        # Cambia a finalizado
        if CambiarFase.ahora > CambiarFase.clarificado:
            ControlProcesos.objects.filter(id=self.estadoId).update(fase="finalizado")
            try:
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[4]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[4]))
            except:
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaFinalizado))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaFinalizado))
            return "finalizado"
        # Sigue en clarificado
        else:
            try:
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[3]))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[3]))
            except:
                serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaClarificado))
                print('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaClarificado))
            return "clarificado"

    def finalizado_(self):
        try:
            serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[4]))
            print('s',str(CambiarFase.arduinoId),str(CambiarFase.temperaturas.split(",")[4]))

        except:
            serial_w('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaFinalizado))
            print('s',str(CambiarFase.arduinoId),str(CambiarFase.datosConfiguraciones.temperaturaFinalizado))
        return "finalizado"


            
            


'''            
0 ferm1
1 ferm2
2 Mad
3 clar
4 final

activos = buscarPorcesosActivos()

for i in activos:
'''    
