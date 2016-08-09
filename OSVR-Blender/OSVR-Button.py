bl_info = {
    "name": "OSVR_Button",
    "category": "Object",
}

import bpy
from bpy.types import Operator
# from ClientKit import ClientKit

class OSVR_Button(Operator):
    """OSVR_Button"""                          # blender tooltip for menu items and buttons
    bl_idname = "object.osvr_button"           # unique identifier for buttons and menu items to reference
    bl_label = "OSVR_Button"                   # displays name in the interface
    bl_options = {'REGISTER', 'UNDO'}    # enable undo for the operator

    def execute(self, context):                  # execute() is called by blender when running the operator
        obj = context.scene.objects.active
        bpy.ops.object.game_property_new(type="BOOL",name="button")
        prop = obj.game.properties["button"];
        prop.value = False
        bpy.ops.logic.sensor_add(type="ALWAYS", name="OSVR-Button-Sensor")
        bpy.ops.logic.controller_add(type="PYTHON", name="OSVR-Button-Controller")
        # sensor = cont.sensors[-1]
        # controller = cont.controllers[-1]
        # sensor.link(controller)

        return {'FINISHED'}             # lets blender know the operator finished successfully

def register():
    bpy.utils.register_class(OSVR_Button)


def unregister():
    bpy.utils.unregister_class(OSVR_Button)

# allows the script to be run directly from blender's text editor
# without having to install the addon

if __name__ == "__main__":
    register()
