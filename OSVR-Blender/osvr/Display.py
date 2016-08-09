from osvr.ClientKitRaw import *

class DisplayConfig:
    """Display Config object"""
    def __init__(self, display, ctx):
        """Initialize display config object"""
        self.disp = display
        self.context = ctx
        self.freed = False
    def checkDisplayStartup():
        """Checks to see if the display is fully configured and ready, having received its 
        first pose update."""
        return osvrCheckDisplayStartup(self.disp)
    def getNumDisplayInputs(self):
        """Display config can have one or more display inputs to pass pixels over:retrieve 
        the number of display inputs in the current configuration."""
        return osvrGetNumDisplayInputs(self.disp)
    def getDisplayDimensions(self, displayInputIndex):
        """Retrieve the pixel dimensions of a given display input."""
        return osvrClientGetDisplayDimensions(self.disp, displayInputIndex)
    def getNumViewers(self):
        """Retrieve the viewer count."""
        return osvrClientGetNumViewers(self.disp)
    def getViewerPose(self, viewer):
        """Get the pose of a viewer."""
        return osvrClientGetViewerPose(self.disp, viewer)
    def getNumEyesForViewer(self, viewer):
        """Each viewer can have one or more "eyes" which have substantially similar pose.
        Get the eye count."""
        return osvrClientGetNumEyesForViewer(self.disp, viewer)
    def getViewerEyePose(self, viewer, eye):
        """Get the "viewpoint" for the given eye of a viewer."""
        return osvrClientGetViewerEyePose(self.disp, viewer, eye)
    def getViewerEyeViewMatrixd(self, viewer, eye, flags):
        """Get the view matrix (inverse of pose) for the given eye of a viewer."""
        return osvrGetViewerEyeViewMatrixd(self.disp, viewer, eye, flags)
    def getViewerEyeViewMatrixf(self, viewer, eye, flags):
        """Get the view matrix in floats."""
        return osvrGetViewerEyeViewMatrixf(self.disp, viewer, eye, flags)
    def getNumSurfacesForViewerEye(self, viewer, eye):
        """Each eye of each viewer has one or more surfaces (aka "screens") on which content
        should be rendered."""
        return osvrClientGetNumSurfacesForViewerEye(self.disp, viewer, eye)
    def getRelativeViewportForViewerEyeSurface(self, viewer, eye, surface):
        """Get the dimensions/location of the viewport within the display input for a surface
        seen by an eye of a viewer."""
        return osvrGetRelativeViewportForViewerEyeSurface(self.disp, viewer, eye, surface)
    def getViewerEyeSurfaceDisplayInputIndex(self, viewer, eye, surface):
        """Get the index of the display input for a surface seen by an eye of a viewer."""
        return osvrGetViewerEyeSurfaceDisplayInputIndex(self.disp, viewer, eye, surface)
    def getProjectionMatrixForViewerEyeSurfaced(self, viewer, eye, surface, near, far, flags):
        """Get the projection matrix for a surface seen by an eye of a viewer."""
        return osvrGetViewerEyeSurfaceProjectionMatrixd(self.disp, viewer, eye, surface, near, far, flags)
    def getProjectionMatrixForViewerEyeSurfacef(self, viewer, eye, surface, near, far, flags):
        """Get the projection matrix in floats."""
        return osvrGetViewerEyeSurfaceProjectionMatrixf(self.disp, viewer, eye, surface, near, far, flags)
    def getViewerEyeSurfaceProjectionClippingPlanes(self, viewer, eye, surface):
        """Get the clipping planes (positions at unit distance) for a surface seen by an eye
        of a viewer."""
        return osvrGetViewerEyeSurfaceProjectionClippingPlanes(self.disp, viewer, eye, surface)
    def doesViewerEyeSurfaceWantDistortion(self, viewer, eye, surface):
        """Returns the priority of radial distortion parameters for a surfaces seen by an eye 
        of a viewer."""
        return osvrDoesViewerEyeSurfaceWantDistortion(self.disp, viewer, eye, surface)
    def dispose(self):
        """Frees the display object."""
        if self.freed == False:
            self.freed = True
            return osvrClientFreeDisplay(self.disp)
    def __del__(self):
        self.dispose()