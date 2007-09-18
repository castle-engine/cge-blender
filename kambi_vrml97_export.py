#!BPY
""" Registration info for Blender menus:
Name: 'Kambi VRML97 (.wrl)...'
Blender: 241
Group: 'Export'
Submenu: 'All Objects...' all
Submenu: 'All Objects compressed...' comp
Submenu: 'Selected Objects...' selected
Tooltip: 'Export to VRML97 file (.wrl) (with some Kambi hacks)'
"""

__author__ = ("Rick Kimball", "Ken Miller", "Steve Matthews", "Bart", "Michalis Kamburelis")
__url__ = ["blender", "elysiun",
"Author's (Rick) homepage, http://kimballsoftware.com/blender",
"Author's (Bart) homepage, http://www.neeneenee.de/vrml",
"Author's (Michalis) project: http://vrmlengine.sourceforge.net/"]
__email__ = ["Bart, bart:neeneenee*de"]
__version__ = "2006/01/17-kambi2"
__bpydoc__ = """\
This script exports to VRML97 format.

Usage:

Run this script from "File->Export" menu.  A pop-up will ask whether you
want to export only selected or all relevant objects.
"""

####################################
# Library dependancies
####################################

import Blender
from Blender import Object, Mesh, Lamp, Draw, BGL, \
	 Image, Text, sys, Mathutils
from Blender.Scene import Render

import math

# Kambi+ for basename
import os

from kambi_vrml97_export_base import VRML2Export

##########################################################
# Global variables
##########################################################

ARG=''
extension=''
_safeOverwrite = True

##########################################################
# Callbacks, needed before Main
##########################################################

def select_file(filename):
	if sys.exists(filename) and _safeOverwrite:
		result = \
			Draw.PupMenu("File Already Exists, Overwrite?%t|Yes%x1|No%x0")
		if(result != 1):
			return

	if not filename.endswith(extension):
		filename += extension

	wrlexport=VRML2Export(filename)
	wrlexport.ARG=ARG
	wrlexport.export()


#########################################################
# main routine
#########################################################

try:
	ARG = __script__['arg'] # user selected argument
except:
	print "older version"

if Blender.Get('version') < 235:
	print "Warning: VRML97 export failed, wrong blender version!"
	print " You aren't running blender version 2.35 or greater"
	print " download a newer version from http://blender3d.org/"
else:
	if ARG == 'comp':
		extension=".wrz"
		from gzip import *
	else:
		extension=".wrl"
	Blender.Window.FileSelector(select_file, "Export VRML97", \
								sys.makename(ext=extension))

