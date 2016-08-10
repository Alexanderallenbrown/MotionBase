#import time
from DugoffBicycleModel import DugoffBicycleModel
import bge
#from bge import logic,constraints

global gas, brake, steer, car

def setup():
    global car
    car = DugoffBicycleModel(U=0)
    controller = bge.logic.getCurrentController()
    cube = controller.owner
    cube.worldPosition = [car.x[2],car.x[0],0]
    cube.worldOrientation = [0,0,car.x[4]]

def gascalc():
    reversePower = 2000.0
    gasPower = 8000.0
    controller = bge.logic.getCurrentController()
    joy = controller.sensors["joygas"]
    val = joy.axisValues[2]
    if val<-130:
        power = val/32768.0*gasPower
    else:
        power = 0

    joy2 = controller.sensors["joyreverse"]
    val2 = joy2.axisValues[1]
    if val2<-130:
        power2 = val2/32768.0*reversePower
    else:
        power2 = 0   
    gasnum = power-power2
    return gasnum                

def brakecalc(): 
    # set braking amount
    brakeAmount = 10.0      # front and back brakes
    ebrakeAmount = 10.0    # back brakes only
    controller = bge.logic.getCurrentController()  
    joy = controller.sensors["joybrake"]
    val = joy.axisValues[3]
    val = -val + 32768
    if val>0:
        front_Brake = val*brakeAmount/32768.0
        back_Brake = val*brakeAmount/32768.0
        brakes = True
    else:
        front_Brake = 0
        back_Brake = 0
        brakes = False
    return front_Brake

def steercalc():
    controller = bge.logic.getCurrentController()
    joy = controller.sensors["joysticksteer"]
    turn = -joy.axisValues[0]*10.0/26000*3.14/180.0 
    return turn

def main():
    global gas, brake, steer, car

    gas = gascalc()
    brake = brakecalc()
    steer = steercalc()
    print("Gas,Brake,Steer: " + str(gas) + "," + str(brake) + "," + str(steer))
    frmrt = bge.logic.getAverageFrameRate()
    car.dT = 1/frmrt
    #print(car.dT)
    car.x, xdot = car.euler_update(brake,gas,steer,'off',0,'off','off',0)
    print(car.x)
    controller = bge.logic.getCurrentController()
    cube = controller.owner
    cube.worldPosition = [car.x[2],car.x[0],0]
    cube.worldOrientation = [0,0,car.x[4]]