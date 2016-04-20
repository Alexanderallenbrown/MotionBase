#!/usr/bin/env python
import socket
import sys, select
import time
from numpy import *
from scipy.signal import *
from matplotlib.pyplot import *
import sys,traceback
import serial


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200) # checked this, not cause of delay
 
host = 'localhost' #does not have to be
port = 8000 # some default

#f=open('yaw.txt','wb')
# f.write(str(1)+'\r\n')

#####create a figure for us to see our data on. MATLAB-like syntax.
ion()
fig,ax = subplots(1,1)
ax.hold(True)
fig.canvas.draw()
plt1 = ax.plot(0,0,'r')[0]
plt2 = ax.plot(0,0,'k')[0]
buffsize = 2000  #might want to change this
t = []
plotXvals = []
plotYvals = []
plot_delay = 0.1 #seconds
plotoldtime = time.time()
######

N = 4
x_desired = zeros(N)
ax_raw = zeros(N)
y_desired = zeros(N)
ay_raw = zeros(N)
z_desired = zeros(N)
az_raw = zeros(N)
ax_tilt=zeros(N)
ay_tilt=zeros(N)
anglex=0
angley=0
anglex_filtered=zeros(N)
angley_filtered=zeros(N)
anglez_filtered=zeros(N)
anglex_raw=zeros(N)
angley_raw=zeros(N)
anglez_raw=zeros(N)
anglez=zeros(N)
ax_tiltLP=0
ay_tiltLP=0

send_address = (host, port) # Set the address to send to
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create Datagram Socket (UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make Socket Reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow incoming broadcasts
s.setblocking(False) # Set socket to non-blocking mode
s.bind(('', port)) #Accept Connections on port
print "Accepting connections on port", hex(port)

starttime = time.time()
oldtime = time.time()
time.sleep(.01)
dt = 0.1

index=0 
#f.write(str(1)+'\r\n')
#print starttime

print "initializing"
ser.close()
time.sleep(2.0)
ser.open()
time.sleep(2.0)
print "done"

lastsendtime = time.time()
arduino_delay = 0.05

lastfilttime = time.time()
filter_delay = 0.01

command = [0,0,0,0,0,0]

while 1:

  try:
        message, address = s.recvfrom(8192) # Buffer size is 8192. Change as needed.
        time.sleep(.001)
  except:
    #print "no message"
    message = None

  tnow = time.time()
  if (tnow-lastfilttime)>filter_delay:
    dt = tnow-oldtime
    oldtime = tnow
    #print dt
    #ay to y_desired, and ax to x_desired
    (num1,den1,dt1) = cont2discrete(([1.],[1,10,20]),dt)
    #print num1,den1
    #ay to ax_tilt
    (num2,den2,dt2) = cont2discrete(([-130000.],[1,100,1300]),dt)
    #print num2,den2
    #anglex to anglex_filtered
    (num3,den3,dt3) = cont2discrete(([1,0],[1,2,4]),dt)
    #print num3,den3

    #az to z_desired
    (num4,den4,dt4) = cont2discrete(([1.,0],[1,11,110,100]),dt)
    #anglez to anglez_filtered
    (num5,den5,dt5) = cont2discrete(([1,0,0],[1,2,4]),dt)

    num1,num2,num3,num4,num5 = num1[0],num2[0],num3[0],num4[0],num5[0]
    #print num1,num2,num3,num4,num5
    #print num5,den5
    #break

      
    if message is not None:
        #print index
        #print address, "> ", message
        message_split = message.split(',')            
        axraw = float(message_split[0])
        ayraw = float(message_split[1])
        azraw = float(message_split[2])
        anglexraw = float(message_split[3])
        angleyraw = float(message_split[4])
        anglezraw = float(message_split[5])
        
        x_desired = append(x_desired[1:],0)
        y_desired = append(y_desired[1:],0)
        z_desired = append(z_desired[1:],0)
        #anglex = append(anglex[1:],0)
        #angley = append(angley[1:],0)
        anglez_filtered = append(anglez_filtered[1:],0)
        ax_raw=append(ax_raw[1:],axraw) 
        ay_raw=append(ay_raw[1:],ayraw ) 
        az_raw=append(ax_raw[1:],azraw) 
        anglex_raw=append(anglex_raw[1:],anglexraw)  
        angley_raw=append(angley_raw[1:],angleyraw)  
        anglez_raw=append(anglez_raw[1:],anglezraw) 
        
        # x_desired[0:-2] = x_desired[1:-1]
        # y_desired[0:-2] = y_desired[1:-1]
        # z_desired[0:-2] = z_desired[1:-1]
        # anglex[0:-2]=anglex[1:-1]
        # angley[0:-2]=angley[1:-1]
        # anglez_filtered[0:-2]=anglez_filtered[1:-1]
        #float_array = array([axraw,ayraw])
        #print float_array
        if index>1:
          #print num1[2]
          y_desired[3]=-den1[1]*y_desired[2]-den1[2]*y_desired[1]+num1[1]*ay_raw[2]+num1[2]*ay_raw[1]
          x_desired[3]=-den1[1]*x_desired[2]-den1[2]*x_desired[1]+num1[1]*ax_raw[2]+num1[2]*ax_raw[1]
          ax_tilt[3]=-den2[1]*ax_tilt[2]-den2[2]*ax_tilt[1]+num2[1]*ay_raw[2]+num2[2]*ay_raw[1]
          if abs(ax_tilt[3])>1.0:
            ax_tilt[3] = sign(ax_tilt[3])
          ax_tiltLP=math.asin(ax_tilt[3])
          ay_tilt[3]=-den2[1]*ay_tilt[2]-den2[2]*ay_tilt[1]+num2[1]*ax_raw[2]+num2[2]*ax_raw[1]
          if abs(ay_tilt[3])>1.0:
            ay_tilt[3] = sign(ax_tilt[3])
          ay_tiltLP=math.asin(-ay_tilt[3])
          #anglex[3]=ax_tilt[3]+anglexraw
          #angley[3]=ay_tilt[3]+angleyraw
          anglex_filtered[3]=-den3[1]*anglex_filtered[2]-den3[2]*anglex_filtered[1]+num3[1]*anglex_raw[2]+num3[2]*anglex_raw[1]
          angley_filtered[3]=-den3[1]*angley_filtered[2]-den3[2]*angley_filtered[1]+num3[1]*angley_raw[2]+num3[2]*angley_raw[1]
          anglex=ax_tiltLP+anglex_filtered[3]
          angley=ay_tiltLP+angley_filtered[3]

          z_desired[3]=-den4[1]*z_desired[2]-den4[2]*z_desired[1]-den4[3]*z_desired[0]+num4[1]*az_raw[2]+num4[2]*az_raw[1]+num4[3]*az_raw[0]
          anglez_filtered[3]=-den5[1]*anglez_filtered[2]-den5[2]*anglez_filtered[1]+num5[0]*anglezraw+num5[1]*anglez_raw[2]+num5[2]*anglez_raw[1]
          #print anglez_filtered
          #anglez_filtered[index]=1.928*anglez_filtered[index-1]-0.9324*anglez_filtered[index-2]+anglezraw-1.998*anglez_raw[index-1]+0.997*anglez_raw[index-2]
        else: 
          y_desired[3]=0
          x_desired[3]=0
          z_desired[3]=0
          ay_tilt[3]=0 
          ax_tilt[3]=0 
          anglex=0
          angley=0
          anglex_filtered[3]=0
          angley_filtered[3]=0
          anglez_filtered[3]=anglezraw
          #print anglez_filtered
        #print dt,x_desired[index],y_desired[index],z_desired[index],anglex[index],angley[index],anglez_filtered[index]     
        #f.write(str(1)+'\r\n')
        #tiltx_desired = arcsin(ax_tilt/9.81)+
        #command = [x_desired[-1],y_desired[-1],z_desired[-1],anglex[-1],angley[-1],anglez_filtered[-1]]
        command = [x_desired[-1],y_desired[-1],z_desired[-1],ax_tiltLP,ay_tiltLP,anglez_filtered[-1]]
        #print "command updated"
        #command = [x_desired[-1],y_desired[-1],z_desired[-1],arcsin(axraw/4),-arcsin(ayraw/4),anglez_filtered[-1]]
        if len(t)<buffsize:
          #this appends our newest values to our variables of interest.
          t.append(time.time()-starttime)
          plotXvals.append(axraw)
          plotYvals.append(ayraw)
          #print "appending"
        else: #this means that the buffer needs to lose the oldest value, and gain the newest value.
          #make t equal to the second oldest value to the second newest value
          t = t[1:]
          t.append(time.time())
          #add the newest value on to the end, maintaining a vector of buffsize.
          plotXvals = plotXvals[1:]
          plotXvals.append(axraw)
          plotYvals = plotYvals[1:]
          plotYvals.append(ayraw)
        #now, we only update plot every now and then.... so check how long it's been since we updated!
        
    else:
        print "junk message received"

  if (time.time()-plotoldtime>plot_delay and len(t)>=buffsize):#if enough time has passed
          print "PLOTTING"
          #set the old time. Maybe this isn't needed?
          plotoldtime = time.time()
          #set our X limits of the plot to only look at the last 5 seconds of data TODO make 5 a variable!!
          ax.set_xlim(t[-1]-5,t[-1])
          # ax.set_ylim(min(r)*1.2,max(r)*1.2)
          ax.set_ylim(-1.3,1.3)
          #this sets the line plt1 data to be our updated t and r vectors.
          plt1.set_data(t,plotXvals)
          #same as above.
          plt2.set_data(t,plotYvals)
          #the draw command is last, and tells matplotlib to update the figure!!
          fig.canvas.draw()
          pause(.0001)#must have a small pause here or nothing will work. Pause is a matplotlib.pyplot function.

  if tnow-lastsendtime>arduino_delay:
    print "sent: "+format(command[0],'0.2f')+","+format(command[1],'0.2f')+","+format(command[2],'0.2f')+","+format(command[3],'0.4f')+","+format(command[4],'0.4f')+","+format(command[5],'0.4f')
    
    lastsendtime = tnow
    for ind in range(0,len(command)-1):
      # print ind
      ser.write('!')
      ser.write(format(command[ind],'0.2f'))
      ser.write(',')
    ser.write(str(command[-1]))
    ser.write('\n')
    #line = ser.readline()
    #print "received: "+line


    #f.write(str(tnow)+','+str(x_desired[-1])+','+str(y_desired[-1])+','+str(z_desired[-1])+','+str(anglex[-1])+','+str(angley[-1])+','+str(anglez_filtered[-1])+'\r\n')
    index=index+1

#f.close()

      
                
