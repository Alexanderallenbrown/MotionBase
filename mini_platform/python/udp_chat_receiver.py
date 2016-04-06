#!/usr/bin/env python
import socket
import sys, select
import time
from numpy import *
 
host = 'localhost' #does not have to be
port = 8102 # some default
 
send_address = (host, port) # Set the address to send to
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create Datagram Socket (UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make Socket Reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow incoming broadcasts
s.setblocking(False) # Set socket to non-blocking mode
s.bind(('', port)) #Accept Connections on port
print "Accepting connections on port", hex(port)
 
while 1:
    try:
        message, address = s.recvfrom(8192) # Buffer size is 8192. Change as needed.
        if message:
            print address, "> ", message
    except:
        pass