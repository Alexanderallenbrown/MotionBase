"""
This module provides access to the OSVR ClientKit C API via the foreign function interface ctypes. 
Each class defines the struct of the same name in the C API. Likewise, each method defines the function of the same name in the C API.
For reference, view the C API documentation at http://resource.osvr.com/docs/OSVR-Core/group__ClientKit.html 
"""
from ctypes import *

mylib = cdll.LoadLibrary("/usr/local/lib/libosvrClientKit.so")

class OSVR_ClientContextObject(Structure):
    pass

OSVR_ClientContext = POINTER(OSVR_ClientContextObject)

class OSVR_ClientInterfaceObject(Structure):
    pass

OSVR_ClientInterface = POINTER(OSVR_ClientInterfaceObject)

class OSVR_DisplayConfigObject(Structure):
    pass

OSVR_DisplayConfig = POINTER(OSVR_DisplayConfigObject)

class OSVR_Vec2(Structure):
    _fields_ = [("data", c_double * 2)]

class OSVR_Vec3(Structure):
    _fields_ = [("data", c_double * 3)]

class OSVR_Quaternion(Structure):
    _fields_ = [("data", c_double * 4)]

class OSVR_Pose3(Structure):
    _fields_ = [("translation", OSVR_Vec3), ("rotation", OSVR_Quaternion)]

class OSVR_RadialDistortionParameters(Structure):
    _fields_ = [("k1", OSVR_Vec3), ("centerOfProjection", OSVR_Vec2)]

class OSVR_TimeValue(Structure):
    _fields_ = [("seconds", c_int64),("microseconds", c_int32)]

class OSVR_DisplayDimensions(Structure):
    _fields_ = [("width", c_int32), ("height", c_int32)]

class OSVR_RelativeViewport(Structure):
    _fields_ = [("left", c_int32), ("bottom", c_int32), ("width", c_int32), ("height", c_int32)]

class OSVR_ClippingPlanes(Structure):
    _fields_ = [("left", c_double), ("right", c_double), ("bottom", c_double), ("top", c_double)]

class OSVR_EyeTracker3DState(Structure):
    _fields_ = [("direction", OSVR_Vec3), ("basePoint", OSVR_Vec3)]

# InterfaceCallbackC.h data types

class OSVR_PoseReport(Structure):
    _fields_ = [("sensor", c_int32), ("pose", OSVR_Pose3)]

class OSVR_PositionReport(Structure):
    _fields_ = [("sensor", c_int32), ("xyz", OSVR_Vec3)]

class OSVR_OrientationReport(Structure):
    _fields_ = [("sensor", c_int32), ("rotation", OSVR_Quaternion)]

class OSVR_ButtonReport(Structure):
    _fields_ = [("sensor", c_int32), ("state", c_uint8)]

class OSVR_AnalogReport(Structure):
    _fields_ = [("sensor", c_int32), ("state", c_double)]

#This does not seem to exist in the C file, probably mention this to Ryan
#class OSVR_ImagingReport(Structure):
#    _fields_ = [(), ()]


class OSVR_Location2DReport(Structure):
    _fields_ = [("sensor", c_uint32), ("location", OSVR_Vec2)]

class OSVR_DirectionReport(Structure):
    _fields_ = [("sensor", c_uint32), ("direction", OSVR_Vec3)]


#using cbool for now, may need to change depending on what exactly bool is in the C code, probably gonna be OSVR_CBool
class OSVR_EyeTracker2DReport(Structure):
    _fields_ = [("locationValid", c_bool), ("sensor", c_uint32), ("state", OSVR_Vec2)]

class OSVR_EyeTracker3DReport(Structure):
    _fields_ = [("directioinValid", c_bool), ("basePointValid", c_bool), ("sensor", c_uint32), ("state", OSVR_EyeTracker3DState)]

class OSVR_EyeTrackerBlinkReport(Structure):
    _fields_ = [("blinkValid", c_bool), ("sensor", c_uint32), ("state", c_uint8)]

class OSVR_NaviVelocityReport(Structure):
    _fields_ = [("sensor", c_uint32), ("state", OSVR_Vec2)]

class OSVR_NaviPositionReport(Structure):
    _fields_ = [("sensor", c_uint32), ("state", OSVR_Vec2)]


#IMPORTANT: To create a TYPECallback function pointer to pass to OSVR_RegisterTYPECallback, you must make a python function to be called
#   and then pass it to OSVR_TYPECallback, i.e.
#
#def my_pose_callback_function(c_void_p variable, POINTER(OSVR_TimeValue) variable, POINTER(OSVR_PoseReport) variable):
#   .....
#
#interface = OSVR_ClientGetInterface(...)
#
#callback = OSVR_PoseCallback(my_pose_callback_function)
#
#osvrRegisterPoseCallback(interface, callback, None)


OSVR_PoseCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_PoseReport))

OSVR_PositionCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_PositionReport))

OSVR_OrientationCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_OrientationReport))

OSVR_ButtonCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_ButtonReport))

OSVR_AnalogCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_AnalogReport))

#Commented out because the OSVR_ImagingReport type is not defined in C, may be included in the future
#OSVR_ImagingCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_ImagingReport))

OSVR_Location2DCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_Location2DReport))

OSVR_DirectionCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_DirectionReport))

OSVR_EyeTracker2DCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_EyeTracker2DReport))

OSVR_EyeTracker3DCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_EyeTracker3DReport))

OSVR_EyeTrackerBlinkCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_EyeTrackerBlinkReport))

OSVR_NaviVelocityCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_NaviVelocityReport))

OSVR_NaviPositionCallback = CFUNCTYPE(None, c_void_p, POINTER(OSVR_TimeValue), POINTER(OSVR_NaviPositionReport))


# Error checking

class ReturnError(Exception):
    def __init__(self, value, function):
        self.value = value
        self.function = function
    def __str__(self):
        return repr(self.function)

def checkReturn(returnvalue, function):
    if returnvalue == 1:
        raise ReturnError(returnvalue, function)

# ContextC.h functions

def osvrClientInit(applicationIdentifier):
    mylib.osvrClientInit.argtypes = [c_char_p, c_uint32]
    mylib.osvrClientInit.restype = OSVR_ClientContext
    return mylib.osvrClientInit(c_char_p(applicationIdentifier.encode("utf8")), c_uint32(0))

def osvrClientUpdate(ctx):
    mylib.osvrClientUpdate.argtypes = [OSVR_ClientContext]
    mylib.osvrClientUpdate.restype = c_int8
    returnvalue = mylib.osvrClientUpdate(ctx)
    checkReturn(returnvalue, 'osvrClientUpdate')
    return

def osvrClientCheckStatus(ctx):
    mylib.osvrClientCheckStatus.argtypes = [OSVR_ClientContext]
    mylib.osvrClientCheckStatus.restype = c_int8
    returnvalue = mylib.osvrClientCheckStatus(ctx)
    checkReturn(returnvalue, 'osvrClientCheckStatus')
    return

def osvrClientShutdown(ctx):
    mylib.osvrClientShutdown.argtypes = [OSVR_ClientContext]
    mylib.osvrClientShutdown.restype = c_int8
    returnvalue = mylib.osvrClientShutdown(ctx)
    checkReturn(returnvalue, 'osvrClientShutdown')
    return

# DisplayC.h functions

def osvrClientGetDisplay(ctx):
    mylib.osvrClientGetDisplay.argtypes = [OSVR_ClientContext, POINTER(OSVR_DisplayConfig)]
    mylib.osvrClientGetDisplay.restype = c_int8
    disp = pointer(OSVR_DisplayConfigObject())
    returnvalue = mylib.osvrClientGetDisplay(ctx, pointer(disp))
    checkReturn(returnvalue, 'osvrClientGetDisplay')
    return disp

def osvrClientFreeDisplay(disp):
    mylib.osvrClientFreeDisplay.argtypes = [OSVR_DisplayConfig]
    mylib.osvrClientFreeDisplay.restype = c_int8
    returnvalue = mylib.osvrClientFreeDisplay(disp)
    checkReturn(returnvalue, 'osvrClientFreeDisplay')
    return

def osvrClientCheckDisplayStartup(disp):
    mylib.osvrClientCheckDisplayStartup.argtypes = [OSVR_DisplayConfig]
    mylib.osvrClientCheckDisplayStartup.restype = c_int8
    returnvalue = mylib.osvrClientCheckDisplayStartup(disp)
    checkReturn(returnvalue, 'osvrClientCheckDisplayStartup')
    return

def osvrClientGetNumDisplayInputs(disp):
    mylib.osvrClientGetNumDisplayInputs.argtypes = [OSVR_DisplayConfig, POINTER(c_uint8)]
    mylib.osvrClientGetNumDisplayInputs.restype = c_int8
    numDisplayInputs = c_uint8()
    returnvalue = mylib.osvrClientGetNumDisplayInputs(disp, pointer(numDisplayInputs))
    checkReturn(returnvalue, 'osvrClientGetNumDisplayInputs')
    return numDisplayInputs

def osvrClientGetDisplayDimensions(disp, displayInputIndex):
    mylib.osvrClientGetDisplayDimensions.argtypes = [OSVR_DisplayConfig, c_uint8, POINTER(c_int32), POINTER(c_int32)]
    mylib.osvrClientGetDisplayDimensions.restype = c_int8
    dimensions = OSVR_DisplayDimensions()
    returnvalue = mylib.osvrClientGetDisplayDimensions(disp, c_uint8(displayInputIndex), pointer(dimensions.width), pointer(dimensions.height))
    checkReturn(returnvalue, 'osvrClientGetDisplayDimensions')
    return dimensions

def osvrClientGetNumViewers(disp):
    mylib.osvrClientGetNumViewers.argtypes = [OSVR_DisplayConfig, POINTER(c_uint32)]
    mylib.osvrClientGetNumViewers.restype = c_int8
    viewers = c_uint32()
    returnvalue = mylib.osvrClientGetNumViewers(disp, pointer(viewers))
    checkReturn(returnvalue, 'osvrClientGetNumViewers')
    return viewers

def osvrClientGetViewerPose(disp, viewer):
    mylib.osvrClientGetViewerPose.argtypes = [OSVR_DisplayConfig, c_uint32, POINTER(OSVR_Pose3)]
    mylib.osvrClientGetViewerPose.restype = c_int8
    pose = OSVR_Pose3()
    returnvalue = mylib.osvrClientGetViewerPose(disp, c_uint32(viewer), pointer(pose))
    checkReturn(returnvalue, 'osvrClientGetViewerPose')
    return pose

def osvrClientGetNumEyesForViewer(disp, viewer):
    mylib.osvrClientGetNumEyesForViewer.argtypes = [OSVR_DisplayConfig, c_uint32, POINTER(c_uint8)]
    mylib.osvrClientGetNumEyesForViewer.restype = c_int8
    eyes = c_uint8()
    returnvalue = mylib.osvrClientGetNumEyesForViewer(disp, c_uint32(viewer), pointer(eyes))
    checkReturn(returnvalue, 'osvrClientGetNumEyesForViewer')
    return eyes

def osvrClientGetViewerEyePose(disp, viewer, eye):
    mylib.osvrClientGetViewerEyePose.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint8, POINTER(OSVR_Pose3)]
    mylib.osvrClientGetViewerEyePose.restype = c_int8
    pose = OSVR_Pose3()
    returnvalue = mylib.osvrClientGetViewerPose(disp, c_uint32(viewer), c_uint8(eye), pointer(pose))
    checkReturn(returnvalue, 'osvrClientGetViewerEyePose')
    return pose

def osvrClientGetViewerEyeViewMatrixd(disp, viewer, eye, flags):
    mylib.osvrClientGetViewerEyeViewMatrixd.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint8, c_uint16, POINTER(c_double)]
    mylib.osvrClientGetViewerEyeViewMatrixd.restype = c_int8
    mat = c_double()
    returnvalue = mylib.osvrClientGetViewerEyeViewMatrixd(disp, c_uint32(viewer), c_uint8(eye), c_uint16(flags), pointer(mat))
    checkReturn(returnvalue, 'osvrClientGetViewerEyeViewMatrixd')
    return mat

def osvrClientGetViewerEyeViewMatrixf(disp, viewer, eye, flags):
    mylib.osvrClientGetViewerEyeViewMatrixf.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint8, c_uint16, POINTER(c_float)]
    mylib.osvrClientGetViewerEyeViewMatrixf.restype = c_int8
    mat = c_float()
    returnvalue = mylib.osvrClientGetViewerEyeViewMatrixd(disp, c_uint32(viewer), c_uint8(eye), c_uint16(flags), pointer(mat))
    checkReturn(returnvalue, 'osvrClientGetViewerEyeViewMatrixf')
    return mat

def osvrClientGetNumSurfacesForViewerEye(disp, viewer, eye):
    mylib.osvrClientGetNumSurfacesForViewerEye.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint8, POINTER(c_uint32)]
    mylib.osvrClientGetNumSurfacesForViewerEye.restype = c_int8
    surfaces = c_uint32()
    returnvalue = mylib.osvrClientGetNumSurfacesForViewerEye(disp, c_uint32(viewer), c_uint8(eye), pointer(surfaces))
    checkReturn(returnvalue, 'osvrClientGetNumSurfacesForViewerEye')
    return surfaces

def osvrClientGetRelativeViewportForViewerEyeSurface(disp, viewer, eye, surface):
    mylib.osvrClientGetRelativeViewportForViewerEyeSurface.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint8, c_uint32, POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32)]
    mylib.osvrClientGetRelativeViewportForViewerEyeSurface.restype = c_int8
    viewport = OSVR_RelativeViewport()
    returnvalue = mylib.osvrClientGetRelativeViewportForViewerEyeSurface(disp, c_uint32(viewer), c_uint8(eye), c_uint32(surface), pointer(viewport.left), pointer(viewport.bottom), pointer(viewport.width), pointer(viewport.height))
    checkReturn(returnvalue, 'osvrClientGetRelativeViewportForViewerEyeSurface')
    return viewport

def osvrClientGetViewerEyeSurfaceDisplayInputIndex(disp, viewer, eye, surface):
    mylib.osvrClientGetViewerEyeSurfaceDisplayInputIndex.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint8, c_uint32, POINTER(c_uint8)]
    mylib.osvrClientGetViewerEyeSurfaceDisplayInputIndex.restype = c_int8
    displayInput = c_uint8()
    returnvalue = osvrClientGetViewerEyeSurfaceDisplayInputIndex(disp, c_uint32(viewer), c_uint8(eye), c_uint32(surface), pointer(displayInput))
    checkReturn(returnvalue, 'osvrClientGetRelativeViewportEyeSurfaceDisplayInputIndex')
    return displayInput

def osvrClientGetViewerEyeSurfaceProjectionMatrixd(disp, viewer, eye, surface, near, far, flags):
    mylib.osvrClientGetViewerEyeSurfaceProjectionMatrixd.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint8, c_uint32, c_double, c_double, c_uint16, POINTER(c_double)]
    mylib.osvrClientGetViewerEyeSurfaceProjectionMatrixd.restype = c_int8
    matrix = c_double()
    returnvalue = mylib.osvrClientGetViewerEyeSurfaceProjectionMatrixd(disp, c_uint32(viewer), c_uint8(eye), c_uint32(surface), c_double(near), c_double(far), c_uint16(flags), pointer(matrix))
    checkReturn(returnvalue, 'osvrClientGetViewerEyeSurfaceProjectionMatrixd')
    return matrix

def osvrClientGetViewerEyeSurfaceProjectionMatrixf(disp, viewer, eye, surface, near, far, flags):
    mylib.osvrClientGetViewerEyeSurfaceProjectionMatrixf.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint8, c_uint32, c_double, c_double, c_uint16, POINTER(c_float)]
    mylib.osvrClientGetViewerEyeSurfaceProjectionMatrixf.restype = c_int8
    matrix = c_float()
    returnvalue = mylib.osvrClientGetViewerEyeSurfaceProjectionMatrixf(disp, c_uint32(viewer), c_uint8(eye), c_uint32(surface), c_double(near), c_double(far), c_uint16(flags), pointer(matrix))
    checkReturn(returnvalue, 'osvrClientGetViewerEyeSurfaceProjectionMatrixf')
    return matrix

def osvrClientGetViewerEyeSurfaceProjectionClippingPlanes(disp, viewer, eye, surface):
    mylib.osvrClientGetViewerEyeSurfaceProjectionClippingPlanes.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint32, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    mylib.osvrClientGetViewerEyeSurfaceProjectionClippingPlanes.restype = c_int8
    planes = OSVR_ClippingPlanes()
    returnvalue = mylib.osvrClientGetViewerEyeSurfaceProjectionClippingPlanes(disp, c_uint32(viewer), c_uint8(eye), c_uint32(surface), pointer(planes.left), pointer(planes.right), pointer(planes.bottom), pointer(planes.top))
    checkReturn(returnvalue, 'osvrClientGetViewerEyeSurfaceProjectionClippingPlanes')
    return planes

def osvrClientDoesViewerEyeSurfaceWantDistortion(disp, viewer, eye, surface):
    mylib.osvrClientDoesViewerEyeSurfaceWantDistortion.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint32, POINTER(c_uint8)]
    mylib.osvrClientDoesViewerEyeSurfaceWantDistortion.restype = c_int8
    request = c_uint8()
    returnvalue = mylib.osvrClientDoesViewerEyeSurfaceWantDistortion(disp, c_uint32(viewer), c_uint8(eye), c_uint32(surface), pointer(request))
    checkReturn(returnvalue, 'osvrClientDoesViewerEyeSurfaceWantDistortion')
    return request

def osvrClientGetViewerEyeSurfaceRadialDistortionPriority(disp, viewer, eye, surface):
    mylib.osvrClientGetViewerEyeSurfaceRadialDistortionPriority.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint32, POINTER(c_int32)]
    mylib.osvrClientGetViewerEyeSurfaceRadialDistortionPriority.restype = c_int8
    priority = c_int32()
    returnvalue = mylib.osvrClientGetViewerEyeSurfaceRadialDistortionPriority(disp, c_uint32(viewer), c_uint8(eye), c_uint32(surface), pointer(priority))
    checkReturn(returnvalue, 'osvrClientGetViewerEyeSurfaceRadialDistortionPriority')
    return priority

def osvrClientGetViewerEyeSurfaceRadialDistortion(disp, viewer, eye, surface):
    mylib.osvrClientGetViewerEyeSurfaceRadialDistortion.argtypes = [OSVR_DisplayConfig, c_uint32, c_uint8, c_uint32, POINTER(OSVR_RadialDistortionParameters)]
    mylib.osvrClientGetViewerEyeSurfaceRadialDistortion.restype = c_int8
    params = OSVR_RadialDistortionParameters()
    returnvalue = mylib.osvrClientGetViewerEyeSurfaceRadialDistortion(disp, c_uint32(viewer), c_uint8(eye), c_uint32(surface), pointer(params))
    checkReturn(returnvalue, 'osvrClientGetViewerEyeSurfaceRadialDistortion')
    return params

# ImagingC.h functions
# These don't seem to be included in the doxygen docs

def osvrClientFreeImage(ctx, buf):
    mylib.osvrClientFreeImage.argtypes = [OSVR_ClientContext, POINTER(c_ubyte)]
    mylib.osvrClientFreeImage.restype = c_int8
    returnvalue = mylib.osvrClientFreeImage(ctx, buf)
    checkReturn(returnvalue, 'osvrClientFreeImage')
    return

# InterfaceC.h functions

def osvrClientGetInterface(ctx, path):
    mylib.osvrClientGetInterface.argtypes = [OSVR_ClientContext, c_char_p, POINTER(OSVR_ClientInterface)]
    mylib.osvrClientGetInterface.restype = c_int8
    interface = pointer(OSVR_ClientInterfaceObject())
    returnvalue = mylib.osvrClientGetInterface(ctx, c_char_p(path.encode("utf8")), pointer(interface))
    checkReturn(returnvalue, 'osvrClientGetInterface')
    return interface

def osvrClientFreeInterface(ctx, iface):
    mylib.osvrClientFreeInterface.argtypes = [OSVR_ClientContext, OSVR_ClientInterface]
    mylib.osvrClientFreeInterface.restype = c_int8
    returnvalue = mylib.osvrClientFreeInterface(ctx, iface)
    checkReturn(returnvalue, 'osvrClientFreeInterface')
    return

# InterfaceCallbackC.h functions

def osvrRegisterPoseCallback(iface, cb, userdata):
    mylib.osvrRegisterPoseCallback.argtypes = [OSVR_ClientInterface, OSVR_PoseCallback, c_void_p]
    mylib.osvrRegisterPoseCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterPoseCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterPoseCallback')
    return
    
def osvrRegisterPositionCallback(iface, cb, userdata):
    mylib.osvrRegisterPositionCallback.argtypes = [OSVR_ClientInterface, OSVR_PositionCallback, c_void_p]
    mylib.osvrRegisterPositionCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterPositionCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterPositionCallback')
    return

def osvrRegisterOrientationCallback(iface, cb, userdata):
    mylib.osvrRegisterOrientationCallback.argtypes = [OSVR_ClientInterface, OSVR_OrientationCallback, c_void_p]
    mylib.osvrRegisterOrientationCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterOrientationCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterOrientationCallback')
    return

def osvrRegisterButtonCallback(iface, cb, userdata):
    mylib.osvrRegisterButtonCallback.argtypes = [OSVR_ClientInterface, OSVR_ButtonCallback, c_void_p]
    mylib.osvrRegisterButtonCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterButtonCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterButtonCallback')
    return

def osvrRegisterAnalogCallback(iface, cb, userdata):
    mylib.osvrRegisterAnalogCallback.argtypes = [OSVR_ClientInterface, OSVR_AnalogCallback, c_void_p]
    mylib.osvrRegisterAnalogCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterAnalogCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterAnalogCallback')
    return

#Commented out because ImagingReport is not defined
#def osvrRegisterImagingCallback(iface, cb, userdata):
#    mylib.osvrRegisterImagingCallback.argtypes = [OSVR_ClientInterface, OSVR_ImagingCallback, c_void_p]
#    mylib.osvrRegisterImagingCallback.restype = c_int8
#    returnvalue = mylib.osvrRegisterImagingCallback(iface, cb, c_void_p(userdata))
#    checkReturn(returnvalue, 'osvrRegisterImagingCallback')
#    return

def osvrRegisterLocation2DCallback(iface, cb, userdata):
    mylib.osvrRegisterLocation2DCallback.argtypes = [OSVR_ClientInterface, OSVR_Location2DCallback, c_void_p]
    mylib.osvrRegisterLocation2DCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterLocation2DCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterLocation2DCallback')
    return

def osvrRegisterDirectionCallback(iface, cb, userdata):
    mylib.osvrRegisterDirectionCallback.argtypes = [OSVR_ClientInterface, OSVR_DirectionCallback, c_void_p]
    mylib.osvrRegisterDirectionCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterDirectionCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterDirectionCallback')
    return

def osvrRegisterEyeTracker2DCallback(iface, cb, userdata):
    mylib.osvrRegisterEyeTracker2DCallback.argtypes = [OSVR_ClientInterface, OSVR_EyeTracker2DCallback, c_void_p]
    mylib.osvrRegisterEyeTracker2DCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterEyeTracker2DCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterEyeTracker2DCallback')
    return

def osvrRegisterEyeTracker3DCallback(iface, cb, userdata):
    mylib.osvrRegisterEyeTracker3DCallback.argtypes = [OSVR_ClientInterface, OSVR_EyeTracker3DCallback, c_void_p]
    mylib.osvrRegisterEyeTracker3DCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterEyeTracker3DCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterEyeTracker3DCallback')
    return

def osvrRegisterEyeTrackerBlinkCallback(iface, cb, userdata):
    mylib.osvrRegisterEyeTrackerBlinkCallback.argtypes = [OSVR_ClientInterface, OSVR_EyeTrackerBlinkCallback, c_void_p]
    mylib.osvrRegisterEyeTrackerBlinkCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterEyeTrackerBlinkCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterEyeTrackerBlinkCallback')
    return

def osvrRegisterNaviVelocityCallback(iface, cb, userdata):
    mylib.osvrRegisterNaviVelocityCallback.argtypes = [OSVR_ClientInterface, OSVR_NaviVelocityCallback, c_void_p]
    mylib.osvrRegisterNaviVelocityCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterNaviVelocityCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterNaviVelocityCallback')
    return

def osvrRegisterNaviPositionCallback(iface, cb, userdata):
    mylib.osvrRegisterNaviPositionCallback.argtypes = [OSVR_ClientInterface, OSVR_NaviPositionCallback, c_void_p]
    mylib.osvrRegisterNaviPositionCallback.restype = c_int8
    returnvalue = mylib.osvrRegisterNaviPositionCallback(iface, cb, c_void_p(userdata))
    checkReturn(returnvalue, 'osvrRegisterNaviPositionCallback')
    return

# InterfaceStateC.h functions

def osvrGetPoseState(iface):
    mylib.osvrGetPoseState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(OSVR_Pose3)]
    mylib.osvrGetPoseState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = OSVR_Pose3()
    returnvalue = mylib.osvrGetPoseState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetPoseState')
    return (state, timestamp)

def osvrGetPositionState(iface):
    mylib.osvrGetPositionState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(OSVR_Vec3)]
    mylib.osvrGetPositionState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = OSVR_Vec3()
    returnvalue = mylib.osvrGetPositionState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetPositionState')
    return (state, timestamp)

def osvrGetOrientationState(iface):
    mylib.osvrGetOrientationState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(OSVR_Quaternion)]
    mylib.osvrGetOrientationState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = OSVR_Quaternion()
    returnvalue = mylib.osvrGetOrientationState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetOrientationState')
    return (state, timestamp)

def osvrGetButtonState(iface):
    mylib.osvrGetButtonState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(c_uint8)]
    mylib.osvrGetButtonState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = c_uint8()
    returnvalue = mylib.osvrGetButtonState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetButtonState')
    return (state, timestamp)

def osvrGetAnalogState(iface):
    mylib.osvrGetAnalogState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(c_double)]
    mylib.osvrGetAnalogState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = c_double()
    returnvalue = mylib.osvrGetAnalogState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetAnalogState')
    return (state, timestamp)

def osvrGetLocation2DState(iface):
    mylib.osvrGetLocation2DState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(OSVR_Vec2)]
    mylib.osvrGetLocation2DState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = OSVR_Vec2()
    returnvalue = mylib.osvrGetLocation2DState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetLocation2DState')
    return (state, timestamp)

def osvrGetDirectionState(iface):
    mylib.osvrGetDirectionState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(OSVR_Vec3)]
    mylib.osvrGetDirectionState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state =OSVR_Vec3()
    returnvalue = mylib.osvrGetDirectionState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetDirectionState')
    return (state, timestamp)

def osvrGetEyeTracker2DState(iface):
    mylib.osvrGetEyeTracker2DState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(OSVR_Vec2)]
    mylib.osvrGetEyeTracker2DState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = OSVR_Vec2()
    returnvalue = mylib.osvrGetEyeTracker2DState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetEyeTracker2DState')
    return (state, timestamp)

def osvrGetEyeTracker3DState(iface):
    mylib.osvrGetEyeTracker3DState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(OSVR_EyeTracker3DState)]
    mylib.osvrGetEyeTracker3DState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = OSVR_EyeTracker3DState()
    returnvalue = mylib.osvrGetEyeTracker3DState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetEyeTracker3DState')
    return (state, timestamp)

def osvrGetEyeTrackerBlinkState(iface):
    mylib.osvrGetEyeTrackerBlinkState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(c_uint8)]
    mylib.osvrGetEyeTrackerBlinkState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = c_uint8()
    returnvalue = mylib.osvrGetEyeTrackerBlinkState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetEyeTrackerBlinkState')
    return (state, timestamp)

def osvrGetNaviVelocityState(iface):
    mylib.osvrGetNaviVelocityState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(OSVR_Vec2)]
    mylib.osvrGetNaviVelocityState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = OSVR_Vec2()
    returnvalue = mylib.osvrGetNaviVelocityState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetNaviVelocityState')
    return (state, timestamp)

def osvrGetNaviPositionState(iface):
    mylib.osvrGetNaviPositionState.argtypes = [OSVR_ClientInterface, POINTER(OSVR_TimeValue), POINTER(OSVR_Vec2)]
    mylib.osvrGetNaviPositionState.restype = c_int8
    timestamp = OSVR_TimeValue()
    state = OSVR_Vec2()
    returnvalue = mylib.osvrGetNaviPositionState(iface, pointer(timestamp), pointer(state))
    checkReturn(returnvalue, 'osvrGetNaviPositionState')
    return (state, timestamp)


# ParametersC.h functions

def osvrClientGetStringParameterLength(ctx, path):
    mylib.osvrClientGetStringParameterLength.argtypes = [OSVR_ClientContext, c_char_p, POINTER(c_size_t)]
    mylib.osvrClientGetStringParameterLength.restype = c_int8
    length = c_size_t()
    returnvalue = mylib.osvrClientGetStringParameterLength(ctx, c_char_p(path.encode("utf8")), pointer(length))
    checkReturn(returnvalue, 'osvrClientGetStringParameterLength')
    return length

def osvrClientGetStringParameter(ctx, path, len):
    mylib.osvrClientGetStringParameter.argtypes = [OSVR_ClientContext, POINTER(c_char), c_char_p, c_size_t]
    mylib.osvrClientGetStringParameter.restype = c_int8
    buf = create_string_buffer(len.value)
    returnvalue = mylib.osvrClientGetStringParameter(ctx, c_char_p(path.encode("utf8")), buf, c_size_t(len.value))
    checkReturn(returnvalue, 'osvrClientGetStringParameter')
    return buf.value.decode("utf8")
