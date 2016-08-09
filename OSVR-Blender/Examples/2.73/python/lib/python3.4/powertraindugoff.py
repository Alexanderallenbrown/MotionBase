from bge import logic,constraints
from suspension import Tire_Grip2 #imports tire grip settings.
import sys
#sys.path.append('/usr/local/lib/python3.4/dist-packages')
#above may not work on MAc, only linux...
import time
import datetime
from math import sin,cos
from numpy import *

#########################################
#
#   Powertrain.py  Blender 2.49
#
#   tutorial can be found at
#
#   www.tutorialsforblender3d.com
#
#   Released under the Creative Commons Attribution 3.0 Unported License.   
#
#   If you use this code, please include this information header.
#
##########################################
f = open('/home/brownlab/Desktop/output.txt','w')
#fricf = open('/home/brownlab/Desktop/output_fric.txt','w')

#coefficient of friction TODO: Pull from CarSetup?
mu = 10.0

# Main Program
def main():
        
    # get the current controller
    controller = logic.getCurrentController()
    #print(controller.sensors)
    vehobj = controller.owner
    
    # get vehicle constraint ID
    vehicleID = ConstraintID(controller)
    # brakes
    brakes,fxf_b,fxr_b = Brakes(vehicleID, controller,vehobj,mu)
        
    # gas & reverse
    Power( vehicleID, controller, brakes,vehobj,mu)
        
    # steering
    steerval = Steering(vehicleID, controller)

    alpha_f,alpha_r = getSlip(vehobj,steerval,f)

    #now we calculate the Dugoff tire Fy. TODO legitimate (or closer) Fz
    Fz = vehobj.mass/4*9.81

    Fyf = dugoffFy(alpha_f,Fz,mu,fxf_b)
    fyf = abs(Fyf/Fz)
    Fyr = dugoffFy(alpha_r,Fz,mu,fxr_b)
    fyr = abs(Fyf/Fz)
    Tire_Grip2(vehicleID,vehobj,fyf,fyf,fyr,fyr)
    #fricf.write(str(time.time())+","+str(fyf)+","+str(fyr)+"\r\n")

    #Tire_Grip2(vehicleID,obj,grip_0=1.0,grip_1=1.0,grip_2=1.0,grip_3=1.0)

########################################################  Vehicle ID

def dugoffFy(alpha,Fz,mu=1,Fx=0,Ca=100000):
    mufz = sqrt((mu*Fz)**2-Fx**2)#De-rate lateral force capacity for braking
    lam= mufz/(2*Ca*abs(tan(alpha))) #lambda
    if lam>=1:
        flam = 1
    else:
        flam = (2-lam)*lam
    Fy = -Ca*tan(alpha)*flam
    return Fy

def getSlip(obj,steerval,fhandle):
    R = obj.worldOrientation.to_euler()
    vx,vy,vz = obj.getLinearVelocity(1)
    vX,vY,vZ = obj.getLinearVelocity(0)
    wx,wy,wz = obj.getAngularVelocity(1)


    fhandle.write(str(time.time())+","+str(vx)+","+str(vy)+","+str(vz)+","+str(vX)+","+str(vY)+","+str(vZ)+","+str(wz)+","+str(steerval)+","+str(R.z)+"\r\n")
    #now look at ISO lateral velocity and yaw rate to determine slip angles
    a = 3
    b = 3#should find a way to pull these out?
    V = -vx
    U = vy

    if U>2:
        alpha_f = (V+a*wz)/U - steerval
        alpha_r = (V-b*wz)/U
    else:
        alpha_f = 0
        alpha_r = 0
    return alpha_f,alpha_r

# get vehicle constraint ID
def ConstraintID(controller):

    # get car the controller is attached to
    car = controller.owner
        
    # get saved vehicle Constraint ID
    vehicleID = car["vehicleID"]
    
    return vehicleID

########################################################  Brakes

def Brakes(vehicleID, controller,obj,mu):

    #get object mass for brake amount:
    m = obj.mass
    #the brakes are applied to pairs of wheels front/back. Assume mu doesn't change with Fz
    Fbmax = mu*m*9.81/2 #half     
    # set braking amount
    brakeAmount = 4000.0      # front and back brakes
    ebrakeAmount = 10000.0    # back brakes only  
    joy = controller.sensors["joygas"]
    #print(joy.axisValues)
    val = joy.axisValues[1]
    if val>0:
        front_Brake = val*brakeAmount/32768.0
        back_Brake = val*brakeAmount/32768.0
        if front_Brake>Fbmax:
            front_Brake=Fbmax
        if back_Brake>Fbmax:
            back_Brake=Fbmax
        brakes = True
    else:
        front_Brake = 0
        back_Brake = 0
        brakes = False

    # brakes    
    print(front_Brake,back_Brake,brakes)
    vehicleID.applyBraking( front_Brake, 0)
    vehicleID.applyBraking( front_Brake, 1)
    vehicleID.applyBraking( back_Brake, 2)
    vehicleID.applyBraking( back_Brake, 3)

    return brakes,front_Brake,back_Brake

##########################################  Gas & Reverse 
    
# gas and reverse   
def Power( vehicleID, controller, brakes,obj,mu):  
    
    # set power amounts.
    #here is a simple thing: approximate as a 1st order system. 
    # dV/dT = a*V
    #Vmax
    reversePower = 2000.0
    gasPower = 4000.0

    # get power sensors
    #gas = controller.sensors["Gas"]             # sensor named "Gas"
    #reverse = controller.sensors["Reverse"]     # sensor named "Reverse"
    joy = controller.sensors["joygas"]
    #print(joy.axisValues)
    val = joy.axisValues[1]
    if val<-130:
        power = val/32768.0*gasPower
    else:
        power = 0
    print(power)
    # # brakes
    # if brakes == True:
        
    #     power = 0.0
                    
    # # reverse
    # elif reverse.positive == True:
        
    #     power = reversePower
    
    # # gas pedal 
    # elif gas.positive == True:
        
    #     power = -gasPower
    
    # # no gas and no reverse
    # else:
        
    #     power = 0.0

    # apply power
    vehicleID.applyEngineForce( power, 0)
    vehicleID.applyEngineForce( power, 1)
    vehicleID.applyEngineForce( power, 2)
    vehicleID.applyEngineForce( power, 3)                                       
        

##################################################  Steering 

def Steering( vehicleID, controller):
    joy = controller.sensors["joysticksteer"]
    # set turn amount
    turn = 0.3
    # get steering sensors
    turn = -joy.axisValues[0]*20.0/26000.0*3.14/180.0 
    print("steer = "+str(turn))
    #else:
     #   pass
        #turn = 0.0
       
     # steer with front tires only
    vehicleID.setSteeringValue(turn,0)
    vehicleID.setSteeringValue(turn,1)
    return turn


###############################################


# run main program
main()
