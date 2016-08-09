
import bge
import osvr.ClientKit

from math import *

cont = bge.logic.getCurrentController()
own = cont.owner
running = True

def testCallback(userdata, timestamp, report):
    import mathutils
    import Math

    print("Position = (%f, %f, %f)" % (report.contents.pose.translation.data[0], report.contents.pose.translation.data[1], report.contents.pose.translation.data[2]))
    print("Orientation = (%f, %f, %f, %f)\n" % (report.contents.pose.rotation.data[0], report.contents.pose.rotation.data[1], report.contents.pose.rotation.data[2], report.contents.pose.rotation.data[3]))
    #own.position[0] = report.contents.pose.translation.data[0]
    #own.position[1] = report.contents.pose.translation.data[1]
    #own.position[2] = report.contents.pose.translation.data[2]\

    #quad of helmet orientation
    q = [report.contents.pose.rotation.data[0],report.contents.pose.rotation.data[1],report.contents.pose.rotation.data[2],report.contents.pose.rotation.data[3]]
    #convert to roll pitch yaw
    tri = [atan2(2*((q[0]*q[1])+(q[2]*q[3])),(1-2*((q[1]*q[1])+(q[2]*q[2])))),asin(2*((q[0]*q[2])-(q[3]*q[1]))),atan2(2*((q[0]*q[3])+(q[1]*q[2])),(1-2*((q[2]*q[2])+(q[3]*q[3]))))]
    #quad of camera orientation
    o = own.orientation
    qw = sqrt(1+o[0][0]+o[1][1]+o[2][2])/2
    qx = (o[2][1]-o[1][2])/(4*qw)
    qy = (o[0][2]-o[2][0])/(4*qw)
    qz = (o[1][0]-o[0][1])/(4*qw)
    q2 = [qw,qx,qy,qz]

    #convert to roll pitch yaw
    tri2 = [atan2(2*((q2[0]*q2[1])+(q2[2]*q2[3])),(1-2*((q2[1]*q2[1])+(q2[2]*q2[2])))),asin(2*((q2[0]*q2[2])-(q2[3]*q2[1]))),atan2(2*((q2[0]*q2[3])+(q2[1]*q2[2])),(1-2*((q2[2]*q2[2])+(q2[3]*q2[3]))))]

    #change roll
    tri[0] = tri[0]+(pi/2)
    #switch pitch and yaw
    temp = tri[1]
    tri[1] = tri[2]
    tri[2] = temp

    tri[2] = tri[2]-(pi/2)
    #change tri to be some of both things
    #tri[0] = tri[0] + tri2[0]
    #tri[1] = tri[1] + tri2[1]
    #tri[2] = tri[2] + tri2[2]
    #convert back to new quat
    q3 = [(cos(tri[0]/2)*cos(tri[1]/2)*cos(tri[2]/2))+(sin(tri[0]/2)*sin(tri[1]/2)*sin(tri[2]/2)),(sin(tri[0]/2)*cos(tri[1]/2)*cos(tri[2]/2))-(cos(tri[0]/2)*sin(tri[1]/2)*sin(tri[2]/2)),(cos(tri[0]/2)*sin(tri[1]/2)*cos(tri[2]/2))+(sin(tri[0]/2)*cos(tri[1]/2)*sin(tri[2]/2)),(cos(tri[0]/2)*cos(tri[1]/2)*sin(tri[2]/2))-(sin(tri[0]/2)*sin(tri[1]/2)*cos(tri[2]/2))]



    #blendrot = mathutils.Quaternion([report.contents.pose.rotation.data[0],report.contents.pose.rotation.data[1],report.contents.pose.rotation.data[2],report.contents.pose.rotation.data[3]])
    blendrot = mathutils.Quaternion([q3[0],q3[1],q3[2],q3[3]])
    own.orientation = blendrot


ctx = osvr.ClientKit.ClientContext("com.osvr.exampleclients.TrackerCallback")
lefthand = ctx.getInterface("/me/head")

OSVRCallback = osvr.ClientKit.PoseCallback(testCallback)

lefthand.registerCallback(OSVRCallback, None)

def blender_runs_this():
    if (running == True):
        ctx.update()


def quit():
    ctx.shutdown()
    running = False

