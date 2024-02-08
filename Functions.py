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
from pathlib import Path
import glob
import re
import json
from mathutils import Vector, Euler



#  ███████████ █████  █████ ██████   █████   █████████  ███████████ █████    ███████    ██████   █████  █████████ 
# ░░███░░░░░░█░░███  ░░███ ░░██████ ░░███   ███░░░░░███░█░░░███░░░█░░███   ███░░░░░███ ░░██████ ░░███  ███░░░░░███
#  ░███   █ ░  ░███   ░███  ░███░███ ░███  ███     ░░░ ░   ░███  ░  ░███  ███     ░░███ ░███░███ ░███ ░███    ░░░ 
#  ░███████    ░███   ░███  ░███░░███░███ ░███             ░███     ░███ ░███      ░███ ░███░░███░███ ░░█████████ 
#  ░███░░░█    ░███   ░███  ░███ ░░██████ ░███             ░███     ░███ ░███      ░███ ░███ ░░██████  ░░░░░░░░███
#  ░███  ░     ░███   ░███  ░███  ░░█████ ░░███     ███    ░███     ░███ ░░███     ███  ░███  ░░█████  ███    ░███
#  █████       ░░████████   █████  ░░█████ ░░█████████     █████    █████ ░░░███████░   █████  ░░█████░░█████████ 
# ░░░░░         ░░░░░░░░   ░░░░░    ░░░░░   ░░░░░░░░░     ░░░░░    ░░░░░    ░░░░░░░    ░░░░░    ░░░░░  ░░░░░░░░░  


# ░█▀▄░█▀▀░█▀▀░█▀▄░█▀▀░█▀▀░█░█░░░█░█░▀█▀
# ░█▀▄░█▀▀░█▀▀░█▀▄░█▀▀░▀▀█░█▀█░░░█░█░░█░
# ░▀░▀░▀▀▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░▀▀▀

# Refresh UI when a Transmogrifier preset is selected.
def refresh_ui(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    imports = bpy.context.scene.transmogrifier_imports
    scripts = bpy.context.scene.transmogrifier_scripts

    if settings.transmogrifier_preset != "NO_PRESET":
        # Load selected Transmogrifier preset as a dictionary.
        transmogrifier_preset_dict = load_transmogrifier_preset('transmogrifier', settings.transmogrifier_preset)
        imports.clear() # Clear any existing imports instances.
        scripts.clear()  # Clear any existing custom script instances.

        # Read dictionary and change UI settings to reflect selected preset.
        for key, value in transmogrifier_preset_dict.items():
            if key == "imports":
                load_imports(value)  # Load imports from JSON file.
                continue
            if key == "scripts":
                load_custom_scripts(value)  # Load custom scripts from JSON file.
                continue
            # Make sure double-backslashes are preserved in directory path.
            directories_set = ("import_directory", "directory_output_custom", "textures_custom_dir", "uv_directory_custom")
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
            if key in ("texture_resolution", "resize_textures_limit", "uv_resolution") and type(value) == int:
                value = "'" + str(value) + "'"   
            # Concatenate the current variable/setting to be updated.
            update_setting = 'settings.' + str(key) + ' = ' + str(value)
            # Make the setting (key) equal to the preset (value)
            exec(update_setting)


# ░█▀█░█▀█░█▀▀░█▀▄░█▀█░▀█▀░█▀█░█▀▄░░░█▀█░█▀▄░█▀▀░█▀▀░█▀▀░▀█▀░█▀▀
# ░█░█░█▀▀░█▀▀░█▀▄░█▀█░░█░░█░█░█▀▄░░░█▀▀░█▀▄░█▀▀░▀▀█░█▀▀░░█░░▀▀█
# ░▀▀▀░▀░░░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀░░░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀

# A Dictionary of operator_name: [list of preset EnumProperty item tuples].
# Blender's doc warns that not keeping reference to enum props array can
# cause crashs and weird issues.
# Also useful for the get_preset_index function.
preset_enum_items_refs = {
    "wm.collada_import": [],
    "wm.alembic_import": [], 
    "wm.usd_import": [],
    "wm.obj_import": [],
    "import_scene.fbx": [],
    "import_scene.x3d": [],
    "NO_OPERATOR": [],
}

# Returns a list of tuples used for an EnumProperty's items (identifier, name, description)
# identifier, and name are the file name of the preset without the file extension (.py)
def get_operator_presets(operator):
    presets = [('NO_PRESET', "(no preset)", "", 0)]
    for d in bpy.utils.script_paths(subdir="presets/operator/" + operator):
        for f in Path(d).iterdir():
            if f.suffix != ".py":
                continue
            f = Path(f).stem
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
        if Path(fp).is_file():  # Found the preset file
            print(f"Using preset {fp}")
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


# ░▀█▀░█▀▄░█▀█░█▀█░█▀▀░█▄█░█▀█░█▀▀░█▀▄░▀█▀░█▀▀░▀█▀░█▀▀░█▀▄░░░█▀█░█▀▄░█▀▀░█▀▀░█▀▀░▀█▀░█▀▀
# ░░█░░█▀▄░█▀█░█░█░▀▀█░█░█░█░█░█░█░█▀▄░░█░░█▀▀░░█░░█▀▀░█▀▄░░░█▀▀░█▀▄░█▀▀░▀▀█░█▀▀░░█░░▀▀█
# ░░▀░░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░░░▀▀▀░▀▀▀░▀░▀░░░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀

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
        for f in Path(d).iterdir():
            if f.suffix != ".json":
                continue
            f = Path(f).stem
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
        if Path(fp).is_file():  # Found the preset file
            print(f"Using preset {fp}")
            
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


# ░▀█▀░█▀█░█▀▀░█▀█░░░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀
# ░░█░░█░█░█▀▀░█░█░░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀
# ░▀▀▀░▀░▀░▀░░░▀▀▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀

# Traverse a given directory for a given file type and return a list of files.
def get_files_in_directory_tree(self, context, directory, extension):
    files = glob.glob(f"{directory}/**/*{extension}", recursive=True)

    # Convert list items to pathlib Paths.
    if files:
        files = [Path(file) for file in files]

    return files

# Count how many files of a given type are in a given directory.
def count_files_in_directory_tree(self, context, directory, extension):
    files = get_files_in_directory_tree(self, context, directory, extension)

    if not files:
        file_count = 0
        return file_count
    
    file_count = len(files)
    return(file_count)

def get_import_ext(self, context, settings):
    # Get import directory
    import_directory = settings.import_directory

    # Get import extension
    import_ext = f".{settings.import_file}".lower()
    
    # Adjust for USD- and glTF-specific extensions
    if settings.import_file == 'USD':
        import_ext = settings.import_usd_extension
    elif settings.import_file == 'glTF':
        import_ext = settings.import_gltf_extension
        
    return import_ext

def update_batch_convert_info_message(self, context):
    # Get variables.
    settings = bpy.context.scene.transmogrifier_settings
    import_directory = settings.import_directory
    import_ext = get_import_ext(self, context, settings)

    # Check if directory is absolute and if Blender session is saved.
    if (Path(import_directory) != Path(bpy.path.abspath(import_directory)).resolve() or import_directory == "") and not bpy.data.is_saved:
        settings.batch_convert_info_message = f"0 {settings.import_file} files detected."
        return

    # Change path to absolute directory.
    import_directory = Path(bpy.path.abspath(import_directory)).resolve()
    # Count models that will be imported.
    models_to_import = count_files_in_directory_tree(self, context, import_directory, import_ext)

    # Check if there are models to import and export.
    if models_to_import and settings.model_quantity != "No Formats":
        if settings.model_quantity == "1 Format":
            settings.batch_convert_info_message = f"{models_to_import} {settings.import_file} ⇒ {models_to_import} {settings.export_file_1}"
        elif settings.model_quantity == "2 Formats":
            settings.batch_convert_info_message = f"{models_to_import} {settings.import_file} ⇒ {models_to_import} {settings.export_file_1} + {models_to_import} {settings.export_file_2}"
    elif not models_to_import:
        settings.batch_convert_info_message = f"{models_to_import} {settings.import_file} files detected."


# ░▀█▀░█▄█░█▀█░█▀█░█▀▄░▀█▀░█▀▀
# ░░█░░█░█░█▀▀░█░█░█▀▄░░█░░▀▀█
# ░▀▀▀░▀░▀░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀

# Load imports from JSON file.
def load_imports(imports):
    for import_file in imports:
        load_import = bpy.context.scene.transmogrifier_imports.add()
        for key, value in import_file.items():
            # Concatenate the current import property assignment.
            property_assignment = f"load_import.{key} = {repr(str(value))}"
            # Make the property (key) equal to the preset (value).
            exec(property_assignment)
        
# Import format dictionary containing [operator preset directory name, operator, options dictionary].
import_dict = {
    "DAE": ["wm.collada_import", "bpy.ops.wm.collada_import(**", {}],
    "ABC": ["wm.alembic_import", "bpy.ops.wm.alembic_import('EXEC_REGION_WIN', **", {}], 
    "USD": ["wm.usd_import", "bpy.ops.wm.usd_import(**", {}],
    "OBJ": ["wm.obj_import", "bpy.ops.wm.obj_import(**", {}],
    "PLY": ["NO_OPERATOR", "bpy.ops.import_mesh.ply(**", {}], 
    "STL": ["NO_OPERATOR", "bpy.ops.import_mesh.stl(**", {}],
    "FBX": ["import_scene.fbx", "bpy.ops.import_scene.fbx(**", {}],
    "glTF": ["NO_OPERATOR", "bpy.ops.import_scene.gltf(**", {}],
    "X3D": ["import_scene.x3d", "bpy.ops.import_scene.x3d(**", {}],
    "BLEND": ["NO_OPERATOR", "bpy.ops.wm.append(**", {
        "filepath": "",
        "directory": "\\Object\\",
        "autoselect": True,
        "active_collection": True,
        "instance_collections": False,
        "instance_object_data": True,
        "set_fake": False,
        "use_recursive": True,
    }],
}

# Get operator options for a given preset for a given format.
def get_operator_options(format, preset):
    options = import_dict[format][2]
    if import_dict[format][0] == "NO_OPERATOR":
        return options
    
    options = load_operator_preset(import_dict[format][0], preset)
    return options

# Update import file names and operators based on file formats.
def update_import_settings(self, context):
    for index, import_file in enumerate(context.scene.transmogrifier_imports):
        # Update box name from import extension.
        import_file.name = import_file.extension.upper()[1:]
        
        # Update import preset from current preset_enum.
        import_file.preset = import_file.preset_enum

        # Update import operator and options
        format = import_file.format
        preset = import_file.preset
        import_file.operator = f"{import_dict[format][1]}"
        import_file.options = str(get_operator_options(format, preset))

# Synchronize import directories with master directory.
def update_import_directories(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    for index, import_file in enumerate(context.scene.transmogrifier_imports):
        import_file.directory = settings.import_directory


# ░█▀▀░█░█░▀█▀░█▀▀░█▀█░█▀▀░▀█▀░█▀█░█▀█░█▀▀
# ░█▀▀░▄▀▄░░█░░█▀▀░█░█░▀▀█░░█░░█░█░█░█░▀▀█
# ░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀

# Dictionary of import/export file extensions.  glTF and USD get updated with additional extensions when User selects those formats.
format_extension_enum_items_refs = {
    "DAE": [(".dae", ".dae", "", 0)],
    "ABC": [(".abc", ".abc", "", 0)],
    "USD": [(".usd", ".usd", "", 0)],
    "OBJ": [(".obj", ".obj", "", 0)],
    "PLY": [(".ply", ".ply", "", 0)],
    "STL": [(".stl", ".stl", "", 0)],
    "FBX": [(".fbx", ".fbx", "", 0)],
    "glTF": [(".gltf", ".gltf", "", 0)],
    "X3D": [(".x3d", ".x3d", "", 0)],
    "BLEND": [(".blend", ".blend", "", 0)],
}

# Get file extension(s) for a given format.
def get_format_extensions(format):
    # Convert format to extension.
    extensions = [(f".{format.lower()}", f".{format.lower()}", "", 0)]

    # USD extensions.
    if format == "USD":
        extensions = [
            (".usdz", "Zipped (.usdz)", "Packs textures and references into one file", 0),
            (".usdc", "Binary Crate (default) (.usdc)", "Binary, fast, hard to edit", 1),
            (".usda", "ASCII (.usda)", "ASCII Text, slow, easy to edit", 2),
            (".usd", "Plain (.usd)", "Can be either binary or ASCII\nIn Blender this imports to binary", 3),
        ]

    # glTF extensions.
    elif format == "glTF":
        extensions = [
            (".glb", "glTF Binary (.glb)", "", 0),
            (".gltf", "glTF Embedded or Separate (.gltf)", "", 1),
        ]

    # Replace dictionary entry for given format with updated extension(s).
    format_extension_enum_items_refs[format] = extensions

    # Return list of extension items.
    return extensions


# ░█▀█░█▀▀░█▀▀░█▀▀░▀█▀░█▀▀
# ░█▀█░▀▀█░▀▀█░█▀▀░░█░░▀▀█
# ░▀░▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀

# A dictionary of one key with a value of a list of asset libraries.
asset_library_enum_items_refs = {"asset_libraries": []}

# Get asset libraries and return a list of them.  Add them as the value to the dictionary.
def get_asset_libraries():
    libraries_list = [('NO_LIBRARY', "(no library)", "Don't move .blend files containing assets to a library.\nInstead, save .blend files adjacent converted items.", 0)]
    asset_libraries = bpy.context.preferences.filepaths.asset_libraries
    for asset_library in asset_libraries:
        library_name = asset_library.name
        libraries_list.append((library_name, library_name, ""))

    asset_library_enum_items_refs["asset_libraries"] = libraries_list

    return libraries_list

# Get index of selected asset library in asset_library_enum property based on its position in the dictionary value list.
def get_asset_library_index(library_name):
    for l in range(len(asset_library_enum_items_refs["asset_libraries"])):
        if asset_library_enum_items_refs["asset_libraries"][l][0] == library_name:
            return l
    return 0


# A dictionary of one key with a value of a list of asset catalogs.
asset_catalog_enum_items_refs = {"asset_catalogs": []}

# Get asset catalogs and return a list of them.  Add them as the value to the dictionary.
def get_asset_catalogs():
    catalogs_list = [('NO_CATALOG', "(no catalog)", "Don't assign assets to a catalog.", 0)]
    settings = bpy.context.scene.transmogrifier_settings
    asset_libraries = bpy.context.preferences.filepaths.asset_libraries
    library_name = settings.asset_library
    library_path = [library.path for library in asset_libraries if library.name == library_name]
    if library_path:  # If the list is not empty, then it found a library path.
        library_path = Path(library_path[0])
        catalog_file = library_path / "blender_assets.cats.txt"
        if catalog_file.is_file():  # Check if catalog file exists
            with catalog_file.open() as f:
                for line in f.readlines():
                    if line.startswith(("#", "VERSION", "\n")):
                        continue
                    # Each line contains : 'uuid:catalog_tree:catalog_name' + eol ('\n')
                    uuid = line.split(":")[0]
                    catalog_name = line.split(":")[2].split("\n")[0]
                    catalogs_list.append((uuid, catalog_name, ""))

    asset_catalog_enum_items_refs["asset_catalogs"] = catalogs_list

    return catalogs_list

# Get index of selected asset catalog in asset_catalog_enum property based on its position in the dictionary value list.
def get_asset_catalog_index(catalog_name):
    for l in range(len(asset_catalog_enum_items_refs["asset_catalogs"])):
        if asset_catalog_enum_items_refs["asset_catalogs"][l][0] == catalog_name:
            return l
    return 0


# ░█▀▀░█░█░█▀▀░▀█▀░█▀█░█▄█░░░█▀▀░█▀▀░█▀▄░▀█▀░█▀█░▀█▀░█▀▀
# ░█░░░█░█░▀▀█░░█░░█░█░█░█░░░▀▀█░█░░░█▀▄░░█░░█▀▀░░█░░▀▀█
# ░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░░░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░░░░▀░░▀▀▀

# Load custom scripts from a JSON file.
def load_custom_scripts(custom_scripts):
    for script in custom_scripts:
        load_script = bpy.context.scene.transmogrifier_scripts.add()
        load_script.name = script["name"]
        load_script.file = script["file"]
        load_script.trigger = script["trigger"]

# Add a custom script.
def add_custom_script(self, context):
    new_script = context.scene.transmogrifier_scripts.add()
    new_script.name = Path(new_script.file).name

# Update custom script names based on file names.
def update_custom_script_names(self, context):
    for index, custom_script in enumerate(context.scene.transmogrifier_scripts):
        file = Path(bpy.path.abspath(custom_script.file)).resolve()

        # Added a new custom script (default name is "*.py")
        if custom_script.file == "*.py"  and file.name == "*.py":
            custom_script.name = f"Script {index + 1}"
        
        # File is not a Python file.
        elif file.suffix != ".py":
            custom_script.name = f"(Not a Python File) {file.name}"

        # File is a Python file but doesn't exist.
        elif not file.is_file() and file.suffix == ".py":
            custom_script.name = f"(Missing) {file.name}"

        # File is a Python file and might exist, but path is relative and current Blend session is unsaved.
        elif file != Path(custom_script.file) and not bpy.data.is_saved:
            custom_script.name = f"(Missing) {file.name}"

        # File is a Python file and exists.
        elif file.is_file() and file.suffix == ".py":
            custom_script.name = file.name


# ░█▀▀░█▀▀░▀█▀░░░█▀▀░█▀▀░▀█▀░▀█▀░▀█▀░█▀█░█▀▀░█▀▀
# ░█░█░█▀▀░░█░░░░▀▀█░█▀▀░░█░░░█░░░█░░█░█░█░█░▀▀█
# ░▀▀▀░▀▀▀░░▀░░░░▀▀▀░▀▀▀░░▀░░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀

# Check if a value is an integer.
def is_int(x):
    try:
        x = int(x)
    except (TypeError, ValueError):
        return False
    else:
        return True

# Get properties of an individual PropertyGroup instance.
def get_properties(propertygroup, use_absolute_paths):
    keys = [key for key in propertygroup.__annotations__ if "enum" not in key]
    values = []
    for key in keys:
        value = eval(f"propertygroup.{key}")
        
        # Check if value is a file or directory path.  If so, and if writing to Settings.json, make it absolute.
        if use_absolute_paths and Path(bpy.path.abspath(str(value))).resolve().exists() and value != "":
            value = str(Path(bpy.path.abspath(value)).resolve())

        # Convert value to integer if it's formatted as a string (for EnumProperty numeric values)
        elif isinstance(value, str) and is_int(value):
            value = int(value)

        # Convert set to tuple.
        elif isinstance(value, set):
            value = tuple(value)
        
        # Convert Vector or Euler to tuple.
        elif isinstance(value, Vector) or isinstance(value, Euler):
            value = [value[0], value[1], value[2]]

        # Append value to list.
        values.append(value)
    
    settings_dict = dict(zip(keys, values))

    return settings_dict

# Loop through instances in an CollectionProperty group and return dictionaries of them.
def get_propertygroups(propertygroup, name, is_collection_property, use_absolute_paths, settings_dict):
    # If PropertyGroup is a CollectionProperty, list the existing instances.
    if is_collection_property: 
        propertygroups = [instance for index, instance in enumerate(propertygroup)]
        collection_of_settings = []
        
        # Loop through each instance, get a dictionary of properties for each, and add each set of properties to the list.
        for propertygroup in propertygroups:
            collection_of_settings.append(get_properties(propertygroup, use_absolute_paths))
        
        # Update the settings dictionary with every instance.
        settings_dict.update({name: collection_of_settings})
    
    # If PropertyGroup is a PointerProperty, simply get a dictionary of properties from it.
    elif not is_collection_property:
        settings_dict.update(get_properties(propertygroup, use_absolute_paths))

    return settings_dict

# Create settings_dict dictionary from PropertyGroups to pass to write_json function later.
def get_settings_dict(self, context, use_absolute_paths):
    settings_dict = {}

    # List all PropertyGroups whose properties need recorded in either Settings.json or a [Transmogrifier_Preset].json.
    property_groups = [
        [bpy.context.scene.transmogrifier_settings, "settings", False, use_absolute_paths],
        [bpy.context.scene.transmogrifier_imports, "imports", True, use_absolute_paths],
        [bpy.context.scene.transmogrifier_scripts, "scripts", True, use_absolute_paths]
    ]

    # Loop through each PropertyGroup and update the dictionary of settings.
    for propertygroup in property_groups:
        settings_dict.update(get_propertygroups(propertygroup[0], propertygroup[1], propertygroup[2], propertygroup[3], settings_dict))

    return settings_dict


# ░▀▀█░█▀▀░█▀█░█▀█░░░█░█░▀█▀░▀█▀░█░░░▀█▀░▀█▀░▀█▀░█▀▀░█▀▀
# ░░░█░▀▀█░█░█░█░█░░░█░█░░█░░░█░░█░░░░█░░░█░░░█░░█▀▀░▀▀█
# ░▀▀░░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀

# Write user variables to a JSON file.
def write_json(settings_dict, json_file):
        
    with open(json_file, "w") as outfile:
        json.dump(settings_dict, outfile)


# Read the JSON file where the conversion count is stored.
def read_json():
    # Open JSON file
    json_file = Path(__file__).parent.resolve() / "Converter_Report.json"

    with open(json_file, 'r') as openfile:
    
        # Read from JSON file
        json_object = json.load(openfile)
    
    return json_object