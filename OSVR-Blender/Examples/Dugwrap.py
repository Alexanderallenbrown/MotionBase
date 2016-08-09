#import time
from DugoffBicycleModel import DugoffBicycleModel
from bge import logic,constrains

def setup():
    car = DugoffBicycleModel()
    cube = controller.owner
    cube.worldPosition = [car.x[2],car.x[0],0]
    cube.worldOrientation = [0,0,car.x[4]]

def gas():
    reversePower = 2000.0
    gasPower = 8000.0
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
    gas = power-power2
    return gas                

def brake(): 
    # set braking amount
    brakeAmount = 1000.0      # front and back brakes
    ebrakeAmount = 10000.0    # back brakes only  
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
    #print("brakes: " + str(front_Brake) + "," + str(back_Brake) + "," + str(brakes))
    vehicleID.applyBraking( front_Brake, 0)
    vehicleID.applyBraking( front_Brake, 1)
    vehicleID.applyBraking( back_Brake, 2)
    vehicleID.applyBraking( back_Brake, 3)

    return brakes

def steer():
    joy = controller.sensors["joysticksteer"]
    turn = -joy.axisValues[0]*30.0/26000*3.14/180.0 
    return turn

def main():
    gas = gas()
    brake = brake()
    steer = steer()
    car.dt = logic.getAverageFrameRate()
    car.dt = 1/car.dt
    car.euler_update(brake,gas,steer,'off',0,'off','off',0)
    cube = controller.owner
    cube.worldPosition = [car.x[2],car.x[0],0]
    cube.worldOrientation = [0,0,car.x[4]]