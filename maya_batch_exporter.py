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
    print 'open :' + f

    del_list = []
    mat_array = cmds.ls( materials=True )
    tex_array = cmds.ls( textures=True )
    for fileNode in tex_array:
        tex_type  = cmds.nodeType( fileNode )
        if tex_type == 'file':
            fullpath = cmds.getAttr("%s.fileTextureName" %fileNode)
            fileName = fullpath.split("/")[-1]
            name , postfix = fileName.split('.')

            #if the texture and material name are the same ,ue4 will fail to import texture
            b_same_name = name in mat_array

            if b_same_name:
                print 'tex mat is same name ,so change the name of material: %s to _mat' % name
                cmds.rename(name,name+'_mat')  
                mat_array.remove(name)

        elif tex_type == 'layeredTexture':
            out_mat = cmds.listConnections(fileNode,d=True, s=False ,t='lambert')

            color_map_tex = None
            content_tex = None

            in_tex_array = cmds.listConnections(fileNode,d=False, s=True )
            for in_tex in in_tex_array:
                in_items = cmds.listConnections(in_tex,d=False, s=True )
                if in_items != None:
                    in_type = cmds.nodeType( in_items[0] )
                    if in_type[:2] == 'uv':
                        color_map_tex = in_tex
                    elif in_type[:2] == 'pl':
                        in_items2 = cmds.listConnections(in_items[0],d=False, s=True )
                        if in_items2 != None:
                                color_map_tex = in_tex
                        else:
                            content_tex = in_tex
                else:
                    content_tex = in_tex

            if out_mat == None:
                break

            iscon = cmds.isConnected(fileNode+'.outColor',out_mat[0] + '.color')
            if iscon:
                cmds.disconnectAttr(fileNode+'.outColor',out_mat[0] + '.color')


            cmds.connectAttr( content_tex + '.outColor', out_mat[0] + '.color' )
            if color_map_tex != None:
                #cmds.delete( color_map_tex )
                del_list.append(color_map_tex)
            #cmds.delete( fileNode )
            del_list.append(fileNode) 



    del_list = {}.fromkeys(del_list).keys()
    for tex in del_list:
        cmds.delete( tex )


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






