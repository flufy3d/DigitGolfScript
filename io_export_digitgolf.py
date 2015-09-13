
bl_info = {
    "name": "Digit Golf Scene Map Exporter",
    "author": "flufy3d",
    "version": (0,1),
    "blender": (2, 74, 0),
    "location": "Properties > Render > DigitGolf",
    "description": "export scene mat type map and height map",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export"
}

import bpy
import os
import os.path
import io
import json

flip_mode = 'Y'

class UL_material_elements_actions(bpy.types.Operator):
    bl_idname = "digitgolf.list_action"
    bl_label = "List Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
        )
    )

    def invoke(self, context, event):
        global material_dataset

        scn = context.scene
        idx = scn.cur_material_elements_index

        try:
            item = scn.cur_material_elements[idx]
        except IndexError:
            pass

        else:
            if self.action == 'UP' and idx > 0:
                scn.cur_material_elements_index -= 1
                info = 'Item %d selected' % (scn.cur_material_elements_index )
                self.report({'INFO'}, info)

            elif self.action == 'DOWN' and idx < len(scn.cur_material_elements) - 1:
                scn.cur_material_elements_index += 1
                info = 'Item %d selected' % (scn.cur_material_elements_index )
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item %s removed from list' % (scn.cur_material_elements[scn.cur_material_elements_index].name)
                scn.cur_material_elements_index -= 1
                self.report({'INFO'}, info)
                scn.cur_material_elements.remove(idx)
                save_cur_phymat(scn)

        if self.action == 'ADD':
            sel_mat = scn.objects.active.active_material.name
            if sel_mat not in material_dataset[scn.mat_group_items_prop]:
                item = scn.cur_material_elements.add()
                item.id = len(scn.cur_material_elements)
                item.name = scn.objects.active.active_material.name
                scn.cur_material_elements_index = (len(scn.cur_material_elements)-1)
                info = '%s added to list' % (item.name)
                self.report({'INFO'}, info)
                save_cur_phymat(scn)

        return {"FINISHED"}

class UL_material_elements(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(0.3)
        split.label("Index: %d" % (index))
        split.prop(item, "name", text="", emboss=False, translate=False, icon='BORDER_RECT')
    def invoke(self, context, event):
        pass   


class OBJECT_PT_digitgolf(bpy.types.Panel):
    bl_label = "DigitGolf"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    def draw(self, context):

        objects = bpy.data.objects
        layout = self.layout
        scn = bpy.context.scene

        row = layout.row()
        col0 = row.column()
        col1 = row.column()

        col0.prop(scn,"mat_group_items_prop")
        col1.prop(scn,"mat_group_items_cur_blur_value")

        row = layout.row()
        row.template_list("UL_material_elements", "", scn, "cur_material_elements", scn, "cur_material_elements_index", rows=5)
        col = row.column(align=True)
        col.operator("digitgolf.list_action", icon='ZOOMIN', text="").action = 'ADD'
        col.operator("digitgolf.list_action", icon='ZOOMOUT', text="").action = 'REMOVE'
        col.separator()
        col.operator("digitgolf.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("digitgolf.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'


        row = layout.row()
        row.operator("digitgolf.auto_set")

        row = layout.row()
        col0 = row.column()
        col1 = row.column()

        col0.operator("digitgolf.render_this")
        col0.operator("digitgolf.render_all")
        col1.operator("digitgolf.render_heightmap")
        col1.operator("digitgolf.export_entity_info")
        
        return

def render_one(scn,name):
    global material_dataset
    if material_dataset == {}:
        return

    tree = scn.node_tree
    tree.nodes.clear()
    #for node in tree.nodes:
    #    tree.nodes.remove(node)

    blur_value = material_dataset[name][0]
    print(blur_value)
    layer_node = tree.nodes.new('CompositorNodeRLayers')
    layer_node.location = 0,0
    blur_node = tree.nodes.new('CompositorNodeBlur')
    blur_node.location = 300,0
    blur_node.filter_type='FAST_GAUSS'
    blur_node.size_x = blur_value
    blur_node.size_y = blur_value
    flip_node = tree.nodes.new('CompositorNodeFlip')
    flip_node.location = 600,0
    flip_node.axis = flip_mode
    composite_node = tree.nodes.new('CompositorNodeComposite')
    composite_node.location =900,0

    links = tree.links
    link_l_b = links.new(layer_node.outputs[0], blur_node.inputs[0])
    link_b_f = links.new(blur_node.outputs[0], flip_node.inputs[0])
    link_f_c = links.new(flip_node.outputs[0], composite_node.inputs[0])


    scn.render.filepath = '//output/'+name

    update_blender_material(name)

    bpy.ops.render.render(animation=False,write_still=True) 


class Op_render_this(bpy.types.Operator):
    bl_idname = "digitgolf.render_this"
    bl_label = "Render This"
    bl_description = "Render this PhyMat"
    @classmethod
    def poll(self, context):
        global material_dataset
        return material_dataset != {}
    def execute(self, context):
        render_one(context.scene,context.scene.mat_group_items_prop)
        info = '%s Rendering is complete' % (context.scene.mat_group_items_prop)
        self.report({'INFO'}, info)
        return{'FINISHED'}

class Op_render_all(bpy.types.Operator):
    bl_idname = "digitgolf.render_all"
    bl_label = "Render All"
    bl_description = "Render all PhyMat"

    @classmethod
    def poll(self, context):
        global material_dataset
        return material_dataset != {}
    def execute(self, context):
        global mat_group_items
        for g in mat_group_items:
            render_one(context.scene , g[0])
            info = '%s Rendering is complete' % (g[0])
            self.report({'INFO'}, info)
        return{'FINISHED'}

class Op_render_heightmap(bpy.types.Operator):
    bl_idname = "digitgolf.render_heightmap"
    bl_label = "Render HeightMap"
    bl_description = "Render HeightMap"

    def execute(self, context):
        scn = context.scene
        tree = scn.node_tree
        tree.nodes.clear()
  

        layer_node = tree.nodes.new('CompositorNodeRLayers')
        layer_node.location = 0,0
        norm_node = tree.nodes.new('CompositorNodeNormalize')
        norm_node.location = 300,0
        invert_node = tree.nodes.new('CompositorNodeInvert')
        invert_node.location =600,0
        maprange_node = tree.nodes.new('CompositorNodeMapRange')
        maprange_node.location = 900,0
        maprange_node.inputs[3].default_value = 0.1
        maprange_node.inputs[4].default_value = 0.9
        flip_node = tree.nodes.new('CompositorNodeFlip')
        flip_node.location = 1200,0
        flip_node.axis = flip_mode
        composite_node = tree.nodes.new('CompositorNodeComposite')
        composite_node.location =1500,0

        links = tree.links
        links.new(layer_node.outputs[2], norm_node.inputs[0])
        links.new(norm_node.outputs[0], invert_node.inputs[1])
        links.new(invert_node.outputs[0],maprange_node.inputs[0])
        links.new(maprange_node.outputs[0],flip_node.inputs[0])
        links.new(flip_node.outputs[0], composite_node.inputs[0])


        scn.render.filepath = '//output/'+'heightmap'
   
        bpy.ops.render.render(animation=False,write_still=True) 

        return{'FINISHED'}


def travel_objects(obj,arl,clist):
    arl.append(obj.name)
    t_node = {}
    t_node['name'] = obj.name
    t_node['trans'] = {}
    t_node['trans']['loc'] = [obj.location[0],obj.location[1],obj.location[2]]
    t_node['trans']['rot'] = [obj.rotation_euler[0],obj.rotation_euler[1],obj.rotation_euler[2]]
    t_node['trans']['scale'] = [obj.scale[0],obj.scale[1],obj.scale[2]]

    t_node['children'] = []
    clist.append(t_node)


    if len(obj.children) != 0:

        for o in obj.children:
            travel_objects(o,arl,t_node['children'])


def _export_entity_info(context,f):

    scn = context.scene
    data = {'version':'1.0','scene':[]}
    already_read_list = []
    for obj in scn.objects:
        if obj.name not in already_read_list:
            travel_objects(obj,already_read_list,data['scene'])



    json.dump(data, f, indent=1, separators=(',',':'), check_circular=False, allow_nan=False)


class Op_export_entity_info(bpy.types.Operator):
    bl_idname = "digitgolf.export_entity_info"
    bl_label = "Export Entity Info"
    bl_description = "Export Entity Info"

    def execute(self, context):

        directory = os.path.dirname(bpy.data.filepath)
        print(directory)

        file_path = directory+'\\output\\scene.json'
        f = io.open(file_path, mode="wt", newline="\n", encoding="utf_8")
        


        try:
            try:
                _export_entity_info(context,f)
            finally:
                f.close()
        except Exception:
            os.remove(file_path)
            info = 'export_entity_info fails!'
            self.report({'INFO'}, info)




            

        return{'FINISHED'}


def auto_set(self,context):
    global material_dataset
    global mat_group_items
    scn = context.scene


    for item in mat_group_items:
        material_dataset[item[0]] = [5.0]

    for item in mat_group_items:
        if item[0] == 'Greens':
            for mat in bpy.data.materials:
                if mat.name.startswith('green'):
                    material_dataset[item[0]].append(mat.name)
                elif mat.name.startswith('tee'):
                    material_dataset[item[0]].append(mat.name)
        elif item[0] == 'Fairway':
            for mat in bpy.data.materials:
                if mat.name.startswith('fairway'):
                    material_dataset[item[0]].append(mat.name)
        elif item[0] == 'Rough':
            for mat in bpy.data.materials:
                if mat.name.startswith('rough'):
                    material_dataset[item[0]].append(mat.name)
        elif item[0] == 'Heather':
            for mat in bpy.data.materials:
                if mat.name.startswith('heather'):
                    material_dataset[item[0]].append(mat.name)
        elif item[0] == 'Bunker':
            for mat in bpy.data.materials:
                if mat.name.startswith('sand'):
                    material_dataset[item[0]].append(mat.name)
        elif item[0] == 'Hill':
            for mat in bpy.data.materials:
                if mat.name.startswith('hill'):
                    material_dataset[item[0]].append(mat.name)
        elif item[0] == 'Road':
            material_dataset[item[0]][0] = 0
            for mat in bpy.data.materials:
                if mat.name.startswith('cartpath'):
                    material_dataset[item[0]].append(mat.name)
                elif mat.name.startswith('road'):
                    material_dataset[item[0]].append(mat.name)
        elif item[0] == 'Water':
            for mat in bpy.data.materials:
                if mat.name.startswith('water'):
                    material_dataset[item[0]].append(mat.name)
                elif mat.name.startswith('river'):
                    material_dataset[item[0]].append(mat.name)
                elif mat.name.startswith('lake'):
                    material_dataset[item[0]].append(mat.name)

    refresh_phymat_ui(scn)

    set_relative_param(scn)

    return


class Op_auto_set(bpy.types.Operator):
    bl_idname = "digitgolf.auto_set"
    bl_label = "Auto Set"
    bl_description = "Auto set relative Properties"

    def execute(self, context):
        auto_set(self,context)
        return{'FINISHED'}


def save_cur_phymat(scn):
    global material_dataset

    tmp_blur = material_dataset[scn.mat_group_items_prop][0]
    material_dataset[scn.mat_group_items_prop] = [tmp_blur]

    for mat in scn.cur_material_elements:
        material_dataset[scn.mat_group_items_prop].append(mat.name)


def get_area_space(scheme,name):
    ret = {}
    tareas = bpy.data.screens[scheme].areas
    for area in tareas:                                                                             
        if area.type == name:
            ret = area.spaces[0]
    return ret



def set_relative_param(scn):
    scn.render.resolution_x = 4096
    scn.render.resolution_y = 4096
    scn.render.resolution_percentage = 100
    scn.render.use_antialiasing = True
    scn.render.antialiasing_samples = '11'
    scn.display_settings.display_device = 'None'
    scn.render.image_settings.file_format = 'PNG'
    scn.render.image_settings.quality = 100
    scn.render.image_settings.color_depth = '16'
    scn.render.image_settings.color_mode = 'BW'
    scn.render.image_settings.compression = 100
    scn.use_nodes = True


    try:
        get_area_space('Default','VIEW_3D').clip_end = 10000
        get_area_space('Scripting','VIEW_3D').clip_end = 10000
    except AttributeError:
        pass

    if 'god_cam' not in bpy.data.cameras:
        bpy.ops.object.camera_add()
        bpy.context.scene.objects.active.data.name = 'god_cam'
        bpy.context.scene.objects.active.name = 'god_cam'
    bpy.data.cameras['god_cam'].type = 'ORTHO'
    bpy.data.cameras['god_cam'].ortho_scale = 1426
    bpy.data.cameras['god_cam'].clip_end = 10000
    bpy.data.objects['god_cam'].rotation_euler = [0,0,0]
    bpy.data.objects['god_cam'].scale = [1,1,1]
    bpy.data.objects['god_cam'].location = [0,0,3000]
    scn.camera = bpy.data.objects['god_cam']

   

def refresh_phymat_ui(scn):
    global material_dataset
    scn.cur_material_elements.clear()
    if material_dataset == {}:
        return

    scn.mat_group_items_cur_blur_value = material_dataset[scn.mat_group_items_prop][0]

    scn.cur_material_elements_index = 0

    for mat in material_dataset[scn.mat_group_items_prop]:
        if type(mat) == str:
            item = scn.cur_material_elements.add()
            item.id = scn.cur_material_elements_index
            item.name = mat
            scn.cur_material_elements_index += 1

def update_blender_material(name):

    for mat in bpy.data.materials:
        if mat.name in material_dataset[name]:
            mat.diffuse_color = (1.0,1.0,1.0) 
        else:
            mat.diffuse_color = (0,0,0) 

        mat.texture_slots.clear(0)
        mat.use_shadeless = True 

def PhyMat_Update(self,context):
    global material_dataset
    #print(context.scene.mat_group_items_prop)
    refresh_phymat_ui(context.scene)
    update_blender_material(context.scene.mat_group_items_prop)

  
    pass

def Blur_Update(self,context):
    global material_dataset
    scn = context.scene
    if material_dataset != {}:
        material_dataset[scn.mat_group_items_prop][0] = scn.mat_group_items_cur_blur_value


mat_group_items = [
    ("Greens", "Greens", "", 'MESH_DATA',1),
    ("Fairway", "Fairway", "", 'MESH_DATA', 2),
    ("Rough", "Rough", "", 'MESH_DATA', 3),
    ("Heather", "Heather", "", 'MESH_DATA', 4),
    ("Bunker", "Bunker", "", 'MESH_DATA', 5),
    ("Hill", "Hill", "", 'MESH_DATA', 6),
    ("Road", "Road", "", 'MESH_DATA', 7),
    ("Water", "Water", "", 'MESH_DATA', 8),
]


material_dataset = {}



class material_elements(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    id = bpy.props.IntProperty()


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.mat_group_items_prop = bpy.props.EnumProperty(items=mat_group_items,name = 'PhyMat',update = PhyMat_Update)
    bpy.types.Scene.mat_group_items_cur_blur_value = bpy.props.FloatProperty(name = 'blur',update =Blur_Update)

    bpy.types.Scene.cur_material_elements = bpy.props.CollectionProperty(type=material_elements)
    bpy.types.Scene.cur_material_elements_index = bpy.props.IntProperty()

    if hasattr( bpy.context , 'scene') :
        bpy.context.scene.cur_material_elements.clear()
        bpy.context.scene.mat_group_items_cur_blur_value = 0


    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.mat_group_items_prop
    del bpy.types.Scene.mat_group_items_cur_blur_value

    del bpy.types.Scene.cur_material_elements
    del bpy.types.Scene.cur_material_elements_index

    pass

if __name__ == "__main__":
    register()
