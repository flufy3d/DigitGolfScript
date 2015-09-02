from os.path import join
from maya.standalone import initialize
import maya.cmds as cmds
import maya.mel as mel
import glob
import sys
import os

export_path = sys.argv[1]
source_path = sys.argv[2]


print 'initialize maya standalone engine'
initialize()
print 'loadPlugin fbxmaya'
cmds.loadPlugin("fbxmaya")
print 'initialize done.'

output = ''


for f in glob.iglob(source_path + "/*.mb"):
    cmds.file (f, force=True, open=True)

    found = False

    tex_array = cmds.ls( textures=True )
    for fileNode in tex_array:

        if 'layeredTexture' in fileNode:

            print fileNode
            found = True

    if found:
        output += f + '\r\n'



if not os.path.exists(export_path):
    os.makedirs(export_path)

file_object = open(export_path + '/multi_txt_files.txt', 'w')
file_object.write(output)
file_object.close( )
 







