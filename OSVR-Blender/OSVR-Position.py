bl_info = {
    "name": "OSVR_Position",
    "category": "Object",
}

import bpy
from bpy.types import Operator
# from ClientKit import ClientKit

class OSVR_Position(Operator):
    """OSVR_Position"""                         # blender tooltip for menu items and buttons
    bl_idname = "object.osvr_position"          # unique identifier for buttons and menu items to reference
    bl_label = "OSVR_Position"                  # displays name in the interface
    bl_options = {'REGISTER', 'UNDO'}           # enable undo for the operator

    def execute(self, context):                 # execute() is called by blender when running the operator
        bpy.ops.logic.sensor_add(type="ALWAYS", name="OSVR-Position-Sensor")
        bpy.ops.logic.controller_add(type="PYTHON", name="OSVR-Position-Controller")

        return {'FINISHED'}                     # lets blender know the operator finished successfully

def register():
    bpy.utils.register_class(OSVR_Position)

def unregister():
    bpy.utils.unregister_class(OSVR_Position)

# allows the script to be run directly from blender's text editor
# without having to install the addon
if __name__ == "__main__":
    register()
