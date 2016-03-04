from numpy import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D

fig = figure()
ax = fig.add_subplot(111, projection='3d')

# x =[1,2,3,4,5,6,7,8,9,10]
# y =[5,6,2,3,13,4,1,2,4,8]
# z =[2,3,3,3,5,7,9,11,9,10]



# ax.scatter(x, y, z, c='r', marker='o')

# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# show()
# platform_z0 = 1.5#meters, the resting height of the base.

# baseradius = 1.5 #meters, the radius of the base
# motorarm = 0.3 #meters, length of the motor arm
# conrod = sqrt(platform_z0**2+motorarm)+.2 #meters, length of the connecting rod

# platform_z0 = 1.5#meters, the resting height of the base.
# platform_radius = 1.3#meters, the radius of the platform

platform_z0 = 1#meters, the resting height of the base.

baseradius = .5 #meters, the radius of the base
motorarm = 0.2 #meters, length of the motor arm
conrod = sqrt(platform_z0**2+motorarm**2)-.05 #meters, length of the connecting rod
platform_radius = .3#meters, the radius of the platform

#these are the yaw angles at which each motor sits.
motor_yaws = arange(0,6)*pi/3-pi/6

#calculate the positions of the motor shafts. X forward, Y left, Z up.
motor_X = baseradius*cos(motor_yaws)
motor_Y = baseradius*sin(motor_yaws)
motor_Z = zeros(6)

motor_thetas = zeros(6)#array([5*pi/6,pi/6,5*pi/6,pi/6,5*pi/6,pi/6])#zeros(6)

#set the motor angles to 45 degrees to start with.

print motor_yaws,motor_X,motor_Y

def calculate_P(X,Y,Z,roll,pitch,yaw):
    #our goal is to take a platform pose and calculate a vector of 3 points on an equillateral triangle, to which all 6 motor con rods are attached.
    platform_yaw0 = array([0,2*pi/3,4*pi/3])
    platform_x = platform_radius*cos(platform_yaw0)#the middle of the platform's position, then transformed to each of the triangle's three points.
    platform_y = platform_radius*sin(platform_yaw0)#similar to X
    platform_z = zeros(3) #height of the platform.

    #now, these are NOT rotated like we wanted! so let's rotate them.
    Rx = array([[1,0,0],[0,cos(roll),-sin(roll)],[0,sin(roll),cos(roll)]])
    Ry = array([[cos(pitch),0,sin(pitch)],[0,1,0],[-sin(pitch),0,cos(pitch)]])
    Rz = array([[cos(yaw),-sin(yaw),0],[sin(yaw),cos(yaw),0],[0,0,1]])
    #print Rx
    R = dot(dot(Rx,Ry),Rz)
    #R = eye(3)

    #initialize our vectors of platform point coordinates.
    PX = zeros(3)
    PY = zeros(3)
    PZ = zeros(3)

    #cycle through each of the three platform points and calculate the rotated version.
    for ind in range(0,3):
        currpoint = vstack([platform_x[ind],platform_y[ind],platform_z[ind]])
        rotpoint = dot(R,currpoint)
        PX[ind] = rotpoint[0]+X
        PY[ind] = rotpoint[1]+Y
        PZ[ind] = rotpoint[2]+Z+platform_z0

    return PX,PY,PZ

def plotbase():
    #plot the lines
    ax.plot(motor_X,motor_Y,motor_Z,'k',marker='o')
    #connect the ends
    ax.plot([motor_X[-1],motor_X[0]],[motor_Y[-1],motor_Y[0]],[motor_Z[-1],motor_Z[0]],'k',marker='o')
    for ind in range(0,6):
        ax.annotate(str(ind+1),xy=(motor_X[ind],motor_Y[ind]),xytext=(motor_X[ind],motor_Y[ind]))

def plotplatform(PX,PY,PZ):
    #plot the lines
    ax.plot(PX,PY,PZ,'r',marker='o')
    #connect the ends
    ax.plot([PX[-1],PX[0]],[PY[-1],PY[0]],[PZ[-1],PZ[0]],'r',marker='o')
    

def plotlegs(RPO_X,RPO_Y,RPO_Z):
    for ind in range(0,6):
        ax.plot([motor_X[ind],motor_X[ind]+RPO_X[ind]],[motor_Y[ind],motor_Y[ind]+RPO_Y[ind]],[motor_Z[ind],motor_Z[ind]+RPO_Z[ind]],'g-.')

def plotmotorarms(qx,qy,qz):
    for ind in range(0,len(qx)):
        ax.plot([motor_X[ind],qx[ind]],[motor_Y[ind],qy[ind]],[motor_Z[ind],qz[ind]],'m',marker='o')

def plotconrods(QX,QY,QZ,PX,PY,PZ):
    for ind in range(0,len(QX)):
        ax.plot([QX[ind],PX[ind]],[QY[ind],PY[ind]],[QZ[ind],PZ[ind]],'m',marker='o')

def plotbot(x,y,z,roll,pitch,yaw):#plots the whole kit.
    ax.clear()
    #ax.axis('equal')
    #ax.xlabel('X (m)')
    #ax.ylabel('Y (m)')
    #plot the base footprint
    plotbase()
    #plot the platform as we want it.
    PX,PY,PZ = calculate_P(x,y,z,roll,pitch,yaw)
    rpox,rpoy,rpoz = findrpo(x,y,z,roll,pitch,yaw)
    #make up some angles for the motors. TODO make this a function to solve for them.
    motor_thetas,junk = findthetam(x,y,z,roll,pitch,yaw,0.01)
    qx,qy,qz = calcQ(motor_thetas)
    plotplatform(PX,PY,PZ)
    plotlegs(rpox,rpoy,rpoz)
    plotmotorarms(qx,qy,qz)
    plotconrods(qx,qy,qz,rpox+motor_X,rpoy+motor_Y,rpoz+motor_Z)

    #axis([-2*baseradius,2*baseradius,-2*baseradius,2*baseradius])
    ax.set_xlim3d(-2*baseradius, 2*baseradius)
    ax.set_ylim3d(-2*baseradius,2*baseradius)
    ax.set_zlim3d(0,4*baseradius)
    
    

def findrpo(x,y,z,roll,pitch,yaw):
    #first calculate the positions of the three platform points.
    PX,PY,PZ = calculate_P(x,y,z,roll,pitch,yaw)
    #now, use these positions to calculate the platform point corresponding to each motor.
    PX_aligned = array([PX[0],PX[0],PX[1],PX[1],PX[2],PX[2]])
    PY_aligned = array([PY[0],PY[0],PY[1],PY[1],PY[2],PY[2]])
    PZ_aligned = array([PZ[0],PZ[0],PZ[1],PZ[1],PZ[2],PZ[2]])

    #now return the vectors FROM the motors TO the points P.
    return PX_aligned-motor_X,PY_aligned-motor_Y,PZ_aligned-motor_Z

def calcQ(thetam):
    #motor index gets us the correct motor. thetam is the motor shaft angle of that motor.
    QX = zeros(6)
    QY = zeros(6)
    QZ = zeros(6)
    for motor_index in range(0,6):
        QX[motor_index] = motor_X[motor_index] -motorarm*sin(motor_yaws[motor_index])*cos(thetam[motor_index])
        QY[motor_index] = motor_Y[motor_index]+motorarm*cos(motor_yaws[motor_index])*cos(thetam[motor_index])
        QZ[motor_index] = motor_Z[motor_index]+motorarm*sin(thetam[motor_index])
    return QX,QY,QZ


def findconroderror(thetam,x,y,z,roll,pitch,yaw,motor_ind):
    qx,qy,qz = calcQ(thetam)#this is just an INITIAL GUESS.
    #now, we know where the points P should be for each of the 6 motors, so we can calculate the con rod length.
    rqox = qx-motor_X
    rqoy = qy-motor_Y
    rqoz = qz-motor_Z

    #now we calculate the rp/o vectors
    rpox,rpoy,rpoz = findrpo(x,y,z,roll,pitch,yaw)

    #now we calculate the con rod vector for each of the 6 motors. rp/q = rp/o-rq/o (difference between P and motor arm)
    rpqx = rpox-rqox
    rpqy = rpoy-rqoy
    rpqz = rpoz-rqoz

    #now we calculate the distance between the motor arm and P for each of the 6 points.
    conlengths = ((rpqx)**2+(rpqy)**2+(rpqz)**2)**.5
    #we are only setting one angle at a time, so let's pull only our current length out TODO INEFFICIENT!!!!!
    conlength = conlengths[motor_ind]
    return (conrod - conlength)

def findthetam(x,y,z,roll,pitch,yaw,tol):
    # thetam = zeros(6)
    # #create an initial guess for all 6 motor shaft angles.
    # thetas = linspace(0,pi/2,50)
    # for ind in range(0,6):

    #     for indtheta in range(0,len(thetas)):
    #         thetam[ind] = thetas[indtheta]

    #thetam = 0*ones(6)#initialize all angles to 45 degrees.
    #initialize connecting rod lengths

    #thetam = motor_thetas
    thetam = zeros(6)
    success = 1 #initialize to success

    for motor_ind in range(0,6):
        length_error = 1000
        iternum = 0
        min_theta = 0
        max_theta = pi/2

        while (abs(length_error)>tol and iternum<20) :
            
            #use the bisection method to find theta_m
            
            length_error = findconroderror(thetam,x,y,z,roll,pitch,yaw,motor_ind) #this is actually error squared.
            if length_error<0:#this means the con rod would have to be longer, so need an angle increase
                min_theta=thetam[motor_ind]
            else:#this means the con rod would have to be shorter. need an angle decrease.
                max_theta=thetam[motor_ind]
            iternum+=1
            
            #adjust current angle based on max    
            if abs(length_error)>tol:
                thetam[motor_ind]=min_theta+(max_theta-min_theta)/2

            if max_theta<=0:
                max_theta=0
            if min_theta>=pi/2:
                max_theta = pi/2

        #if iternum is greater than 19, then we have failed. we need to set success to 0.
        if iternum>=19:
            success=0
    return thetam,success


    
if __name__=='__main__':


        
    #thetas = findthetam(0,0,0,0,0,.1,0.01)
    makemovie = True

    if makemovie==True:
                import matplotlib
                #matplotlib.use('Agg')
                import matplotlib.animation as manimation
                FFMpegWriter = manimation.writers['ffmpeg']
                metadata = dict(title='Demo Movie',artist = 'Matplotlib',comment='motion base')
                writer = FFMpegWriter(fps=30,metadata=metadata)

    ion()
    t = linspace(0,10,100)
    rolls = .1*sin(1*t)
    zs = .05*(sin(1*t))

    for ind in range(0,len(t)):
        with writer.saving(fig,'output.mp4',len(t)):
            plotbot(0,0,zs[ind],rolls[ind],0,0)
            writer.grab_frame()
            pause(.01)


    show()