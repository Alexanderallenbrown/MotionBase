from osvr.ClientKitRaw import *
class Interface:
    """Interface object"""
    def __init__(self, iface, ctx):
        """Initializes an interface object."""
        self.interface = iface
        self.context = ctx
        self.freed = False
    def registerCallback(self, cb, userdata):
        """Registers a callback to the interface."""
        if isinstance(cb, OSVR_PoseCallback):
            osvrRegisterPoseCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_PositionCallback):
            osvrRegisterPositionCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_ButtonCallback):
            osvrRegisterButtonCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_AnalogCallback):
            osvrRegisterAnalogCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_Location2DCallback):
            osvrRegisterLocation2DCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_DirectionCallback):
            osvrRegisterDirectionCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_EyeTracker2DCallback):
            osvrRegisterEyetracker2DCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_EyeTracker3DCallback):
            osvrRegisterEyeTracker3DCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_EyeTrackerBlinkCallback):
            osvrRegisterEyeTrackerBlinkCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_NaviVelocityCallback):
            osvrRegisterNaviVelocityCallback(self.interface, cb, userdata)
        if isinstance(cb, OSVR_NaviPositionCallback):
            osvrRegisterNaviPositionCallback(self.interface, cb, userdata)
    def getPoseState(self):
        """Returns the pose state of the interface."""
        return osvrGetPoseState(self.interface)
    def getPositionState(self):
        """Returns the position state of the interface."""
        return osvrGetPositionState(self.interface)
    def getOrientationState(self):
        """Returns the orientation state of the interface."""
        return osvrGetOrientationState(self.interface)
    def getButtonState(self):
        """Returns the button state of the interface."""
        return osvrGetButtonState(self.interface)
    def getAnalogState(self):
        """Returns the analog state of the interface."""
        return osvrGetAnalogState(self.interface)
    def getLocation2DState(self):
        """Returns the location 2D state of the interface."""  
        return osvrGetLocation2DState(self.interface)
    def getDirectionState(self):
        """Returns the direction state of the interface."""
        return osvrGetDirectionState(self.interface)
    def getEyeTracker2DState(self):
        """Returns the eye tracker 2D state of the interface."""
        return osvrGetEyeTracker2DState(self.interface)
    def getEyeTracker3DState(self):
        """Returns the eye tracker 3D state of the interface."""
        return osvrGetEyeTracker3DState(self.interface)
    def getEyeTrackerBlinkState(self):
        """Returns the eye tracker blink state of the interface."""
        return osvrGetEyeTrackerBlinkState(self.interface)
    def getNaviVelocityState(self):
        """Returns the navi velocity state of the interface."""
        return osvrGetNaviVelocityState(self.interface)
    def getNaviPositionState(self):
        """Returns the navi position state of the interface."""
        return osvrGetNaviPositionState(self.interface)
    def dispose(self):
        """Frees the interface object."""
        if self.freed == False:
            self.freed = True
            return osvrClientFreeInterface(self.context, self.interface)
    def __del__(self):
        self.dispose()