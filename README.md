# Deprecated

This repository is deprecated, these scripts were maintained only for old Blender versions (<= 2.8). They will _not work with the latest Blender_.

**Instead of this**: We recommend to use glTF format to create 3D (and 2D too) models in _Blender_ and export them into _Castle Game Engine_. Latest Blender allows to export to glTF perfectly, out-of-the-box. You don't need any scripts from this repo. See our [Blender](https://castle-engine.io/blender) documentation and [glTF documentation](https://castle-engine.io/gltf).

# Blender + Castle Game Engine and X3D scripts

Blender scripts to:

* Export to X3D (improved version of the Blender standard X3D exporter).

* Export to castle-anim-frames ("Castle Game Engine Animation Frames",
  a simple format capable of transferring *any* animation designed in Blender,
  whether it's armature, transformation, color animation, mesh deformation
  by shape keys or hooks, physics...
  Underneath, it uses X3D for static scene snapshots.)

* Render a skybox (or a cube map texture) following the X3D naming conventions.

See http://castle-engine.sourceforge.net/blender.php for the documentation.
