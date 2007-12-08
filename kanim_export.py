#!BPY
""" Registration info for Blender menus:
Name: 'Kambi Animation (.kanim & .wrl)...'
Blender: 241
Group: 'Export'
Submenu: 'All Objects...' all
Submenu: 'All Objects compressed...' comp
Submenu: 'Selected Objects...' selected
Tooltip: 'Exports to Kambi Animation format'
"""

__author__ = ("Grzegorz Hermanowicz", "Michalis Kamburelis", "Parts based on vrml97_export.py")
__url__ = ["http://vrmlengine.sourceforge.net/kanim_format.php"]
__bpydoc__ = """\
This script exports to kanim format, which stands for
\"Kambi VRML game engine animations\".
[http://vrmlengine.sourceforge.net/kanim_format.php] explains all.

Usage:

Run this script from "File->Export" menu.  A pop-up will ask whether you
want to export only selected or all relevant objects.

Implementation details:

This script uses VRML 97 export class in file kambi_vrml97_export_base.py.
This way changes to kambi_vrml97_export_base.py are shared by this
script as well as by single-file exporter in kambi_vrml97_export.py script.
"""

# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****

####################################
# Library dependancies
####################################

import Blender
from Blender import Object, Mesh, Lamp, Draw, BGL, \
	 Image, Text, sys, Mathutils
from Blender.Scene import Render

import os.path

from kambi_vrml97_export_base import VRML2Export

##########################################################
# Global variables
##########################################################

ARG=''
extension=''
_safeOverwrite = True
animextension = '.kanim'

##########################################################
# Callbacks, needed before Main
##########################################################

def select_file(filename):
	if sys.exists(filename) and _safeOverwrite:
		result = \
			Draw.PupMenu("File Already Exists, Overwrite?%t|Yes%x1|No%x0")
		if(result != 1):
			return

	scn = Blender.Scene.GetCurrent()
	context = scn.getRenderingContext()
	sFrame = context.sFrame
	eFrame = context.eFrame
	oFrame = context.cFrame

	if filename.endswith(animextension):
		filename=filename.rsplit('.',1)[0]

	# Output kanim file
	animfile = open (filename + animextension,'w')
	print >> animfile, '<?xml version="1.0"?>'
	print >> animfile, '<animation scenes_per_time="' + str(context.framesPerSec())+'" optimization="separate-shape-states-no-transform" equality_epsilon="0.001" loop="false" backwards="false" >'

	for frame in range(sFrame, eFrame+1):
		print >> animfile, '<frame file_name="'+os.path.basename(filename)+str(frame)+extension+'" time="'+str(1.0/context.framesPerSec()*(frame-1))+'" />'

	print >> animfile, '</animation>'

	# Output VRML for each frame
	for frame in range(sFrame, eFrame+1):
		Blender.Set('curframe', frame)
		Blender.Redraw()

		ffilename = filename
		ffilename+=str(frame)
		ffilename+= extension

		wrlexport=VRML2Export(ffilename, ARG)
		wrlexport.export()

	# Back to frame where user was
	Blender.Set('curframe', oFrame)
	Blender.Redraw()

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
	else:
		extension=".wrl"
	Blender.Window.FileSelector(select_file, "Export Kambi VRML engine's animations", \
								sys.makename(ext=animextension))
