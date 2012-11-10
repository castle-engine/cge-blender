#!/bin/bash
set -eu

# Just copy this script in place.
# Adjust path below to your blender installation.
# If you know how to make it generally usable, report
# (what is the generic dir name under $HOME, regardless of Blender version,
# that works with Blender 2.5x?)

cp -f export_x3d.py ~/installed/blender/2.64/scripts/addons/io_scene_x3d/export_x3d.py
