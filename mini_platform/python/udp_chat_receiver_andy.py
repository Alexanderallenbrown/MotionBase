#!/usr/bin/env python
import socket
import sys, select
import time
from numpy import *
from scipy.signal import *
from matplotlib.pyplot import *

 
host = 'localhost' #does not have to be
port = 8102 # some default
dt = 0.1
N = 1200
x_desired = zeros(N)
ax_raw = zeros(N)
y_desired = zeros(N)
ay_raw = zeros(N)
z_desired = zeros(N)
az_raw = zeros(N)
ytilt= zeros(N)

send_address = (host, port) # Set the address to send to
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create Datagram Socket (UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make Socket Reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow incoming broadcasts
s.setblocking(False) # Set socket to non-blocking mode
s.bind(('', port)) #Accept Connections on port
print "Accepting connections on port", hex(port)

index=0 
while 1:
    try:
        message, address = s.recvfrom(8192) # Buffer size is 8192. Change as needed.
        if message:
            #print address, "> ", message
            message_split = message.split(',')            
            axraw = float(message_split[0])
            ayraw = float(message_split[1])
            azraw = float(message_split[2])
            #wxraw = float(message_split[3])
            #wyraw = float(message_split[4])
            #wzraw = float(message_split[5])

            #float_array = array([axraw,ayraw])
            #print float_array
            if index>1:
               
               x_desired[index]= (2/dt/dt+10/dt)*x_desired[index-1]-x_desired[index-2]/dt/dt+2.5*axraw
               x_desired[index]=x_desired[index]/(1/dt/dt+10/dt+20)
               y_desired[index]= (2/dt/dt+10/dt)*y_desired[index-1]-y_desired[index-2]/dt/dt+2.5*ayraw
               y_desired[index]=y_desired[index]/(1/dt/dt+10/dt+20)
               ytilt[index]=(2/dt/dt+100/dt)*ytilt[index-1]-ytilt[index-2]/dt/dt+130*axraw
               ytilt[index]=ytilt[index]/(1/dt/dt+100/dt+1300)
               xtilt[index]=(2/dt/dt+100/dt)*ytilt[index-1]-ytilt[index-2]/dt/dt+130*axraw
               xtilt[index]=ytilt[index]/(1/dt/dt+100/dt+1300)
            else:
               x_desired[index]=0
               y_desired[index]=0
               z_desired[index]=0
               ytilt[index]=0

        ax_raw[index]=axraw
        ay_raw[index]=ayraw
        az_raw[index]=azraw
        ytilt=ytilt+wxraw
        xtilt=xtilt+wyraw
        print ytilt[index]
        index=index+1

    except:
        pass

