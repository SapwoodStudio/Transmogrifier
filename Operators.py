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
    Operator, 
) 
from bpy.props import (
    IntProperty,
    StringProperty
)
import os
import subprocess
import shutil
from pathlib import Path
from bpy_extras.io_utils import ImportHelper
import json
from . import Functions



#     ███████    ███████████  ██████████ ███████████     █████████   ███████████    ███████    ███████████    █████████ 
#   ███░░░░░███ ░░███░░░░░███░░███░░░░░█░░███░░░░░███   ███░░░░░███ ░█░░░███░░░█  ███░░░░░███ ░░███░░░░░███  ███░░░░░███
#  ███     ░░███ ░███    ░███ ░███  █ ░  ░███    ░███  ░███    ░███ ░   ░███  ░  ███     ░░███ ░███    ░███ ░███    ░░░ 
# ░███      ░███ ░██████████  ░██████    ░██████████   ░███████████     ░███    ░███      ░███ ░██████████  ░░█████████ 
# ░███      ░███ ░███░░░░░░   ░███░░█    ░███░░░░░███  ░███░░░░░███     ░███    ░███      ░███ ░███░░░░░███  ░░░░░░░░███
# ░░███     ███  ░███         ░███ ░   █ ░███    ░███  ░███    ░███     ░███    ░░███     ███  ░███    ░███  ███    ░███
#  ░░░███████░   █████        ██████████ █████   █████ █████   █████    █████    ░░░███████░   █████   █████░░█████████ 
#    ░░░░░░░    ░░░░░        ░░░░░░░░░░ ░░░░░   ░░░░░ ░░░░░   ░░░░░    ░░░░░       ░░░░░░░    ░░░░░   ░░░░░  ░░░░░░░░░  

# Operator called when pressing the Batch Convert button.
class TRANSMOGRIFIER_OT_transmogrify(Operator):
    """Batch converts 3D files and associated textures into other formats"""
    bl_idname = "transmogrifier.transmogrify"
    bl_label = "Batch Convert"
    file_count = 0

    def execute(self, context):
        settings = bpy.context.scene.transmogrifier_settings
        imports = bpy.context.scene.transmogrifier_imports
        exports = bpy.context.scene.transmogrifier_exports
        scripts = bpy.context.scene.transmogrifier_scripts

        # Check if there are imports and exports. Stop batch converter if there is not at least one of each.
        if not imports or not exports:
            if not imports:
                message = "Please Add Import"
            elif not exports: 
                message = "Please Add Export"

            self.report({'ERROR'}, message)
            return {'FINISHED'}

        # Check directory and file paths.  Stop batch converter if they don't check-out.
        collection_properties_to_check = [imports, exports]
        for collection_property in collection_properties_to_check:
            for index, instance in enumerate(collection_property):
                if collection_property == exports and settings.export_adjacent:  # Skip if models are getting exported adjacent to their respective imports.
                    continue
                directory_checks_out, message = Functions.check_directory_path(self, context, instance.directory)
                if not directory_checks_out:
                    self.report({'ERROR'}, message)
                    return {'FINISHED'}
        
        custom_menu_options_to_check = [settings.textures_source, settings.uv_export_location]
        directories_to_check = [settings.textures_custom_dir, settings.uv_directory_custom]
        for index, menu in enumerate(custom_menu_options_to_check):
            if menu != "Custom":
                continue
            directory_checks_out, message = Functions.check_directory_path(self, context, directories_to_check[index])
            if not directory_checks_out:
                self.report({'ERROR'}, message)
                return {'FINISHED'}
                
        for index, custom_script in enumerate(scripts):
            custom_script_checks_out, message = Functions.check_custom_script_path(self, context, custom_script.file, custom_script.name)
            if not custom_script_checks_out:
                self.report({'ERROR'}, message)
                return {'FINISHED'}

        # Create path to Converter.py
        converter_py = Path(__file__).parent.resolve() / "Converter.py"

        self.file_count = 0

        # Transmogrify! (aka Batch Convert)
        self.transmogrify(context)

        # Report batch conversion results.
        if self.file_count == 0:
            self.report({'ERROR'}, "Could not convert.")
        else:
            converter_report_json = Path(__file__).parent.resolve() / "Converter_Report.json"
            converter_report_dict = Functions.read_json(converter_report_json)
            conversion_count = converter_report_dict["conversion_count"]
            if conversion_count > 1:
                self.report({'INFO'}, f"Conversion complete. {conversion_count} files were converted.")
            elif conversion_count == 1:
                self.report({'INFO'}, f"Conversion complete. {conversion_count} file was converted.")
            else:
                self.report({'INFO'}, f"Could not convert or no items needed conversion. {conversion_count} files were converted.")

        return {'FINISHED'}


    def select_children_recursive(self, obj, context):
        for c in obj.children:
            if obj.type in context.scene.transmogrifier.texture_resolution_include:
                c.select_set(True)
            self.select_children_recursive(c, context)


    def transmogrify(self, context):
        # Create settings_dict dictionary from transmogrifier_settings to pass to write_json function later.
        settings_dict = Functions.get_settings_dict(self, context, True, True)

        # Create path to blender.exe
        blender_dir = bpy.app.binary_path

        # Create path to Converter.blend
        converter_blend = Path(__file__).parent.resolve() / "Converter.blend"

        # Create path to Converter.py
        converter_py = Path(__file__).parent.resolve() / "Converter.py"
        
        # Create path to Transmogrifier directory
        transmogrifier_dir = Path(__file__).parent.resolve()

        # Write settings to JSON file.
        settings_json = Path(__file__).parent.resolve() / "Settings.json"
        Functions.write_json(settings_dict, settings_json)


        # Run Converter.py
        subprocess.call(
            [
                blender_dir,
                converter_blend,
                "--python",
                converter_py,
            ],
            cwd=transmogrifier_dir
        ) 
        

        print("Conversion Complete")
        self.file_count += 1


class TRANSMOGRIFIER_OT_forecast(Operator):
    """Calculate batch conversion and display info message of the forecast"""
    bl_idname = "transmogrifier.forecast"
    bl_label = "Forecast Conversion"

    def execute(self, context):
        settings = bpy.context.scene.transmogrifier_settings
        imports = bpy.context.scene.transmogrifier_imports
        exports = bpy.context.scene.transmogrifier_exports
        
        # Check if any imports exist.
        if not imports or not exports:
            if not imports:
                message = "Please Add Import"
            elif not exports:
                message = "Please Add Export"
            self.popup_message(context, message=message, title="Forecast", icon='INFO')
            self.report({'INFO'}, message)
            return {'FINISHED'}


        # Check to make sure import directories exist.
        for i in imports:
            directory_checks_out, message = Functions.check_directory_path(self, context, i.directory)
            if not directory_checks_out:
                self.report({'ERROR'}, message)
                return {'FINISHED'}
        
        # If import directories exist, get import files.
        import_files_dict = Functions.get_import_files(self, context)

        # Concatenate import formats with the respective number of files found for each.
        imports_string = ""
        count_total = 0
        for key, value in import_files_dict.items():
            count = len(import_files_dict[key])
            count_total += count
            imports_string += f"{count} {key}, "

        # Concatenate exports formats with the total count.
        exports_string = ""
        for index, instance in enumerate(exports):
            exports_string += f"{count_total} {instance.name}, "

        # Trim off ending space and comma.
        imports_string = imports_string[:-2]
        exports_string = exports_string[:-2]

        # Info message.
        message = f"{imports_string}  ⇒  {exports_string}"

        # Report message.
        self.popup_message(context, message=message, title="Forecast", icon='INFO')
        self.report({'INFO'}, message)
        return {'FINISHED'}


    # Message box pop-up.
    def popup_message(self, context, message="", title="Message Box", icon='INFO'):

        def draw(self, context):
            self.layout.label(text=message)

        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)



# Copy import/export/transmogrifier presets shipped with Transmogrifier to relevant Blender Preferences directory.
class TRANSMOGRIFIER_OT_copy_assets(Operator):
    """Copy example presets shipped with Transmogrifier to User Preferences"""
    bl_idname = "transmogrifier.copy_assets"
    bl_label = "Copy Assets to Preferences"

    def execute(self, context):
        # Define paths.
        assets_dir = Path(__file__).parent / "assets"
        presets_dir_src = assets_dir / "presets" / "operator"
        presets_dir_dest = bpy.utils.user_resource('SCRIPTS', path="presets/operator")

        # Make list of source paths and destination paths (parents).
        dir_src_list = [presets_dir_src]
        dir_dest_list = [presets_dir_dest]
        
        # Loop through list of source paths and copy files to parent- (or operator) specific destinations. Overwrite original files to ensure they get updated with each release.
        for dir_src in dir_src_list:
            for subdir, dirs, files in os.walk(dir_src):
                for file in files:
                    operator = Path(subdir).name
                    file_src = Path(subdir, file)
                    dir_dest_parent = dir_dest_list[dir_src_list.index(dir_src)]
                    file_dest = Path(dir_dest_parent, operator, file)
                    dir_dest = Path(file_dest).parent
                    if not Path(dir_dest).exists():
                        Path(dir_dest).mkdir(parents=True, exist_ok=True)
                    shutil.copy(file_src, file_dest)
        
        self.report({'INFO'}, "Copied Assets to Preferences")

        return {'FINISHED'}


class TRANSMOGRIFIER_OT_add_preset(Operator):
    """Creates a Transmogrifier preset from current settings"""
    bl_idname = "transmogrifier.add_preset"
    bl_label = "Add Transmogrifier Preset"

    # Captured preset name from pop-up dialog window.
    preset_name: bpy.props.StringProperty(name="Name", default="")

    def execute(self, context):
        # Set Transmogrifier operator preset directory and new preset file.
        add_preset_name = f"{self.preset_name}.json"
        transmogrifier_preset_dir = Path(bpy.utils.user_resource('SCRIPTS', path="presets/operator")) / "transmogrifier"
        if not Path(transmogrifier_preset_dir).exists():  # Check if operator preset directory exists.
            Path(transmogrifier_preset_dir).mkdir(parents=True, exist_ok=True)  # Make Transmogrifier operator preset directory.
        preset_json = transmogrifier_preset_dir / add_preset_name

        # Get current Transmogrifier settings.
        settings_dict = Functions.get_settings_dict(self, context, False, False)

        # Save new Transmogrifier operator preset as JSON file.
        Functions.write_json(settings_dict, preset_json)
        self.report({'INFO'}, f"Added Transmogrifier preset: {add_preset_name}")
        return {'FINISHED'}
    
    # Pop-up dialog window to capture new preset name.
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)
    

class TRANSMOGRIFIER_OT_remove_preset(Operator):
    """Removes currently selected Transmogrifier preset"""
    bl_idname = "transmogrifier.remove_preset"
    bl_label = "Remove Transmogrifier Preset"

    def execute(self, context):
        # Get selected Transmogrifier operator preset.
        settings = bpy.context.scene.transmogrifier_settings
        remove_preset_name = f"{settings.transmogrifier_preset_enum}.json"

        # Set Transmogrifier operator preset directory and preset file to be removed.
        transmogrifier_preset_dir = Path(bpy.utils.user_resource('SCRIPTS', path="presets/operator")) / "transmogrifier"
        if not Path(transmogrifier_preset_dir).exists():  # Check if operator preset directory exists.
            Path(transmogrifier_preset_dir).mkdir(parents=True, exist_ok=True)  # Make Transmogrifier operator preset directory.
        preset_json = transmogrifier_preset_dir / remove_preset_name

        # Return early and report error if Transmogrifier operator preset does not exist.
        if not preset_json.is_file():
            self.report({'ERROR'}, f"Transmogrifier preset does not exist: {remove_preset_name}")
            return {'CANCELLED'}

        # Remove Transmogrifier operator preset.
        self.report({'INFO'}, f"Removed Transmogrifier preset: {remove_preset_name}")
        Path.unlink(preset_json)
        return {'FINISHED'}


# Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), preset_manager.py, Line 124
class TRANSMOGRIFIER_OT_load_preset(Operator, ImportHelper):
    """Load a Transmogrifier preset from a JSON file"""
    bl_idname = "transmogrifier.load_preset"
    bl_label = "Load Preset"
    bl_options = {'UNDO'}

    filename_ext = '.json'

    filter_glob: StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )

    def execute(self, context):
        settings = bpy.context.scene.transmogrifier_settings
        
        # Get filepath from browser.
        preset_src = Path(self.filepath)

        # Get preset name.
        preset_name = preset_src.name
        
        # Check if Transmogrifier preset directory exists.
        transmogrifier_preset_dir = Path(bpy.utils.user_resource('SCRIPTS', path="presets/operator")) / "transmogrifier"
        if not Path(transmogrifier_preset_dir).exists():  # Check if operator preset directory exists.
            Path(transmogrifier_preset_dir).mkdir(parents=True, exist_ok=True)  # Make Transmogrifier operator preset directory.
        preset_dest = transmogrifier_preset_dir / preset_name
        
        # Copy preset file to preset directory.  Overwrite existing.
        shutil.copy(preset_src, preset_dest)
        
        # Concatenate the current property assignment.
        property_assignment = f"settings.transmogrifier_preset = {repr(preset_src.stem)}"

        # Make the property (key) equal to the preset (value).
        exec(property_assignment)
        
        # Load preset (Update settings and UI from preset file).
        Functions.set_settings(self, context)

        self.report({'INFO'}, f"Added Transmogrifier preset: {preset_name}")
        return {'FINISHED'}


# Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 782
class TRANSMOGRIFIER_OT_add_import(Operator):
    '''Add new import to UI'''

    bl_idname = "transmogrifier.add_import"
    bl_label = "Add Import"
    bl_description = "Add new import to UI"

    def execute(self, context):
        new_import = context.scene.transmogrifier_imports.add()
        new_import.name = new_import.format
        Functions.link_import_directories(self, context)
        return {'FINISHED'}


class TRANSMOGRIFIER_OT_remove_import(Operator):
    '''Remove import from UI'''

    bl_idname = "transmogrifier.remove_import"
    bl_label = "Remove Import"
    bl_description = "Remove import from UI"

    index: IntProperty(
        name="Index to remove",
        description="Index of the import to remove",
        min=0, 
    )   

    def execute(self, context):
        context.scene.transmogrifier_imports.remove(self.index)
        return {'FINISHED'}


# Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 782
class TRANSMOGRIFIER_OT_add_export(Operator):
    '''Add new export to UI'''

    bl_idname = "transmogrifier.add_export"
    bl_label = "Add Export"
    bl_description = "Add new export to UI"

    def execute(self, context):
        new_export = context.scene.transmogrifier_exports.add()
        Functions.link_export_settings(self, context)
        return {'FINISHED'}


class TRANSMOGRIFIER_OT_remove_export(Operator):
    '''Remove export from UI'''

    bl_idname = "transmogrifier.remove_export"
    bl_label = "Remove Export"
    bl_description = "Remove export from UI"

    index: IntProperty(
        name="Index to remove",
        description="Index of the export to remove",
        min=0, 
    )   

    def execute(self, context):
        context.scene.transmogrifier_exports.remove(self.index)
        return {'FINISHED'}


# Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), UI.py, Line 782
class TRANSMOGRIFIER_OT_add_custom_script(Operator):
    '''Add new custom script to UI'''

    bl_idname = "transmogrifier.add_custom_script"
    bl_label = "Add Script"
    bl_description = "Add new custom script to UI"

    def execute(self, context):
        # Import Functions
        Functions.add_custom_script(self, context)
        Functions.update_custom_script_names(self, context)
        return {'FINISHED'}


class TRANSMOGRIFIER_OT_remove_custom_script(Operator):
    '''Remove custom script from UI'''

    bl_idname = "transmogrifier.remove_custom_script"
    bl_label = "Remove Custom Script"
    bl_description = "Remove custom script from UI"

    custom_script_index: IntProperty(
        name="Index to remove",
        description="Index of the custom script to remove",
        min=0, 
    )   

    def execute(self, context):
        context.scene.transmogrifier_scripts.remove(self.custom_script_index)
        Functions.update_custom_script_names(self, context)
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
    TRANSMOGRIFIER_OT_transmogrify,
    TRANSMOGRIFIER_OT_forecast,
    TRANSMOGRIFIER_OT_copy_assets,
    TRANSMOGRIFIER_OT_add_preset,
    TRANSMOGRIFIER_OT_remove_preset,
    TRANSMOGRIFIER_OT_load_preset,
    TRANSMOGRIFIER_OT_add_import, 
    TRANSMOGRIFIER_OT_remove_import,
    TRANSMOGRIFIER_OT_add_export, 
    TRANSMOGRIFIER_OT_remove_export, 
    TRANSMOGRIFIER_OT_add_custom_script,
    TRANSMOGRIFIER_OT_remove_custom_script,
)

# Register Classes.
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

# Unregister Classes.
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)