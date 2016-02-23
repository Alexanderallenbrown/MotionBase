from numpy import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D


class MotionBase:

    def __init__(self,z0,baseradius,platformradius,motorarm,conrod):
        self.fig = figure()
        self.ax = self.fig.add_subplot(111, projection='3d')


        self.platform_z0 = z0#meters, the resting height of the base.

        self.baseradius = baseradius #meters, the radius of the base
        self.motorarm = motorarm #meters, length of the motor arm
        self.conrod= sqrt(self.platform_z0**2+self.motorarm**2)-.05 #meters, length of the connecting rod
        self.platform_radius = platformradius#meters, the radius of the platform

        #these are the yaw angles at which each motor sits.
        self.motor_yaws = arange(0,6)*pi/3-pi/6

        #calculate the positions of the motor shafts. X forward, Y left, Z up.
        self.motor_X = self.baseradius*cos(self.motor_yaws)
        self.motor_Y = self.baseradius*sin(self.motor_yaws)
        self.motor_Z = zeros(6)

        self.motor_thetas = zeros(6)#array([5*pi/6,pi/6,5*pi/6,pi/6,5*pi/6,pi/6])#zeros(6)

    def calculate_P(self,X,Y,Z,roll,pitch,yaw):
        #our goal is to take a platform pose and calculate a vector of 3 points on an equillateral triangle, to which all 6 motor con rods are attached.
        platform_yaw0 = array([0,2*pi/3,4*pi/3])
        platform_x = self.platform_radius*cos(platform_yaw0)#the middle of the platform's position, then transformed to each of the triangle's three points.
        platform_y = self.platform_radius*sin(platform_yaw0)#similar to X
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
            PZ[ind] = rotpoint[2]+Z+self.platform_z0

        return PX,PY,PZ

    def plotbase(self):
        #plot the lines
        self.ax.plot(self.motor_X,self.motor_Y,self.motor_Z,'k',marker='o')
        #connect the ends
        self.ax.plot([self.motor_X[-1],self.motor_X[0]],[self.motor_Y[-1],self.motor_Y[0]],[self.motor_Z[-1],self.motor_Z[0]],'k',marker='o')
        for ind in range(0,6):
            self.ax.annotate(str(ind+1),xy=(self.motor_X[ind],self.motor_Y[ind]),xytext=(self.motor_X[ind],self.motor_Y[ind]))

    def plotplatform(self,PX,PY,PZ):
        #plot the lines
        self.ax.plot(PX,PY,PZ,'r',marker='o')
        #connect the ends
        self.ax.plot([PX[-1],PX[0]],[PY[-1],PY[0]],[PZ[-1],PZ[0]],'r',marker='o')
    

    def plotlegs(self,RPO_X,RPO_Y,RPO_Z):
        for ind in range(0,6):
            self.ax.plot([self.motor_X[ind],self.motor_X[ind]+RPO_X[ind]],[self.motor_Y[ind],self.motor_Y[ind]+RPO_Y[ind]],[self.motor_Z[ind],self.motor_Z[ind]+RPO_Z[ind]],'g-.')

    def plotmotorarms(self,qx,qy,qz):
        for ind in range(0,len(qx)):
            self.ax.plot([self.motor_X[ind],qx[ind]],[self.motor_Y[ind],qy[ind]],[self.motor_Z[ind],qz[ind]],'m',marker='o')

    def plotconrods(self,QX,QY,QZ,PX,PY,PZ):
        for ind in range(0,len(QX)):
            self.ax.plot([QX[ind],PX[ind]],[QY[ind],PY[ind]],[QZ[ind],PZ[ind]],'m',marker='o')

    def plotbot(self,x,y,z,roll,pitch,yaw):#plots the whole kit.
        self.ax.clear()
        #self.ax.self.axis('equal')
        #self.ax.xlabel('X (m)')
        #self.ax.ylabel('Y (m)')
        #plot the base footprint
        self.plotbase()
        #plot the platform as we want it.
        PX,PY,PZ = self.calculate_P(x,y,z,roll,pitch,yaw)
        rpox,rpoy,rpoz = self.findrpo(x,y,z,roll,pitch,yaw)
        #make up some angles for the motors. TODO make this a function to solve for them.
        self.motor_thetas,junk = self.findthetam(x,y,z,roll,pitch,yaw,0.01)
        qx,qy,qz = self.calcQ(self.motor_thetas)
        self.plotplatform(PX,PY,PZ)
        self.plotlegs(rpox,rpoy,rpoz)
        self.plotmotorarms(qx,qy,qz)
        self.plotconrods(qx,qy,qz,rpox+self.motor_X,rpoy+self.motor_Y,rpoz+self.motor_Z)

        #self.axis([-2*self.baseradius,2*self.baseradius,-2*self.baseradius,2*self.baseradius])
        self.ax.set_xlim3d(-2*self.baseradius, 2*self.baseradius)
        self.ax.set_ylim3d(-2*self.baseradius,2*self.baseradius)
        self.ax.set_zlim3d(0,4*self.baseradius)
    
    

    def findrpo(self,x,y,z,roll,pitch,yaw):
        #first calculate the positions of the three platform points.
        PX,PY,PZ = self.calculate_P(x,y,z,roll,pitch,yaw)
        #now, use these positions to calculate the platform point corresponding to each motor.
        PX_aligned = array([PX[0],PX[0],PX[1],PX[1],PX[2],PX[2]])
        PY_aligned = array([PY[0],PY[0],PY[1],PY[1],PY[2],PY[2]])
        PZ_aligned = array([PZ[0],PZ[0],PZ[1],PZ[1],PZ[2],PZ[2]])

        #now return the vectors FROM the motors TO the points P.
        return PX_aligned-self.motor_X,PY_aligned-self.motor_Y,PZ_aligned-self.motor_Z

    def calcQ(self,thetam):
        #motor index gets us the correct motor. thetam is the motor shaft angle of that motor.
        QX = zeros(6)
        QY = zeros(6)
        QZ = zeros(6)
        for motor_index in range(0,6):
            QX[motor_index] = self.motor_X[motor_index] -self.motorarm*sin(self.motor_yaws[motor_index])*cos(thetam[motor_index])
            QY[motor_index] = self.motor_Y[motor_index]+self.motorarm*cos(self.motor_yaws[motor_index])*cos(thetam[motor_index])
            QZ[motor_index] = self.motor_Z[motor_index]+self.motorarm*sin(thetam[motor_index])
        return QX,QY,QZ


    def findconroderror(self,thetam,x,y,z,roll,pitch,yaw,motor_ind):
        qx,qy,qz = self.calcQ(thetam)#this is just an INITIAL GUESS.
        #now, we know where the points P should be for each of the 6 motors, so we can calculate the con rod length.
        rqox = qx-self.motor_X
        rqoy = qy-self.motor_Y
        rqoz = qz-self.motor_Z

        #now we calculate the rp/o vectors
        rpox,rpoy,rpoz = self.findrpo(x,y,z,roll,pitch,yaw)

        #now we calculate the con rod vector for each of the 6 motors. rp/q = rp/o-rq/o (difference between P and motor arm)
        rpqx = rpox-rqox
        rpqy = rpoy-rqoy
        rpqz = rpoz-rqoz

        #now we calculate the distance between the motor arm and P for each of the 6 points.
        conlengths = ((rpqx)**2+(rpqy)**2+(rpqz)**2)**.5
        #we are only setting one angle at a time, so let's pull only our current length out TODO INEFFICIENT!!!!!
        conlength = conlengths[motor_ind]
        return (self.conrod- conlength)

    def findthetam(self,x,y,z,roll,pitch,yaw,tol):
        # #create an initial guess for all 6 motor shaft angles.
        thetam = zeros(6)
        success = 1 #initialize to success

        for motor_ind in range(0,6):
            length_error = 1000
            iternum = 0
            min_theta = 0
            max_theta = pi/2

            while (abs(length_error)>tol and iternum<20) :
                
                #use the bisection method to find theta_m
                
                length_error = self.findconroderror(thetam,x,y,z,roll,pitch,yaw,motor_ind) #this is actually error squared.
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

    base = MotionBase(1.0,0.5,0.3,0.3,1.0)
        
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
        with writer.saving(base.fig,'output.mp4',len(t)):
            base.plotbot(0,0,zs[ind],rolls[ind],0,0)
            writer.grab_frame()
            pause(.01)


    show()