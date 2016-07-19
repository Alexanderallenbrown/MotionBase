import serial
from numpy import *
import time
from matplotlib.pyplot import *
print "1"
ser = serial.Serial(
    port='/dev/ttyUSB100',
    baudrate=115200)
    # parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,
    # bytesize=serial.EIGHTBITS,
    # xonxoff=serial.XOFF,
    # rtscts=False,
    # dsrdtr=False
#)
print "2"
omega = (2*3.14)/2.0
print "3"
starttime = time.time()


print "initializing"
#ser.close()
print "4"
#time.sleep(2.0)
#ser.open()
print "5"
#time.sleep(2.0)
print "done"
while ser.isOpen():
    timenow = time.time()-starttime
    #command = [int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1)),int(10*(sin(timenow/3.)+1))]
    #ser.write('6')
    #ser.write(bytearray(command))
    x = 0*sin(omega*timenow)
    y = 0*sin(.5*omega*timenow)
    z = 0#3*sin(omega*timenow)
    r = 0#.1*(sin(omega*timenow))
    p = 0#.2*(sin(omega*timenow))
    a = 0#.1*(sin(omega*timenow))

    command = [x,y,z,r,p,a]
    ser.write('!')
    for ind in range(0,len(command)-1):
        #print ind
        #print(format(command[ind],'0.2f')
        ser.write(format(command[ind],'0.2f'))
        ser.write(',')
    ser.write(str(command[-1]))
    ser.write('\n')

    line = ser.readline()
    
    #print command
    print('!'+format(command[0],'0.2f')+','+format(command[1],'0.2f')+','+format(command[2],'0.2f')+','+format(command[3],'0.2f')+','+format(command[4],'0.2f')+','+format(command[5],'0.2f'))
    print line
    #print ser.readline()
    # for ind in range(0,len(command)):
    # 	ser.write(bytes(command[ind]))
    #print command
    time.sleep(.01)

