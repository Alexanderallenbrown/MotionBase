import serial
from numpy import *
import time
from matplotlib.pyplot import *

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200)
    # parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,
    # bytesize=serial.EIGHTBITS,
    # xonxoff=serial.XOFF,
    # rtscts=False,
    # dsrdtr=False
#)

omega = (2*3.14)/1.0

starttime = time.time()


print "initializing"
ser.close()
time.sleep(2.0)
ser.open()
time.sleep(2.0)
print "done"
while ser.isOpen():
	timenow = time.time()-starttime
	#command = [int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1))]
	#ser.write('6')
	#ser.write(bytearray(command))
	x = 0
	y = 0
	z = 0.5*(sin(omega*timenow)+1)
	r = 0
	p = 0
	a = 0

	command = [x,y,z,r,p,a]
	for ind in range(0,len(command)-1):
		#print ind
		ser.write(format(command[ind],'0.2f'))
		ser.write(',')
	ser.write(str(command[-1]))
	ser.write('\n')
	line = ser.readline()
	print line
	#print ser.readline()
	# for ind in range(0,len(command)):
	# 	ser.write(bytes(command[ind]))
	#print command
	time.sleep(.01)

