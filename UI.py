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
    row = self.layout.row(align=True)
    row.label(text=title)
    row.prop(settings, 'advanced_ui', expand=False, text="", icon="OPTIONS")

    # Batch Convert button
    row = self.layout.row(align=True)   
    row.operator('transmogrifier.transmogrify', icon='PLAY')
    row.scale_x = 1.25
    row.operator('transmogrifier.forecast', text='', icon='INFO')
    row.scale_y = 1.5

    self.layout.separator(factor = separator_factor)

    # Transmogrifier Presets Menu
    col = self.layout.column(align=True)
    col.label(text="Workflow:", icon='DRIVER')
    layout = self.layout
    # Align menu items to the left.
    self.layout.use_property_split = False
    row = layout.row(align=True)
    row.prop(settings, 'transmogrifier_preset_enum')
    row.operator("transmogrifier.add_preset", text="", icon="ADD")
    row.operator("transmogrifier.remove_preset", text="", icon="REMOVE")

    self.layout.separator(factor = separator_factor)

    # Import Settings
    self.layout.use_property_split = True
    row = self.layout.row(align=True)
    row.label(text="Imports:", icon='IMPORT')
    
    if len(imports) > 1:
        if settings.link_import_directories:
            icon = "LINKED"
        elif not settings.link_import_directories:
            icon = "UNLINKED"
        row.prop(settings, 'link_import_directories', expand=False, text="", icon=icon)

    # Add Import button
    col = self.layout.column(align=True)
    col.operator('transmogrifier.add_import', icon="ADD")

    # Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 508
    for index, import_file in enumerate(context.scene.transmogrifier_imports):   
        layout = self.layout
        import_file_box = layout.box()
        row = import_file_box.row()
        col = import_file_box.column(align=True)
        
        # Import file name
        row.label(text=import_file.name, icon='IMPORT')

        # Remove import button
        props = row.operator('transmogrifier.remove_import', text = "", icon = 'PANEL_CLOSE')
        props.index = index

        # Format
        col.prop(import_file, "format")

        # Extension options for USD and glTF formats.
        if import_file.format == 'USD' or import_file.format == "glTF":
            col.prop(import_file, 'extension') 

        # Preset
        if Functions.operator_dict[import_file.format][0][0] != "NO_OPERATOR":
            col.prop(import_file, "preset_enum")

        # Directory
        if not settings.link_import_directories:
            col = import_file_box.column(align=True)
            col.prop(import_file, "directory")

    # Import Directory (synced)
    if len(imports) > 1 or (len(imports) == 1 and settings.link_import_directories):
        if settings.link_import_directories:
            col = self.layout.column(align=True)
            col.prop(settings, 'import_directory')
    
    self.layout.separator(factor = separator_factor)

    # Export Settings
    self.layout.use_property_split = True
    row = self.layout.row(align=True)
    row.label(text="Exports:", icon='EXPORT')
    
    if len(exports) > 0:
        row.prop(settings, 'export_adjacent', expand=False, text="", icon='UV_SYNC_SELECT')
        if len(exports) > 1:
            if settings.link_export_settings:
                icon = "LINKED"
            elif not settings.link_export_settings:
                icon = "UNLINKED"
            row.prop(settings, 'link_export_settings', expand=False, text="", icon=icon)

    # Add Export button
    col = self.layout.column(align=True)
    col.operator('transmogrifier.add_export', icon="ADD")

    # Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 508
    for index, export_file in enumerate(context.scene.transmogrifier_exports):   
        layout = self.layout
        export_file_box = layout.box()
        row = export_file_box.row()
        col = export_file_box.column(align=True)
        
        # Export file name
        row.label(text=export_file.name, icon='EXPORT')

        # Remove export button
        props = row.operator('transmogrifier.remove_export', text = "", icon = 'PANEL_CLOSE')
        props.index = index

        # Format
        col.prop(export_file, "format")

        # Extension options for USD and glTF formats.
        if export_file.format == 'USD' or export_file.format == "glTF":
            col.prop(export_file, 'extension') 

        # Preset
        if Functions.operator_dict[export_file.format][1][0] != "NO_OPERATOR":
            col.prop(export_file, "preset_enum")

        # Directory
        if not settings.link_export_settings:
            if not settings.export_adjacent:
                row = export_file_box.row()
                row.prop(export_file, "directory")
                if settings.advanced_ui:
                    if export_file.use_subdirectories:
                        row.prop(export_file, "copy_original_contents", text='', icon='COPYDOWN')
                    row.prop(export_file, "use_subdirectories", text='', icon='FOLDER_REDIRECT')
            col = export_file_box.column(align=True)
            col.prop(export_file, 'prefix')
            col.prop(export_file, 'suffix')
            if settings.advanced_ui:
                col = export_file_box.column(align=True)
                col.prop(export_file, 'set_data_names')                
            
    
    # Additional export settings
    if settings.link_export_settings and (len(exports) > 1 or (len(exports) == 1 and settings.link_export_settings)):
        if not settings.export_adjacent:
            row = self.layout.row(align=True)
            row.prop(settings, 'export_directory')
            if settings.advanced_ui:
                if settings.use_subdirectories:
                    row.prop(settings, "copy_original_contents", text='', icon='COPYDOWN')
                row.prop(settings, "use_subdirectories", text='', icon='FOLDER_REDIRECT')
        
        col = self.layout.column(align=True)
        col.prop(settings, 'prefix')
        col.prop(settings, 'suffix')
        if settings.advanced_ui:
            col = self.layout.column(align=True)
            col.prop(settings, 'set_data_names')

    self.layout.separator(factor = separator_factor)
    

# Texture Settings
def draw_settings_textures(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    self.layout.use_property_split = True
    self.layout.use_property_decorate = False
    col = self.layout.column(align=True)
    # Align menu items to the left.
    self.layout.use_property_split = True
    # col = self.layout.column(align=True)
    col.label(text="Textures:", icon='TEXTURE')
    col.prop(settings, 'use_textures')

    if settings.use_textures:
        if settings.advanced_ui:
            col.prop(settings, 'regex_textures')
            col.prop(settings, 'keep_modified_textures')
            self.layout.use_property_split = True
            col = self.layout.column(align=True)
        col.prop(settings, 'textures_source')
        if settings.advanced_ui:
            import_formats = [i.format for i in bpy.context.scene.transmogrifier_imports]
            if "BLEND" in import_formats and settings.textures_source == "External":
                col.prop(settings, 'use_linked_blend_textures')
                col = self.layout.column(align=True)
        if settings.textures_source == "Custom":
            col.prop(settings, 'textures_custom_dir')
            if settings.advanced_ui:
                col.prop(settings, 'copy_textures_custom_dir')
                if settings.copy_textures_custom_dir:
                    col.prop(settings, 'replace_textures')
                col = self.layout.column(align=True)
        
        if settings.advanced_ui:
            # col = self.layout.column(align=True)
            col.prop(settings, 'texture_resolution')

            if settings.texture_resolution != "Default":
                # Align menu items to the left.
                self.layout.use_property_split = False

                grid = self.layout.grid_flow(columns=3, align=True)
                grid.prop(settings, 'texture_resolution_include')
            
                # Align menu items to the right.
                self.layout.use_property_split = True
                col = self.layout.column(align=True)

            col.prop(settings, 'image_format')
            lossy_compression_support = ("JPEG", "WEBP")
            if settings.image_format != "Default":
                if settings.image_format in lossy_compression_support:
                    col.prop(settings, 'image_quality')
                # Align menu items to the left.
                self.layout.use_property_split = False

                grid = self.layout.grid_flow(columns=3, align=True)
                grid.prop(settings, 'image_format_include')
        
    if settings.advanced_ui:
        self.layout.use_property_split = True
        col = self.layout.column(align=True)
        col.label(text="UVs:", icon='UV')
        col.prop(settings, 'rename_uvs')
        if settings.rename_uvs:
            col.prop(settings, 'rename_uvs_name')
            col = self.layout.column(align=True)
        col.prop(settings, 'export_uv_layout')
        if settings.export_uv_layout:
            col.prop(settings, 'modified_uvs')
            col = self.layout.column(align=True)
            col.prop(settings, 'uv_export_location')
            if settings.uv_export_location == "Custom":
                col.prop(settings, 'uv_directory_custom')
            col.prop(settings, 'uv_combination')
            col.prop(settings, 'uv_resolution')
            col.prop(settings, 'uv_format')
            if settings.uv_format in lossy_compression_support:
                col.prop(settings, 'uv_image_quality')  # Only show this option for formats that support lossy compression (i.e. JPEG & WEBP).
            col.prop(settings, 'uv_fill_opacity')
            # self.layout.separator()
            

def draw_settings_transforms(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    self.layout.use_property_split = True
    self.layout.use_property_decorate = False
    col = self.layout.column(align=True)

    # Transformation options.
    self.layout.use_property_split = True
    # col = self.layout.column(align=True)
    if settings.advanced_ui:
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
def draw_settings_optimize_files(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    self.layout.use_property_split = True
    self.layout.use_property_decorate = False
    col = self.layout.column(align=True)

    # self.layout.use_property_split = True
    # col = self.layout.column(align=True)
    col.label(text="Auto-Optimize:", icon='TRIA_DOWN_BAR')
    col.prop(settings, 'auto_resize_files')
    self.layout.use_property_split = True
    if settings.advanced_ui:
        if settings.auto_resize_files != "None":
            col.prop(settings, 'file_size_maximum')
            grid = self.layout.grid_flow(columns=1, align=True)
            grid.prop(settings, 'file_size_methods')
            col = self.layout.column(align=True)
            if 'Resize Textures' in settings.file_size_methods:
                col.prop(settings, 'resize_textures_limit')
            if 'Reformat Textures' in settings.file_size_methods:
                col.prop(settings, 'reformat_normal_maps')
            if 'Decimate Meshes' in settings.file_size_methods:
                col.prop(settings, 'decimate_limit')
                

# Archive options
def draw_settings_archive(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    self.layout.use_property_split = True
    self.layout.use_property_decorate = False
    col = self.layout.column(align=True)

    # Align menu items to the Right.
    self.layout.use_property_split = True
    col.label(text="Archive:", icon='ASSET_MANAGER')
    col.prop(settings, 'save_conversion_log')
    col.prop(settings, 'archive_assets')

    if settings.advanced_ui:
        if settings.archive_assets:
            self.layout.use_property_split = False
            col.label(text="Mark Assets:")
            grid = self.layout.grid_flow(columns=6, align=True)
            grid.prop(settings, 'asset_types_to_mark')
            col = self.layout.column(align=True)
            
            col.prop(settings, 'assets_ignore_duplicates')
            if settings.assets_ignore_duplicates:
                grid = self.layout.grid_flow(columns=6, align=True)
                grid.prop(settings, 'assets_ignore_duplicates_filter')
                col = self.layout.column(align=True)

            col.prop(settings, 'asset_extract_previews')
            if settings.asset_extract_previews:
                grid = self.layout.grid_flow(columns=6, align=True)
                grid.prop(settings, 'asset_extract_previews_filter')
                col = self.layout.column(align=True)
                        
            self.layout.use_property_split = False
            import_formats = [i.format for i in bpy.context.scene.transmogrifier_imports]
            if "Collections" in settings.asset_types_to_mark and "BLEND" in import_formats:
                col.label(text="Collections:")
                col.prop(settings, 'mark_only_master_collection')
                col = self.layout.column(align=True)

            if "Objects" in settings.asset_types_to_mark:
                col.label(text="Object Types:")
                grid = self.layout.grid_flow(columns=3, align=True)
                grid.prop(settings, 'asset_object_types_filter')
                self.layout.use_property_split = True  # Align menu items to the right.
                col = self.layout.column(align=True)

            self.layout.use_property_split = True
        
            col = self.layout.column(align=True)
            col.prop(settings, 'asset_library_enum')
            col.prop(settings, 'asset_catalog_enum')
            if settings.asset_library != "NO_LIBRARY":
                col.prop(settings, 'asset_blend_location')
            col.prop(settings, 'pack_resources')
            col.prop(settings, 'asset_add_metadata')
            if settings.asset_add_metadata:
                col.prop(settings, 'asset_description')
                col.prop(settings, 'asset_license')
                col.prop(settings, 'asset_copyright')
                col.prop(settings, 'asset_author')
                col.prop(settings, 'asset_tags')
                col = self.layout.column(align=True)
    
    if not settings.archive_assets:
        col.prop(settings, 'asset_extract_previews')


# Custom Script Settings
def draw_settings_scripts(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    self.layout.use_property_split = True
    self.layout.use_property_decorate = False

    col = self.layout.column(align=True)
    col.scale_y = 1.0
    grid = col.grid_flow(row_major = True, columns = 2, even_columns = False)
    grid.label(text="Custom Scripts:", icon='FILE_SCRIPT')

    if settings.advanced_ui:
        col = self.layout.column(align=True)
        col.operator('transmogrifier.add_custom_script', icon="ADD")

        # Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 508
        for index, custom_script in enumerate(context.scene.transmogrifier_scripts):   
            layout = self.layout
            # layout.separator(factor = 1.0)
            custom_script_box = layout.box()

            file = Path(bpy.path.abspath(custom_script.file))
            
            # Added a new custom script (default name is "*.py")
            if custom_script.file == "*.py"  and file.name == "*.py":
                icon = "FILE_SCRIPT"

            # File is not a Python file.
            elif file.suffix != ".py":
                icon = "ERROR"

            # File is a Python file but doesn't exist.
            elif not file.is_file() and file.suffix == ".py":
                icon = "ERROR"

            # File is a Python file and might exist, but path is relative and current Blend session is unsaved.
            elif file != Path(custom_script.file) and not bpy.data.is_saved:
                icon = "ERROR"

            # File is a Python file and exists.
            elif file.is_file() and file.suffix == ".py":
                icon = "FILE_SCRIPT"
            
            row = custom_script_box.row()
            row.label(text=custom_script.name, icon=icon)
            props = row.operator('transmogrifier.remove_custom_script', text = "", icon = 'PANEL_CLOSE')
            props.custom_script_index = index

            col = custom_script_box.column()
            col.prop(custom_script, "file")  
            col.prop(custom_script, "trigger")
    
    elif not settings.advanced_ui:# == "Simple":
        col.label(text="(Toggle 'Advanced UI' to view)")
        

# Draws the button and popover dropdown button used in the
# 3D Viewport Header or Top Bar
def draw_popover(self, context):
    row = self.layout.row()
    row = row.row(align=True)
    row.operator('transmogrifier.transmogrify', text='', icon='FILE_CACHE')
    row.popover(panel='POPOVER_PT_transmogrifier', text='')


# Side Panel panel (used with Side Panel option)
class VIEW3D_PT_transmogrifier_general(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "⚙  General"

    def draw(self, context):
        draw_settings_general(self, context)
        
class VIEW3D_PT_transmogrifier_textures(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "🏁  Textures"

    def draw(self, context):
        draw_settings_textures(self, context)

class VIEW3D_PT_transmogrifier_scene(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "📐  Scene"

    def draw(self, context):
        draw_settings_transforms(self, context)

class VIEW3D_PT_transmogrifier_optimize_files(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "⏬  Optimize"

    def draw(self, context):
        draw_settings_optimize_files(self, context)

class VIEW3D_PT_transmogrifier_archive(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "🗄  Archive"

    def draw(self, context):
        draw_settings_archive(self, context)

class VIEW3D_PT_transmogrifier_scripts(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transmogrifier"
    bl_label = "🐍  Scripts"

    def draw(self, context):
        draw_settings_scripts(self, context)

# Popover panel (used on 3D Viewport Header or Top Bar option)
class POPOVER_PT_transmogrifier(Panel):
    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_label = "Transmogrifier"

    def draw(self, context):
        draw_settings_general(self, context)
        draw_settings_textures(self, context)
        draw_settings_transforms(self, context)
        draw_settings_optimize_files(self, context)
        draw_settings_archive(self, context)
        draw_settings_scripts(self, context)


# Addon settings that are NOT specific to a .blend file
class TransmogrifierPreferences(AddonPreferences):
    bl_idname = bl_info["name"]

    def addon_location_updated(self, context):
        bpy.types.TOPBAR_MT_editor_menus.remove(draw_popover)
        bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)
        if hasattr(bpy.types, "VIEW3D_PT_transmogrifier_general"):
            bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_general)
            bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_textures)
            bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_scene)
            bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_optimize_files)
            bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_archive)
            bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_scripts)
        if self.addon_location == 'TOPBAR':
            bpy.types.TOPBAR_MT_editor_menus.append(draw_popover)
        elif self.addon_location == '3DHEADER':
            bpy.types.VIEW3D_MT_editor_menus.append(draw_popover)
        elif self.addon_location == '3DSIDE':
            bpy.utils.register_class(VIEW3D_PT_transmogrifier_general)
            bpy.utils.register_class(VIEW3D_PT_transmogrifier_textures)
            bpy.utils.register_class(VIEW3D_PT_transmogrifier_scene)
            bpy.utils.register_class(VIEW3D_PT_transmogrifier_optimize_files)
            bpy.utils.register_class(VIEW3D_PT_transmogrifier_archive)
            bpy.utils.register_class(VIEW3D_PT_transmogrifier_scripts)


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
        col.operator("transmogrifier.copy_assets", text="Copy Assets to Preferences", icon="DUPLICATE")



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
        bpy.utils.register_class(VIEW3D_PT_transmogrifier_general)
        bpy.utils.register_class(VIEW3D_PT_transmogrifier_textures)
        bpy.utils.register_class(VIEW3D_PT_transmogrifier_scene)
        bpy.utils.register_class(VIEW3D_PT_transmogrifier_optimize_files)
        bpy.utils.register_class(VIEW3D_PT_transmogrifier_archive)
        bpy.utils.register_class(VIEW3D_PT_transmogrifier_scripts)

# Unregister Classes.
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Remove UI
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_popover)
    bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)
    if hasattr(bpy.types, "VIEW3D_PT_transmogrifier_general"):
        bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_general)
        bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_textures)
        bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_scene)
        bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_optimize_files)
        bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_archive)
        bpy.utils.unregister_class(VIEW3D_PT_transmogrifier_scripts)