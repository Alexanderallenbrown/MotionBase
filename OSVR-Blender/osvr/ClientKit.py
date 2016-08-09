from osvr.ClientKitRaw import *
from osvr.Interface import *
from osvr.Display import *
class ClientContext:
    """ClientContext object
    """
    def __init__(self, applicationIdentifier): 
        """Initializes the library."""
        self.context = osvrClientInit(applicationIdentifier)
        self.objList = []
    def checkStatus(self):
        """Checks to see if the client context is fully started up and connected properly to a server."""
        return osvrClientCheckStatus(self.context)
    def update(self):
        """Updates the state of the context - call regularly in your main loop."""
        return osvrClientUpdate(self.context)
    def getInterface(self, path):
        """Get the interface associated with the given path."""
        iface = osvrClientGetInterface(self.context, path)
        ret = Interface(iface, self.context)
        self.objList.append(ret)
        return ret
    def getDisplayConfig(self): 
        """Allocates a display configuration object populated with data from the OSVR system.
        Before this call will succeed, your application will need to be correctly and fully 
        connected to an OSVR server. You may consider putting this call in a loop alternating 
        with osvrClientUpdate() until this call succeeds."""
        disp = osvrClientGetDisplay(self.context)
        ret = DisplayConfig(disp, self.context)
        self.objList.append(ret)
        return ret
    def getStringParameter(self, path):
        """Get a string parameter associated with the given path."""
        length = osvrClientGetStringParameterLength(self.context, path)
        return osvrClientGetStringParameter(self.context, path, length)
    def shutdown(self):
        """Shuts down the library, disposing of associated objects."""
        for object in self.objList:
            object.dispose()
            object.freed = True
        return osvrClientShutdown(self.context)
def PoseCallback(cb):
    """Creates a pose callback from a function pointer."""
    return OSVR_PoseCallback(cb) 
def PositionCallback(cb):
    """Creates a position callback from a function pointer."""
    return OSVR_PositionCallback(cb)
def OrientationCallback(cb):
    """Creates an orientation callback from a function pointer."""
    return OSVR_OrientationCallback(cb)
def ButtonCallback(cb):
    """Creates a button callback from a function pointer."""
    return OSVR_ButtonCallback(cb)
def AnalogCallback(cb):
    """Creates an analog callback from a function pointer."""
    return OSVR_AnalogCallback(cb)
def Location2DCallback(cb):
    """Creates a location callback from a function pointer."""
    return OSVR_Location2DCallback(cb)
def DirectionCallback(cb):
    """Creates a direction callback from a function pointer."""
    return OSVR_DirectionCallback(cb)
def EyeTracker2DCallback(cb):
    """Creates an eye tracker 2D callback from a function pointer."""
    return OSVR_EyeTracker2DCallback(cb)
def EyeTracker3DCallback(cb):
    """Creates an eye tracker 3D callback from a function pointer."""
    return OSVR_EyeTracker3DCallback(cb)
def EyeTrackerBlinkCallback(cb):
    """Creates an eye tracker blink callback from a function pointer."""
    return OSVR_EyeTrackerBlinkCallback(cb)
def NaviVelocityCallback(cb):
    """Creates a navi velocity callback from a function pointer."""
    return OSVR_NaviVelocityCallback(cb)
def NaviPositionCallback(cb):
    """Creates a navi position callback from a function pointer."""
    return OSVR_NaviPositionCallback(cb)

