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
import re
import json



#  ███████████ █████  █████ ██████   █████   █████████  ███████████ █████    ███████    ██████   █████  █████████ 
# ░░███░░░░░░█░░███  ░░███ ░░██████ ░░███   ███░░░░░███░█░░░███░░░█░░███   ███░░░░░███ ░░██████ ░░███  ███░░░░░███
#  ░███   █ ░  ░███   ░███  ░███░███ ░███  ███     ░░░ ░   ░███  ░  ░███  ███     ░░███ ░███░███ ░███ ░███    ░░░ 
#  ░███████    ░███   ░███  ░███░░███░███ ░███             ░███     ░███ ░███      ░███ ░███░░███░███ ░░█████████ 
#  ░███░░░█    ░███   ░███  ░███ ░░██████ ░███             ░███     ░███ ░███      ░███ ░███ ░░██████  ░░░░░░░░███
#  ░███  ░     ░███   ░███  ░███  ░░█████ ░░███     ███    ░███     ░███ ░░███     ███  ░███  ░░█████  ███    ░███
#  █████       ░░████████   █████  ░░█████ ░░█████████     █████    █████ ░░░███████░   █████  ░░█████░░█████████ 
# ░░░░░         ░░░░░░░░   ░░░░░    ░░░░░   ░░░░░░░░░     ░░░░░    ░░░░░    ░░░░░░░    ░░░░░    ░░░░░  ░░░░░░░░░  

# Refresh UI when a Transmogrifier preset is selected.
def refresh_ui(self, context):
    settings = bpy.context.scene.TransmogrifierSettings

    if settings.transmogrifier_preset != "NO_PRESET":
        # Load selected Transmogrifier preset as a dictionary.
        transmogrifier_preset_dict = load_transmogrifier_preset('transmogrifier', settings.transmogrifier_preset)

        # Read dictionary and change UI settings to reflect selected preset.
        for key, value in transmogrifier_preset_dict.items():
            # Make sure double-backslashes are preserved in directory path.
            directories_set = ("directory", "directory_output_custom", "textures_custom_dir", "uv_directory_custom")
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
    settings = bpy.context.scene.TransmogrifierSettings
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



# Create variables_dict dictionary from TransmogrifierSettings to pass to write_json function later.
def get_transmogrifier_settings(self, context):
    settings = bpy.context.scene.TransmogrifierSettings
    keys = [key for key in settings.__annotations__ if "enum" not in key]
    values = []
    for key in keys:
        # Get value as string to be evaluated later.
        value = eval('settings.' + str(key))
        # Convert relative paths to absolute paths.
        directory_path = ("directory", "directory_output_custom", "textures_custom_dir", "uv_directory_custom")
        if key in directory_path:
            value = bpy.path.abspath(value)
        # Convert enumproperty numbers to numbers.
        if key == "texture_resolution" or key == "resize_textures_limit" or key == "uv_resolution":
            if value != "Default":
                value = int(value)
        # Convert dictionaries and vectors to tuples.
        if "{" in str(value):
            value = tuple(value)
        elif "<" in str(value):
            value = str(value)
            char_start = "("
            char_end = ")"
            value = eval(re.sub('[xyz=]', '', "(" + ''.join(value).split(char_start)[1].split(char_end)[0] + ")"))
        values.append(value)

    variables_dict = dict(zip(keys, values))

    return variables_dict


# Write user variables to a JSON file.
def write_json(variables_dict, json_file):
        
    with open(json_file, "w") as outfile:
        json.dump(variables_dict, outfile)


# Read the JSON file where the conversion count is stored.
def read_json():
    # Open JSON file
    json_file = Path(__file__).parent.resolve() / "Converter_Report.json"

    with open(json_file, 'r') as openfile:
    
        # Read from JSON file
        json_object = json.load(openfile)
    
    return json_object