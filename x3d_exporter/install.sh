#!/bin/bash
set -eu

# Easy installation, for devs.
# Just copy this script in place.
# Adjust path below to your blender installation.

BLENDER_VERSION='2.78'

cp -f export_x3d.py __init__.py \
  ~/installed/blender/"$BLENDER_VERSION"/scripts/addons/io_scene_x3d/
