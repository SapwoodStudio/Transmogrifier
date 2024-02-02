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



#  ███████████ █████  █████ ██████   █████   █████████  ███████████ █████    ███████    ██████   █████  █████████ 
# ░░███░░░░░░█░░███  ░░███ ░░██████ ░░███   ███░░░░░███░█░░░███░░░█░░███   ███░░░░░███ ░░██████ ░░███  ███░░░░░███
#  ░███   █ ░  ░███   ░███  ░███░███ ░███  ███     ░░░ ░   ░███  ░  ░███  ███     ░░███ ░███░███ ░███ ░███    ░░░ 
#  ░███████    ░███   ░███  ░███░░███░███ ░███             ░███     ░███ ░███      ░███ ░███░░███░███ ░░█████████ 
#  ░███░░░█    ░███   ░███  ░███ ░░██████ ░███             ░███     ░███ ░███      ░███ ░███ ░░██████  ░░░░░░░░███
#  ░███  ░     ░███   ░███  ░███  ░░█████ ░░███     ███    ░███     ░███ ░░███     ███  ░███  ░░█████  ███    ░███
#  █████       ░░████████   █████  ░░█████ ░░█████████     █████    █████ ░░░███████░   █████  ░░█████░░█████████ 
# ░░░░░         ░░░░░░░░   ░░░░░    ░░░░░   ░░░░░░░░░     ░░░░░    ░░░░░    ░░░░░░░    ░░░░░    ░░░░░  ░░░░░░░░░  


# Load custom scripts from JSON file.
def load_custom_scripts(custom_scripts_list):
    for script in custom_scripts_list:
        new_custom_script = bpy.context.scene.transmogrifier_scripts.add()
        new_custom_script.script_name = script[0]
        new_custom_script.script_filepath = script[1]
        new_custom_script.script_trigger = script[-1]


# Refresh UI when a Transmogrifier preset is selected.
def refresh_ui(self, context):
    settings = bpy.context.scene.transmogrifier_settings
    scripts = bpy.context.scene.transmogrifier_scripts

    if settings.transmogrifier_preset != "NO_PRESET":
        # Load selected Transmogrifier preset as a dictionary.
        transmogrifier_preset_dict = load_transmogrifier_preset('transmogrifier', settings.transmogrifier_preset)

        # Read dictionary and change UI settings to reflect selected preset.
        for key, value in transmogrifier_preset_dict.items():
            scripts.clear()  # Clear any existing custom script instances.
            if key == "custom_scripts":
                load_custom_scripts(value)  # Load custom scripts from JSON file.
                continue
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



# Create variables_dict dictionary from transmogrifier_settings and transmogrifier_scripts to pass to write_json function later.
def get_transmogrifier_settings(self, context, use_absolute_paths):
    settings = bpy.context.scene.transmogrifier_settings
    keys = [key for key in settings.__annotations__ if "enum" not in key]
    values = []
    
    for key in keys:    
        # Get value as string to be evaluated later.
        value = eval(f"settings.{key}")
        
        # Convert relative paths to absolute paths.
        directory_paths = ("directory", "directory_output_custom", "textures_custom_dir", "uv_directory_custom")
        if use_absolute_paths and key in directory_paths:
            value = str(Path(bpy.path.abspath(value)).resolve())
        
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

    # Make a dictionary of lists of values of custom scripts.
    scripts = bpy.context.scene.transmogrifier_scripts
    custom_scripts = []
    
    for script in scripts:
        values = []
        for key in script.__annotations__:
            value = eval(f"script.{key}")
            if use_absolute_paths and key == "script_filepath":
                value = str(Path(bpy.path.abspath(value)).resolve())
            values.append(value)
        custom_scripts.append(values)
    custom_scripts_dict = {"custom_scripts": custom_scripts}

    # Add custom scripts list to dictionary of settings.
    variables_dict.update(custom_scripts_dict)

    return variables_dict


# Add a custom script.
def add_customscript(self, context):
    new_custom_script = context.scene.transmogrifier_scripts.add()
    new_custom_script.script_name = Path(new_custom_script.script_filepath).name


# Update custom script names based on file names.
def update_customscript_names(self, context):
    for index, custom_script in enumerate(context.scene.transmogrifier_scripts):
        script_filepath = Path(bpy.path.abspath(custom_script.script_filepath)).resolve()

        # Added a new custom script (default name is "*.py")
        if custom_script.script_filepath == "*.py"  and script_filepath.name == "*.py":
            custom_script.script_name = f"Script {index + 1}"
        
        # File is not a Python file.
        elif script_filepath.suffix != ".py":
            custom_script.script_name = f"(Not a Python File) {script_filepath.name}"

        # File is a Python file but doesn't exist.
        elif not script_filepath.is_file() and script_filepath.suffix == ".py":
            custom_script.script_name = f"(Missing) {script_filepath.name}"

        # File is a Python file and might exist, but path is relative and current Blend session is unsaved.
        elif script_filepath != Path(custom_script.script_filepath) and not bpy.data.is_saved:
            custom_script.script_name = f"(Missing) {script_filepath.name}"

        # File is a Python file and exists.
        elif script_filepath.is_file() and script_filepath.suffix == ".py":
            custom_script.script_name = script_filepath.name


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
    import_directory = settings.directory

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
    import_directory = settings.directory
    import_ext = get_import_ext(self, context, settings)

    # Check if directory is absolute and if Blender session is saved.
    if (Path(import_directory) != Path(bpy.path.abspath(import_directory)).resolve() or import_directory == "") and not bpy.data.is_saved:
        settings.batch_convert_info_message = f"0 {import_ext.upper()[1:]} files detected."
        return

    # Change path to absolute directory.
    import_directory = Path(bpy.path.abspath(import_directory)).resolve()
    # Count models that will be imported.
    models_to_import = count_files_in_directory_tree(self, context, import_directory, import_ext)

    # Check if there are models to import and export.
    if models_to_import and settings.model_quantity != "No Formats":
        if settings.model_quantity == "1 Format":
            settings.batch_convert_info_message = f"{models_to_import} {import_ext.upper()[1:]} ⇒ {models_to_import} {settings.export_file_1}"
        elif settings.model_quantity == "2 Formats":
            settings.batch_convert_info_message = f"{models_to_import} {import_ext.upper()[1:]} ⇒ {models_to_import} {settings.export_file_1} + {models_to_import} {settings.export_file_2}"
    elif not models_to_import:
        settings.batch_convert_info_message = f"{models_to_import} {import_ext.upper()[1:]} files detected."