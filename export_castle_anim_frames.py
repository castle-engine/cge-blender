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

# This script exports from Blender to castle-anim-frames format,
# which stands for "Castle Game Engine's Animation Frames".
# The format specification is on
# http://castle-engine.sourceforge.net/castle_animation_frames.php
# Each still frame is exported to a separate X3D graph.
# We call actual Blender X3D exporter to do this.
#
# The latest version of this script can be found on
# http://castle-engine.sourceforge.net/creating_data_blender.php

bl_info = {
    "name": "Export Castle Animation Frames",
    "description": "Export animation to Castle Game Engine's Animation Frames format.",
    "author": "Michalis Kamburelis",
    "version": (1, 0),
    "blender": (2, 64, 0),
    "location": "File > Export > Castle Animation Frames (.castle-anim-frames)",
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

class ExportCastleAnimFrames(bpy.types.Operator):
    """Export the animation to Castle Animation Frames (castle-anim-frames) format"""
    bl_idname = "export.castle_anim_frames"
    bl_label = "Castle Animation Frames (.castle-anim-frames)"

    # properties for interaction with fileselect_add
    filepath = StringProperty(subtype="FILE_PATH")
    filter_glob = StringProperty(default="*.castle-anim-frames", options={'HIDDEN'})

    # properties special for castle-anim-frames export
    frame_skip = IntProperty(name="Frames to skip",
        # As part of exporting to castle-anim-frames, we export each still
        # frame to X3D. We iterate over all animation frames, from the start,
        # exporting it and skipping this number of following frames.
        # Smaller values mean less files (less disk usage, faster animation
        # loading in game) but also worse quality (as castle-anim-frames loader in game
        # only interpolates linearly between frames). Default is 4, which
        # means every 5th frame is exported, which means 5 frames for each
        # second (for default 25fps)
        description="How many frames to skip between exported frames. The game using castle-anim-frames format will reconstruct these frames using linear interpolation",
            default=4, min=0, max=50)

    # properies passed through to the X3D exporter,
    # definition copied from io_scene_x3d/__init__.py
    use_selection = BoolProperty(
            name="Selection Only",
            description="Export selected objects only",
            default=False,
            )
    use_mesh_modifiers = BoolProperty(
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

    def output_frame(self, context, output_file, frame, frame_start):
        """Output a given frame to a single X3D file, and add <frame...> line to
        castle-anim-frames file.

        Arguments:
        output_file   -- the handle to write xxx.castle-anim-frames file,
                         to add <frame...> line.
        frame         -- current frame number.
        frame_start   -- the start frame number, used to shift frame times
                         such that castle-anim-frames animation starts from time = 0.0.
        """

        # calculate filenames stuff
        (output_dir, output_basename) = os.path.split(self.filepath)
        x3d_file_name = os.path.join(output_dir, os.path.splitext(output_basename)[0] + "_tmp.x3d")

        # write castle-anim-frames line
        output_file.write('  <frame time="%f">\n' %
          ((frame-frame_start) / 25.0))

        # write X3D with animation frame
        context.scene.frame_set(frame)
        bpy.ops.export_scene.x3d(filepath=x3d_file_name,
            check_existing = False,
            use_compress = False, # never compress
            # pass through our properties to X3D exporter
            use_selection       = self.use_selection,
            use_mesh_modifiers  = self.use_mesh_modifiers,
            use_triangulate     = self.use_triangulate,
            use_normals         = self.use_normals,
            use_hierarchy       = self.use_hierarchy,
            name_decorations    = self.name_decorations,
            use_h3d             = self.use_h3d,
            axis_forward        = self.axis_forward,
            axis_up             = self.axis_up,
            path_mode           = self.path_mode)

        # read from temporary X3D file, and remove it
        with open(x3d_file_name, 'r') as x3d_contents_file:
            x3d_contents = x3d_contents_file.read()
        os.remove(x3d_file_name)

        # add X3D content
        x3d_contents = x3d_contents.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        x3d_contents = x3d_contents.replace('<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.0//EN" "http://www.web3d.org/specifications/x3d-3.0.dtd">', '')
        output_file.write(x3d_contents)
        output_file.write('  </frame>\n')

    def execute(self, context):
        output_file = open(self.filepath, 'w')
        output_file.write('<?xml version="1.0"?>\n')
        output_file.write('<animation>\n')

        frame = context.scene.frame_start
        while frame < context.scene.frame_end:
            self.output_frame(context, output_file, frame, context.scene.frame_start)
            frame += 1 + self.frame_skip
        # the last frame should be always output, regardless if we would "hit"
        # it with given frame_skip.
        self.output_frame(context, output_file, context.scene.frame_end, context.scene.frame_start)

        output_file.write('</animation>\n')
        output_file.close()

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

            self.filepath = blend_filepath + ".castle-anim-frames"

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ExportCastleAnimFrames.bl_idname, text=ExportCastleAnimFrames.bl_label)

def register():
    bpy.utils.register_class(ExportCastleAnimFrames)
    bpy.types.INFO_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ExportCastleAnimFrames)
    bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
    bpy.ops.export.castle_anim_frames('INVOKE_DEFAULT')
