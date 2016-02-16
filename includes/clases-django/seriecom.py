#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
from time import sleep
import glob

# BUSQUEDA DE PUERTOS AARDUINO
def serial_ports():
    #ports = glob.glob('/dev/ttyACM[0-10]*')
    ports = glob.glob('/dev/ttyUSB[0-10]*')
    result = ""
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result = port
        except (OSError, serial.SerialException):
            print("No se pudo estableecer conexion con arduino")
            pass
    return result

# LECTURA DE PUERTO SERIE
def serial_w(mode,ferm,temp=''):
    port = serial_ports()
    serie = serial.Serial(port,9600,timeout = 3)
    temperatura =''

    if (mode == 's'):
        serie.write(mode+ferm+temp)
        print(mode+ferm+temp)

    elif (mode == 'g' or 'f'):
        serie.write(mode+ferm)
        time.sleep(0.1)
        while serie.inWaiting() > 0:
            temperatura += serie.read(1)
        return temperatura
        temperatura = ''
    serie.close()
