# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Render the scene to a 6 textures.
# Camera position matters.
# Camera rotation is overridden by this script
# to capture all 6 sides of the world around.
#
# Outputs are named front/back/top/bottom/left/right.
# Suitable to create skyboxes or cubemap textures for games.
# The orientation and naming matches the X3D (Background node,
# ComposedCubeMapTexture node) and Castle Game Engine.
# (Assuming you use the standard exporter parameters that rotate
# Blender up (+Z) to X3D up (+Y).)
#
# To have sensible results, make sure that render resolution width
# is equal height, and that camera has field of view = 90 degrees.

bl_info = {
    "name": "Render Skybox",
    "description": "Render the scene to a 6 skybox textures.",
    "author": "Michalis Kamburelis",
    "version": (1, 0),
    "blender": (2, 78, 0),
#TODO:    "location": "File > Export > Castle Animation Frames (.castle-anim-frames)",
    "warning": "", # used for warning icon and text in addons panel
    # Note: this should only lead to official Blender wiki.
    # But since this script (probably) will not be official part of Blender,
    # we can overuse it. Normal "link:" item is not visible in addons window.
    "wiki_url": "http://castle-engine.sourceforge.net/blender.php",
    "link": "http://castle-engine.sourceforge.net/blender.php",
    "category": "Render"}

import bpy
import os
import mathutils
import math

# See
# https://www.blender.org/api/blender_python_api_current/
# http://blender.stackexchange.com/questions/31702/how-to-set-objects-rotation-from-python
# http://blender.stackexchange.com/questions/8850/how-to-take-images-with-multiple-cameras-with-script

# TODO:
# - modifies and doesn't restore camera rotation
# - doesn't check (or create new camera) that camera has field of view = 90 deg
# - doesn't check that resolution width == height

class RenderSkybox(bpy.types.Operator):
    """Render the scene 6 times, to outputs named front/back/top/bottom/left/right. Suitable to create skyboxes or cubemap textures for games. The orientation and naming matches X3D and Castle Game Engine."""
    bl_idname = "render.skybox"
    bl_label = "Render Skybox"

    def one_render(self, context, output_path, rotation, name):
        # set camera
        cam = context.scene.camera
        cam.rotation_euler = rotation

        # render
        context.scene.render.filepath = output_path + "/" + name + ".png"
        bpy.ops.render.render(write_still=True)

        # increase progress
        self.current_progress = self.current_progress + 1
        wm = context.window_manager
        wm.progress_update(self.current_progress)

    def execute(self, context):
        old_filepath = context.scene.render.filepath
        try:
            wm = context.window_manager

            (output_path, output_basename_ignored) = \
                os.path.split(context.scene.render.filepath)

            self.current_progress = 0
            wm.progress_begin(self.current_progress, 6)

            self.one_render(context, output_path, mathutils.Euler((               0.0 , 0.0, math.radians(-180.0))), "bottom")
            self.one_render(context, output_path, mathutils.Euler((math.radians(180.0), 0.0, math.radians(-180.0))), "top")

            self.one_render(context, output_path, mathutils.Euler((math.radians(90.0), 0.0,                 0.0 )), "back")
            self.one_render(context, output_path, mathutils.Euler((math.radians(90.0), 0.0,  math.radians(180.0))), "front")
            self.one_render(context, output_path, mathutils.Euler((math.radians(90.0), 0.0,  math.radians(-90.0))), "left")
            self.one_render(context, output_path, mathutils.Euler((math.radians(90.0), 0.0,  math.radians( 90.0))), "right")

            wm.progress_end()
        finally:
            context.scene.render.filepath = old_filepath

        return {'FINISHED'}

def register():
    bpy.utils.register_class(RenderSkybox)

def unregister():
    bpy.utils.unregister_class(RenderSkybox)

if __name__ == "__main__":
    register()
    bpy.ops.render.skybox()
