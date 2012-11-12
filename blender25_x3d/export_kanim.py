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

# This script exports to KAnim format,
# which stands for Castle Game Engine's animations.
# The format specification is on
# http://castle-engine.sourceforge.net/kanim_format.php
# Each still frame is exported to a separate X3D file.
# We call actual Blender X3D exporter to do this.
#
# The latest version of this script can be found on
# http://castle-engine.sourceforge.net/blender.php
#
# Note: Eventually, we would like to implement exporting animations
# inside normal Blender X3D exporter. Our Castle Game Engine
# can already perfectly read and animate normal X3D models. When this
# happens, this script will stop being useful, as exporting whole animation
# to a single X3D file will be much better than using KAnim.

bl_info = {
    "name": "Export KAnim",
    "description": "Export animation to KAnim format (Castle Game Engine's animations).",
    "author": "Michalis Kamburelis",
    "version": (1, 0),
    "blender": (2, 64, 0),
    "location": "File > Export > Export KAnim (.kanim)",
    "warning": "", # used for warning icon and text in addons panel
    # Note: this should only lead to official Blender wiki.
    # But since this script (probably) will not be official part of Blender,
    # we can overuse it. Normal "link:" item is not visible in addons window.
    "wiki_url": "http://castle-engine.sourceforge.net/blender.php",
    "link": "http://castle-engine.sourceforge.net/blender.php",
    "category": "Import-Export"}

import bpy
import os
from bpy_extras.io_utils import path_reference_mode
from bpy.props import *

class ExportKAnim(bpy.types.Operator):
    """Export the animation to KAnim format (Castle Game Engine's animations)"""
    bl_idname = "export.kanim"
    bl_label = "Export KAnim (.kanim)"

    # properties for interaction with fileselect_add
    filepath = StringProperty(subtype="FILE_PATH")
    filter_glob = StringProperty(default="*.kanim", options={'HIDDEN'})

    # properties special for KAnim export
    frame_skip = IntProperty(name="Frames to skip",
        # As part of exporting to KAnim, we export each still frame to X3D. We iterate over all animation frames, from the start, exporting it and skipping this number of following frames. Smaller values mean less files (less disk usage, faster animation loading in game) but also worse quality (as KAnim loader in game only interpolates linearly between frames). Default is 4, which means every 5th frame is exported, which means 5 frames for each second (for default 25fps)
        description="How many frames to skip between exported frames. The game using KAnim format will reconstruct these frames using linear interpolation",
            default=4, min=0, max=50)

    # properies passed through to the X3D exporter,
    # definition copied from io_scene_x3d/__init__.py
    use_selection = BoolProperty(
            name="Selection Only",
            description="Export selected objects only",
            default=False,
            )
    use_apply_modifiers = BoolProperty(
            name="Apply Modifiers",
            description="Use transformed mesh data from each object",
            default=True,
            )
    use_triangulate = BoolProperty(
            name="Triangulate",
            description="Write quads into 'IndexedTriangleSet'",
            default=False,
            )
    use_normals = BoolProperty(
            name="Normals",
            description="Write normals with geometry",
            default=False,
            )
    use_hierarchy = BoolProperty(
            name="Hierarchy",
            description="Export parent child relationships",
            default=True,
            )
    name_decorations = BoolProperty(
            name="Name decorations",
            description=("Add prefixes to the names of exported nodes to "
                         "indicate their type"),
            default=True,
            )
    use_h3d = BoolProperty(
            name="H3D Extensions",
            description="Export shaders for H3D",
            default=False,
            )

    axis_forward = EnumProperty(
            name="Forward",
            items=(('X', "X Forward", ""),
                   ('Y', "Y Forward", ""),
                   ('Z', "Z Forward", ""),
                   ('-X', "-X Forward", ""),
                   ('-Y', "-Y Forward", ""),
                   ('-Z', "-Z Forward", ""),
               ),
        default='Z',
        )

    axis_up = EnumProperty(
            name="Up",
            items=(('X', "X Up", ""),
                   ('Y', "Y Up", ""),
                   ('Z', "Z Up", ""),
                   ('-X', "-X Up", ""),
                   ('-Y', "-Y Up", ""),
                   ('-Z', "-Z Up", ""),
                   ),
            default='Y',
            )

    path_mode = path_reference_mode

    def output_frame(self, context, kanim_file, frame, frame_start):
        """Output a given frame to a single X3D file, and add <frame...> line to
        kanim file.

        Arguments:
        kanim_file    -- the handle to write xxx.kanim file,
                         to add <frame...> line.
        frame         -- current frame number.
        frame_start   -- the start frame number, used to shift frame times
                         such that KAnim animation starts from time = 0.0.
        """

        # calculate filenames stuff
        (output_dir, output_basename) = os.path.split(self.filepath)
        output_basename = os.path.splitext(output_basename)[0] \
            + "_" + ("%04d" % frame) + '.x3d.gz'

        # write kanim line
        kanim_file.write('  <frame file_name="%s" time="%f" />\n' %
          (output_basename, (frame-frame_start) / 25.0))

        # write X3D with animation frame
        context.scene.frame_set(frame)
        bpy.ops.export_scene.x3d(filepath=os.path.join(output_dir, output_basename),
            check_existing = False,
            use_compress = True, # always compress, as we pass x3d.gz filename
            # pass through our properties to X3D exporter
            use_selection       = self.use_selection,
            use_apply_modifiers = self.use_apply_modifiers,
            use_triangulate     = self.use_triangulate,
            use_normals         = self.use_normals,
            use_hierarchy       = self.use_hierarchy,
            name_decorations    = self.name_decorations,
            use_h3d             = self.use_h3d,
            axis_forward        = self.axis_forward,
            axis_up             = self.axis_up,
            path_mode           = self.path_mode)

    def execute(self, context):
        kanim_file = open(self.filepath, 'w')
        kanim_file.write('<?xml version="1.0"?>\n')
        kanim_file.write('<animation>\n')

        frame = context.scene.frame_start
        while frame < context.scene.frame_end:
            self.output_frame(context, kanim_file, frame, context.scene.frame_start)
            frame += 1 + self.frame_skip
        # the last frame should be always output, regardless if we would "hit"
        # it with given frame_skip.
        self.output_frame(context, kanim_file, context.scene.frame_end, context.scene.frame_start)

        kanim_file.write('</animation>\n')
        kanim_file.close()

        return {'FINISHED'}

    def invoke(self, context, event):
        # set self.filepath (will be used by fileselect_add)
        # just like bpy_extras/io_utils.py
        if not self.filepath:
            blend_filepath = context.blend_data.filepath
            if not blend_filepath:
                blend_filepath = "untitled"
            else:
                blend_filepath = os.path.splitext(blend_filepath)[0]

            self.filepath = blend_filepath + ".kanim"

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ExportKAnim.bl_idname, text=ExportKAnim.bl_label)

def register():
    bpy.utils.register_class(ExportKAnim)
    bpy.types.INFO_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ExportKAnim)
    bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
    bpy.ops.export.kanim('INVOKE_DEFAULT')
