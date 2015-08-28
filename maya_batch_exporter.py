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




for f in glob.iglob(source_path + "/*.mb"):
    cmds.file (f, force=True, open=True)


    mat_array = cmds.ls( materials=True )
    tex_array = cmds.ls( textures=True )
    for fileNode in tex_array:
        try:
            fullpath = cmds.getAttr("%s.fileTextureName" %fileNode)
            fileName = fullpath.split("/")[-1]
            name , postfix = fileName.split('.')

            #if the texture and material name are the same ,ue4 will fail to import texture
            b_same_name = name in mat_array

            if b_same_name:
                print 'tex mat is same name ,so change the name of material: %s to _mat' % name
                cmds.rename(name,name+'_mat')  
                mat_array.remove(name)
                

        except ValueError, e:

            print 'can not get :' + ("%s.fileTextureName" %fileNode)


    split_group = f.split("/")
    if len(split_group) == 1:
        split_group = f.split("\\")

    fileName = split_group[-1]

    name , postfix = fileName.split('.')
    fileName =  name + '.fbx'
    print fileName
    
    if not os.path.exists(export_path):
        os.makedirs(export_path)
    newPath = join(export_path,fileName).replace('\\', '/')

    print 'export fbx :' + newPath

    cmds.FBXExport('-file', newPath, '-a')

    print 'export fbx done!'






