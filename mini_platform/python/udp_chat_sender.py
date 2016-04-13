#!/usr/bin/env python
import socket
import sys, select
import time
from numpy import *
 
host = 'localhost'
port = 8000#some value
 
send_address = (host, port) # Set the address to send to
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create Datagram Socket (UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make Socket Reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow incoming broadcasts
s.setblocking(False) # Set socket to non-blocking mode
#s.bind(('', port)) #Accept Connections on port

starttime = time.time()#in seconds... big number
 
while 1:
    #curr_time = time.time()-starttime
    #my_datagram = sin(curr_time)
    on=0.3
    off=0
    print "sending: "+str(off)+","+str(off)
    s.sendto(str(off)+","+str(off)+","+str(off)+","+str(off)+","+str(off)+","+str(on), send_address)#send the data
    time.sleep(0.001)#wait for .1 seconds