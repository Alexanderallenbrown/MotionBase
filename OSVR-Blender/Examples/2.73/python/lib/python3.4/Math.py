import mathutils
import math
import osvr.ClientKit

class Math:
    def ConvertPosition(vec):
        #Blender uses a right handed coordinate system. But y and z are swapped
        temp_vec = mathutils.Vector(float(vec.data[0]), float(vec.data[1]), float(vec.data[2]))
        #may need to be -90 degrees
        rot_mat = mathutils.Matrix.Rotation(math.degrees(90), 4, 'X')
        return rot_mat * temp_vec

    def ConvertPosition(vec):
        return mathutils.Vector(float(vec.data[0]), float(vec.data[1]))

    def ConvertOrientation(quat):
        # Wikipedia may say quaternions are not handed, but these needed modification in Unity. Check if Blender is same
        return mathutils.Quaternion(float(quat.data[0]), float(quat.data[1]), float(quat.data[2]), float(quat.data[3]))

    def ConvertPose(pose):
        matrix_location = mathutils.Matrix.Translation(ConvertPosition(pose.translation)).to_4x4()
        #rotation parameters are angle (float), size (int), axis (string or vector)
        axis, angle = ConvertOrientation(pose.rotation).to_axis_angle()
        matrix_rotation = mathutils.Matrix.Rotation(angle, 4, axis).to_4x4()
        #scale parameters are factor (float), size (int), axis (string or vector)
        matrix_scale = mathutils.Matrix.Scale(ConvertPosition(mathutils.Vector(1,1,1))).to_4x4()
        matrix4x4 = matrix_location * matrix_rotation * matrix_scale
        return matrix4x4

    #Convert OSVR.ClientKit.Viewport to Rect. Blender equivalent?
    # Did some searching, didn't find anything about needing to normalize viewport.
    #Rect ConvertViewport(OSVR.ClientKit.Viewport viewport)
        #Unity expects normalized coordinates, not pixel coordinates. What about Blender?
        #@todo below assumes left and right eyes split the screen in half horizontally
        #return Rect(viewport.Left / (2f*viewport.Width), viewport.Bottom / viewport.Height, viewport.Width/(viewport.Width*2f), 1);

    #Convert OSVR.ClientKit.Matrix44f to Matrix4x4
    def ConvertMatrix(matrix):
        matrix4x4 = mathutils.Matrix()
        matrix4x4[0][0] = matrix.M0
        matrix4x4[1][0] = matrix.M1
        matrix4x4[2][0] = matrix.M2
        matrix4x4[3][0] = matrix.M3
        matrix4x4[0][1] = matrix.M4
        matrix4x4[1][1] = matrix.M5
        matrix4x4[2][1] = matrix.M6
        matrix4x4[3][1] = matrix.M7
        matrix4x4[0][2] = matrix.M8
        matrix4x4[1][2] = matrix.M9
        matrix4x4[2][2] = matrix.M10
        matrix4x4[3][2] = matrix.M11
        matrix4x4[0][3] = matrix.M12
        matrix4x4[1][3] = matrix.M13
        matrix4x4[2][3] = matrix.M14
        matrix4x4[3][3] = matrix.M15
        return matrix4x4
