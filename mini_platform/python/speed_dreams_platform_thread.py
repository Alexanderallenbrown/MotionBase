#!/usr/bin/env python
import socket
import sys, select
import time
from numpy import *
from scipy.signal import *
from matplotlib.pyplot import *
import sys,traceback
import serial
from threading import Thread

####


###### filtering function
def filt():

  global t, ax_raw, ay_raw, az_raw, anglex_raw, angley_raw, anglez_raw, buffsize, anglezraw

  # initialize position variables
  N = 4
  x_desired = zeros(N)
  y_desired = zeros(N)
  z_desired = zeros(N)
  ax_tilt = zeros(N)
  ay_tilt = zeros(N)
  anglex = 0
  angley = 0
  anglex_filtered=zeros(N)
  angley_filtered=zeros(N)
  anglez_filtered=zeros(N)
  anglez=zeros(N)
  ax_tiltLP=0
  ay_tiltLP=0
  index=0 
  command = [0,0,0,0,0,0]

  # initialize time variables
  starttime = time.time()
  oldtime = time.time()
  time.sleep(.01)
  dt = 0.1
  lastsendtime = time.time()
  arduino_delay = 0.05
  lastfilttime = time.time()
  filter_delay = 0.01

  # Set up socket to send data
  ser = serial.Serial(
      port='/dev/ttyUSB0',
      baudrate=115200) # checked this, not cause of delay
  print "initializing"
  ser.close()
  time.sleep(2.0)
  ser.open()
  time.sleep(2.0)
  print "done"

  if (len(t)>=buffsize):
    
    while 1:
      # take 4 most recent values read from buffer
      ax_raw_small = array(ax_raw[-4:-1])
      ay_raw_small = array(ay_raw[-4:-1])
      az_raw_small = array(az_raw[-4:-1])
      anglex_raw_small = array(anglex_raw[-4:-1])
      angley_raw_small = array(angley_raw[-4:-1])
      anglez_raw_small = array(anglez_raw[-4:-1])


      tnow = time.time()  # what time is it mr. fox??

      if (tnow-lastfilttime)>filter_delay:

        #determine time step
        dt = tnow-oldtime
        oldtime = tnow

        #ay to y_desired, and ax to x_desired
        (num1,den1,dt1) = cont2discrete(([1.],[1,10,20]),dt)

        #ay to ax_tilt
        (num2,den2,dt2) = cont2discrete(([-32500.],[1,100,1300]),dt)
  
        #anglex to anglex_filtered
        (num3,den3,dt3) = cont2discrete(([1,0],[1,2,4]),dt)

        #az to z_desired
        (num4,den4,dt4) = cont2discrete(([1.,0],[1,11,110,100]),dt)

        #anglez to anglez_filtered
        (num5,den5,dt5) = cont2discrete(([1,0,0],[1,2,4]),dt)

        num1,num2,num3,num4,num5 = num1[0],num2[0],num3[0],num4[0],num5[0]

        x_desired = append(x_desired[1:],0)
        y_desired = append(y_desired[1:],0)
        z_desired = append(z_desired[1:],0)
        print ay_raw

        anglez_filtered = append(anglez_filtered[1:],0)

        if index>1:
          y_desired[3]=-den1[1]*y_desired[2]-den1[2]*y_desired[1]+num1[1]*ay_raw_small[2]+num1[2]*ay_raw_small[1]
          x_desired[3]=-den1[1]*x_desired[2]-den1[2]*x_desired[1]+num1[1]*ax_raw_small[2]+num1[2]*ax_raw_small[1]
          ax_tilt[3]=-den2[1]*ax_tilt[2]-den2[2]*ax_tilt[1]+num2[1]*ay_raw_small[2]+num2[2]*ay_raw_small[1]
          if abs(ax_tilt[3])>1.0:
            ax_tilt[3] = sign(ax_tilt[3])
          ax_tiltLP=math.asin(ax_tilt[3])
          ay_tilt[3]=-den2[1]*ay_tilt[2]-den2[2]*ay_tilt[1]+num2[1]*ax_raw_small[2]+num2[2]*ax_raw_small[1]
          if abs(ay_tilt[3])>1.0:
            ay_tilt[3] = sign(ax_tilt[3])
          ay_tiltLP=math.asin(-ay_tilt[3])

          anglex_filtered[3]=-den3[1]*anglex_filtered[2]-den3[2]*anglex_filtered[1]+num3[1]*anglex_raw_small[2]+num3[2]*anglex_raw_small[1]
          angley_filtered[3]=-den3[1]*angley_filtered[2]-den3[2]*angley_filtered[1]+num3[1]*angley_raw_small[2]+num3[2]*angley_raw_small[1]
          anglex=ax_tiltLP+anglex_filtered[3]
          angley=ay_tiltLP+angley_filtered[3]

          z_desired[3]=-den4[1]*z_desired[2]-den4[2]*z_desired[1]-den4[3]*z_desired[0]+num4[1]*az_raw_small[2]+num4[2]*az_raw_small[1]+num4[3]*az_raw_small[0]
          anglez_filtered[3]=-den5[1]*anglez_filtered[2]-den5[2]*anglez_filtered[1]+num5[0]*anglezraw+num5[1]*anglez_raw_small[2]+num5[2]*anglez_raw_small[1]
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
        
        command = [x_desired[-1],y_desired[-1],z_desired[-1],ax_tiltLP,ay_tiltLP,anglez_filtered[-1]]

        if tnow-lastsendtime>arduino_delay:
          print "sent: "+format(command[0],'0.2f')+","+format(command[1],'0.2f')+","+format(command[2],'0.2f')+","+format(command[3],'0.4f')+","+format(command[4],'0.4f')+","+format(command[5],'0.4f')
    
          lastsendtime = tnow
          ser.write('!')
          for ind in range(0,len(command)-1):
            ser.write(format(command[ind],'0.2f'))
            ser.write(',')
          ser.write(str(command[-1]))
          ser.write('\n')

          index=index+1

      
########### function to read stuff from buffer and plot data
def getdata():
  
  global t, ax_raw, ay_raw, az_raw, anglex_raw, angley_raw, anglez_raw, anglezraw, buffsize

  # initialize stuff
  starttime = time.time()
  axraw = 0
  ayraw = 0
  azraw = 0
  anglexraw = 0
  angleyraw = 0
  anglezraw = 0
  ax_raw = []
  ay_raw = []
  az_raw = []
  anglex_raw = []
  angley_raw = []
  anglez_raw = []

  # create UDP socket to receive data
  host = 'localhost' #does not have to be
  port = 8000 # some default
  send_address = (host, port) # Set the address to send to
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create Datagram Socket (UDP)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make Socket Reusable
  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow incoming broadcasts
  s.setblocking(False) # Set socket to non-blocking mode
  s.bind(('', port)) #Accept Connections on port
  print "Accepting connections on port", hex(port)
  

  # create a figure for us to see our data on
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

  # now loop through to get data
  while 1:
    time.sleep(.0005)

    try:
      message, address = s.recvfrom(8192) # Buffer size. Change as needed.  
    except:
      message = None
      
    if message is not None:
      message_split = message.split(',')            
      axraw = float(message_split[0])
      ayraw = float(message_split[1])
      azraw = float(message_split[2])
      anglexraw = float(message_split[3])
      angleyraw = float(message_split[4])
      anglezraw = float(message_split[5])
      ax_raw=append(ax_raw,axraw) 
      ay_raw=append(ay_raw,ayraw) 
      az_raw=append(ax_raw,azraw) 
      anglex_raw=append(anglex_raw,anglexraw)  
      angley_raw=append(angley_raw,angleyraw)  
      anglez_raw=append(anglez_raw,anglezraw) 
      
      #for plotting
      if len(t)<buffsize:
        t.append(time.time()-starttime)
        plotXvals.append(axraw)
        plotYvals.append(ayraw)
      else: 
        t = t[1:]
        t.append(time.time())
        plotXvals = plotXvals[1:]
        plotXvals.append(axraw)
        plotYvals = plotYvals[1:]
        plotYvals.append(ayraw)

      if (time.time()-plotoldtime>plot_delay and len(t)>=buffsize):#if enough time has passed
        #set the old time
        plotoldtime = time.time()
        #set our X limits of the plot to only look at the last 5 seconds of data
        ax.set_xlim(t[-1]-5,t[-1])
        ax.set_ylim(-1.3,1.3)
        #this sets the line plt1 data to be our updated t and r vectors.
        plt1.set_data(t,plotXvals)
        plt2.set_data(t,plotYvals)
        #the draw command is last, and tells matplotlib to update the figure!!
        fig.canvas.draw()
        pause(.0001)#must have a small pause here or nothing will work. Pause is a matplotlib.pyplot function.

    else:
        pass



####### execute the thread
if __name__ == "__main__" :

    thread1 = Thread(target=getdata,args=())
    thread2 = Thread(target=filt,args=())

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
   
    
