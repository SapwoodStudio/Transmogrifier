#  █████       █████   █████████  ██████████ ██████   █████  █████████  ██████████
# ░░███       ░░███   ███░░░░░███░░███░░░░░█░░██████ ░░███  ███░░░░░███░░███░░░░░█
#  ░███        ░███  ███     ░░░  ░███  █ ░  ░███░███ ░███ ░███    ░░░  ░███  █ ░ 
#  ░███        ░███ ░███          ░██████    ░███░░███░███ ░░█████████  ░██████   
#  ░███        ░███ ░███          ░███░░█    ░███ ░░██████  ░░░░░░░░███ ░███░░█   
#  ░███      █ ░███ ░░███     ███ ░███ ░   █ ░███  ░░█████  ███    ░███ ░███ ░   █
#  ███████████ █████ ░░█████████  ██████████ █████  ░░█████░░█████████  ██████████
# ░░░░░░░░░░░ ░░░░░   ░░░░░░░░░  ░░░░░░░░░░ ░░░░░    ░░░░░  ░░░░░░░░░  ░░░░░░░░░░ 

##### BEGIN GPL LICENSE BLOCK #####

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 

##### END GPL LICENSE BLOCK #####



#  █████       █████ ███████████  ███████████     █████████   ███████████   █████ ██████████  █████████ 
# ░░███       ░░███ ░░███░░░░░███░░███░░░░░███   ███░░░░░███ ░░███░░░░░███ ░░███ ░░███░░░░░█ ███░░░░░███
#  ░███        ░███  ░███    ░███ ░███    ░███  ░███    ░███  ░███    ░███  ░███  ░███  █ ░ ░███    ░░░ 
#  ░███        ░███  ░██████████  ░██████████   ░███████████  ░██████████   ░███  ░██████   ░░█████████ 
#  ░███        ░███  ░███░░░░░███ ░███░░░░░███  ░███░░░░░███  ░███░░░░░███  ░███  ░███░░█    ░░░░░░░░███
#  ░███      █ ░███  ░███    ░███ ░███    ░███  ░███    ░███  ░███    ░███  ░███  ░███ ░   █ ███    ░███
#  ███████████ █████ ███████████  █████   █████ █████   █████ █████   █████ █████ ██████████░░█████████ 
# ░░░░░░░░░░░ ░░░░░ ░░░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░   ░░░░░ ░░░░░   ░░░░░ ░░░░░ ░░░░░░░░░░  ░░░░░░░░░  


import bpy
from bpy.types import (
    AddonPreferences, 
    Panel,
    Operator, 
) 
from bpy.props import (
    IntProperty,
    EnumProperty,
    StringProperty,
)
from pathlib import Path
from bpy.utils import previews
from . import bl_info
from . import Functions



#  █████  █████ █████
# ░░███  ░░███ ░░███ 
#  ░███   ░███  ░███ 
#  ░███   ░███  ░███ 
#  ░███   ░███  ░███ 
#  ░███   ░███  ░███ 
#  ░░████████   █████
#   ░░░░░░░░   ░░░░░ 


# Draws the .blend file specific settings used in the
# Popover panel or Side Panel panel
def draw_settings_general(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    imports = bpy.context.scene.transmogrifier_imports
    exports = bpy.context.scene.transmogrifier_exports

    separator_factor = 0.25
    self.layout.use_property_split = True
    self.layout.use_property_decorate = False

    # Display combination of title and version from bl_info.
    version = ''
    for num in bl_info["version"]:
        version = version + "." + str(num)
    version = version.lstrip(".")
    title = bl_info["name"] + " " + version
    row = self.layout.row(align=False)
    row.label(text=title)
    row.prop(settings, 'logging_save_summary', text='', icon="SPREADSHEET")
    row.operator('transmogrifier.advanced_ui', text="", icon="OPTIONS", depress=True if settings.advanced_ui else False)
    help = row.operator('transmogrifier.help', text="", icon="QUESTION")
    help.link = "https://sapwoodstudio.github.io/Transmogrifier"

    # Batch Convert button
    row = self.layout.row(align=True)
    row.operator('transmogrifier.transmogrify', icon_value=custom_icons['Transmogrifier_Icon'].icon_id)
    row.scale_x = 1.25
    row.operator('transmogrifier.forecast', text='', icon='INFO')
    row.scale_y = 1.5

    self.layout.separator(factor = separator_factor)

    # Transmogrifier Presets Menu
    col = self.layout.column(align=True)
    col.label(text="Workflow Preset", icon='DRIVER')
    layout = self.layout
    # Align menu items to the left.
    self.layout.use_property_split = False
    row = layout.row(align=True)
    row.prop(settings, 'transmogrifier_preset_enum')
    row.operator("transmogrifier.add_preset", text="", icon="ADD")
    row.operator("transmogrifier.remove_preset", text="", icon="REMOVE")
    row.operator("transmogrifier.load_preset", text="", icon="FILE_FOLDER")

    self.layout.separator(factor = separator_factor)

    # Import Settings
    box_imports = self.layout.box()
    box_imports.use_property_split = True
    row = box_imports.row(align=True)
    row.label(text="Imports", icon='IMPORT')
    
    if len(imports) > 0:
        row.prop(settings, 'link_import_settings', expand=False, text="", icon="LINKED" if settings.link_import_settings else "UNLINKED")

    # Add Import button
    col = box_imports.column(align=True)
    col.operator('transmogrifier.add_import', icon="ADD")

    # Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 508
    # Adapted from Gaffer v3.1.18 (GPL-3.0 License, https://github.com/gregzaal/Gaffer), UI.py, Line 1327
    for index, instance in enumerate(context.scene.transmogrifier_imports):   
        box = box_imports.box()
        grid = box.grid_flow(columns=2, align=True)
        row = grid.row()
        row.use_property_split = False
        row.alignment = "LEFT"
        
        row.prop(
            instance,
            "show_settings",
            icon="DOWNARROW_HLT" if instance.show_settings else "RIGHTARROW_THIN",
            emboss=False,
            toggle=True,
            text=instance.name
        )

        # Remove import button
        row = grid.row()
        row.alignment = "RIGHT"
        props = row.operator('transmogrifier.remove_import', text = "", icon = 'PANEL_CLOSE')
        props.index = index

        if instance.show_settings:
            col = box.column(align=True)
            self.layout.use_property_split = True

            # Format
            col.prop(instance, "format")

            # Extension options for USD and glTF formats.
            if instance.format == 'USD' or instance.format == "glTF":
                col.prop(instance, 'extension') 

            # Preset
            if Functions.operator_dict[instance.format][0][0] != "NO_OPERATOR":
                col.prop(instance, "preset_enum")

            # Directory
            if not settings.link_import_settings:
                col = box.column(align=True)
                col.prop(instance, "directory")

    # Import Directory (synced)
    if len(imports) > 1 or (len(imports) == 1 and settings.link_import_settings):
        if settings.link_import_settings:
            col = box_imports.column(align=True)
            col.prop(settings, 'import_directory')
    

    self.layout.separator(factor = separator_factor)


    # Export Settings
    self.layout.use_property_split = True
    box_exports = self.layout.box()
    row = box_exports.row(align=False)
    row.label(text="Exports", icon='EXPORT')
    
    
    if len(exports) > 0:
        if settings.link_export_settings and settings.advanced_ui:
            row.prop(settings, 'overwrite_files', text='', icon="FILE_TICK")
            row.prop(settings, 'export_adjacent', expand=False, text="", icon='DECORATE_OVERRIDE')
            row.prop(settings, 'set_data_names', text='', icon_value=custom_icons['Data_Names_From_Objects_Icon'].icon_id)
        row.prop(settings, 'link_export_settings', expand=False, text="", icon="LINKED" if settings.link_export_settings else "UNLINKED")

    # Add Export button
    col = box_exports.column(align=True)
    col.operator('transmogrifier.add_export', icon="ADD")

    # Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 508
    # Adapted from Gaffer v3.1.18 (GPL-3.0 License, https://github.com/gregzaal/Gaffer), UI.py, Line 1327
    for index, instance in enumerate(context.scene.transmogrifier_exports):   
        box = box_exports.box()
        grid = box.grid_flow(columns=2, align=True)
        row = grid.row()
        row.use_property_split = False
        row.alignment = "LEFT"
        
        row.prop(
            instance,
            "show_settings",
            icon="DOWNARROW_HLT" if instance.show_settings else "RIGHTARROW_THIN",
            emboss=False,
            toggle=True,
            text=instance.name
        )

        # Remove Export button
        row = grid.row()
        row.alignment = "RIGHT"
        if not settings.link_export_settings and settings.advanced_ui:
            row.prop(instance, 'overwrite_files', text='', icon="FILE_TICK")
            row.prop(instance, 'export_adjacent', expand=False, text="", icon='DECORATE_OVERRIDE')
            row.prop(instance, 'set_data_names', text='', icon_value=custom_icons['Data_Names_From_Objects_Icon'].icon_id)
        props = row.operator('transmogrifier.remove_export', text = "", icon = 'PANEL_CLOSE')
        props.index = index

        if instance.show_settings:
            col = box.column(align=True)
            self.layout.use_property_split = True

            # Format
            row = col.row(align=True)
            row.prop(instance, "format")
            if settings.advanced_ui and instance.format == "BLEND":
                if not instance.pack_resources:
                   row.prop(instance, 'use_absolute_paths', text='', icon="LOCKED" if instance.use_absolute_paths else "UNLOCKED") 
                row.prop(instance, 'pack_resources', text='', icon="PACKAGE" if instance.pack_resources else "UGLYPACKAGE")

            # Extension options for USD and glTF formats.
            if instance.format == 'USD' or instance.format == "glTF":
                col.prop(instance, 'extension') 

            # Preset
            if Functions.operator_dict[instance.format][1][0] != "NO_OPERATOR":
                col.prop(instance, "preset_enum")

            # Directory
            if not settings.link_export_settings:
                col = box.column(align=True)
                col.prop(instance, 'scale')

                col = box.column(align=True)
                col.prop(instance, 'prefix')
                col.prop(instance, 'suffix')            

                if not instance.export_adjacent:
                    row = box.row()
                    row.prop(instance, "directory")
                    if settings.advanced_ui:
                        if instance.use_subdirectories:
                            row.prop(instance, "copy_original_contents", text='', icon='COPYDOWN')
                        row.prop(instance, "use_subdirectories", text='', icon='FOLDER_REDIRECT')      
            
    
    # Additional export settings
    if settings.link_export_settings and (len(exports) > 1 or (len(exports) == 1 and settings.link_export_settings)):
        col = box_exports.column(align=True)
        col.prop(settings, 'scale')

        col = box_exports.column(align=True)
        col.prop(settings, 'prefix')
        col.prop(settings, 'suffix')

        if not settings.export_adjacent:
            row = box_exports.row(align=True)
            row.prop(settings, 'export_directory')
            if settings.advanced_ui:
                if settings.use_subdirectories:
                    row.prop(settings, "copy_original_contents", text='', icon='COPYDOWN')
                row.prop(settings, "use_subdirectories", text='', icon='FOLDER_REDIRECT')

    self.layout.separator(factor = separator_factor)
    

# Texture Settings
def draw_settings_textures(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    imports = bpy.context.scene.transmogrifier_imports
    textures = bpy.context.scene.transmogrifier_textures

    self.layout.use_property_split = False
    self.layout.use_property_decorate = False
    box_textures = self.layout.box()
    row = box_textures.row(align=False)
    row.label(text="Textures", icon='TEXTURE')
    if settings.use_textures and settings.advanced_ui:
        row.prop(settings, 'keep_temporary_textures', text='', icon="FAKE_USER_ON" if settings.keep_temporary_textures else "FAKE_USER_OFF")
        row.prop(settings, 'regex_textures', text='', icon_value=custom_icons['Regex_Textures_Icon'].icon_id)
        row.prop(settings, 'edit_textures', text='', icon_value=custom_icons['Edit_Textures_Icon'].icon_id)
    row.prop(settings, 'use_textures', text='', icon="CHECKBOX_HLT" if settings.use_textures else "CHECKBOX_DEHLT")

    if settings.use_textures:
        if settings.textures_source != "Custom":
            row = box_textures.row(align=True)
            row.use_property_split = True
            row.prop(settings, 'textures_source')

            if settings.advanced_ui and settings.textures_source == "External" and any(instance.format == "BLEND" for instance in imports):
                row.prop(settings, 'use_linked_blend_textures', text='', icon="LINKED" if settings.use_linked_blend_textures else "UNLINKED")

        elif settings.textures_source == "Custom":
            col = box_textures.column(align=True)
            col.use_property_split = True
            col.prop(settings, 'textures_source')
            row = col.row(align=True)
            row.use_property_split = True
            row.prop(settings, 'textures_custom_dir')
            if settings.advanced_ui:
                if settings.copy_textures_custom_dir:
                    row.prop(settings, 'overwrite_textures', text='', icon="FILE_TICK")
                row.prop(settings, 'copy_textures_custom_dir', text='', icon='COPYDOWN')

        if settings.advanced_ui and settings.edit_textures:
            lossy_compression_support = ("JPEG", "WEBP")
            box_edit_textures = box_textures.box()
            box_edit_textures.use_property_split = False
            grid = box_edit_textures.grid_flow(columns=2, align=True)
            row = grid.row()
            row.use_property_split = False
            row.alignment = "LEFT"
            row.label(text='Edit Textures', icon_value=custom_icons['Edit_Textures_Icon'].icon_id)

            if len(textures) > 0:
                row = grid.row()
                row.alignment = "RIGHT"
                row.prop(settings, 'link_texture_settings', expand=False, text="", icon="LINKED" if settings.link_texture_settings else "UNLINKED")

            col = box_edit_textures.column(align=True)
            row = col.row(align=True)
            row.prop(settings, 'edit_textures_preset_enum')
            row.operator("transmogrifier.edit_textures_add_preset", text="", icon="ADD")
            row.operator("transmogrifier.edit_textures_remove_preset", text="", icon="REMOVE")
            row.operator("transmogrifier.edit_textures_load_preset", text="", icon="FILE_FOLDER")

            col = box_edit_textures.column(align=True)
            col.operator('transmogrifier.add_texture', icon="ADD")
            
            if len(textures) > 0:
                col = box_edit_textures.column(align=True)

            # Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 508
            # Adapted from Gaffer v3.1.18 (GPL-3.0 License, https://github.com/gregzaal/Gaffer), UI.py, Line 1327
            for index, instance in enumerate(context.scene.transmogrifier_textures):   
                row = col.row(align=True)
                split = row.split(factor=0.45, align=True)
                split.prop(instance, "texture_map", text='')
                sub = split.row(align=True)
                sub.active = not settings.link_texture_settings
                sub.prop(instance, "texture_resolution", text='')
                sub.prop(instance, "texture_format", text='')
                props = row.operator('transmogrifier.remove_texture', text = "", icon = 'PANEL_CLOSE')
                props.index = index

            if len(textures) >= 1 and settings.link_texture_settings:
                box_edit_textures.use_property_split = True
                col = box_edit_textures.column(align=True)
                col.prop(settings, 'texture_resolution')
                col.prop(settings, 'texture_format')
                if settings.texture_format in lossy_compression_support:
                    col.prop(settings, 'image_quality')

    self.layout.separator(factor = 0.25)


# Set max file size options.
def draw_settings_optimize_exports(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    exports = bpy.context.scene.transmogrifier_exports
    self.layout.use_property_split = False
    self.layout.use_property_decorate = False
    box_optimize = self.layout.box()
    row = box_optimize.row(align=False)
    row.label(text="Auto-Optimize Files", icon='TRIA_DOWN_BAR')
    row.prop(settings, 'optimize', text='', icon="CHECKBOX_HLT" if settings.optimize else "CHECKBOX_DEHLT")


    if settings.optimize:
        col = box_optimize.column(align=True)
        col.use_property_split = True
        col.prop(settings, 'optimize_target_file_size')
        if settings.advanced_ui and len(exports) > 0 and ((settings.link_export_settings and settings.overwrite_files) or (not settings.link_export_settings and len(exports) > 0 and any(instance.overwrite_files == True for instance in exports))):
            col.prop(settings, 'optimize_overwrite_filter')

        # Adapted from Gaffer v3.1.18 (GPL-3.0 License, https://github.com/gregzaal/Gaffer), UI.py, Line 1327
        if settings.advanced_ui:
            self.layout.use_property_split = False
            col = box_optimize.column(align=True)
            box = col.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.alignment = "LEFT"
            row.prop(
                settings,
                "optimize_show_methods",
                icon="DOWNARROW_HLT" if settings.optimize_show_methods else "RIGHTARROW_THIN",
                emboss=False,
                toggle=True,
            )
            
            if settings.optimize_show_methods:
                col.separator()
                
                check_for_gltf = [export.format for export in exports if export.format == "glTF"]
                if check_for_gltf:
                    row = col.row(align=True)
                    row.prop(settings, "optimize_draco", icon='FULLSCREEN_EXIT', toggle=True)
                    sub = row.row(align=True)
                    sub.active = settings.optimize_draco
                    sub.prop(settings, "compression_level", text='')

                row = col.row(align=True)
                row.prop(settings, "optimize_texture_resize", icon='NODE_TEXTURE', toggle=True)
                sub = row.row(align=True)
                sub.active = settings.optimize_texture_resize
                sub.prop(settings, "resize_textures_limit", text='')

                row = col.row(align=True)
                row.prop(settings, "optimize_texture_reformat", icon='IMAGE_DATA', toggle=True)
                sub = row.row(align=True)
                sub.active = settings.optimize_texture_reformat
                sub.prop(settings, "include_normal_maps", icon='NORMALS_FACE')

                row = col.row(align=True)
                row.prop(settings, "optimize_decimate", icon='MOD_DECIM', toggle=True)
                sub = row.row(align=True)
                sub.active = settings.optimize_decimate
                sub.prop(settings, "decimate_limit", text='')
    
    self.layout.separator(factor = 0.25)


# Archive options
def draw_settings_assets(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    self.layout.use_property_split = False
    self.layout.use_property_decorate = False
    box_assets = self.layout.box()
    row = box_assets.row(align=False)
    row.label(text="Assets", icon='ASSET_MANAGER')
    if settings.advanced_ui:
        row.prop(settings, 'asset_extract_previews', text='', icon='IMAGE_PLANE')
        if settings.mark_as_assets:
            row.prop(settings, 'assets_allow_duplicates', text='', icon='DUPLICATE')
            row.prop(settings, 'asset_add_metadata', text='', icon='COLOR')
    row.prop(settings, 'mark_as_assets', text='', icon='ASSET_MANAGER')
    
    if settings.mark_as_assets:
        if settings.advanced_ui:
            col = box_assets.column(align=True)
            col.use_property_split = True
            col.prop(settings, 'asset_quality')
        
        box_mark_assets = box_assets.box()
        row = box_mark_assets.row(align=False)
        row.label(text='Mark Assets', icon='ASSET_MANAGER')
        
        if settings.advanced_ui:
            import_formats = [i.format for i in bpy.context.scene.transmogrifier_imports]
            if "Collections" in settings.asset_types_to_mark and "BLEND" in import_formats:
                row.prop(settings, 'mark_only_master_collection', text='', icon='GROUP')
        grid = box_mark_assets.grid_flow(columns=6, align=True)
        grid.prop(settings, 'asset_types_to_mark')
    
        if settings.advanced_ui:
            if "Objects" in settings.asset_types_to_mark:
                box_objects = box_mark_assets.box()
                col = box_objects.column(align=True)
                col.label(text="Object Types", icon='OBJECT_DATA')
                grid = box_objects.grid_flow(columns=5, align=True)
                grid.prop(settings, 'asset_object_types_filter', text='')
                
            if settings.asset_add_metadata:
                box_metadata = box_assets.box()
                col = box_metadata.column(align=True)
                col.label(text='Metadata', icon='COLOR')
                col = box_metadata.column(align=True)
                col.use_property_split = True
                col.prop(settings, 'asset_description')
                col.prop(settings, 'asset_license')
                col.prop(settings, 'asset_copyright')
                col.prop(settings, 'asset_author')
                col.prop(settings, 'asset_tags')
            
            box_assets.use_property_split = False
            if settings.assets_allow_duplicates:
                box_duplicates = box_assets.box()
                col = box_duplicates.column(align=True)
                col.label(text='Allow Duplicates', icon='DUPLICATE')
                grid = box_duplicates.grid_flow(columns=6, align=True)
                grid.prop(settings, 'assets_allow_duplicates_filter')

    if settings.mark_as_assets:
        box_assets.use_property_split = True
        box_library = box_assets.box()        
        row = box_library.row(align=False)
        row.label(text='Storage', icon='HOME')
        col = box_library.column(align=True)
        col.prop(settings, 'asset_library_enum')
        col.prop(settings, 'asset_catalog_enum')
        if settings.advanced_ui:
            row = box_library.row(align=False)
            row.prop(settings, 'asset_blend_location')
            if not settings.asset_pack_resources:
                   row.prop(settings, 'asset_use_absolute_paths', text='', icon="LOCKED" if settings.asset_use_absolute_paths else "UNLOCKED") 
            row.prop(settings, 'asset_pack_resources', text='', icon="PACKAGE" if settings.asset_pack_resources else "UGLYPACKAGE")

    if settings.advanced_ui and settings.asset_extract_previews:
        box_assets.use_property_split = False
        box_previews = box_assets.box()
        col = box_previews.column(align=True)
        col.label(text='Save Previews', icon='IMAGE_PLANE')
        grid = box_previews.grid_flow(columns=6, align=True)
        grid.prop(settings, 'asset_extract_previews_filter')

    if settings.advanced_ui:
        self.layout.separator(factor = 0.25)
        

# UV Settings
def draw_settings_uvs(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    if settings.advanced_ui:
        box_uvs = self.layout.box()
        box_uvs.use_property_split = False
        box_uvs.use_property_decorate = False
        
        row = box_uvs.row(align=False)
        row.label(text="UVs", icon='UV')
        if settings.advanced_ui:
            row.prop(settings, 'rename_uvs', text='', icon='OUTLINER_OB_FONT')
        row.prop(settings, 'export_uv_layout', text='', icon="EXPORT")
        
        if settings.export_uv_layout:
            box_uvs.use_property_split = True
            col = box_uvs.column(align=True)
            col.prop(settings, 'uv_export_location')
            if settings.uv_export_location == "Custom":
                col.prop(settings, 'uv_directory_custom')

            if settings.advanced_ui:
                col = box_uvs.column(align=True)
                col.prop(settings, 'modified_uvs')
                col.prop(settings, 'uv_combination')
                col.prop(settings, 'uv_resolution')
                col.prop(settings, 'uv_format')
                lossy_compression_support = ("JPEG", "WEBP")
                if settings.uv_format in lossy_compression_support:
                    col.prop(settings, 'uv_image_quality')  # Only show this option for formats that support lossy compression (i.e. JPEG & WEBP).
                col.prop(settings, 'uv_fill_opacity')
            
        if settings.rename_uvs:
            box_uvs.use_property_split = True
            col = box_uvs.column(align=True)
            col.prop(settings, 'rename_uvs_name')

        self.layout.separator(factor = 0.25)


def draw_settings_transforms(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    
    if settings.advanced_ui:
        self.layout.use_property_split = False
        self.layout.use_property_decorate = False
        box_transforms = self.layout.box()
        row = box_transforms.row(align=False)
        
        row.label(text="Transformations", icon='CON_PIVOT')
        row.prop(settings, 'set_transforms', text='', icon='OBJECT_ORIGIN')
        row.prop(settings, 'apply_transforms', text='', icon='FREEZE')
    
        if settings.apply_transforms:
            box_transforms_apply = box_transforms.box()
            box_transforms_apply.use_property_split = True
            row = box_transforms_apply.row(align=True)
            row.label(text='Apply Transforms', icon='FREEZE')
            
            row = box_transforms_apply.row(align=True)
            row.use_property_split = False
            row.prop(settings, 'apply_transforms_filter')

        if settings.set_transforms:
            box_transforms_set = box_transforms.box()
            row = box_transforms_set.row(align=True)
            row.label(text='Set Transforms', icon='OBJECT_ORIGIN')
            
            row.use_property_split = True
            row = box_transforms_set.row(align=True)
            row.prop(settings, 'set_transforms_filter')
                        
            if 'Location' in settings.set_transforms_filter:
                col = box_transforms_set.column(align=True)
                col.prop(settings, 'set_location')
            if 'Rotation' in settings.set_transforms_filter:
                col = box_transforms_set.column(align=True)
                col.prop(settings, 'set_rotation')
            if 'Scale' in settings.set_transforms_filter:
                col = box_transforms_set.column(align=True)
                col.prop(settings, 'set_scale')

        self.layout.separator(factor = 0.25)


def draw_settings_animations(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    if settings.advanced_ui:
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False
        box_animations = self.layout.box()
        row = box_animations.row(align=False)
        row.label(text="Animations", icon='ANIM')
        row.prop(settings, 'use_animations', text='', icon="CHECKBOX_HLT" if settings.use_animations else "CHECKBOX_DEHLT")

        self.layout.separator(factor = 0.25)


def draw_settings_scene(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    if settings.advanced_ui:
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False
        box_scene = self.layout.box()
        col = box_scene.column(align=True)
        # Set scene unit options.
        col.label(text="Scene", icon='SCENE_DATA')
        col.prop(settings, 'unit_system')
        if settings.unit_system != "NONE":
            col.prop(settings, 'length_unit')

        self.layout.separator(factor = 0.25)


# Custom Script Settings
def draw_settings_scripts(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    scripts = bpy.context.scene.transmogrifier_scripts
    self.layout.use_property_split = True
    self.layout.use_property_decorate = False

    box_scripts = self.layout.box()
    # col = box_scripts.column(align=True)
    # col.scale_y = 1.0
    row = box_scripts.row(align=False)
    
    row.label(text="Custom Scripts", icon='FILE_SCRIPT')

    if len(scripts) > 0:
        row.prop(settings, 'link_script_settings', text='', icon="LINKED" if settings.link_script_settings else "UNLINKED")

    if settings.advanced_ui:
        row = box_scripts.row(align=False)
        row.operator('transmogrifier.add_custom_script', icon="ADD")

        # Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 508
        for index, instance in enumerate(scripts):   
            box = box_scripts.box()
            grid = box.grid_flow(columns=2, align=True)
            row = grid.row()
            row.use_property_split = False
            row.alignment = "LEFT"
            
            row.prop(
                instance,
                "show_settings",
                icon="DOWNARROW_HLT" if instance.show_settings else "RIGHTARROW_THIN",
                emboss=False,
                toggle=True,
                text=instance.name
            )

            # Remove import button
            row = grid.row()
            row.alignment = "RIGHT"
            props = row.operator('transmogrifier.remove_custom_script', text = "", icon = 'PANEL_CLOSE')
            props.custom_script_index = index

            if instance.show_settings:
                col = box.column(align=True)
                self.layout.use_property_split = True

                file = Path(bpy.path.abspath(instance.file))
                
                # Added a new custom script (default name is "*.py")
                if instance.file == "*.py"  and file.name == "*.py":
                    icon = "FILE_SCRIPT"

                # File is not a Python file.
                elif file.suffix != ".py":
                    icon = "ERROR"

                # File is a Python file but doesn't exist.
                elif not file.is_file() and file.suffix == ".py":
                    icon = "ERROR"

                # File is a Python file and might exist, but path is relative and current Blend session is unsaved.
                elif file != Path(instance.file) and not bpy.data.is_saved:
                    icon = "ERROR"

                # File is a Python file and exists.
                elif file.is_file() and file.suffix == ".py":
                    icon = "FILE_SCRIPT"

                col.prop(instance, "file")  
                
                if not settings.link_script_settings:
                    col.prop(instance, "trigger")
        
        if len(scripts) > 0 and settings.link_script_settings:
            col = box_scripts.column(align=True)
            col.prop(settings, "trigger")
        
    elif not settings.advanced_ui:
        col = self.layout.column(align=True)
        col.label(text="(Toggle 'Advanced UI' to view)")


# Set max file size options.
def draw_settings_logging(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    self.layout.use_property_split = False
    self.layout.use_property_decorate = False
    box_logging = self.layout.box()
    row = box_logging.row(align=False)
    row.label(text="Logging", icon="TEXT")
    row.prop(settings, 'logging_save_log', text='', icon="FILE_TEXT")
    row.prop(settings, 'logging_save_summary', text='', icon="SPREADSHEET")

    if settings.logging_save_summary:
        box_summary = box_logging.box()
        col = box_summary.column(align=True)
        col.use_property_split = True
        col.label(text='Conversion Summary', icon='SPREADSHEET')
        grid = box_summary.grid_flow(columns=2, align=True)
        grid.prop(settings, 'logging_summary_filter')

        # Compare File Size
        if "File Size" in settings.logging_summary_filter:
            box_file_size = box_summary.box()
            col = box_file_size.column(align=True)
            col.use_property_split = True
            col.label(text='Compare File Size', icon='FILE')
            col.prop(settings, 'optimize_target_file_size')

        # Compare Dimensions
        if "Dimensions" in settings.logging_summary_filter:
            box_dimensions = box_summary.box()
            col = box_dimensions.column(align=True)
            col.use_property_split = True
            col.label(text='Compare Dimensions', icon='CUBE')
            col.prop(settings, 'logging_unit_system')
            col.prop(settings, 'logging_length_unit')

            col = box_dimensions.column(align=True)
            col.use_property_split = True
            row = col.row(align=True)
            row.prop(settings, 'logging_bounds_x', text=f"X ({settings.logging_length_unit_abbr})")
            row = col.row(align=True)
            row.prop(settings, 'logging_bounds_y', text=f"Y ({settings.logging_length_unit_abbr})")
            row = col.row(align=True)
            row.prop(settings, 'logging_bounds_z', text=f"Z ({settings.logging_length_unit_abbr})")


# Draws the button and popover dropdown button used in the
# 3D Viewport Header or Top Bar
def draw_popover(self, context):
    row = self.layout.row()
    row = row.row(align=True)
    row.operator('transmogrifier.transmogrify', text='', icon_value=custom_icons['Transmogrifier_Icon'].icon_id)
    row.popover(panel='POPOVER_PT_transmogrifier', text='')


# Side Panel panel (used with Side Panel option)
class VIEW3D_PT_transmogrifier(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "Transmogrifier"

    def draw(self, context):
        settings = bpy.context.scene.transmogrifier_settings
        draw_settings_general(self, context)
        if not settings.advanced_ui:
            draw_settings_textures(self, context)
            draw_settings_uvs(self, context)
            draw_settings_transforms(self, context)
            draw_settings_animations(self, context)
            draw_settings_scene(self, context)
            draw_settings_optimize_exports(self, context)
            draw_settings_assets(self, context)


class VIEW3D_PT_transmogrifier_textures(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "Textures"

    def draw(self, context):
        draw_settings_textures(self, context)


class VIEW3D_PT_transmogrifier_optimize(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "Optimize"

    def draw(self, context):
        draw_settings_optimize_exports(self, context)


class VIEW3D_PT_transmogrifier_assets(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "Assets"

    def draw(self, context):
        draw_settings_assets(self, context)


class VIEW3D_PT_transmogrifier_uvs(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "UVs"

    def draw(self, context):
        draw_settings_uvs(self, context)


class VIEW3D_PT_transmogrifier_scene(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "Scene"

    def draw(self, context):
        draw_settings_scene(self, context)
        draw_settings_animations(self, context)


class VIEW3D_PT_transmogrifier_transformations(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "Transformations"

    def draw(self, context):
        draw_settings_transforms(self, context)


class VIEW3D_PT_transmogrifier_scripts(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "Scripts"

    def draw(self, context):
        draw_settings_scripts(self, context)


class VIEW3D_PT_transmogrifier_logging(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "Logging"

    def draw(self, context):
        draw_settings_logging(self, context)


# Popover panel (used on 3D Viewport Header or Top Bar option)
class POPOVER_PT_transmogrifier(Panel):
    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_label = "Transmogrifier"

    def draw(self, context):
        settings = bpy.context.scene.transmogrifier_settings

        draw_settings_general(self, context)
        draw_settings_textures(self, context)
        draw_settings_optimize_exports(self, context)
        draw_settings_assets(self, context)
        draw_settings_uvs(self, context)
        draw_settings_transforms(self, context)
        draw_settings_animations(self, context)
        draw_settings_scene(self, context)
        if settings.advanced_ui:
            draw_settings_scripts(self, context)
            draw_settings_logging(self, context)


# Addon settings that are NOT specific to a .blend file
class TransmogrifierPreferences(AddonPreferences):
    bl_idname = bl_info["name"]

    def addon_location_updated(self, context):
        bpy.types.TOPBAR_MT_editor_menus.remove(draw_popover)
        bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)
        settings = bpy.context.scene.transmogrifier_settings
        if hasattr(bpy.types, "VIEW3D_PT_transmogrifier"):
            bpy.utils.unregister_class(VIEW3D_PT_transmogrifier)
            if settings.advanced_ui:
                bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_textures)
                bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_optimize)
                bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_assets)
                bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_uvs)
                bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_scene)
                bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_transformations)
                bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_scripts)
                bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_logging)
        if self.addon_location == 'TOPBAR':
            bpy.types.TOPBAR_MT_editor_menus.append(draw_popover)
        elif self.addon_location == '3DHEADER':
            bpy.types.VIEW3D_MT_editor_menus.append(draw_popover)
        elif self.addon_location == '3DSIDE':
            bpy.utils.register_class(VIEW3D_PT_transmogrifier)
            if settings.advanced_ui:
                bpy.utils.register_class(VIEW3D_PT_transmogrifier_textures)
                bpy.utils.register_class(VIEW3D_PT_transmogrifier_optimize)
                bpy.utils.register_class(VIEW3D_PT_transmogrifier_assets)
                bpy.utils.register_class(VIEW3D_PT_transmogrifier_uvs)
                bpy.utils.register_class(VIEW3D_PT_transmogrifier_scene)
                bpy.utils.register_class(VIEW3D_PT_transmogrifier_transformations)
                bpy.utils.register_class(VIEW3D_PT_transmogrifier_scripts)
                bpy.utils.register_class(VIEW3D_PT_transmogrifier_logging)


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
        default='3DSIDE',
        update=addon_location_updated,
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        # Display addon location options
        layout.prop(self, "addon_location")
        
        # Display copy assets button
        box = layout.box()
        col = box.column(align=True)
        col.operator("transmogrifier.install_presets", icon="DUPLICATE")


# Toggles Advanced UI setting.  Registers and unregisters additional panels when the addon's UI is in the 3D Viewport Side Menu.
class TRANSMOGRIFIER_OT_advanced_ui(Operator):
    '''Toggle advanced settings'''

    bl_idname = "transmogrifier.advanced_ui"
    bl_label = "Advanced UI"
    bl_description = "Toggle simple/advanced user interface options"

    def execute(self, context):
        settings = bpy.context.scene.transmogrifier_settings
        prefs = bpy.context.preferences.addons[bl_info["name"]].preferences
        panels = [
            VIEW3D_PT_transmogrifier_textures, 
            VIEW3D_PT_transmogrifier_optimize, 
            VIEW3D_PT_transmogrifier_assets, 
            VIEW3D_PT_transmogrifier_uvs, 
            VIEW3D_PT_transmogrifier_scene, 
            VIEW3D_PT_transmogrifier_transformations, 
            VIEW3D_PT_transmogrifier_scripts, 
            VIEW3D_PT_transmogrifier_logging, 
        ]
        
        if settings.advanced_ui:
            if prefs.addon_location == '3DSIDE':
                for panel in panels: 
                    try: 
                        bpy.utils.unregister_class(panel)
                    except:
                        bpy.utils.register_class(panel)
                        bpy.utils.unregister_class(panel)
            settings.advanced_ui = False

        elif not settings.advanced_ui:
            if prefs.addon_location == '3DSIDE':
                for panel in panels: 
                    try: 
                        bpy.utils.register_class(panel)
                    except:
                        bpy.utils.unregister_class(panel)
                        bpy.utils.register_class(panel)
            settings.advanced_ui = True
            
        return {'FINISHED'}
        


#  ███████████   ██████████   █████████  █████  █████████  ███████████ ███████████   █████ █████
# ░░███░░░░░███ ░░███░░░░░█  ███░░░░░███░░███  ███░░░░░███░█░░░███░░░█░░███░░░░░███ ░░███ ░░███ 
#  ░███    ░███  ░███  █ ░  ███     ░░░  ░███ ░███    ░░░ ░   ░███  ░  ░███    ░███  ░░███ ███  
#  ░██████████   ░██████   ░███          ░███ ░░█████████     ░███     ░██████████    ░░█████   
#  ░███░░░░░███  ░███░░█   ░███    █████ ░███  ░░░░░░░░███    ░███     ░███░░░░░███    ░░███    
#  ░███    ░███  ░███ ░   █░░███  ░░███  ░███  ███    ░███    ░███     ░███    ░███     ░███    
#  █████   █████ ██████████ ░░█████████  █████░░█████████     █████    █████   █████    █████   
# ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░░░░░  ░░░░░  ░░░░░░░░░     ░░░░░    ░░░░░   ░░░░░    ░░░░░    

classes = (
    TransmogrifierPreferences,
    POPOVER_PT_transmogrifier,
    TRANSMOGRIFIER_OT_advanced_ui,
)

# Register Classes.
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Show addon UI
    prefs = bpy.context.preferences.addons[bl_info["name"]].preferences
    if prefs.addon_location == 'TOPBAR':
        bpy.types.TOPBAR_MT_editor_menus.append(draw_popover)
    if prefs.addon_location == '3DHEADER':
        bpy.types.VIEW3D_MT_editor_menus.append(draw_popover)
    elif prefs.addon_location == '3DSIDE':
        bpy.utils.register_class(VIEW3D_PT_transmogrifier)

    # Custom icons    
    global custom_icons
    custom_icons = previews.new()
    icons_dir = Path(__file__).parent.resolve() / "icons"
    
    custom_icons.load("Transmogrifier_Icon", str(icons_dir / "Transmogrifier_Icon.png"), 'IMAGE')
    custom_icons.load("Data_Names_From_Objects_Icon", str(icons_dir / "Data_Names_From_Objects_Icon.png"), 'IMAGE')
    custom_icons.load("Regex_Textures_Icon", str(icons_dir / "Regex_Textures_Icon.png"), 'IMAGE')
    custom_icons.load("Edit_Textures_Icon", str(icons_dir / "Edit_Textures_Icon.png"), 'IMAGE')


# Unregister Classes.
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Remove UI
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_popover)
    bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)
    if hasattr(bpy.types, "VIEW3D_PT_transmogrifier"):
        bpy.utils.unregister_class(VIEW3D_PT_transmogrifier)

    # Remove icons
    global custom_icons
    previews.remove(custom_icons)