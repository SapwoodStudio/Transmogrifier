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



# ░▀█▀░█▄█░█▀█░█▀█░█▀▄░▀█▀░█▀▀
# ░░█░░█░█░█▀▀░█░█░█▀▄░░█░░▀▀█
# ░▀▀▀░▀░▀░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀

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


# Traverse a given directory for a given file type and return a dictionary of files.
def get_import_files(self, context):
    imports = bpy.context.scene.transmogrifier_imports

    import_files_dict = {}

    for i in imports:
        directory = str(Path(bpy.path.abspath(i.directory)).resolve())
        files = glob.glob(f"{directory}/**/*{i.extension}", recursive=True)
        import_files_dict[i.name] = files

    return import_files_dict



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



# ░█▀▀░█░█░█▀▀░█▀▀░█░█░░░█▀█░█▀█░▀█▀░█░█░█▀▀
# ░█░░░█▀█░█▀▀░█░░░█▀▄░░░█▀▀░█▀█░░█░░█▀█░▀▀█
# ░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░░░▀░░░▀░▀░░▀░░▀░▀░▀▀▀

# Stop batch converter and update info message if directory has not been selected or .blend file has not been saved.
def check_directory_path(self, context, directory):
    # Check if path is absolute and if blend file has been saved.
    if Path(directory) != Path(bpy.path.abspath(directory)).resolve() and not bpy.data.is_saved:
        message = f"Cannot find directory: {Path(bpy.path.abspath(directory)).resolve().name}.  \nSave .blend file somewhere before using a relative directory path\n(or use an absolute directory path instead)"
        return False, message
    
    # Convert to absolute path.
    directory = Path(bpy.path.abspath(directory)).resolve()
    
    # Check if directory exists.
    if not directory.is_dir():
        message = f"Directory doesn't exist: {directory.name}"
        return False, message
    
    message = "Directory checks out"
    return True, message


# Stop batch converter if script has not been selected or .blend file has not been saved.
def check_custom_script_path(self, context, filepath, name):
    # Check if file is a Python file.
    if Path(filepath).suffix != ".py":
        message = f"Custom Script is not a Python file: {Path(filepath).name}"
        return False, message
    
    # Check if path is absolute and if blend file has been saved.
    if Path(filepath) != Path(bpy.path.abspath(filepath)).resolve() and not bpy.data.is_saved:
        message = f"Cannot find Custom Script: {Path(filepath).name}. \nSave .blend file somewhere before using a relative script path\n(or use an absolute script path instead)"
        return False, message
    
    # Convert to absolute path.
    filepath = Path(bpy.path.abspath(filepath)).resolve()
    
    # Check if Python file exists.
    if filepath.suffix == ".py" and not filepath.is_file():
        message = f"Custom Script doesn't exist: {filepath.name}"
        return False, message
    
    message = "Script path checks out"
    return True, message



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



# ░█▀█░█▀▄░█▀█░█▀█░█▀▀░█▀▄░▀█▀░█░█░░░█▀▀░█▀▄░█▀█░█░█░█▀█░█▀▀
# ░█▀▀░█▀▄░█░█░█▀▀░█▀▀░█▀▄░░█░░░█░░░░█░█░█▀▄░█░█░█░█░█▀▀░▀▀█
# ░▀░░░▀░▀░▀▀▀░▀░░░▀▀▀░▀░▀░░▀░░░▀░░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░░░▀▀▀

# Get a list of all PropertyGroups whose properties need recorded/read to/from either Settings.json or a [Transmogrifier_Preset].json.
# Used for Get Settings and Set Settings.
# [PropertyGroup, name, is a CollectionProperty, properties to ignore]
def get_propertygroups():
    property_groups = {
        "settings": [bpy.context.scene.transmogrifier_settings, False, [
            "advanced_ui",
            "transmogrifier_preset",
            ]
        ],
        "imports": [bpy.context.scene.transmogrifier_imports, True, []],
        "scripts": [bpy.context.scene.transmogrifier_scripts, True, []],
    }
    
    return property_groups



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
def get_properties(propertygroup, properties_to_ignore, use_absolute_paths):
    keys = [key for key in propertygroup.__annotations__ if key not in properties_to_ignore and "_enum" not in key]  # Eventually remove the need for "_enum" condition.
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


# Loop through instances in a CollectionProperty group and return dictionary of them.
def get_propertygroups_properties(name, propertygroup, is_collection_property, properties_to_ignore, use_absolute_paths, settings_dict):
    # If PropertyGroup is a CollectionProperty, list the existing instances.
    if is_collection_property: 
        propertygroups = [instance for index, instance in enumerate(propertygroup)]
        collection_of_settings = []
        
        # Loop through each instance, get a dictionary of properties for each, and add each set of properties to the list.
        for propertygroup in propertygroups:
            collection_of_settings.append(get_properties(propertygroup, properties_to_ignore, use_absolute_paths))
        
        # Update the settings dictionary with every instance.
        settings_dict.update({name: collection_of_settings})
    
    # If PropertyGroup is a PointerProperty, simply get a dictionary of properties from it.
    elif not is_collection_property:
        settings_dict.update(get_properties(propertygroup, properties_to_ignore, use_absolute_paths))

    return settings_dict


# Create settings_dict dictionary from PropertyGroups to pass to write_json function later.
def get_settings_dict(self, context, use_absolute_paths):
    settings_dict = {}
    property_groups = get_propertygroups()

    # Loop through each PropertyGroup and update the dictionary of settings.
    for key, value in property_groups.items():
        settings_dict.update(get_propertygroups_properties(key, value[0], value[1], value[2], use_absolute_paths, settings_dict))

    return settings_dict
    


# ░█▀▀░█▀▀░▀█▀░░░█▀▀░█▀▀░▀█▀░▀█▀░▀█▀░█▀█░█▀▀░█▀▀
# ░▀▀█░█▀▀░░█░░░░▀▀█░█▀▀░░█░░░█░░░█░░█░█░█░█░▀▀█
# ░▀▀▀░▀▀▀░░▀░░░░▀▀▀░▀▀▀░░▀░░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀

# Load/set each property within a given PropertyGroup.
def load_propertygroup_settings(property_groups, properties, group):
    # Loop through each property in the PropertyGroup and load/set value from the given Transmogrifier preset.
    for key, value in properties.items():
        # If a property name shares the same name of a PropertyGroup, skip.  The value is a list of dictionaries of properties of each instance that will be looped through later.
        if key in property_groups:
            continue
        
        # Wrap strings in quotations to ensure they're interpreted as strings in exec() function below.
        elif isinstance(value, str):
            value = repr(value)

        # If a value is a list that contains strings, then change the list to a set.
        elif isinstance(value, list) and isinstance(value[0], str):
            value = set(value)

        # If an integer is an option of a certain EnumProperty drop down, make it a string.
        elif key in ("texture_resolution", "resize_textures_limit", "uv_resolution") and isinstance(value, int):
            value = repr(str(value))

        # Concatenate the current property assignment.
        property_assignment = f"group.{key} = {value}"

        # Make the property (key) equal to the preset (value).
        exec(property_assignment)


# If PropertyGroup is a CollectionProperty, instantiate and load settings for each instance.
def instantiate_propertygroups(property_groups, properties_list, propertygroup):
    for properties in properties_list:
        # Add new instance.
        group = propertygroup.add()

        # Load/set properties for that group.
        load_propertygroup_settings(property_groups, properties, group)
        

# Update settings when a Transmogrifier preset is selected.
def set_settings(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    imports = bpy.context.scene.transmogrifier_imports
    scripts = bpy.context.scene.transmogrifier_scripts

    # Get PropertyGroups.
    property_groups = get_propertygroups()

    if settings.transmogrifier_preset != "NO_PRESET":
        # Load selected Transmogrifier preset as a dictionary.
        transmogrifier_preset_dict = load_transmogrifier_preset('transmogrifier', settings.transmogrifier_preset)

        # Clear any existing imports instances.
        imports.clear()
        
        # Clear any existing custom script instances.
        scripts.clear()

        # Loop through each PropertyGroup ("settings", "imports", etc.)
        for key, value in property_groups.items():
            try:
                # If PropertyGroup is not a CollectionProperty, go straight to loading/setting the properties from the preset.
                if value[1] == False:
                    load_propertygroup_settings(property_groups, transmogrifier_preset_dict, value[0])
                
                # If PropertyGroup is a CollectionProperty, instantiate and load settings for each instance.
                else:
                    instantiate_propertygroups(property_groups, transmogrifier_preset_dict[key], value[0])

            # If using an old Transmogrifier preset (i.e. without new properties such as "imports" and "scripts"), skip.
            except KeyError:
                continue



# ░▀▀█░█▀▀░█▀█░█▀█░░░█░█░▀█▀░▀█▀░█░░░▀█▀░▀█▀░▀█▀░█▀▀░█▀▀
# ░░░█░▀▀█░█░█░█░█░░░█░█░░█░░░█░░█░░░░█░░░█░░░█░░█▀▀░▀▀█
# ░▀▀░░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀

# Write user variables to a JSON file.
def write_json(settings_dict, json_file):
        
    with open(json_file, "w") as outfile:
        json.dump(settings_dict, outfile)


# Read the JSON file and return contents.
def read_json(json_file):
    # Open JSON file
    with open(json_file, 'r') as openfile:
    
        # Read from JSON file
        json_object = json.load(openfile)
    
    return json_object