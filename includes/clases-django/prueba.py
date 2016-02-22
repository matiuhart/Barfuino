#!/usr/bin/python3.4
# -*- encoding: utf-8 -*-


import time
from time import sleep
import glob
import serial
import serial.tools.list_ports

from estadoarduino import *

sys.path.append("/home/mati/bin/django/barfuino")
os.environ["DJANGO_SETTINGS_MODULE"] = "barfuino.settings"
django.setup()

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
def serial_w(mode='',ferm='',temp=''):
    port = serial_ports()
    #port = '/dev/ttyUSB0'
    serie = serial.Serial(port,9600,timeout = 1.0)
    comando = str(mode) + str(ferm) + "\n"
    temperatura = ''
   
    time.sleep(1)
    serie.write(bytes(comando.encode('ascii')))
    
    with serie:        
        try:
            temperatura += serie.read(2).decode('UTF-8', 'ignore')
        except:
            print("no se pudo recuperar la temperatura")

    #print(temperatura)
    return temperatura


try:
    while 1:
        serial_w('g',1)
        time.sleep(10)
except KeyboardInterrupt:
            print("\ndone")







