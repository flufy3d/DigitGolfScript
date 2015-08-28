import sys
import os

export_path = sys.argv[1]
source_path = sys.argv[2]
texture_path1 = sys.argv[3]
texture_path2 = sys.argv[4]
extension = sys.argv[5]

texture_group1 = []
texture_group2 = []

from os.path import join
from maya.standalone import initialize
import maya.cmds as cmds
import maya.mel as mel
import glob



print 'initialize maya standalone engine'
initialize()
print 'initialize done.'


print 'init texture group info'
for f in glob.iglob(texture_path1 + "/*."+extension):
    split_group = f.split("/")
    if len(split_group) == 1:
        split_group = f.split("\\")

    fileName = split_group[-1]

    name , postfix = fileName.split('.')
    fileName =  name + '.' + extension
    texture_group1.append(fileName)

for f in glob.iglob(texture_path2 + "/*."+extension):
    split_group = f.split("/")
    if len(split_group) == 1:
        split_group = f.split("\\")

    fileName = split_group[-1]

    name , postfix = fileName.split('.')
    fileName =  name + '.' + extension
    texture_group2.append(fileName)


mat_array = cmds.ls( materials=True )


for f in glob.iglob(source_path + "/*.mb"):
    cmds.file (f, force=True, open=True)


    array = cmds.ls( textures=True )
    for fileNode in array:

        try:

            fullpath = cmds.getAttr("%s.fileTextureName" %fileNode)
            fileName = fullpath.split("/")[-1]
            name , postfix = fileName.split('.')

            #print  name , postfix 
            fileName =  name + '.' + extension

            if fileName in texture_group1:
                newPath = join(texture_path1,fileName).replace('\\', '/')
            elif fileName in texture_group2:
                newPath = join(texture_path2,fileName).replace('\\', '/')
            else:
                print 'can not find texture!!!!!!!!!!!!!!'
                newPath = join(texture_path1,fileName).replace('\\', '/')

            #print newPath
            cmds.setAttr("%s.fileTextureName" %fileNode, newPath,type="string")

            #if the texture and material name are the same ,ue4 will fail to import texture
            b_same_name = name in mat_array

            if b_same_name:
                cmds.rename(name,name+'_mat')  


        except ValueError, e:
            print 'can not get :' + ("%s.fileTextureName" %fileNode)



    split_group = f.split("/")
    if len(split_group) == 1:
        split_group = f.split("\\")

    fileName = split_group[-1]

    name , postfix = fileName.split('.')
    fileName =  name + '.mb'
    print fileName

    if not os.path.exists(export_path):
        os.makedirs(export_path)
    
    newPath = join(export_path,fileName).replace('\\', '/')
    cmds.file( rename= newPath  )
    cmds.file( save=True )

