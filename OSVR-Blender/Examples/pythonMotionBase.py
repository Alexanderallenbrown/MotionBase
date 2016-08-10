import bge
import osvr.ClientKit
import socket
import sys, select
import time
from math import *
#from numpy import *
from bge import logic

def main():
    print("print")
    global velx, velxOld, vely, velyOld, velz, velzOld, host, port, send_address, s, rotVelx, rotVely, rotVelz
    velx=0
    velxOld=0
    vely=0
    velyOld=0
    velz=0
    velzOld=0
    rotVelx=0
    rotVely=0
    rotVelz=0

    host = 'localhost'
    port = 8000#some value
 
    send_address = (host, port) # Set the address to send to
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create Datagram Socket (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make Socket Reusable
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow incoming broadcasts
    s.setblocking(False) # Set socket to non-blocking mode
    #s.bind(('', port)) #Accept Connections on port

def motion_base():
    global velx, velxOld, vely, velyOld, velz, velzOld, host, port, send_address, s, rotVelx, rotVely, rotVelz
    cont = bge.logic.getCurrentController()
    own = cont.owner
    velocity = own.getLinearVelocity(1)
    rotVelocity = own.getAngularVelocity(1)
    rotVelx = rotVelocity[0]
    rotVely = rotVelocity[1]
    rotVelz = rotVelocity[2]
    # velx = velocity[0]
    # vely = velocity[1]
    velz = velocity[2]

    #this is a +90 degree rotation matrix about z
    velx = velocity[1]
    vely = -velocity[0]
    rotVelx = rotVelocity[1]
    rotVely = -rotVelocity[0]

    accelx = ((velx-velxOld) * logic.getAverageFrameRate()-vely*rotVelz+velz*rotVely)/9.8
    accely = ((vely-velyOld) * logic.getAverageFrameRate()+velx*rotVelz-velz*rotVelx)/9.8
    accelz = ((velz-velzOld) * logic.getAverageFrameRate()-velx*rotVely+vely*rotVelx)/9.8

    #send accelx
    velxOld = velx
    velyOld = vely
    velzOld = velz

    #print ("Acceleration: "+str(format(accelx,'0.4f'))+","+str(format(accely,'0.4f'))+","+str(format(accelz,'0.4f'))+ "\t" + "Angular Velocity: "+str(format(rotVelx,'0.4f'))+","+str(format(rotVely,'0.4f'))+","+str(format(rotVelz,'0.4f')))

    sendString = (str(format(accelx,'0.4f'))+","+str(format(accely,'0.4f'))+","+str(format(accelz,'0.4f'))+","+str(format(rotVelx,'0.4f'))+","+str(format(rotVely,'0.4f'))+","+str(format(rotVelz,'0.4f')))
    sentBytes = bytearray(sendString,'utf-8')
    s.sendto(sentBytes, send_address)