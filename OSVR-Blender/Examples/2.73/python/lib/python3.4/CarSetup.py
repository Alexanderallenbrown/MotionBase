#########################################
#
#   CarSetup.py  Blender 2.71ME240_
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
from bpy import *
from bge import logic, constraints


def main():
    
    # get car object
    carObj = Car_Object()
    
    # create a vehicle constraint ID
    vehicleID = Car_Constraint(carObj)  

    # get tire objects
    tireObj = Tire_Objects()
    
    # tire positions
    tirePos = Tire_Positions()
    
    # tire radius
    tireRadius = Tire_Radius()
    
    # tire suspension height
    tireSuspension = Tire_Suspension()
    
    # tire suspension angle
    tireSuspensionAngle = Tire_SuspensionAngle()
        
    # tire axis attached to frame
    tireAxis = Tire_Axis()
    
    # tire has steering?
    tireSteering = Tire_Steering()
    
    # add wheels to car
    Add_Tires(vehicleID, tireObj, tirePos, tireSuspensionAngle, tireAxis, tireSuspension, tireRadius, tireSteering)
        
##########################   Get Car

def Car_Object():
    
    # get current controller
    controller = logic.getCurrentController()
    
    # get car the controller is attached to
    carObj = controller.owner
    
    return carObj

##########################   Vehicle Constraint

def Car_Constraint(carObj):

    # # import PhysicsConstraints
    # import PhysicsConstraints
        
    # get physics ID
    car_PhysicsID = carObj.getPhysicsId()
     
    # create a vehicle constraint 
    # vehicle_Constraint = PhysicsConstraints.createConstraint(car_PhysicsID, 0, 11)
    vehicle_Constraint = constraints.createConstraint(car_PhysicsID, 0, constraints.VEHICLE_CONSTRAINT)
     
    # # get the constraint ID
    constraint_ID = vehicle_Constraint.getConstraintId()
      
    # # get the vehicle constraint ID
    vehicleID = constraints.getVehicleConstraint(constraint_ID)

    # save vehicle constraint ID as an object variable
    carObj["vehicleID"] = vehicleID

    return vehicleID    

##########################   Tire names

def Tire_Objects():
    
    # tire names
    frontDriver    = "TireFD"  # front driver's tire 
    frontPassenger = "TireFP"  # front passenger's tire 
    rearDriver     = "TireRD"  # rear driver's tire
    rearPassenger  = "TireRP"  # rear passenger's tire
        
    # get current scene
    scene = logic.getCurrentScene()
    
    # get list of objects in scene
    objList = scene.objects

    # tire Name
    tire_0 = objList[frontDriver]    # front driver's tire 
    tire_1 = objList[frontPassenger] # front passenger's tire 
    tire_2 = objList[rearDriver]     # rear driver's tire
    tire_3 = objList[rearPassenger]  # rear passenger's tire

    return (tire_0, tire_1, tire_2, tire_3)

##########################   Tire positions

def Tire_Positions():

    # tire position
    tire_0_Pos = [ -2.0,   2.0,  0.0]  # front driver's tire 
    tire_1_Pos = [  2.0,   2.0,  0.0]  # front passenger's tire 
    tire_2_Pos = [ -2.0,  -3.0,  0.0]  # rear driver's tire 
    tire_3_Pos = [  2.0,  -3.0,  0.0]  # rear passenger's tire 
    
    return (tire_0_Pos, tire_1_Pos, tire_2_Pos, tire_3_Pos)

##########################   Tire radius

def Tire_Radius():

    # tire radius
    tire_0_Radius = 0.75   # front driver's tire 
    tire_1_Radius = 0.75   # front passenger's tire 
    tire_2_Radius = 0.75   # rear driver's tire 
    tire_3_Radius = 0.75   # rear passenger's tire 
    
    return (tire_0_Radius, tire_1_Radius, tire_2_Radius, tire_3_Radius)

##########################   Tire suspension

def Tire_Suspension():

    # tire suspension height
    tire_0_suspensionHeight = 0.3   # front driver's tire 
    tire_1_suspensionHeight = 0.3   # front passenger's tire 
    tire_2_suspensionHeight = 0.3   # rear driver's tire 
    tire_3_suspensionHeight = 0.3   # rear passenger's tire 
    
    return (tire_0_suspensionHeight, tire_1_suspensionHeight, tire_2_suspensionHeight, tire_3_suspensionHeight)

##########################   Tire suspension angle

def Tire_SuspensionAngle():

    # suspension angle from car object center
    tire_0_suspensionAngle = [ 0.0, 0.0, -1.0]   # front driver's tire 
    tire_1_suspensionAngle = [ 0.0, 0.0, -1.0]   # front passenger's tire 
    tire_2_suspensionAngle = [ 0.0, 0.0, -1.0]   # rear driver's tire 
    tire_3_suspensionAngle = [ 0.0, 0.0, -1.0]   # rear passenger's tire 
    
    return (tire_0_suspensionAngle, tire_1_suspensionAngle, tire_2_suspensionAngle, tire_3_suspensionAngle)

##########################   Tire axis

def Tire_Axis():

    # tire axis attached to axle
    tire_0_Axis = [ -1.0, 0.0, 0.0]   # front driver's tire 
    tire_1_Axis = [ -1.0, 0.0, 0.0]   # front passenger's tire 
    tire_2_Axis = [ -1.0, 0.0, 0.0]   # rear driver's tire 
    tire_3_Axis = [ -1.0, 0.0, 0.0]   # rear passenger's tire 
    
    return (tire_0_Axis, tire_1_Axis, tire_2_Axis, tire_3_Axis)


##########################   Tire steering

def Tire_Steering():

    # tire has steering
    tire_0_Steering = True   # front driver's tire 
    tire_1_Steering = True   # front passenger's tire 
    tire_2_Steering = False   # rear driver's tire 
    tire_3_Steering = False   # rear passenger's tire 
    
    return (tire_0_Steering, tire_1_Steering, tire_2_Steering, tire_3_Steering)


##########################   add tires

def Add_Tires(vehicleID, tireObj, tirePos, tireSuspensionAngle, tireAxis, tireSuspension, tireRadius, tireSteering):
    
    # loop through variables:  add wheels
    for tire in range(0,4):
        
        obj = tireObj[tire]
        pos = tirePos[tire]
        suspensionAngle = tireSuspensionAngle[tire]
        axis = tireAxis[tire]
        suspension = tireSuspension[tire]
        radius = tireRadius[tire]
        steering = tireSteering[tire]
    
        # Add front driver tire
        vehicleID.addWheel( obj, pos, suspensionAngle, axis,
                        suspension,  radius, steering )


####################################################

# run program
main()