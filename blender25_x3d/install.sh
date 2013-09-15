#!/bin/bash
set -eu

# Just copy this script in place.
# Adjust path below to your blender installation.
# If you know how to make it generally usable, report
# (what is the generic dir name under $HOME, regardless of Blender version?).

BLENDER_VERSION='2.68'

cp -f export_x3d.py ~/installed/blender/"$BLENDER_VERSION"/scripts/addons/io_scene_x3d/export_x3d.py
cp -f export_kanim.py ~/installed/blender/"$BLENDER_VERSION"/scripts/addons/export_kanim.py
