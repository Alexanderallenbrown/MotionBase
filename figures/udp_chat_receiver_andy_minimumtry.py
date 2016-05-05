#!/usr/bin/env python
import socket
import sys, select
import time
from numpy import *
from scipy.signal import *
from matplotlib.pyplot import *
import sys,traceback

 
host = 'localhost' #does not have to be
port = 8102 # some default

f=open('yaw.txt','wb')
# f.write(str(1)+'\r\n')

N = 1200
x_desired = zeros(N)
ax_raw = zeros(N)
y_desired = zeros(N)
ay_raw = zeros(N)
z_desired = zeros(N)
az_raw = zeros(N)
ax_tilt=zeros(N)
ay_tilt=zeros(N)
anglex=zeros(N)
angley=zeros(N)
anglex_filtered=zeros(N)
angley_filtered=zeros(N)
anglez_filtered=zeros(N)
anglex_raw=zeros(N)
angley_raw=zeros(N)
anglez_raw=zeros(N)
anglez=zeros(N)

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

while 1:
  time.sleep(.01)
  tnow = time.time()
  dt = tnow-oldtime
  oldtime = tnow
  
  #ay to y_desired, and ax to x_desired
  (num1,den1,dt1) = cont2discrete(([2.5],[1,10,20]),dt)
  #print num1,den1
  #ay to ax_tilt
  (num2,den2,dt2) = cont2discrete(([-325],[1,100,1300]),dt)
  #print num2,den2
  #ax_tilt+ anglex to anglex_filtered
  (num3,den3,dt3) = cont2discrete(([50],[1,7,50]),dt)
  #print num3,den3
  #az to z_desired
  (num4,den4,dt4) = cont2discrete(([2.5,0],[1,11,110,100]),dt)
  #anglez to anglez_filtered
  (num5,den5,dt5) = cont2discrete(([1,0,0],[1,2,4]),dt)

  num1,num2,num3,num4,num5 = num1[0],num2[0],num3[0],num4[0],num5[0]
  #print num1,num2,num3,num4,num5
  #print num5,den5
  #break
  try:
        message, address = s.recvfrom(8192) # Buffer size is 8192. Change as needed.
  except:
    #print "no message"
    message = None
    
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

      #float_array = array([axraw,ayraw])
      #print float_array
      if index>1:
        #print num1[2]
        y_desired[index]=-den1[1]*y_desired[index-1]-den1[2]*y_desired[index-2]+num1[1]*ay_raw[index-1]+num1[2]*ay_raw[index-2]
        x_desired[index]=-den1[1]*x_desired[index-1]-den1[2]*x_desired[index-2]+num1[1]*ax_raw[index-1]+num1[2]*ax_raw[index-2]
        ax_tilt[index]=-den2[1]*ax_tilt[index-1]-den2[2]*ax_tilt[index-2]+num2[1]*ay_raw[index-1]+num2[2]*ay_raw[index-2]
        ax_tilt[index]=math.asin(ax_tilt[index])
        ay_tilt[index]=-den2[1]*ay_tilt[index-1]-den2[2]*ay_tilt[index-2]+num2[1]*ax_raw[index-1]+num2[2]*ax_raw[index-2]
        ay_tilt[index]=math.asin(ay_tilt[index])
        anglex[index]=ax_tilt[index]+anglexraw
        angley[index]=ay_tilt[index]+angleyraw
        anglex_filtered[index]=-den3[1]*anglex_filtered[index-1]-den3[2]*anglex_filtered[index-2]+anglex[index]+num3[1]*anglex[index-1]+num3[2]*anglex[index-2]
        angley_filtered[index]=-den3[1]*angley_filtered[index-1]-den3[2]*angley_filtered[index-2]+angley[index]+num3[1]*angley[index-1]+num3[2]*angley[index-2]
        z_desired[index]=-den4[1]*z_desired[index-1]-den4[2]*z_desired[index-2]-den4[3]*z_desired[index-3]+num4[1]*az_raw[index-1]+num4[2]*az_raw[index-2]+num4[3]*az_raw[index-3]
        anglez_filtered[index]=-den5[1]*anglez_filtered[index-1]-den5[2]*anglez_filtered[index-2]+num5[0]*anglezraw+num5[1]*anglez_raw[index-1]+num5[2]*anglez_raw[index-2]
        #anglez_filtered[index]=1.928*anglez_filtered[index-1]-0.9324*anglez_filtered[index-2]+anglezraw-1.998*anglez_raw[index-1]+0.997*anglez_raw[index-2]
      else: 
        y_desired[index]=0
        x_desired[index]=0
        z_desired[index]=0
        ay_tilt[index]=0 
        ax_tilt[index]=0 
        anglex[index]=0
        angley[index]=0
        anglex_filtered[index]=0
        angley_filtered[index]=0
        anglez_filtered[index]=anglezraw

      ax_raw[index]=axraw  
      ay_raw[index]=ayraw 
      az_raw[index]=azraw 
      anglex_raw[index]=anglexraw  
      angley_raw[index]=angleyraw 
      anglez_raw[index]=anglezraw 
      print dt,x_desired[index],y_desired[index],z_desired[index],anglex[index],angley[index],anglez_filtered[index]     
      #f.write(str(1)+'\r\n')
      
      f.write(str(tnow)+','+str(x_desired[index])+','+str(y_desired[index])+','+str(z_desired[index])+','+str(anglex[index])+','+str(angley[index])+','+str(anglez_filtered[index])+'\r\n')
      index=index+1

f.close()