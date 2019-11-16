import bpy

from .renaming_proFeatures import RENAMING_MT_variableMenu
from bpy.props import StringProperty

#############################################
############ PANELS ########################
#############################################
# addon Panel

def drawSimpleUi(self, context):
    layout = self.layout
    scene = context.scene

    layout.label(text="Target")
    split = layout.split(align=True, factor=0.3)
    split.label(text="Type")
    split.prop(scene, "renaming_object_types", text="")
    if str(scene.renaming_object_types) == 'OBJECT':
        layout.prop(scene, "renaming_object_types_specified", expand=True)
    # elif str(scene.renaming_object_types) == 'ADDOBJECTS':
    #    layout.prop(scene, "renaming_object_addtypes_specified", expand=True)

    # layout.use_property_split = False  # Activate single-column layout

    if str(scene.renaming_object_types) in ('MATERIAL', 'DATA'):
        layout.prop(scene, "renaming_only_selection", text="Only Of Selected Objects")
    elif str(scene.renaming_object_types) in ('OBJECT', 'ADDOBJECTS', 'BONE'):
        layout.prop(scene, "renaming_only_selection", text="Only Selected")

    layout.separator()

    ###############################################
    layout.label(text="Rename")

    row = layout.row(align=True)
    # row.scale_y = 1.5
    row.prop(scene, "renaming_newName", text="")
    row.operator("renaming.name_replace", icon="FORWARD")
    layout.separator()

    ###############################################

    if scene.renaming_useRegex == False:
        row = layout.row(align=True)
        row.prop(scene, "renaming_useRegex")
        row.prop(scene, "renaming_matchcase")
    else:
        layout.prop(scene, "renaming_useRegex")

    layout.prop(scene, "renaming_search")
    layout.prop(scene, "renaming_replace")
    row = layout.row(align=True)
    #row.scale_y = 1.5
    row.operator("renaming.search_replace", icon="FILE_REFRESH")
    layout.separator()

    ###############################################
    layout.label(text="Other")

    ###############################################
    row = layout.row(align=True)
    row.prop(scene, "renaming_prefix", text="")
    row.operator("renaming.add_prefix", icon="REW")

    ###############################################
    row = layout.row(align=True)
    row.prop(scene, "renaming_suffix", text="")
    row.operator("renaming.add_suffix", icon="FF")

    ###############################################
    row = layout.row(align=True)
    row.prop(scene, "renaming_digits_numerate", text="")
    row.operator("renaming.numerate", icon="LINENUMBERS_ON")

    ###############################################
    row = layout.row(align=True)
    row.prop(scene, "renaming_cut_size", text="")
    row.operator("renaming.cut_string", icon="X")

    if str(scene.renaming_object_types) in ('DATA', 'OBJECT', 'ADDOBJECTS'):
        row = layout.row(align=True)
        row.prop(scene, "renaming_sufpre_data_02", text="")
        row.operator("renaming.dataname_from_obj", icon="MOD_DATA_TRANSFER")

def drawAdvancedUI(self, context, advancedMode):

    layout = self.layout
    scene = context.scene

    layout.label(text="Target")

    split = layout.split(align=True, factor=0.3)
    split.label(text="Type")
    split.prop(scene, "renaming_object_types", text="")

    if str(scene.renaming_object_types) == 'OBJECT':
        layout.prop(scene, "renaming_object_types_specified", expand=True)
    # elif str(scene.renaming_object_types) == 'ADDOBJECTS':
    #    layout.prop(scene, "renaming_object_addtypes_specified", expand=True)

    # layout.use_property_split = True  # Activate single-column layout

    if str(scene.renaming_object_types) in ('MATERIAL', 'DATA'):
        layout.prop(scene, "renaming_only_selection", text="Only Of Selected Objects")
    elif str(scene.renaming_object_types) in ('OBJECT', 'ADDOBJECTS', 'BONE'):
        layout.prop(scene, "renaming_only_selection", text="Only Selected")

    layout.separator()
    # layout.use_property_split = False  # Activate single-column layout

    layout.label(text="Rename")
    if str(scene.renaming_object_types) in ('OBJECT'):

        ###### NEW NAME #######
        row = layout.row(align=True)
        if advancedMode == True:
            split = layout.split(factor=0.6, align=True)
            split.prop(scene, "renaming_newName", text='Name')
            split = split.split(factor=0.75, align=True)
            split.prop(scene, "renaming_numerate", text='')
            button = split.operator("object.renaming_set_variable", text="@").inputBox = "newName"

        row = layout.row()
        row.scale_y = 1.5
        row.operator("renaming.name_replace", icon="FORWARD")
        layout.separator()

        ###### SEARCH REPLACE #######


        if advancedMode == True:
            if scene.renaming_useRegex == False:
                row = layout.row(align=True)
                row.prop(scene, "renaming_useRegex")
                row.prop(scene, "renaming_matchcase")
            else:
                layout.prop(scene, "renaming_useRegex")

            row = layout.row(align=True)
            split = row.split(factor=0.9, align=True)
            split.prop(scene, "renaming_search", text='Search')
            button = split.operator("object.renaming_set_variable", text="@").inputBox = "search"
            row = layout.row(align=True)
            split = row.split(factor=0.9, align=True)
            split.prop(scene, "renaming_replace", text='Replace')
            button = split.operator("object.renaming_set_variable", text="@").inputBox = "replace"



        row = layout.row(align=True)
        row.scale_y = 1.5
        row.operator("renaming.search_replace", icon="FILE_REFRESH")
        layout.separator()

        ###############################################
        layout.label(text="Other")

        #### REFIX SUFFIX
        if advancedMode == True:
            row = layout.row(align=True)
            split = row.split(factor=0.9, align=True)
            split.prop(scene, "renaming_prefix", text='Prefix')
            button = split.operator("object.renaming_set_variable", text="@").inputBox = "prefix"
            layout.operator("renaming.add_prefix", icon="REW")

            row = layout.row(align=True)
            split = row.split(factor=0.9, align=True)
            split.prop(scene, "renaming_suffix", text='Suffix')
            button = split.operator("object.renaming_set_variable", text="@").inputBox = "suffix"
            layout.operator("renaming.add_suffix", icon="FF")

        if advancedMode == True:
            layout.prop(scene, "renaming_digits_numerate")
            layout.operator("renaming.numerate", icon="LINENUMBERS_ON")
            layout.prop(scene, "renaming_cut_size")
            layout.operator("renaming.cut_string", icon="X")

    else:
        layout.prop(scene, "renaming_newName", text='Name')
        layout.operator("renaming.name_replace")

        layout.prop(scene, "renaming_search", text='Search')
        layout.prop(scene, "renaming_replace", text='Replace')
        layout.prop(scene, "renaming_useRegex")
        if scene.renaming_useRegex == False:
            layout.prop(scene, "renaming_matchcase")
        layout.operator("renaming.search_replace", icon="FILE_REFRESH")

        layout.prop(scene, "renaming_prefix", text='Prefix')
        layout.operator("renaming.add_prefix", icon="REW")

        layout.prop(scene, "renaming_suffix", text='Suffix')
        layout.operator("renaming.add_suffix", icon="FF")

        layout.prop(scene, "renaming_digits_numerate")
        layout.operator("renaming.numerate", icon="LINENUMBERS_ON")
        layout.prop(scene, "renaming_cut_size")
        layout.operator("renaming.cut_string", icon="X")

    if str(scene.renaming_object_types) in ('DATA', 'OBJECT', 'ADDOBJECTS'):
        if advancedMode == True:
            row = layout.row(align=True)
            split = row.split(factor=0.9, align=True)
            split.prop(scene, "renaming_sufpre_data_02", text='Data')
            button = split.operator("object.renaming_set_variable", text="@").inputBox = "dataFromObj"
            layout.operator("renaming.dataname_from_obj", icon="MOD_DATA_TRANSFER")

class VIEW3D_PT_tools_renaming_panel(bpy.types.Panel):
    """Creates a renaming Panel"""
    bl_label = "Simple Renaming Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rename"

    def draw(self, context):


        prefs = bpy.context.preferences.addons[__package__].preferences
        advancedMode = prefs.renamingPanel_advancedMode

        layout = self.layout
        layout.prop(prefs, "renamingPanel_advancedMode")

        if advancedMode == True:
            drawAdvancedUI(self, context, advancedMode)
        else:
            drawSimpleUi(self, context)


# addon Panel
class VIEW3D_PT_tools_type_suffix(bpy.types.Panel):
    """Creates a renaming Panel"""
    bl_label = "Prefix/Suffix by Type"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rename"


    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.prop(scene, "type_pre_sub_only_selection", text="Only Selected Objects")
        layout.prop(scene, "renaming_sufpre_type", expand=True)
        # layout.prop(scene, "renaming_sufpre_types_specified")


        if scene.renaming_sufpre_type == "PRE":
            layout.label(text="Add Type Prefix")
        else:
            layout.label(text="Add Type Suffix")

        split = layout.split()

        col = split.column()
        row = col.row()
        row.prop(scene, "renaming_sufpre_empty", text = "")
        op = row.operator("renaming.add_sufpre_by_type", text = "Empties").option = 'empty'

        row = col.row()
        row.prop(scene, "renaming_sufpre_geometry", text = "")
        op = row.operator('renaming.add_sufpre_by_type', text = "Meshes").option = 'mesh'

        row = col.row()
        row.prop(scene, "renaming_sufpre_material", text = "")
        op = row.operator('renaming.add_sufpre_by_type', text = "Materials").option = 'material'

        row = col.row()
        row.prop(scene, "renaming_sufpre_curve", text = "")
        op = row.operator('renaming.add_sufpre_by_type', text = "Curves").option = 'curve'

        row = col.row()
        row.prop(scene, "renaming_sufpre_armature", text = "")
        op = row.operator('renaming.add_sufpre_by_type', text = "Armatures").option = 'armature'

        row= col.row()
        row.prop(scene, "renaming_sufpre_lattice", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Lattices").option = 'lattice'

        row= col.row()
        row.prop(scene, "renaming_sufpre_data", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Data").option = 'data'

        row = col.row()
        row.prop(scene, "renaming_sufpre_surfaces", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Surfaces").option = 'surface'

        row = col.row()
        row.prop(scene, "renaming_sufpre_cameras", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Cameras").option = 'camera'

        row = col.row()
        row.prop(scene, "renaming_sufpre_lights", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Lights").option = 'light'

        row = col.row()
        row.prop(scene, "renaming_sufpre_collection", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Collections").option = 'collection'

        row = col.row()
        row.prop(scene, "renaming_sufpre_text", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Texts").option = 'text'

        row = col.row()
        row.prop(scene, "renaming_sufpre_gpencil", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Grease Pencil").option = 'gpencil'

        row = col.row()
        row.prop(scene, "renaming_sufpre_metaball", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Metaballs").option = 'metaball'

        row = col.row()
        row.prop(scene, "renaming_sufpre_bone", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Bones").option = 'bone'

        row = col.row()
        row.prop(scene, "renaming_sufpre_speakers", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Speakers").option = 'speakers'

        row = col.row()
        row.prop(scene, "renaming_sufpre_lightprops", text = "")
        row.operator('renaming.add_sufpre_by_type', text = "Light Probes").option = 'lightprops'

        row = col.row()
        row.operator('renaming.add_sufpre_by_type', text = "All").option = 'all'

class VIEW3D_OT_SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.renaming_set_variable"
    bl_label = "Simple Object Operator"

    inputBox: StringProperty()

    def execute(self, context):
        bpy.context.scene.renaming_inputContext = self.inputBox
        bpy.ops.wm.call_menu(name = RENAMING_MT_variableMenu.bl_idname)
        return {'FINISHED'}



class VIEW3D_OT_RenamingPopupOperator(bpy.types.Operator):
    bl_idname = "renaming.f_popup_operator"
    bl_label = "Simple Renaming Panel"

    my_float : bpy.props.FloatProperty(name="Some Floating Point")
    my_bool : bpy.props.BoolProperty(name="Toggle Option")
    my_string : bpy.props.StringProperty(name="String Value")

    def execute(self, context):
        print("Dialog Runs")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class LITTLE_RENAMING_HELPERS(bpy.types.Operator):
    """Creates a renaming Panel"""
    bl_label = "Renaming Helpers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rename"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        return {'FINISHED'}

