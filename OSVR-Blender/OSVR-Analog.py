bl_info = {
    "name": "OSVR_Analog",
    "category": "Object",
}

import bpy
from bpy.types import Operator
# from ClientKit import ClientKit

class OSVR_Analog(Operator):
    """OSVR_Analog"""                          # blender tooltip for menu items and buttons
    bl_idname = "object.osvr_analog"           # unique identifier for buttons and menu items to reference
    bl_label = "OSVR_Analog"                   # displays name in the interface
    bl_options = {'REGISTER', 'UNDO'}    # enable undo for the operator

    def execute(self, context):                  # execute() is called by blender when running the operator
        obj = context.scene.objects.active
        bpy.ops.object.game_property_new(type="FLOAT",name="analog")
        prop = obj.game.properties["analog"];
        prop.value = 0
        bpy.ops.logic.sensor_add("ALWAYS", "OSVR-Analog-Sensor")
        bpy.ops.logic.controller_add(type="PYTHON", name="OSVR-Analog-Controller")

        return {'FINISHED'}             # lets blender know the operator finished successfully

def register():
    bpy.utils.register_class(OSVR_Analog)

def unregister():
    bpy.utils.unregister_class(OSVR_Analog)

# allows the script to be run directly from blender's text editor
# without having to install the addon
if __name__ == "__main__":
    register()
