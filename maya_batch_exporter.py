from os.path import join
from maya.standalone import initialize
import maya.cmds as cmds
import maya.mel as mel
import glob
import sys


export_path = sys.argv[1]
source_path = sys.argv[2]


print 'initialize maya standalone engine'
initialize()
print 'loadPlugin fbxmaya'
cmds.loadPlugin("fbxmaya")
print 'initialize done.'



for f in glob.iglob(source_path + "/*.mb"):
    cmds.file (f, force=True, open=True)


    split_group = f.split("/")
    if len(split_group) == 1:
        split_group = f.split("\\")

    fileName = split_group[-1]

    name , postfix = fileName.split('.')
    fileName =  name + '.fbx'
    print fileName
    
    newPath = join(export_path,fileName).replace('\\', '/')

    print 'export fbx :' + newPath

    cmds.FBXExport('-file', newPath, '-a')

    print 'export fbx done!'






