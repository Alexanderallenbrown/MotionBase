#########################################
#
#   Suspension.py  Blender 2.49
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
from bge import logic,constraints

def main():

    # get the current controller
    controller = logic.getCurrentController()
    vehobj = controller.owner
    
    # get vehicle constraint ID
    vehicleID = ConstraintID(controller)
    


    # set tire grip
    Tire_Grip(vehicleID)
    
    # set suspension compression
    Suspension_Compression(vehicleID)
    
    # set suspension damping
    Suspension_Damping(vehicleID)
    
    # set suspension stiffness
    Suspension_Stiffness(vehicleID)
    
    # set roll influence
    Roll_Influence(vehicleID)

#########################################################

# get vehicle constraint ID
def ConstraintID(controller):

    # get car the controller is attached to
    carObj = controller.owner
        
    # get saved vehicle Constraint ID
    vehicleID = carObj["vehicleID"]
    
    return vehicleID


##########################################################

# set tire grip
def Tire_Grip(vehicleID,grip_0=1.0,grip_1=1.0,grip_2=1.0,grip_3=1.0):

    # grip_0 = 30.0     # front driver's tire 
    # grip_1 = 30.0     # front passenger's tire 
    # grip_2 = 30.0     # rear driver's tire
    # grip_3 = 30.0     # rear passenger's tire

    vehicleID.setTyreFriction(grip_0, 0)  # front driver's tire 
    vehicleID.setTyreFriction(grip_1, 1)  # front passenger's tire 
    vehicleID.setTyreFriction(grip_2, 2)  # rear driver's tire
    vehicleID.setTyreFriction(grip_3, 3)  # rear passenger's tire 

    # set tire grip
def Tire_Grip2(vehicleID,obj,grip_0=1.0,grip_1=1.0,grip_2=1.0,grip_3=1.0):



    vehicleID.setTyreFriction(grip_0, 0)  # front driver's tire 
    vehicleID.setTyreFriction(grip_1, 1)  # front passenger's tire 
    vehicleID.setTyreFriction(grip_2, 2)  # rear driver's tire
    vehicleID.setTyreFriction(grip_3, 3)  # rear passenger's tire 

##########################################################

# set suspendion compression
def Suspension_Compression(vehicleID):

    compression_0 = 6.0/2     # front driver's tire 
    compression_1 = 6.0/2     # front passenger's tire 
    compression_2 = 6.0/2     # rear driver's tire
    compression_3 = 6.0/2     # rear passenger's tire

    vehicleID.setSuspensionCompression(compression_0, 0)  # front driver's tire 
    vehicleID.setSuspensionCompression(compression_1, 1)  # front passenger's tire 
    vehicleID.setSuspensionCompression(compression_2, 2)  # rear driver's tire
    vehicleID.setSuspensionCompression(compression_3, 3)  # rear passenger's tire 


##########################################################
    
# set suspension damping
def Suspension_Damping(vehicleID):
    
    damp_0 = 5.0     # front driver's tire 
    damp_1 = 5.0     # front passenger's tire 
    damp_2 = 5.0     # rear driver's tire
    damp_3 = 5.0     # rear passenger's tire
    
    vehicleID.setSuspensionDamping(damp_0, 0)  # front driver's tire 
    vehicleID.setSuspensionDamping(damp_1, 1)  # front passenger's tire 
    vehicleID.setSuspensionDamping(damp_2, 2)  # rear driver's tire
    vehicleID.setSuspensionDamping(damp_3, 3)  # rear passenger's tire 


###########################################################

# set suspension stiffness
def Suspension_Stiffness(vehicleID):
    
    stiffness_0 = 125/2.0     # front driver's tire 
    stiffness_1 = 125/2.0     # front passenger's tire 
    stiffness_2 = 125/2.0     # rear driver's tire
    stiffness_3 = 125/2.0     # rear passenger's tire
    
    vehicleID.setSuspensionStiffness(stiffness_0, 0)  # front driver's tire 
    vehicleID.setSuspensionStiffness(stiffness_1, 1)  # front passenger's tire 
    vehicleID.setSuspensionStiffness(stiffness_2, 2)  # rear driver's tire
    vehicleID.setSuspensionStiffness(stiffness_3, 3)  # rear passenger's tire 

############################################################

# set roll influence
def Roll_Influence(vehicleID):

    # roll_0 = 0.6     # front driver's tire 
    # roll_1 = 0.6     # front passenger's tire 
    # roll_2 = 0.6     # rear driver's tire
    # roll_3 = 0.6     # rear passenger's tire
    roll_0 = 1     # front driver's tire 
    roll_1 = 1     # front passenger's tire 
    roll_2 = 1     # rear driver's tire
    roll_3 = 1     # rear passenger's tire

    vehicleID.setRollInfluence( roll_0, 0)  # front driver's tire 
    vehicleID.setRollInfluence( roll_1, 1)  # front passenger's tire 
    vehicleID.setRollInfluence( roll_2, 2)  # rear driver's tire
    vehicleID.setRollInfluence( roll_3, 3)  # rear passenger's tire 
    

###########################################################

# run main program
main()