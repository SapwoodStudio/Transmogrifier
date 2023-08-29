# BEGIN GPL LICENSE BLOCK #####
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
#
# END GPL LICENSE BLOCK #####


import bpy
from bpy.types import AddonPreferences, PropertyGroup, Operator, Panel
from bpy.props import BoolProperty, IntProperty, EnumProperty, StringProperty, PointerProperty, FloatVectorProperty
import os
import shutil
import pathlib
import re
import json
import subprocess

bl_info = {
    "name": "Transmogrifier",
    "author": "Sapwood Studio",
    "version": (1, 2, 0),
    "blender": (3, 6, 0),
    "category": "Import-Export",
    "location": "Set in preferences below. Default: Top Bar (After File, Edit, ...Help)",
    "description": "Batch converts 3D files and associated textures into other formats.",
    "doc_url": "github.com/SapwoodStudio/Transmogrifier",
    "tracker_url": "github.com/sapwoodstudio/Transmogrifier/issues",
}

# A Dictionary of operator_name: [list of preset EnumProperty item tuples].
# Blender's doc warns that not keeping reference to enum props array can
# cause crashs and weird issues.
# Also useful for the get_preset_index function.
preset_enum_items_refs = {}

# Returns a list of tuples used for an EnumProperty's items (identifier, name, description)
# identifier, and name are the file name of the preset without the file extension (.py)
def get_operator_presets(operator):
    presets = [('NO_PRESET', "(no preset)", "", 0)]
    for d in bpy.utils.script_paths(subdir="presets/operator/" + operator):
        for f in os.listdir(d):
            if not f.endswith(".py"):
                continue
            f = os.path.splitext(f)[0]
            presets.append((f, f, ""))
    # Blender's doc warns that not keeping reference to enum props array can
    # cause crashs and weird issues:
    preset_enum_items_refs[operator] = presets
    return presets

# Returns a dictionary of options from an operator's preset.
# When calling an operator's method, you can use ** before a dictionary
# in the method's arguments to set the arguments from that dictionary's
# key: value pairs. Example:
# bpy.ops.category.operator(**options)
def load_operator_preset(operator, preset):
    options = {}
    if preset == 'NO_PRESET':
        return options

    for d in bpy.utils.script_paths(subdir="presets/operator/" + operator):
        fp = "".join([d, "/", preset, ".py"])
        if os.path.isfile(fp):  # Found the preset file
            print("Using preset " + fp)
            file = open(fp, 'r')
            for line in file.readlines():
                # This assumes formatting of these files remains exactly the same
                if line.startswith("op."):
                    line = line.removeprefix("op.")
                    split = line.split(" = ")
                    key = split[0]
                    value = split[1]
                    options[key] = eval(value)
            file.close()
            return options
    # If it didn't find the preset, use empty options
    # (the preset option should look blank if the file doesn't exist anyway)
    return options

# Finds the index of a preset with preset_name and returns it
# Useful for transferring the value of a saved preset (in a StringProperty)
# to the NOT saved EnumProperty for that preset used to present a nice GUI.
def get_preset_index(operator, preset_name):
    for p in range(len(preset_enum_items_refs[operator])):
        if preset_enum_items_refs[operator][p][0] == preset_name:
            return p
    return 0



# A Dictionary of operator_name: [list of preset EnumProperty item tuples].
# Blender's doc warns that not keeping reference to enum props array can
# cause crashs and weird issues.
# Also useful for the get_preset_index function.
transmogrifier_preset_enum_items_refs = {}

# Returns a list of tuples used for an EnumProperty's items (identifier, name, description)
# identifier, and name are the file name of the preset without the file extension (.json)
def get_transmogrifier_presets(operator):
    presets = [('NO_PRESET', "(no preset)", "", 0)]
    for d in bpy.utils.script_paths(subdir="presets/operator/" + operator):
        for f in os.listdir(d):
            if not f.endswith(".json"):
                continue
            f = os.path.splitext(f)[0]
            presets.append((f, f, ""))
    # Blender's doc warns that not keeping reference to enum props array can
    # cause crashs and weird issues:
    transmogrifier_preset_enum_items_refs[operator] = presets
    return presets

# Returns a dictionary of options from an operator's preset.
# When calling an operator's method, you can use ** before a dictionary
# in the method's arguments to set the arguments from that dictionary's
# key: value pairs. Example:
# bpy.ops.category.operator(**options)
def load_transmogrifier_preset(operator, preset):
    json_dict = {}
    if preset == 'NO_PRESET':
        return json_dict

    for d in bpy.utils.script_paths(subdir="presets/operator/" + operator):
        fp = "".join([d, "/", preset, ".json"])
        if os.path.isfile(fp):  # Found the preset file
            print("Using preset " + fp)
            
            # Open JSON file
            with open(fp, 'r') as openfile:
            
                # Read from JSON file
                json_dict = json.load(openfile)
            
            return json_dict
            
    # If it didn't find the preset, use empty options
    # (the preset option should look blank if the file doesn't exist anyway)
    return json_dict

# Finds the index of a preset with preset_name and returns it
# Useful for transferring the value of a saved preset (in a StringProperty)
# to the NOT saved EnumProperty for that preset used to present a nice GUI.
def get_transmogrifier_preset_index(operator, preset_name):
    for p in range(len(transmogrifier_preset_enum_items_refs[operator])):
        if transmogrifier_preset_enum_items_refs[operator][p][0] == preset_name:
            return p
    return 0

# Refresh UI when a Transmogrifier preset is selected by running REFRESHUI operator.
def refresh_ui(self, context):
    eval('bpy.ops.refreshui.transmogrifier()')

# Draws the .blend file specific settings used in the
# Popover panel or Side Panel panel
def draw_settings(self, context):
    self.layout.use_property_split = True
    self.layout.use_property_decorate = False

    # Display combination of title and version from bl_info.
    version = ''
    for num in bl_info["version"]:
        version = version + "." + str(num)
    version = version.lstrip(".")
    title = bl_info["name"] + " " + version
    self.layout.label(text = title)

    settings = context.scene.transmogrifier

    # Batch Convert button
    # self.layout.operator('transmogrifier.transmogrify', icon='FILE_CACHE')
    row = self.layout.row()
    row = row.row(align=True)
    row.operator('transmogrifier.transmogrify', text='Batch Convert', icon='FILE_CACHE')
    row.scale_y = 1.5

    # Transmogrifier Presets Menu
    self.layout.separator()
    col = self.layout.column(align=True)
    col.label(text="WORKFLOW", icon='DRIVER')
    layout = self.layout
    row = layout.row(align=True)
    row.prop(settings, 'transmogrifier_preset_enum')
    row.operator("transmogrifierpreset.add", text="", icon="ADD")
    row.operator("transmogrifierpreset.remove", text="", icon="REMOVE")
    # Manually refresh UI via operator button. No longer needed because of update_enum in transmogrifier_preset propertygroup.
    # if settings.transmogrifier_preset != "NO_PRESET":
    #     # Refresh UI
    #     row = self.layout.row()
    #     row = row.row(align=True)
    #     row.operator('refreshui.transmogrifier', text='Refresh UI from Preset', icon='FILE_REFRESH')
    #     row.scale_y = 1.0


    # Import Settings
    self.layout.separator()
    col = self.layout.column(align=True)
    col.label(text="IMPORT SETTINGS:", icon='IMPORT')
    # Directory input
    col.prop(settings, 'directory')
    col.prop(settings, 'import_file')
    # self.layout.separator()
    # col = self.layout.column()

    # col.label(text=settings.import_file + " Settings:")
    if settings.import_file == 'DAE':
        col.prop(settings, 'import_dae_preset_enum')
    elif settings.import_file == 'ABC':
        col.prop(settings, 'import_abc_preset_enum')
    elif settings.import_file == 'USD':
        col.prop(settings, 'import_usd_extension')
        col.prop(settings, 'import_usd_preset_enum')
    elif settings.import_file == 'OBJ':
        col.prop(settings, 'import_obj_preset_enum')
    elif settings.import_file == 'PLY':
        col.prop(settings, 'import_ply_ascii')
    elif settings.import_file == 'STL':
        col.prop(settings, 'import_stl_ascii')
    elif settings.import_file == 'FBX':
        col.prop(settings, 'import_fbx_preset_enum')
    elif settings.import_file == 'glTF':
        col.prop(settings, 'import_gltf_extension')
    elif settings.import_file == 'X3D':
        col.prop(settings, 'import_x3d_preset_enum')



    # Export Settings
    self.layout.separator()
    # self.layout.separator()
    col = self.layout.column(align=True)
    col.label(text="EXPORT SETTINGS:", icon='EXPORT')
    
    # col.label(text="Models:", icon='OUTLINER_OB_MESH')
    col.prop(settings, "directory_output_location")
    if settings.directory_output_location == "Custom":
        col.prop(settings, "directory_output_custom")
        if settings.directory_output_custom:
            col.prop(settings, "use_subdirectories")
            if settings.use_subdirectories:
                col.prop(settings, "copy_item_dir_contents")
    col.prop(settings, "model_quantity")

    # Align menu items to the right.
    self.layout.use_property_split = True

    if settings.model_quantity == "2 Formats":
        # File Format 1
        col = self.layout.column(align=True)
        col.label(text="Format 1:", icon='OUTLINER_OB_MESH')
        col.prop(settings, 'export_file_1')

        if settings.export_file_1 == 'DAE':
            col.prop(settings, 'dae_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'ABC':
            col.prop(settings, 'abc_preset_enum')
            col.prop(settings, 'frame_start')
            col.prop(settings, 'frame_end')
        elif settings.export_file_1 == 'USD':
            col.prop(settings, 'usd_extension')
            col.prop(settings, 'usd_preset_enum')
        elif settings.export_file_1 == 'OBJ':
            col.prop(settings, 'obj_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'PLY':
            col.prop(settings, 'ply_ascii')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'STL':
            col.prop(settings, 'stl_ascii')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'FBX':
            col.prop(settings, 'fbx_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'glTF':
            col.prop(settings, 'gltf_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'X3D':
            col.prop(settings, 'x3d_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        
        # Set scale
        col = self.layout.column(align=True)
        col.prop(settings, 'export_file_1_scale')
        # self.layout.separator()

        # File Format 2
        col = self.layout.column(align=True)
        col.label(text="Format 2:", icon='OUTLINER_OB_MESH')
        col.prop(settings, 'export_file_2')
        # col.prop(settings, 'mode')

        if settings.export_file_2 == 'DAE':
            col.prop(settings, 'dae_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_2 == 'ABC':
            col.prop(settings, 'abc_preset_enum')
            col.prop(settings, 'frame_start')
            col.prop(settings, 'frame_end')
        elif settings.export_file_2 == 'USD':
            col.prop(settings, 'usd_extension')
            col.prop(settings, 'usd_preset_enum')
        elif settings.export_file_2 == 'OBJ':
            col.prop(settings, 'obj_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_2 == 'PLY':
            col.prop(settings, 'ply_ascii')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_2 == 'STL':
            col.prop(settings, 'stl_ascii')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_2 == 'FBX':
            col.prop(settings, 'fbx_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_2 == 'glTF':
            col.prop(settings, 'gltf_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_2 == 'X3D':
            col.prop(settings, 'x3d_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        
        # Set scale
        col = self.layout.column(align=True)
        col.prop(settings, 'export_file_2_scale')


    elif settings.model_quantity == "1 Format":
        # File Format 1
        col = self.layout.column(align=True)
        col.label(text="Format 1:", icon='OUTLINER_OB_MESH')
        col.prop(settings, 'export_file_1')
        # col.prop(settings, 'mode')

        if settings.export_file_1 == 'DAE':
            col.prop(settings, 'dae_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'ABC':
            col.prop(settings, 'abc_preset_enum')
            col.prop(settings, 'frame_start')
            col.prop(settings, 'frame_end')
        elif settings.export_file_1 == 'USD':
            col.prop(settings, 'usd_extension')
            col.prop(settings, 'usd_preset_enum')
        elif settings.export_file_1 == 'OBJ':
            col.prop(settings, 'obj_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'PLY':
            col.prop(settings, 'ply_ascii')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'STL':
            col.prop(settings, 'stl_ascii')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'FBX':
            col.prop(settings, 'fbx_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'glTF':
            col.prop(settings, 'gltf_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        elif settings.export_file_1 == 'X3D':
            col.prop(settings, 'x3d_preset_enum')
            self.layout.prop(settings, 'apply_mods')
        
        # Set scale
        col = self.layout.column(align=True)
        col.prop(settings, 'export_file_1_scale')
        # self.layout.sepaqrator()
        
    # else:
    #     self.layout.separator()


    col = self.layout.column(align=True)

    # Name Settings
    col.label(text="Names:", icon='SORTALPHA')
    col = self.layout.column(align=True)
    col.prop(settings, 'prefix')
    col.prop(settings, 'suffix')
    col = self.layout.column(align=True)
    col.prop(settings, 'set_data_names')
    col.prop(settings, 'set_UV_map_names')

    # Texture Settings
    # Align menu items to the left.
    self.layout.use_property_split = True
    # col = self.layout.column(align=True)
    col.label(text="Textures:", icon='TEXTURE')
    col.prop(settings, 'use_textures')

    if settings.use_textures:
        col.prop(settings, 'regex_textures')
        col.prop(settings, 'keep_modified_textures')
        self.layout.use_property_split = True
        col = self.layout.column(align=True)
        col.prop(settings, 'textures_source')
        if settings.textures_source == "Custom":
            col.prop(settings, 'textures_custom_dir')
            col.prop(settings, 'copy_textures_custom_dir')
            if settings.copy_textures_custom_dir:
                col.prop(settings, 'replace_textures')

        # col = self.layout.column(align=True)
        col.prop(settings, 'texture_resolution')

        if settings.texture_resolution != "Default":
            # Align menu items to the left.
            self.layout.use_property_split = False

            grid = self.layout.grid_flow(columns=3, align=True)
            grid.prop(settings, 'texture_resolution_include')
            # self.layout.separator()
        
            # Align menu items to the right.
            self.layout.use_property_split = True
            col = self.layout.column(align=True)

        col.prop(settings, 'image_format')
        if settings.image_format != "Default":
            col.prop(settings, 'image_quality')
            # Align menu items to the left.
            self.layout.use_property_split = False

            grid = self.layout.grid_flow(columns=3, align=True)
            grid.prop(settings, 'image_format_include')
        
        # self.layout.separator()

    # Transformation options.
    self.layout.use_property_split = True
    col = self.layout.column(align=True)
    col.label(text="Transformations:", icon='CON_PIVOT')
    col.prop(settings, 'set_transforms')
    if settings.set_transforms:
        self.layout.use_property_split = False
        grid = self.layout.grid_flow(columns=3, align=True)
        grid.prop(settings, 'set_transforms_filter')
        col = self.layout.column(align=True)
        
        if 'Location' in settings.set_transforms_filter:
            col.prop(settings, 'set_location')
        if 'Rotation' in settings.set_transforms_filter:
            col.prop(settings, 'set_rotation')
        if 'Scale' in settings.set_transforms_filter:
            col.prop(settings, 'set_scale')
    
        self.layout.use_property_split = True
        col = self.layout.column(align=True)


    col.prop(settings, 'apply_transforms')
    if settings.apply_transforms:
        self.layout.use_property_split = False
        grid = self.layout.grid_flow(columns=3, align=True)
        grid.prop(settings, 'apply_transforms_filter')
        # col = self.layout.column(align=True)
    # col = self.layout.column(align=True)

    # Set animation options.
    self.layout.use_property_split = True
    col = self.layout.column(align=True)
    col.label(text="Animations:", icon='ANIM')
    col.prop(settings, 'delete_animations')

    # Set scene unit options.
    # self.layout.use_property_split = True
    # col = self.layout.column(align=True)
    col.label(text="Scene:", icon='SCENE_DATA')
    col.prop(settings, 'unit_system')
    if settings.unit_system == "METRIC":
        col.prop(settings, 'length_unit_metric')
    elif settings.unit_system == "IMPERIAL":
        col.prop(settings, 'length_unit_imperial')

    # self.layout.separator()
    
    # Set max file size options.
    self.layout.use_property_split = True
    col = self.layout.column(align=True)
    col.label(text="File Size:", icon='FILE')
    col.prop(settings, 'auto_resize_files')
    # Align menu items to the left.
    self.layout.use_property_split = False
    col = self.layout.column(align=True)
    if settings.auto_resize_files != "None":
        col.prop(settings, 'file_size_maximum')
        grid = self.layout.grid_flow(columns=1, align=True)
        grid.prop(settings, 'file_size_methods')
        if 'Resize Textures' in settings.file_size_methods:
            self.layout.use_property_split = True
            col = self.layout.column(align=True)
            col.prop(settings, 'resize_textures_limit')
        if 'Decimate Meshes' in settings.file_size_methods:
            self.layout.use_property_split = False
            col = self.layout.column(align=True)
            col.prop(settings, 'decimate_limit')
        # self.layout.separator()

    # Archive options
    # Align menu items to the Right.
    self.layout.use_property_split = True
    col = self.layout.column(align=True)
    col.label(text="Archive:", icon='ASSET_MANAGER')
    col.prop(settings, 'save_preview_image')
    col.prop(settings, 'save_blend')
    col.prop(settings, 'save_conversion_log')


# Draws the button and popover dropdown button used in the
# 3D Viewport Header or Top Bar
def draw_popover(self, context):
    row = self.layout.row()
    row = row.row(align=True)
    row.operator('transmogrifier.transmogrify', text='', icon='FILE_CACHE')
    row.popover(panel='POPOVER_PT_transmogrify', text='')


# Create variables_dict dictionary from TransmogrifierSettings to pass to write_json function later.
def get_transmogrifier_settings(self, context):
    settings = context.scene.transmogrifier
    keys = [key for key in TransmogrifierSettings.__annotations__ if "enum" not in key]
    values = []
    for key in keys:
        # Get value as string to be evaluated later.
        value = eval('settings.' + str(key))
        # Convert enumproperty numbers to numbers, dictionaries and vectors to tuples
        if key == "texture_resolution" or key == "resize_textures_limit":
            if value != "Default":
                value = int(value)
        if "{" in str(value):
            value = tuple(value)
        elif "<" in str(value):
            value = str(value)
            char_start = "("
            char_end = ")"
            value = eval(re.sub('[xyz=]', '', "(" + ''.join(value).split(char_start)[1].split(char_end)[0] + ")"))
        values.append(value)
        # print(key, "=", value)

    variables_dict = dict(zip(keys, values))

    return variables_dict


# Write user variables to a JSON file.
def write_json(variables_dict, json_file):
        
    with open(json_file, "w") as outfile:
        json.dump(variables_dict, outfile)


# Read the JSON file where the conversion count is stored.
def read_json():
    # Open JSON file
    json_file = os.path.join(pathlib.Path(__file__).parent.resolve(), "Converter_Report.json")

    with open(json_file, 'r') as openfile:
    
        # Read from JSON file
        json_object = json.load(openfile)
    
    return json_object



# Side Panel panel (used with Side Panel option)
class VIEW3D_PT_transmogrify(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "Transmogrifier"

    def draw(self, context):
        draw_settings(self, context)

# Popover panel (used on 3D Viewport Header or Top Bar option)
class POPOVER_PT_transmogrify(Panel):
    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_label = "Transmogrifier"

    def draw(self, context):
        draw_settings(self, context)

# Addon settings that are NOT specific to a .blend file
class TransmogrifierPreferences(AddonPreferences):
    bl_idname = __name__

    def addon_location_updated(self, context):
        bpy.types.TOPBAR_MT_editor_menus.remove(draw_popover)
        bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)
        if hasattr(bpy.types, "VIEW3D_PT_transmogrify"):
            bpy.utils.unregister_class(VIEW3D_PT_transmogrify)
        if self.addon_location == 'TOPBAR':
            bpy.types.TOPBAR_MT_editor_menus.append(draw_popover)
        elif self.addon_location == '3DHEADER':
            bpy.types.VIEW3D_MT_editor_menus.append(draw_popover)
        elif self.addon_location == '3DSIDE':
            bpy.utils.register_class(VIEW3D_PT_transmogrify)


    # Copy import/export presets and studiolights shipped with Transmogrifier to relevant Blender Preferences directories
    def copy_assets(self, context):
        # Copy provided HDRI to Blender Preferences directory for use in rendering preview images
        # Create path to studiolights/world directory in Blender Preferences directory
        studiolight_dir = str(pathlib.Path(__file__).parents[3]) + '\\datafiles\\studiolights\\world'
        neutral_hdr_source = str(pathlib.Path(__file__).parent) + "\\assets\\neutral.hdr"
        neutral_hdr_destination = os.path.join(pathlib.Path(studiolight_dir).resolve(), "neutral.hdr")
                
        # Copy neutral.hdr from addon directory to studiolights/world.
        if not os.path.exists(studiolight_dir):
            os.makedirs(studiolight_dir)
        if not os.path.isfile(neutral_hdr_destination):
            shutil.copy(neutral_hdr_source, neutral_hdr_destination)

        # Copy provided export presets to Blender Preferences directory
        gltf_presets_source = str(pathlib.Path(__file__).parent) + '\\assets\\presets\\operator\\export_scene.gltf'
        gltf_presets_destination = str(pathlib.Path(__file__).parents[2]) + '\\presets\\operator\\export_scene.gltf'
        usd_presets_source = str(pathlib.Path(__file__).parent) + '\\assets\\presets\\operator\\wm.usd_export'
        usd_presets_destination = str(pathlib.Path(__file__).parents[2]) + '\\presets\\operator\\wm.usd_export'
        glb_preset_src = str(pathlib.Path(__file__).parent) + '\\assets\\presets\\operator\\export_scene.gltf\\GLB_Preset.py'
        glb_preset_dest = str(pathlib.Path(__file__).parents[2]) + '\\presets\\operator\\export_scene.gltf\\GLB_Preset.py'
        glb_draco_preset_src = str(pathlib.Path(__file__).parent) + '\\assets\\presets\\operator\\export_scene.gltf\\GLB_Draco_Preset.py'
        glb_draco_preset_dest = str(pathlib.Path(__file__).parents[2]) + '\\presets\\operator\\export_scene.gltf\\GLB_Draco_Preset.py'
        usd_preset_src = str(pathlib.Path(__file__).parent) + '\\assets\\presets\\operator\\wm.usd_export\\USDZ_Preset.py'
        usd_preset_dest = str(pathlib.Path(__file__).parents[2]) + '\\presets\\operator\\wm.usd_export\\USDZ_Preset.py'

        # Copy entire presets directory from addon directory to presets directory if there is no presets directory
        if not os.path.exists(gltf_presets_destination):
            shutil.copytree(gltf_presets_source, gltf_presets_destination)
        if not os.path.exists(usd_presets_destination):
            shutil.copytree(usd_presets_source, usd_presets_destination)

        # Copy individual preset files from addon directory to presets directory if presets directory exists without these specific presets.
        if not os.path.isfile(glb_preset_dest):
            shutil.copy(glb_preset_src, glb_preset_dest)
        if not os.path.isfile(glb_draco_preset_dest):
            shutil.copy(glb_draco_preset_src, glb_draco_preset_dest)
        if not os.path.isfile(usd_preset_dest):
            shutil.copy(usd_preset_src, usd_preset_dest)


    addon_location: EnumProperty(
        name="Addon Location",
        description="Where to put the Transmogrifier Addon UI",
        items=[
            ('TOPBAR', "Top Bar",
             "Place on Blender's Top Bar (Next to File, Edit, Render, Window, Help)"),
            ('3DHEADER', "3D Viewport Header",
             "Place in the 3D Viewport Header (Next to View, Select, Add, etc.)"),
            ('3DSIDE', "3D Viewport Side Panel (Transmogrifier Tab)",
             "Place in the 3D Viewport's right side panel, in the Transmogrifier Tab"),
        ],
        update=addon_location_updated,
    )

    copy_assets: BoolProperty(
        name="Copy assets to Preferences",
        default=False,
        description="Copy import/export presets and studiolights shipped with Transmogrifier to relevant Blender Preferences directories",
        update=copy_assets
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        # Display addon location options
        layout.prop(self, "addon_location")
        
        # Display copy assets button
        box = layout.box()
        col = box.column(align=True)
        col.prop(self, "copy_assets", text='Copy Assets to Preferences Directory', toggle=True, icon='DUPLICATE')


# Operator called when Transmogrifier preset is selected.
class REFRESHUI(Operator):
    """Refreshes Transmogrifier UI to reflect preset settings"""
    bl_idname = "refreshui.transmogrifier"
    bl_label = "Refresh UI"

    def execute(self, context):
        settings = context.scene.transmogrifier

        if settings.transmogrifier_preset != "NO_PRESET":
            # Load selected Transmogrifier preset as a dictionary.
            transmogrifier_preset_dict = load_transmogrifier_preset('transmogrifier', settings.transmogrifier_preset)

            # Read dictionary and change UI settings to reflect selected preset.
            for key, value in transmogrifier_preset_dict.items():
                # Make sure double-backslashes are preserved in directory path.
                directories_set = ("directory", "directory_output_custom", "textures_custom_dir")
                if key in directories_set and value != "":
                    value = "'" + repr(value) + "'"
                # Don't affect currently selected Transmogrifier preset
                elif key == "transmogrifier_preset":
                    continue
                # Wrap strings in quotations to ensure they're interpreted as strings in exec() function below.
                if type(value) == str:
                    if value == '':
                        value = "''"
                    else:
                        value = "'" + value + "'"
                # If a value is a list that contains strings, then change the list to a set.
                elif type(value) == list and type(value[0]) == str:
                    value = set(value)
                # If an integer object is an option of an EnumProperty drop down, make it a string.
                if key in ("texture_resolution", "resize_textures_limit") and type(value) == int:
                    value = "'" + str(value) + "'"   
                # Concatenate the current variable/setting to be updated.
                update_setting = 'settings.' + str(key) + ' = ' + str(value)
                # Make the setting (key) equal to the preset (value)
                exec(update_setting)

        return {'FINISHED'} 


class ADD_TRANSMOGRIFIER_PRESET(Operator):
    """Creates a Transmogrifier preset from current settings"""
    bl_idname = "transmogrifierpreset.add"
    bl_label = "Add Preset"

    preset_name: bpy.props.StringProperty(name="Name", default="")


    def execute(self, context):
        
        variables_dict = get_transmogrifier_settings(self, context)
        add_preset_name = self.preset_name
        json_file = os.path.join(str(bpy.utils.script_paths(subdir="presets\\operator\\transmogrifier")[0]), add_preset_name + ".json")
        write_json(variables_dict, json_file)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)
    
class REMOVE_TRANSMOGRIFIER_PRESET(Operator):
    """Removes currently selected Transmogrifier preset"""
    bl_idname = "transmogrifierpreset.remove"
    bl_label = "Remove Preset"


    def execute(self, context):
        
        settings = context.scene.transmogrifier
        remove_preset_name = settings.transmogrifier_preset_enum
        json_file = os.path.join(str(bpy.utils.script_paths(subdir="presets\\operator\\transmogrifier")[0]), remove_preset_name + ".json")

        if remove_preset_name != "NO_PRESET":
            os.remove(json_file)

        return {'FINISHED'}

# Operator called when pressing the Batch Convert button.
class TRANSMOGRIFY(Operator):
    """Batch converts 3D files and associated textures into other formats"""
    bl_idname = "transmogrifier.transmogrify"
    bl_label = "Batch Convert"
    file_count = 0

    def execute(self, context):
        settings = context.scene.transmogrifier
        
        # Refresh UI from preset if one is selected before writing new JSON and converting.
        # Turned off because it will delete any edits to settings before conversion even after preset has been selected and UI updated.
        # bpy.ops.refreshui.transmogrifier()

        base_dir = settings.directory
        if not bpy.path.abspath('//'):  # Then the blend file hasn't been saved
            # Then the path should be relative
            if base_dir != bpy.path.abspath(base_dir):
                self.report(
                    {'ERROR'}, "Save .blend file somewhere before importing models from a relative directory\n(or use an absolute directory)")
                return {'FINISHED'}
        base_dir = bpy.path.abspath(base_dir)  # convert to absolute path
        if not os.path.isdir(base_dir):
            self.report({'ERROR'}, "Conversion directory doesn't exist")
            return {'FINISHED'}


        # Create path to Converter.py
        converter_file = os.path.join(pathlib.Path(__file__).parent.resolve(), "Converter.py")


        self.file_count = 0


        self.export_selection(context, base_dir)


        if self.file_count == 0:
            self.report({'ERROR'}, "Could not convert.")
        else:
            converter_report_dict = read_json()
            conversion_count = converter_report_dict["conversion_count"]
            if conversion_count > 1:
                self.report({'INFO'}, "Conversion complete. " + str(conversion_count) + " files were converted.")
            elif conversion_count == 1:
                self.report({'INFO'}, "Conversion complete. " + str(conversion_count) + " file was converted.")
            else:
                self.report({'INFO'}, "Could not convert or no items needed conversion. " + str(conversion_count) + " files were converted.")

        return {'FINISHED'}

    def select_children_recursive(self, obj, context):
        for c in obj.children:
            if obj.type in context.scene.transmogrifier.texture_resolution_include:
                c.select_set(True)
            self.select_children_recursive(c, context)


    def export_selection(self, context, base_dir):
        settings = context.scene.transmogrifier

        # Create variables_dict dictionary from TransmogrifierSettings to pass to write_json function later.
        variables_dict = get_transmogrifier_settings(self, context)

        # Create path to StartConverter.cmd
        start_converter_file = os.path.join(pathlib.Path(__file__).parent.resolve(), "StartConverter.cmd")

        # Create path to blender.exe
        blender_dir = bpy.app.binary_path

        # Create path to Converter.py
        converter_file = os.path.join(pathlib.Path(__file__).parent.resolve(), "Converter.py")
        
        # Create path to Transmogrifier directory
        transmogrifier_dir = pathlib.Path(__file__).parent.resolve()

        # Assign user input to variables to be written to Converter_Variables.json
        import_file = settings.import_file
        directory_output_location = settings.directory_output_location
        directory_output_custom = settings.directory_output_custom
        use_subdirectories = settings.use_subdirectories
        copy_item_dir_contents = settings.copy_item_dir_contents
        model_quantity = settings.model_quantity
        export_file_1_scale = settings.export_file_1_scale
        export_file_2_scale = settings.export_file_2_scale
        prefix = settings.prefix
        suffix = settings.suffix
        set_data_names = settings.set_data_names
        set_UV_map_names = settings.set_UV_map_names
        use_textures = settings.use_textures
        regex_textures = settings.regex_textures

        textures_source = settings.textures_source
        textures_custom_dir = settings.textures_custom_dir
        if textures_source == "Custom":
            if not bpy.path.abspath('//'):  # Then the blend file hasn't been saved
                # Then the path should be relative
                if textures_custom_dir != bpy.path.abspath(textures_custom_dir):
                    self.report(
                        {'ERROR'}, "Save .blend file somewhere before importing textures from a relative, custom directory\n(or use an absolute directory)")
                    return {'FINISHED'}
            textures_custom_dir = bpy.path.abspath(textures_custom_dir)  # convert to absolute path
            if not os.path.isdir(textures_custom_dir):
                self.report({'ERROR'}, "Textures directory doesn't exist")
                return {'FINISHED'}

        copy_textures_custom_dir = settings.copy_textures_custom_dir
        replace_textures = settings.replace_textures
        if not copy_textures_custom_dir:  # If User initially elects to copy textures from custom directory and then to replace textures, but then decides not to copy textures, replace_textures is still True. Make it false.
            replace_textures = False
        keep_modified_textures = settings.keep_modified_textures
        texture_resolution = settings.texture_resolution
        texture_resolution_include = list(settings.texture_resolution_include)
        image_format = settings.image_format
        image_quality = settings.image_quality
        image_format_include = list(settings.image_format_include)
        set_transforms = settings.set_transforms
        set_transforms_filter = list(settings.set_transforms_filter)
        set_location = list(settings.set_location)
        set_rotation = list(settings.set_rotation)
        set_scale = list(settings.set_scale)
        apply_transforms = settings.apply_transforms
        apply_transforms_filter = list(settings.apply_transforms_filter)
        if not apply_transforms:
            apply_transforms_filter = []
        delete_animations = settings.delete_animations
        unit_system = settings.unit_system
        if unit_system == "METRIC":
            length_unit = settings.length_unit_metric
        elif unit_system == "IMPERIAL":
            length_unit = settings.length_unit_imperial
        elif unit_system == "NONE":
            length_unit = "NONE"
        auto_resize_files = settings.auto_resize_files
        file_size_maximum = settings.file_size_maximum
        file_size_methods = list(settings.file_size_methods)
        resize_textures_limit = int(settings.resize_textures_limit)
        decimate_limit = settings.decimate_limit
        save_preview_image = settings.save_preview_image
        save_blend = settings.save_blend
        save_conversion_log = settings.save_conversion_log


        # Import File Format

        if settings.import_file == "DAE":
            options = load_operator_preset(
                'wm.collada_import', settings.import_dae_preset)
            #bpy.ops.wm.collada_import(**options)
            import_file_command = "bpy.ops.wm.collada_import(**"
            
            
        elif settings.import_file == "ABC":
            options = load_operator_preset(
                'wm.alembic_import', settings.import_abc_preset)
            # options["start"] = settings.frame_start
            # options["end"] = settings.frame_end
            # By default, alembic_export operator runs in the background, this messes up batch
            # export though. alembic_export has an "as_background_job" arg that can be set to
            # false to disable it, but its marked deprecated, saying that if you EXECUTE the
            # operator rather than INVOKE it it runs in the foreground. Here I change the
            # execution context to EXEC_REGION_WIN.
            # docs.blender.org/api/current/bpy.ops.html?highlight=exec_default#execution-context
            #bpy.ops.wm.alembic_import('EXEC_REGION_WIN', **options)
            import_file_command = "bpy.ops.wm.alembic_import('EXEC_REGION_WIN', **"


        elif settings.import_file == "USD":
            options = load_operator_preset(
                'wm.usd_import', settings.import_usd_preset)
            #bpy.ops.wm.usd_import(**options)
            import_file_command = "bpy.ops.wm.usd_import(**"


        elif settings.import_file == "OBJ":
            options = load_operator_preset(
                'wm.obj_import', settings.import_obj_preset)
            #bpy.ops.wm.obj_import(**options)
            import_file_command = "bpy.ops.wm.obj_import(**"
            

        elif settings.import_file == "PLY":
            options = {
                'filepath': '',
            }
            # bpy.ops.import_mesh.ply(
            #     filepath="import_file", use_ascii=settings.ply_ascii, use_selection=True, use_mesh_modifiers=settings.apply_mods)
            import_file_command = "bpy.ops.import_mesh.ply(**"
            

        elif settings.import_file == "STL":
            # bpy.ops.import_mesh.stl(
            #     filepath="import_file", ascii=settings.stl_ascii, use_selection=True, use_mesh_modifiers=settings.apply_mods)
            options = {
                'filepath': '',
            }
            import_file_command = "bpy.ops.import_mesh.stl(**"


        elif settings.import_file == "FBX":
            options = load_operator_preset(
                'import_scene.fbx', settings.import_fbx_preset)
            import_file_command = "bpy.ops.import_scene.fbx(**"


        elif settings.import_file == "glTF":
            options = {
                'filepath': '',
            }
            #bpy.ops.import_scene.gltf(**options)
            import_file_command = "bpy.ops.import_scene.gltf(**"
            

        elif settings.import_file == "X3D":
            options = load_operator_preset(
                'import_scene.x3d', settings.import_x3d_preset)
            #bpy.ops.import_scene.x3d(**options)
            import_file_command = "bpy.ops.import_scene.x3d(**"


        
        # Set import variables to write to JSON
        
        # Set import file extension
        if settings.import_file == "glTF":
            import_file_ext = settings.import_gltf_extension
        elif settings.import_file == "USD":
            import_file_ext = settings.import_usd_extension
        else:
            import_file_ext = "." + settings.import_file.lower()
        
        
        # Set import file options
        import_file_options = options


        


        # Export File Format 1

        if settings.export_file_1 == "DAE":
            options = load_operator_preset(
                'wm.collada_export', settings.dae_preset)
            options["filepath"] = "export_file_1"
            options["selected"] = True
            options["apply_modifiers"] = settings.apply_mods
            #bpy.ops.wm.collada_export(**options)
            export_file_1_command = "bpy.ops.wm.collada_export(**"
            
            
        elif settings.export_file_1 == "ABC":
            options = load_operator_preset(
                'wm.alembic_export', settings.abc_preset)
            options["filepath"] = "export_file_1"
            options["selected"] = True
            options["start"] = settings.frame_start
            options["end"] = settings.frame_end
            # By default, alembic_export operator runs in the background, this messes up batch
            # export though. alembic_export has an "as_background_job" arg that can be set to
            # false to disable it, but its marked deprecated, saying that if you EXECUTE the
            # operator rather than INVOKE it it runs in the foreground. Here I change the
            # execution context to EXEC_REGION_WIN.
            # docs.blender.org/api/current/bpy.ops.html?highlight=exec_default#execution-context
            #bpy.ops.wm.alembic_export('EXEC_REGION_WIN', **options)
            export_file_1_command = "bpy.ops.wm.alembic_export('EXEC_REGION_WIN', **"


        elif settings.export_file_1 == "USD":
            options = load_operator_preset(
                'wm.usd_export', settings.usd_preset)
            options["filepath"] = "export_file_1"
            options["selected_objects_only"] = True
            #bpy.ops.wm.usd_export(**options)
            export_file_1_command = "bpy.ops.wm.usd_export(**"


        elif settings.export_file_1 == "SVG":
            options = {
                'filepath': '',
            }
            # bpy.ops.wm.gpencil_export_svg(
            #     filepath="export_file_1", selected_object_type='SELECTED')
            export_file_1_command = "bpy.ops.wm.gpencil_export_svg(**"


        elif settings.export_file_1 == "PDF":
            options = {
                'filepath': '',
            }
            # bpy.ops.wm.gpencil_export_pdf(
            #     filepath="export_file_1", selected_object_type='SELECTED')
            export_file_1_command = "bpy.ops.wm.gpencil_export_pdf(**"


        elif settings.export_file_1 == "OBJ":
            options = load_operator_preset(
                'wm.obj_export', settings.obj_preset)
            options["filepath"] = "export_file_1"
            options["export_selected_objects"] = True
            options["apply_modifiers"] = settings.apply_mods
            #bpy.ops.wm.obj_export(**options)
            export_file_1_command = "bpy.ops.wm.obj_export(**"
            

        elif settings.export_file_1 == "PLY":
            options = {
                'filepath': '',
            }
            # bpy.ops.export_mesh.ply(
            #     filepath="export_file_1", use_ascii=settings.ply_ascii, use_selection=True, use_mesh_modifiers=settings.apply_mods)
            export_file_1_command = "bpy.ops.export_mesh.ply(**"
            

        elif settings.export_file_1 == "STL":
            options = {
                'filepath': '',
            }
            # bpy.ops.export_mesh.stl(
            #     filepath="export_file_1", ascii=settings.stl_ascii, use_selection=True, use_mesh_modifiers=settings.apply_mods)
            export_file_1_command = "bpy.ops.export_mesh.stl(**"


        elif settings.export_file_1 == "FBX":
            options = load_operator_preset(
                'export_scene.fbx', settings.fbx_preset)
            options["filepath"] = "export_file_1"
            options["use_selection"] = True
            options["use_mesh_modifiers"] = settings.apply_mods
            #bpy.ops.export_scene.fbx(**options)
            export_file_1_command = "bpy.ops.export_scene.fbx(**"


        elif settings.export_file_1 == "glTF":
            options = load_operator_preset(
                'export_scene.gltf', settings.gltf_preset)
            options["filepath"] = "export_file_1"
            options["use_selection"] = True
            options["export_apply"] = settings.apply_mods
            #bpy.ops.export_scene.gltf(**options)
            export_file_1_command = "bpy.ops.export_scene.gltf(**"
            

        elif settings.export_file_1 == "X3D":
            options = load_operator_preset(
                'export_scene.x3d', settings.x3d_preset)
            options["filepath"] = "export_file_1"
            options["use_selection"] = True
            options["use_mesh_modifiers"] = settings.apply_mods
            #bpy.ops.export_scene.x3d(**options)
            export_file_1_command = "bpy.ops.export_scene.x3d(**"



        # Set export variables to write to JSON
        
        # Set export file 1 extension
        if settings.export_file_1 == "glTF":
            try:
                if options["export_format"] == 'GLB':
                    export_file_1_ext = ".glb"
                else:
                    export_file_1_ext = ".gltf"
            except:
                export_file_1_ext = ".glb"
        elif settings.export_file_1 == "USD":
            export_file_1_ext = settings.usd_extension
        else:
            export_file_1_ext = "." + settings.export_file_1.lower()
        
        # Set export file options
        export_file_1_options = options



        

        # Export File Format 2

        if settings.export_file_2 == "DAE":
            options = load_operator_preset(
                'wm.collada_export', settings.dae_preset)
            options["filepath"] = "export_file_2"
            options["selected"] = True
            options["apply_modifiers"] = settings.apply_mods
            #bpy.ops.wm.collada_export(**options)
            export_file_2_command = "bpy.ops.wm.collada_export(**"
            
            
        elif settings.export_file_2 == "ABC":
            options = load_operator_preset(
                'wm.alembic_export', settings.abc_preset)
            options["filepath"] = "export_file_2"
            options["selected"] = True
            options["start"] = settings.frame_start
            options["end"] = settings.frame_end
            # By default, alembic_export operator runs in the background, this messes up batch
            # export though. alembic_export has an "as_background_job" arg that can be set to
            # false to disable it, but its marked deprecated, saying that if you EXECUTE the
            # operator rather than INVOKE it it runs in the foreground. Here I change the
            # execution context to EXEC_REGION_WIN.
            # docs.blender.org/api/current/bpy.ops.html?highlight=exec_default#execution-context
            #bpy.ops.wm.alembic_export('EXEC_REGION_WIN', **options)
            export_file_2_command = "bpy.ops.wm.alembic_export('EXEC_REGION_WIN', **"


        elif settings.export_file_2 == "USD":
            options = load_operator_preset(
                'wm.usd_export', settings.usd_preset)
            options["filepath"] = "export_file_2"
            options["selected_objects_only"] = True
            #bpy.ops.wm.usd_export(**options)
            export_file_2_command = "bpy.ops.wm.usd_export(**"


        elif settings.export_file_2 == "SVG":
            options = {
                'filepath': '',
            }
            # bpy.ops.wm.gpencil_export_svg(
            #     filepath="export_file_2", selected_object_type='SELECTED')
            export_file_2_command = "bpy.ops.wm.gpencil_export_svg(**"


        elif settings.export_file_2 == "PDF":
            options = {
                'filepath': '',
            }
            # bpy.ops.wm.gpencil_export_pdf(
            #     filepath="export_file_2", selected_object_type='SELECTED')
            export_file_2_command = "bpy.ops.wm.gpencil_export_pdf(**"


        elif settings.export_file_2 == "OBJ":
            options = load_operator_preset(
                'wm.obj_export', settings.obj_preset)
            options["filepath"] = "export_file_2"
            options["export_selected_objects"] = True
            options["apply_modifiers"] = settings.apply_mods
            #bpy.ops.wm.obj_export(**options)
            export_file_2_command = "bpy.ops.wm.obj_export(**"
            

        elif settings.export_file_2 == "PLY":
            options = {
                'filepath': '',
            }
            # bpy.ops.export_mesh.ply(
            #     filepath="export_file_2", use_ascii=settings.ply_ascii, use_selection=True, use_mesh_modifiers=settings.apply_mods)
            export_file_2_command = "bpy.ops.export_mesh.ply(**"
            

        elif settings.export_file_2 == "STL":
            options = {
                'filepath': '',
            }
            # bpy.ops.export_mesh.stl(
            #     filepath="export_file_2", ascii=settings.stl_ascii, use_selection=True, use_mesh_modifiers=settings.apply_mods)
            export_file_2_command = "bpy.ops.export_mesh.stl(**"


        elif settings.export_file_2 == "FBX":
            options = load_operator_preset(
                'export_scene.fbx', settings.fbx_preset)
            options["filepath"] = "export_file_2"
            options["use_selection"] = True
            options["use_mesh_modifiers"] = settings.apply_mods
            #bpy.ops.export_scene.fbx(**options)
            export_file_2_command = "bpy.ops.export_scene.fbx(**"


        elif settings.export_file_2 == "glTF":
            options = load_operator_preset(
                'export_scene.gltf', settings.gltf_preset)
            options["filepath"] = "export_file_2"
            options["use_selection"] = True
            options["export_apply"] = settings.apply_mods
            #bpy.ops.export_scene.gltf(**options)
            export_file_2_command = "bpy.ops.export_scene.gltf(**"
            

        elif settings.export_file_2 == "X3D":
            options = load_operator_preset(
                'export_scene.x3d', settings.x3d_preset)
            options["filepath"] = "export_file_2"
            options["use_selection"] = True
            options["use_mesh_modifiers"] = settings.apply_mods
            #bpy.ops.export_scene.x3d(**options)
            export_file_2_command = "bpy.ops.export_scene.x3d(**"
       


        # Set export file 2 extension
        if settings.export_file_2 == "glTF":
            try:
                if options["export_format"] == 'GLB':
                    export_file_2_ext = ".glb"
                else:
                    export_file_2_ext = ".gltf"
            except:
                export_file_2_ext = ".glb"
        elif settings.export_file_2 == "USD":
            export_file_2_ext = settings.usd_extension
        else:
            export_file_2_ext = "." + settings.export_file_2.lower()
        
        # Set export file options
        export_file_2_options = options

        # Update variables_dict with additional import/export options
        additional_settings_dict = {
            "import_file_ext": import_file_ext,
            "import_file_command": import_file_command, 
            "import_file_options": import_file_options, 
            "export_file_1_ext": export_file_1_ext, 
            "export_file_1_command": export_file_1_command, 
            "export_file_1_options": export_file_1_options, 
            "export_file_2_ext": export_file_2_ext, 
            "export_file_2_command": export_file_2_command, 
            "export_file_2_options": export_file_2_options, 
            "length_unit": length_unit
        }
        variables_dict.update(additional_settings_dict)

        # Write variables to JSON file before running converter
        json_file = os.path.join(pathlib.Path(__file__).parent.resolve(), "Converter_Variables.json")
        write_json(variables_dict, json_file)

        # Run Converter.py
        # subprocess.call(start_converter_file, creationflags=subprocess.CREATE_NEW_CONSOLE) # Use for troubleshooting purposes
        subprocess.call(
            [
                blender_dir,
                "Converter.blend",
                "--python",
                "Converter.py",
            ],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            cwd=transmogrifier_dir
        ) 
        
        

        print("Conversion Complete")
        self.file_count += 1


# Groups together all the addon settings that are saved in each .blend file
class TransmogrifierSettings(PropertyGroup):
    # Import Settings
    directory: StringProperty(
        name="Directory",
        description="Parent directory to search through and import files\nDefault of // will import from the same directory as the blend file (only works if the blend file is saved)",
        default="//",
        subtype='DIR_PATH',
    )
    import_file: EnumProperty(
        name="Format",
        description="Which file format to import",
        items=[
            ("DAE", "Collada (.dae)", "", 1),
            ("ABC", "Alembic (.abc)", "", 9),
            ("USD", "Universal Scene Description (.usd/.usdc/.usda/.usdz)", "", 2),
            ("OBJ", "Wavefront (.obj)", "", 7),
            ("PLY", "Stanford (.ply)", "", 3),
            ("STL", "STL (.stl)", "", 4),
            ("FBX", "FBX (.fbx)", "", 5),
            ("glTF", "glTF (.glb/.gltf)", "", 6),
            ("X3D", "X3D Extensible 3D (.x3d)", "", 8),
        ],
        default="FBX",
    )
    # Import Format specific options:
    import_usd_extension: EnumProperty(
        name="Extension",
        description="Which type of USD to import",
        items=[
            (".usd", "Plain (.usd)",
             "Can be either binary or ASCII\nIn Blender this imports to binary", 1),
            (".usdc", "Binary Crate (default) (.usdc)",
             "Binary, fast, hard to edit", 2),
            (".usda", "ASCII (.usda)", "ASCII Text, slow, easy to edit", 3),
            (".usdz", "Zipped (.usdz)", "Packs textures and references into one file", 4),
        ],
        default=".usdz",
    )
    import_gltf_extension: EnumProperty(
        name="Extension",
        description="Which type of glTF to import",
        items=[
            (".glb", "glTF Binary (.glb)", "", 1),
            (".gltf", "glTF Embedded or Separate (.gltf)", "", 2),
        ],
        default=".glb"
    )
    ply_ascii: BoolProperty(name="ASCII Format", default=False)
    stl_ascii: BoolProperty(name="ASCII Format", default=False)

    # Presets: A string property for saving your option (without new presets changing your choice), and enum property for choosing
    import_abc_preset: StringProperty(default='NO_PRESET')
    import_abc_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use import settings from a preset.\n(Create in the import settings from the File > import > Alembic (.abc))",
        items=lambda self, context: get_operator_presets('wm.alembic_import'),
        get=lambda self: get_preset_index(
            'wm.alembic_import', self.import_abc_preset),
        set=lambda self, value: setattr(
            self, 'import_abc_preset', preset_enum_items_refs['wm.alembic_import'][value][0]),
    )
    import_dae_preset: StringProperty(default='NO_PRESET')
    import_dae_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use import settings from a preset.\n(Create in the import settings from the File > import > Collada (.dae))",
        items=lambda self, context: get_operator_presets('wm.collada_import'),
        get=lambda self: get_preset_index(
            'wm.collada_import', self.import_dae_preset),
        set=lambda self, value: setattr(
            self, 'import_dae_preset', preset_enum_items_refs['wm.collada_import'][value][0]),
    )
    import_usd_preset: StringProperty(default='NO_PRESET')
    import_usd_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use import settings from a preset.\n(Create in the import settings from the File > import > Universal Scene Description (.usd, .usdc, .usda, .usdz))",
        items=lambda self, context: get_operator_presets('wm.usd_import'),
        get=lambda self: get_preset_index('wm.usd_import', self.import_usd_preset),
        set=lambda self, value: setattr(
            self, 'import_usd_preset', preset_enum_items_refs['wm.usd_import'][value][0]),
    )
    import_obj_preset: StringProperty(default='NO_PRESET')
    import_obj_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use import settings from a preset.\n(Create in the import settings from the File > import > Wavefront (.obj))",
        items=lambda self, context: get_operator_presets('wm.obj_import'),
        get=lambda self: get_preset_index('wm.obj_import', self.import_obj_preset),
        set=lambda self, value: setattr(
            self, 'import_obj_preset', preset_enum_items_refs['wm.obj_import'][value][0]),
    )
    import_fbx_preset: StringProperty(default='NO_PRESET')
    import_fbx_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use import settings from a preset.\n(Create in the import settings from the File > import > FBX (.fbx))",
        items=lambda self, context: get_operator_presets('import_scene.fbx'),
        get=lambda self: get_preset_index('import_scene.fbx', self.import_fbx_preset),
        set=lambda self, value: setattr(
            self, 'import_fbx_preset', preset_enum_items_refs['import_scene.fbx'][value][0]),
    )
    import_gltf_preset: StringProperty(default='NO_PRESET')
    import_gltf_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use import settings from a preset.\n(Create in the import settings from the File > import > glTF (.glb/.gltf))",
        items=lambda self, context: get_operator_presets('import_scene.gltf'),
        get=lambda self: get_preset_index(
            'import_scene.gltf', self.import_gltf_preset),
        set=lambda self, value: setattr(
            self, 'import_gltf_preset', preset_enum_items_refs['import_scene.gltf'][value][0]),
    )
    import_x3d_preset: StringProperty(default='NO_PRESET')
    import_x3d_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use import settings from a preset.\n(Create in the import settings from the File > import > X3D Extensible 3D (.x3d))",
        items=lambda self, context: get_operator_presets('import_scene.x3d'),
        get=lambda self: get_preset_index('import_scene.x3d', self.import_x3d_preset),
        set=lambda self, value: setattr(
            self, 'import_x3d_preset', preset_enum_items_refs['import_scene.x3d'][value][0]),
    )



    # Preset Settings:
    # Option to select Transmogrifier presets
    transmogrifier_preset: StringProperty(default='NO_PRESET')
    transmogrifier_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use batch conversion settings from a preset.\n(Create by clicking '+' after adjusting settings in the Transmogrifier menu)",
        items=lambda self, context: get_transmogrifier_presets('transmogrifier'),
        get=lambda self: get_transmogrifier_preset_index(
            'transmogrifier', self.transmogrifier_preset),
        set=lambda self, value: setattr(
            self, 'transmogrifier_preset', transmogrifier_preset_enum_items_refs['transmogrifier'][value][0]),
        update=refresh_ui
    )

    # Export Settings:
    # Option for to where models should be exported.
    directory_output_location: EnumProperty(
        name="Location(s)",
        description="Select where models should be exported.",
        items=[
            ("Adjacents", "Adjacents", "Export each converted model to the same directory from which it was imported", 1),
            ("Custom", "Custom", "Export each converted model to a custom directory", 2),
        ],
        default="Adjacents",
    )
    # Custom export directory
    directory_output_custom: StringProperty(
        name="Directory",
        description="Set a custom directory to which each converted model will be exported\nDefault of // will export to same directory as the blend file (only works if the blend file is saved)",
        default="//",
        subtype='DIR_PATH',
    )
    # Option to export models to subdirectories in custom directory
    use_subdirectories: BoolProperty(
        name="Subdirectories",
        description="Export models to their own subdirectories within the parent output custom directory",
        default=False,
    )
    # Option to include only models or also copy original folder contents to custom directory
    copy_item_dir_contents: BoolProperty(
        name="Copy Original Contents",
        description="Include original contents of each item's directory to its custom subdirectory",
        default=False,
    )
    # Option for how many models to export at a time.
    model_quantity: EnumProperty(
        name="Quantity",
        description="Choose whether to export one, two, or no model formats at a time",
        items=[
            ("1 Format", "1 Format", "Export one 3D model format for every model imported", 1),
            ("2 Formats", "2 Formats", "Export two 3D model formats for every model imported", 2),
            ("No Formats", "No Formats", "Don't export any 3D models (Useful if only batch texture conversion is desired)", 3),
        ],
        default="1 Format",
    )
    prefix: StringProperty(
        name="Prefix",
        description="Text to put at the beginning of all the exported file names",
    )
    suffix: StringProperty(
        name="Suffix",
        description="Text to put at the end of all the exported file names",
    )
    # Set data names from object names.
    set_data_names: BoolProperty(
        name="Data Names from Objects",
        description="Rename object data names according to their corresponding object names",
        default=True,
    )
    # Set all UV map names to "UVMap". This prevents a material issue with USDZ's - when object A and object B share the same material, but their UV
    # map names differ, the material has to pick one UVMap in the UV Map node inputs connected to each texture channel. So if object A's UV map is called
    # "UVMap" but object B's UV map is called "UV_Channel", then the shared material may pick "UV_Channel" as the UV inputs, thus causing object A to appear
    # untextured despite the fact that it shares the same material as object B.
    set_UV_map_names: BoolProperty(
        name="Rename UV Maps",
        description="Set all UV Map names to 'UVMap'. Multiple UV maps within the same object will increment as 'UVMap', 'UVMap_1', 'UVMap_2', and so on. This prevents an issue in USD formats when two or more objects share the same material but have different UV map names, which causes some objects to appear untextured",
        default=True,
    )
    use_textures: BoolProperty(
        name="Use Textures", 
        description="Texture models with images from a selected source",
        default=True,
    )
    regex_textures: BoolProperty(
        name="Regex Textures", 
        description="Use regex to correct misspellings and inconsistencies in texture PBR names. This helps to guarantee their detection and import by Transmogrifier",
        default=True,
    )
    textures_source: EnumProperty(
        name="Source", 
        description="Set the source of textures to be used",
        items=[
            ("External", "External", "Use textures nearby the imported model\n(Texture sets can exist in either 1) the same directory as the imported model, 2) a 'textures' subdirectory, or 3) texture set subdirectories within a 'textures' subdirectory)", 'FILE_FOLDER', 1),
            ("Packed", "Packed", "Use textures packed into each imported model", 'PACKAGE', 2),
            ("Custom", "Custom", "Use textures from a specific location for all models", 'NEWFOLDER', 3),
        ],
        default="External",
    )
    textures_custom_dir: StringProperty(
        name="Directory",
        description="Custom folder from which textures will be imported and applied to all converted objects",
        default="//",
        subtype='DIR_PATH',
    )
    copy_textures_custom_dir: BoolProperty(
        name="Copy to Model Folders", 
        description="Copy textures from custom directory to every folder from which a model is imported",
        default=False,
    )
    replace_textures: BoolProperty(
        name="Replace Textures", 
        description="Replace any existing textures folders with textures from custom directory",
        default=False,
    )
    keep_modified_textures: BoolProperty(
        name="Keep Modified Textures", 
        description="Don't delete the textures directory used to modify image textures by regex and resolution and/or format",
        default=False,
    )
    texture_resolution: EnumProperty(
        name="Resolution",
        description="Set a custom image texture resolution for exported models without affecting resolution of original/source texture files",
        items=[
            ("Default", "Default", "Don't resize, use imported resolution", 1),
            ("8192", "8192", "Square aspect ratio", 2),
            ("4096", "4096", "Square aspect ratio", 3),
            ("2048", "2048", "Square aspect ratio", 4),
            ("1024", "1024", "Square aspect ratio", 5),
            ("512", "512", "Square aspect ratio", 6),
            ("256", "256", "Square aspect ratio", 7),
            ("128", "128", "Square aspect ratio", 8),
        ],
        default="Default",
    )
    # Which textures to include in resizing.
    texture_resolution_include: EnumProperty(
        name="Included Textures",
        options={'ENUM_FLAG'},
        items=[
            ('BaseColor', "BaseColor", "", 1),
            ('Subsurface', "Subsurface", "", 2),
            ('Metallic', "Metallic", "", 4),
            ('Specular', "Specular", "", 16),
            ('Roughness', "Roughness", "", 32),
            ('Normal', "Normal", "", 64),
            ('Bump', "Bump", "", 128),
            ('Displacement', "Displacement", "", 256),
            ('Emission', "Emission", "", 512),
            ('Opacity', "Opacity", "", 1024),
            ('Ambient_Occlusion', "Ambient_Occlusion", "", 2048),
        ],
        description="Filter texture maps to resize",
        default={
            'BaseColor', 
            'Subsurface', 
            'Metallic', 
            'Specular', 
            'Roughness', 
            'Normal', 
            'Bump', 
            'Displacement', 
            'Emission', 
            'Opacity', 
            'Ambient_Occlusion'
        },
    )
    image_format: EnumProperty(
        name="Format",
        description="Set a custom texture image type for exported models without affecting resolution of original/source texture files",
        items=[
            ("Default", "Default", "Don't convert image textures", 1),
            ("PNG", "PNG", "Save image textures in PNG format", 2),
            ("JPEG", "JPEG", "Save image textures in JPEG format", 3),
            ("TARGA", "TARGA", "Save image textures in TARGA format", 4),
            ("TIFF", "TIFF", "Save image textures in TIFF format", 5),
            ("WEBP", "WEBP", "Save image textures in WEBP format", 6),
            ("BMP", "BMP", "Save image textures in BMP format", 7),
            # ("OPEN_EXR", "OPEN_EXR", "Save image textures in OPEN_EXR format", 8),
            # ("JPEG2000", "JPEG2000", "Save image textures in JPEG2000 format", 9),
            # ("CINEON", "CINEON", "Save image textures in CINEON format", 10),
            # ("DPX", "DPX", "Save image textures in DPX format", 11),
            # ("HDR", "HDR", "Save image textures in HDR format", 12),
        ],
        default="Default",
    )
    image_quality: IntProperty(
        name="Quality", 
        description="(%) Quality for image formats that support lossy compression",
        default=90,
        soft_min=0,
        soft_max=100,
        step=5,
    )
    # Which textures to include in converting.
    image_format_include: EnumProperty(
        name="Included Textures",
        options={'ENUM_FLAG'},
        items=[
            ('BaseColor', "BaseColor", "", 1),
            ('Subsurface', "Subsurface", "", 2),
            ('Metallic', "Metallic", "", 4),
            ('Specular', "Specular", "", 16),
            ('Roughness', "Roughness", "", 32),
            ('Normal', "Normal", "", 64),
            ('Bump', "Bump", "", 128),
            ('Displacement', "Displacement", "", 256),
            ('Emission', "Emission", "", 512),
            ('Opacity', "Opacity", "", 1024),
            ('Ambient_Occlusion', "Ambient_Occlusion", "", 2048),
        ],
        description="Filter texture maps to convert",
        default={
            'BaseColor', 
            'Subsurface', 
            'Metallic', 
            'Specular', 
            'Roughness', 
            'Normal', 
            'Bump', 
            'Displacement', 
            'Emission', 
            'Opacity', 
            'Ambient_Occlusion'
        },
    )
    # # Option to set custom transformations
    set_transforms: BoolProperty(
        name="Set", 
        description="Set custom transformations of the imported object(s) before exporting", 
        default=False
    )
    # Option to set custom transformations.
    set_transforms_filter: EnumProperty(
        name="Filter",
        options={'ENUM_FLAG'},
        items=[
            ('Location', "Location", "", 1),
            ('Rotation', "Rotation", "", 2),
            ('Scale', "Scale", "", 4),
        ],
        description="Filter transforms to set",
        default={
            'Location', 
            'Rotation', 
            'Scale', 
        },
    )
    # Set location amount.
    set_location: FloatVectorProperty(
        name="Location", 
        default=(0.0, 0.0, 0.0), 
        subtype="TRANSLATION"
    )
    # Set rotation amount.
    set_rotation: FloatVectorProperty(
        name="Rotation (XYZ Euler)", 
        default=(0.0, 0.0, 0.0), 
        subtype="EULER"
    )
    # Set scale amount.
    set_scale: FloatVectorProperty(
        name="Scale", 
        default=(1.0, 1.0, 1.0), 
        subtype="XYZ"
    )
    # Apply transformations.
    apply_transforms: BoolProperty(
        name="Apply", 
        description="Apply all transformations on all objects",
        default=True,
    )
    # Filter what transforms to apply.
    apply_transforms_filter: EnumProperty(
        name="Filter",
        options={'ENUM_FLAG'},
        items=[
            ('Location', "Location", "", 1),
            ('Rotation', "Rotation", "", 2),
            ('Scale', "Scale", "", 4),
        ],
        description="Filter transforms to apply during conversion",
        default={
            'Location', 
            'Rotation', 
            'Scale', 
        },
    )
    # Clear animation data.
    delete_animations: BoolProperty(
        name="Delete", 
        description="Remove all animation data from all objects",
        default=True,
    )
    # Set unit system:
    unit_system: EnumProperty(
        name="Unit System",
        description="Set the unit system to use for export",
        items=[
            ("METRIC", "Metric", "", 1),
            ("IMPERIAL", "Imperial", "", 2),
            ("NONE", "None", "", 3),
        ],
        default="METRIC",
    )
    # Set length unit if metric system was selected.
    length_unit_metric: EnumProperty(
        name="Length",
        description="Set the length unit to use for export",
        items=[
            ("ADAPTIVE", "Adaptive", "", 1),
            ("KILOMETERS", "Kilometers", "", 2),
            ("METERS", "Meters", "", 3),
            ("CENTIMETERS", "Centimeters", "", 4),
            ("MILLIMETERS", "Millimeters", "", 5),
            ("MICROMETERS", "Micrometers", "", 6),
        ],
        default="CENTIMETERS",
    )
    # Set length unit if imperial system was selected.
    length_unit_imperial: EnumProperty(
        name="Length",
        description="Set the length unit to use for export",
        items=[
            ("ADAPTIVE", "Adaptive", "", 1),
            ("MILES", "Miles", "", 2),
            ("FEET", "Feet", "", 3),
            ("INCHES", "Inches", "", 4),
            ("THOU", "Thousandths", "", 5),
        ],
        default="INCHES",
    )
    # Option to set file size maximum.
    auto_resize_files: EnumProperty(
        name="Auto Resize",
        description="Set a maximum file size and Transmogrifier will automatically try to resize the file according to the requested size. Only takes the first file format into account",
        items=[
            ("All", "All", "Convert all specified files in the given directory even if some previously exported files are already below the target maximum", 1),
            ("Only Above Max", "Only Above Max", "Only convert such specified files in the given directory that are still above the target maximum. Ignore the rest already below the target maximum", 2),
            ("None", "None", "Don't auto-resize any exported files", 3),
        ],
        default="All",
    )
    # File size maximum target.
    file_size_maximum: bpy.props.FloatProperty(
        name="Max. File Size (MB)", 
        description="Set the target maximum to which Transmogrifier should attempt to lower the file size (Megabytes)",
        default=15.0,
        soft_min=0.0,
        soft_max=1000.0,
        step=10,
    )
    # Filter file size reduction methods.
    file_size_methods: EnumProperty(
        name="File Size Methods",
        options={'ENUM_FLAG'},
        items=[
            ('Draco-Compress', "Draco-Compress", "(Only for GLB export). Try Draco-compression to lower the exported file size.", 'FULLSCREEN_EXIT', 1),
            ('Resize Textures', "Resize Textures", "Try resizing textures to lower the exported file size.", 'NODE_TEXTURE', 2),
            ('Reformat Textures', "Reformat Textures", "Try reformatting all textures except the normal map to JPEG's to lower the exported file size.", 'IMAGE_DATA', 4),
            ('Decimate Meshes', "Decimate Meshes", "Try decimating objects to lower the exported file size.", 'MOD_DECIM', 16),
        ],
        description="Filter file size reduction methods to use for automatic export file size reduction",
        default={
            'Resize Textures', 
            'Reformat Textures', 
            'Draco-Compress', 
        },
    )
    # Limit resolution that auto resize files should not go below.
    resize_textures_limit: EnumProperty(
        name="Min. Resolution",
        description="Set minimum image texture resolution for auto file size not to go below. Images will not be upscaled",
        items=[
            ("8192", "8192", "Square aspect ratio", 1),
            ("4096", "4096", "Square aspect ratio", 2),
            ("2048", "2048", "Square aspect ratio", 3),
            ("1024", "1024", "Square aspect ratio", 4),
            ("512", "512", "Square aspect ratio", 5),
            ("256", "256", "Square aspect ratio", 6),
            ("128", "128", "Square aspect ratio", 7),
        ],
        default="512",
    )
    # Limit how many time a mesh can be decimated during auto resize files.
    decimate_limit: IntProperty(
        name="Decimate Max.", 
        description="Limit the number of times an item can be decimated. Items will be decimated by 50% each time",
        default=3,
        soft_min=0,
        soft_max=10,
        step=1,
    )
    # Save preview image.
    save_preview_image: BoolProperty(
        name="Render Preview",
        description="Save preview image thumbnails for every model",
        default=True,
        )
    # Save .blend file.
    save_blend: BoolProperty(
        name="Save .blend",
        description="Save a Blender file for every model. This can help troubleshoot conversion errors",
        default=False,
        )
    # Save conversion log.
    save_conversion_log: BoolProperty(
        name="Save Log",
        description="Save a log of the batch conversion in the given directory. This can help troubleshoot conversion errors",
        default=False,
        )
    # Export Settings 1:
    export_file_1: EnumProperty(
        name="Format",
        description="Which file format to export to",
        items=[
            ("DAE", "Collada (.dae)", "", 1),
            ("ABC", "Alembic (.abc)", "", 9),
            ("USD", "Universal Scene Description (.usd/.usdc/.usda/.usdz)", "", 2),
            # ("SVG", "Grease Pencil as SVG (.svg)", "", 10),
            # ("PDF", "Grease Pencil as PDF (.pdf)", "", 11),
            ("OBJ", "Wavefront (.obj)", "", 7),
            ("PLY", "Stanford (.ply)", "", 3),
            ("STL", "STL (.stl)", "", 4),
            ("FBX", "FBX (.fbx)", "", 5),
            ("glTF", "glTF (.glb/.gltf)", "", 6),
            ("X3D", "X3D Extensible 3D (.x3d)", "", 8),
        ],
        default="glTF",
    )
    # File 1 scale.
    export_file_1_scale: bpy.props.FloatProperty(
        name="Scale", 
        description="Set the scale of the model before exporting",
        default=1.0,
        soft_min=0.0,
        soft_max=10000.0,
        step=500,
    )
    # Export Settings 2:
    export_file_2: EnumProperty(
        name="Format",
        description="Which file format to export to",
        items=[
            ("DAE", "Collada (.dae)", "", 1),
            ("ABC", "Alembic (.abc)", "", 9),
            ("USD", "Universal Scene Description (.usd/.usdc/.usda/.usdz)", "", 2),
            # ("SVG", "Grease Pencil as SVG (.svg)", "", 10),
            # ("PDF", "Grease Pencil as PDF (.pdf)", "", 11),
            ("OBJ", "Wavefront (.obj)", "", 7),
            ("PLY", "Stanford (.ply)", "", 3),
            ("STL", "STL (.stl)", "", 4),
            ("FBX", "FBX (.fbx)", "", 5),
            ("glTF", "glTF (.glb/.gltf)", "", 6),
            ("X3D", "X3D Extensible 3D (.x3d)", "", 8),
        ],
        default="USD",
    )
    # File 2 scale.
    export_file_2_scale: bpy.props.FloatProperty(
        name="Scale", 
        description="Set the scale of the model before exporting",
        default=1.0,
        soft_min=0.0,
        soft_max=10000.0,
        step=500,
    )
    # Export format specific options:
    usd_extension: EnumProperty(
        name="Extension",
        items=[
            (".usd", "Plain (.usd)",
             "Can be either binary or ASCII\nIn Blender this exports to binary", 1),
            (".usdc", "Binary Crate (default) (.usdc)",
             "Binary, fast, hard to edit", 2),
            (".usda", "ASCII (.usda)", "ASCII Text, slow, easy to edit", 3),
            (".usdz", "Zipped (.usdz)", "Packs textures and references into one file", 4),
        ],
        default=".usdz",
    )
    ply_ascii: BoolProperty(name="ASCII Format", default=False)
    stl_ascii: BoolProperty(name="ASCII Format", default=False)

    # Presets: A string property for saving your option (without new presets changing your choice), and enum property for choosing
    abc_preset: StringProperty(default='NO_PRESET')
    abc_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > Alembic (.abc))",
        items=lambda self, context: get_operator_presets('wm.alembic_export'),
        get=lambda self: get_preset_index(
            'wm.alembic_export', self.abc_preset),
        set=lambda self, value: setattr(
            self, 'abc_preset', preset_enum_items_refs['wm.alembic_export'][value][0]),
    )
    dae_preset: StringProperty(default='NO_PRESET')
    dae_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > Collada (.dae))",
        items=lambda self, context: get_operator_presets('wm.collada_export'),
        get=lambda self: get_preset_index(
            'wm.collada_export', self.dae_preset),
        set=lambda self, value: setattr(
            self, 'dae_preset', preset_enum_items_refs['wm.collada_export'][value][0]),
    )
    usd_preset: StringProperty(default='USDZ_Preset')
    usd_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > Universal Scene Description (.usd, .usdc, .usda, .usdz))",
        items=lambda self, context: get_operator_presets('wm.usd_export'),
        get=lambda self: get_preset_index('wm.usd_export', self.usd_preset),
        set=lambda self, value: setattr(
            self, 'usd_preset', preset_enum_items_refs['wm.usd_export'][value][0]),
    )
    obj_preset: StringProperty(default='NO_PRESET')
    obj_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > Wavefront (.obj))",
        items=lambda self, context: get_operator_presets('wm.obj_export'),
        get=lambda self: get_preset_index('wm.obj_export', self.obj_preset),
        set=lambda self, value: setattr(
            self, 'obj_preset', preset_enum_items_refs['wm.obj_export'][value][0]),
    )
    fbx_preset: StringProperty(default='NO_PRESET')
    fbx_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > FBX (.fbx))",
        items=lambda self, context: get_operator_presets('export_scene.fbx'),
        get=lambda self: get_preset_index('export_scene.fbx', self.fbx_preset),
        set=lambda self, value: setattr(
            self, 'fbx_preset', preset_enum_items_refs['export_scene.fbx'][value][0]),
    )
    gltf_preset: StringProperty(default='GLB_Preset')
    gltf_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > glTF (.glb/.gltf))",
        items=lambda self, context: get_operator_presets('export_scene.gltf'),
        get=lambda self: get_preset_index(
            'export_scene.gltf', self.gltf_preset),
        set=lambda self, value: setattr(
            self, 'gltf_preset', preset_enum_items_refs['export_scene.gltf'][value][0]),
    )
    x3d_preset: StringProperty(default='NO_PRESET')
    x3d_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > X3D Extensible 3D (.x3d))",
        items=lambda self, context: get_operator_presets('export_scene.x3d'),
        get=lambda self: get_preset_index('export_scene.x3d', self.x3d_preset),
        set=lambda self, value: setattr(
            self, 'x3d_preset', preset_enum_items_refs['export_scene.x3d'][value][0]),
    )

    apply_mods: BoolProperty(
        name="Apply Modifiers",
        description="Should the modifiers by applied onto the exported mesh?\nCan't export Shape Keys with this on",
        default=True,
    )
    frame_start: IntProperty(
        name="Frame Start",
        min=0,
        description="First frame to export",
        default = 1,
    )
    frame_end: IntProperty(
        name="Frame End",
        min=0,
        description="Last frame to export",
        default = 1,
    )


def register():
    # Register classes
    bpy.utils.register_class(TransmogrifierPreferences)
    bpy.utils.register_class(TransmogrifierSettings)
    bpy.utils.register_class(POPOVER_PT_transmogrify)
    bpy.utils.register_class(REFRESHUI)
    bpy.utils.register_class(ADD_TRANSMOGRIFIER_PRESET)
    bpy.utils.register_class(REMOVE_TRANSMOGRIFIER_PRESET)
    bpy.utils.register_class(TRANSMOGRIFY)

    # Add Batch Convert settings to Scene type
    bpy.types.Scene.transmogrifier = PointerProperty(type=TransmogrifierSettings)

    # Show addon UI
    prefs = bpy.context.preferences.addons[__name__].preferences
    if prefs.addon_location == 'TOPBAR':
        bpy.types.TOPBAR_MT_editor_menus.append(draw_popover)
    if prefs.addon_location == '3DHEADER':
        bpy.types.VIEW3D_MT_editor_menus.append(draw_popover)
    elif prefs.addon_location == '3DSIDE':
        bpy.utils.register_class(VIEW3D_PT_transmogrify)


def unregister():
    # Delete the settings from Scene type (Doesn't actually remove existing ones from scenes)
    del bpy.types.Scene.transmogrifier

    # Unregister Classes
    bpy.utils.unregister_class(TransmogrifierPreferences)
    bpy.utils.unregister_class(TransmogrifierSettings)
    bpy.utils.unregister_class(POPOVER_PT_transmogrify)
    bpy.utils.unregister_class(REFRESHUI)
    bpy.utils.unregister_class(ADD_TRANSMOGRIFIER_PRESET)
    bpy.utils.unregister_class(REMOVE_TRANSMOGRIFIER_PRESET)
    bpy.utils.unregister_class(TRANSMOGRIFY)

    # Remove UI
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_popover)
    bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)
    if hasattr(bpy.types, "VIEW3D_PT_transmogrify"):
        bpy.utils.unregister_class(VIEW3D_PT_transmogrify)


if __name__ == '__main__':
    register()
