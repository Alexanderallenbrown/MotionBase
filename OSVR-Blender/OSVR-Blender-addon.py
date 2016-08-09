bl_info = {
    "name": "OSVR",
    "category": "Object",
}

import bpy
from bpy.types import Operator
from ClientKit import ClientKit

clientKit = ClientKit()
context = clientKit.instance.context
running = False

class OSVR(Operator):
    """OSVR"""                          # blender tooltip for menu items and buttons
    bl_idname = "object.osvr"           # unique identifier for buttons and menu items to reference
    bl_label = "OSVR"                   # displays name in the interface
    bl_options = {'REGISTER', 'UNDO'}    # enable undo for the operator

    def execute(self, context):                  # execute() is called by blender when running the operator
        game_settings = bpy.data.scenes["Scene"].game_settings
        game_settings.stereo = 'STEREO'          # change camera to stereo
        game_settings.stereo_mode = 'SIDEBYSIDE' # change stereo settings to side by side views

        return {'FINISHED'}             # lets blender know the operator finished successfully

def register():
    bpy.utils.register_class(OSVR)


def unregister():
    bpy.utils.unregister_class(OSVR)

# allows the script to be run directly from blender's text editor
# without having to install the addon
if __name__ == "__main__":
    register()

def updateButton():
    from bge.logic import getCurrentController

    controller = getCurrentController()       #gets Python Controller associated with this script
    obj = bpy.data.objects[controller.owner.name]
    bpy.context.scene.objects.active = obj
    obj.game.properties["button"].value = not obj.game.properties["button"].value

def contextUpdate():
    if running:
        global context
        context.update()
    else:
        print("Object is null")

def updatePosition():
    from bge.logic import getCurrentController
    import Math

    head = clientKit.instance.context.getInterface("/me/head")

    timestamp, pose = head.getPoseState()

    blendvec = Math.convertPosition(pose.translation)

    controller = getCurrentController()
    obj = bpy.data.objects[controller.owner.name]
    bpy.context.scene.objects.active = obj
    obj.location.x = blendvec.x
    obj.location.y = blendvec.y
    obj.location.z = blendvec.z

def updateOrientation(rotation):
    from bge.logic import getCurrentController
    import mathutils
    import Math
    
    blendrot = Math.convertOrientation(rotation)

    controller = getCurrentController()
    obj = controller.owner
    obj.orientation = blendrot

def startOSVR():
    if not running:
        from osvr.ClientKit import OrientationCallback

        iface = clientKit.instance.context.getInterface("/me/head")

        def testCallback(userdata, timestamp, report):
            print("Doing Callback")
            print("Got ORIENTATION report: Orientation = (%f, %f, %f, %f)" % (report.contents.rotation.data[0], report.contents.rotation.data[1], report.contents.rotation.data[2], report.contents.rotation.data[3]))

        OSVRCallback = OrientationCallback(testCallback)

        iface.registerCallback(OSVRCallback, None)
        global running
        running = True
        print("Starting OSVR...")

def shutdownOSVR():
    if running:
        from bge.logic import endGame

        clientKit.instance.context.shutdown()
        global running
        running = False
        print("OSVR shutting down, exiting.")

        endGame()