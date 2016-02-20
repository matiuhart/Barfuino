import time
import serial
import numpy as np
N = 3
data = np.zeros((N, 2))

# Abrimos la conexión con Arduino
def arduino_w(mode='',ferm='',temp=''):
	arduino = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1.0)
	comando = str(mode) + str(ferm)
	arduino.write(bytes(comando.encode('ascii')))
	time.sleep(1)
	with arduino:
	    ii = 0
	    while ii < N:
	        try:
	            line = arduino.read()
	            if not line:
	                # HACK: Descartamos líneas vacías porque fromstring produce
	                # resultados erróneos, ver
	                # https://github.com/numpy/numpy/issues/1714
	                continue
	            data[ii] = np.fromstring(line.decode('ascii', errors='replace'),
	                                     sep=' ')
	            ii += 1
	            #print(ii)
	        except KeyboardInterrupt:
	            print("Exiting")
	            break
	print(data)

arduino_w()

def serial_w(mode='',ferm='',temp=''):
    #port = serial_ports()
    port = '/dev/ttyUSB0'
    serie = serial.Serial(port,9600,timeout = 1.0)
    temperatura = ''
    
    comando = str(mode) + str(ferm)
    print(b'comando')
    time.sleep(1)
    serie.write(bytes(comando.encode('ascii')))
    with serie:
        while serie.inWaiting() > 0:
            temperatura += serie.read().decode('UTF-8', 'ignore')
    print("Temperatura: " + temperatura)