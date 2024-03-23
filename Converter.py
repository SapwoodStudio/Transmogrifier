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
import os
import glob
import datetime
import sys
import shutil
from pathlib import Path
import json
import re
import logging
from bpy.app.handlers import persistent
from itertools import chain
import time
import numpy as np



#  ███████████ █████  █████ ██████   █████   █████████  ███████████ █████    ███████    ██████   █████  █████████ 
# ░░███░░░░░░█░░███  ░░███ ░░██████ ░░███   ███░░░░░███░█░░░███░░░█░░███   ███░░░░░███ ░░██████ ░░███  ███░░░░░███
#  ░███   █ ░  ░███   ░███  ░███░███ ░███  ███     ░░░ ░   ░███  ░  ░███  ███     ░░███ ░███░███ ░███ ░███    ░░░ 
#  ░███████    ░███   ░███  ░███░░███░███ ░███             ░███     ░███ ░███      ░███ ░███░░███░███ ░░█████████ 
#  ░███░░░█    ░███   ░███  ░███ ░░██████ ░███             ░███     ░███ ░███      ░███ ░███ ░░██████  ░░░░░░░░███
#  ░███  ░     ░███   ░███  ░███  ░░█████ ░░███     ███    ░███     ░███ ░░███     ███  ░███  ░░█████  ███    ░███
#  █████       ░░████████   █████  ░░█████ ░░█████████     █████    █████ ░░░███████░   █████  ░░█████░░█████████ 
# ░░░░░         ░░░░░░░░   ░░░░░    ░░░░░   ░░░░░░░░░     ░░░░░    ░░░░░    ░░░░░░░    ░░░░░    ░░░░░  ░░░░░░░░░  


# Read Settings.json file where the user variables are stored.
def read_json(json_file):
    try:
        with open(json_file, 'r') as openfile:
        
            # Read from JSON file
            json_object = json.load(openfile)
        
        return json_object

        print(f"Read {json_file.name}")
        logging.info(f"Read {json_file.name}")

    except Exception as Argument:
        logging.exception(f"Could Not Read {json_file.name}")


# Set global variables from JSON dictionary.
def set_settings(json_dict):
    try:
        for key, value in json_dict.items():
            # Preserve quotation marks during exec() if value is a string type object.
            if isinstance(value, str):
                value = repr(value)
            
            # Don't preserve quotation marks during exec() if value is not a string type object.
            else:
                value = str(value)
            
            # Concatenate command.
            variable_assignment_command = f"globals()['{key}'] = {value}"
            
            # Execute variable assignment.
            exec(variable_assignment_command)
        
        print("Set setting from JSON")
        logging.info("Set settings from JSON")

    except Exception as Argument:
        logging.exception("Could not set settings from JSON")


# Read dictionary of settings from JSON file.
def get_settings(json_files):
    try:
        # Loop through JSON files list.
        for json_file in json_files:
            json_file = Path(__file__).parent.resolve() / json_file
            
            # Assign variables from dictionary and make all variables global
            json_dict = read_json(json_file)

            # Set settings.
            set_settings(json_dict)
        

        print("Got setting from JSON")
        logging.info("Got settings from JSON")

    except Exception as Argument:
        logging.exception("Could not get settings from JSON")


# Make a log file to log conversion process.
def make_log_file():
    # Set path to log file with timestamp
    timestamp = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    log_file = Path(import_directory, f"Transmogrifier_Log_{timestamp}.txt")
    
    # Create log file.
    logging.basicConfig(
        level=logging.INFO, 
        filename=log_file, 
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
        force=True
    )


# Enable addons that the Converter depends upon, namely Node Wrangler and Materials Utilities.
def enable_addons():
    try:
        bpy.ops.preferences.addon_enable(module='node_wrangler')
        bpy.ops.preferences.addon_enable(module='materials_utils')

        print("Enabled addons")
        logging.info("Enabled addons")

    except Exception as Argument:
        logging.exception("Could not enable addons")


# Copy file from source to destination.
def copy_file(directory, file_source):
    try:
        file_destination = Path(directory, Path(file_source).name)  # Set destination path.
        
        if Path(file_source).is_dir():  # Check if "file" is a directory.
            if Path(file_destination).exists():
                shutil.rmtree(file_destination)  # Remove any existing destination directory.
            shutil.copytree(file_source, file_destination)  # Copy the directory.

        elif Path(file_source).is_file():  # Check if "file" is a file.
            if Path(file_destination).is_file():
                Path.unlink(file_destination)  # Remove any existing destination file.
            shutil.copy(file_source, file_destination)  # Copy the file.

        else:
            return  # Return nothing if source file doesn't exist.

        print(f"Copied {Path(file_source).name} to {directory}")
        logging.info(f"Copied {Path(file_source).name} to {directory}")
    
    except Exception as Argument:
        logging.exception(f"Could not copy {Path(file_source).name} to {directory}")


# Move file from source to destination.
def move_file(directory, file_source):
    try:
        file_destination = Path(directory, Path(file_source).name)  # Set destination path.
        
        if Path(file_source).is_dir():  # Check if "file" is a directory.
            if Path(file_destination).exists():
                shutil.rmtree(file_destination)  # Remove any existing destination directory.
            shutil.move(file_source, file_destination)  # Move the directory.

        elif Path(file_source).is_file():  # Check if "file" is a file.
            if Path(file_destination).is_file():
                Path.unlink(file_destination)  # Remove any existing destination file.
            shutil.move(file_source, file_destination)  # Move the file.

        else:
            return  # Return nothing if source file doesn't exist.
                
        print(f"Moved {Path(file_source).name} to {directory}")
        logging.info(f"Moved {Path(file_source).name} to {directory}")
    
    except Exception as Argument:
        logging.exception(f"Could not move {Path(file_source).name} to {directory}")


# Override context perform certain context-dependent Blender operators.
def override_context(area_type, region_type):
    try:
        win = bpy.context.window
        scr = win.screen
        areas  = [area for area in scr.areas if area.type == area_type]
        regions = [region for region in areas[0].regions if region.type == region_type]

        override = {
            'window': win,
            'screen': scr,
            'area': areas[0],
            'region': regions[0],
        }

        print("Overrode context")
        logging.info("Overrode context")
        return override

    except Exception as Argument:
        logging.exception("Could not override context")


# Preserve unused materials & textures by setting fake user(s).
def use_fake_user():
    try:
        for datablock in chain(bpy.data.materials, bpy.data.textures):
            datablock.use_fake_user = True
        
        print("Used fake user for textures & materials")
        logging.info("Used fake user for textures & materials")

    except Exception as Argument:
        logging.exception("Could not use fake user for textures & materials")


# Sometimes purge orphans won't delete data blocks (e.g. images) even though they have no users. This will force the deletion of any data blocks within a specified bpy.data.[data type]
def clean_data_block(block):
    try:
        # iterate over every entry in the data block
        for data in block:
            block.remove(data)

        print(f"Cleaned data block: {str(block).upper()}")
        logging.info(f"Cleaned data block: {str(block).upper()}")

    except Exception as Argument:
        logging.exception(f"Could not clean data block: {str(block).upper()}")
		

# Add new collection with name of import_file.
def add_collection(item_name):
    try:
        # Add new collection.
        collection_name = item_name
        collection = bpy.data.collections.new(collection_name)

        # Add collection to scene collection.
        bpy.context.scene.collection.children.link(collection)

        # Make collection active so imported file contents are put inside/linked to the collection.
        layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
        bpy.context.view_layer.active_layer_collection = layer_collection

        print(f"Added new collection: {collection.name}")
        logging.info(f"Added new collection: {collection.name}")

    except Exception as Argument:
        logging.exception(f"Could not add new collection: {collection.name}")


# Recursively delete orphaned data blocks.
def purge_orphans():
    try:
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        print("Purged orphaned data blocks recursively")
        logging.info("Purged orphaned data blocks recursively")

    except Exception as Argument:
        logging.exception("Could not purge orphaned data blocks recursively")
		

# Enable addon dependencies and clear the scene
def setup_scene(item_name):
    try:
        clean_data_block(bpy.data.objects)
        clean_data_block(bpy.data.collections)
        purge_orphans()
        add_collection(item_name)

        print("Set up scene")
        logging.info("Set up scene")

    except Exception as Argument:
        logging.exception("Could not set up scene")
		

# Append a blend file's objects to Converter.blend.
def append_blend_objects(import_file_command, import_file_options, import_file):
    try:
        with bpy.data.libraries.load(str(import_file), link=False) as (data_from, data_to):  # Append all objects.
            data_to.objects = [object for object in data_from.objects]
        
        for object in data_to.objects: # Link all objects to current scene.
            if object is not None:
                bpy.context.collection.objects.link(object)

        print(f"Appended blend file objects: {import_file.name}")
        logging.info(f"Appended blend file objects: {import_file.name}")

    except Exception as Argument:
        logging.exception(f"Could not append blend file objects: {import_file.name}")


# Import file of a format type supplied by the user.
def import_a_file(import_file, import_settings_dict):
    try:
        # Get import options as a dictionary.
        options = eval(import_settings_dict["options"])

        # Update options with filepath to the location of the model to be imported.
        options["filepath"] = str(import_file)
        
        # Get import operator.
        operator = import_settings_dict["operator"]
        
        # Select "Objects" Library to append from current .blend file if importing a blend file.
        if operator == "bpy.ops.wm.append(**": 
            append_blend_objects(operator, options, import_file)
            return
        
        # Concatenate the import command with the import options dictionary
        operator = f"{operator}{options})"
        print(operator)
        logging.info(operator)

        # Run operator, which is stored as a string and won't run otherwise.
        exec(operator)

        print(f"Imported file: {import_file.name}")
        logging.info(f"Imported file: {import_file.name}")

    except Exception as Argument:
        logging.exception(f"Could not import file: {import_file.name}")
		  

# Move all objects and collections to item_name collection.
def move_objects_and_collections_to_item_collection(item_name):
    try:
        item_collection = bpy.data.collections[item_name]
        collections_to_move = [collection for collection in bpy.context.scene.collection.children if collection != item_collection]  # Get a list of additional collections in the scene.
        objects_to_move = [object for object in bpy.context.scene.collection.objects]  # Get a list of objects that exist directly in the default Scene Collection.

        if collections_to_move:
            for collection in collections_to_move:
                bpy.context.scene.collection.children.unlink(collection)
                item_collection.children.link(collection)

        if objects_to_move:
            for object in objects_to_move:
                bpy.context.scene.collection.objects.unlink(object)
                item_collection.objects.link(object)
            
        print(f"Moved objects in to Collection: {item_collection.name}")
        logging.info(f"Moved objects in to Collection: {item_collection.name}")

    except Exception as Argument:
        logging.exception(f"Could not move objects in to Collection: {item_collection.name}")


# Remove all animation data from imported objects. Sometimes 3DS Max exports objects with keyframes that cause scaling/transform issues in a GLB and USDZ.
def clear_animation_data():
    try:
        bpy.ops.object.select_all(action='SELECT')
        objects = bpy.context.scene.objects

        for object in objects:
            object.animation_data_clear()
            print(f"Deleted animations for {object.name}")
            logging.info(f"Deleted animations for {object.name}")
        
        print("Cleared animation data")
        logging.info("Cleared animation data")

    except Exception as Argument:
        logging.exception("Could not clear animation data")
		

# Select all imported objects and apply transformations
def apply_transformations(apply_transforms_filter):
    try:
        # Set default filters to true
        filter_location = True
        filter_rotation = True
        filter_scale = True

        # Disable filters if User elected not to include them
        if "Location" not in apply_transforms_filter:
            filter_location = False
        if "Rotation" not in apply_transforms_filter:
            filter_rotation = False
        if "Scale" not in apply_transforms_filter:
            filter_scale = False

        # Select all objects
        bpy.ops.object.select_all(action='SELECT')
        obj = bpy.context.window.scene.objects[0]
        bpy.context.view_layer.objects.active = obj

        # Apply transformations according to filter
        bpy.ops.object.transform_apply(location=filter_location, rotation=filter_rotation, scale=filter_scale)

        print(f"Applied transformations: {apply_transforms_filter}")
        logging.info(f"Applied transformations: {apply_transforms_filter}")

    except Exception as Argument:
        logging.exception(f"Could not apply transformations: {apply_transforms_filter}")
		

# Clear all users of all materials.
def clear_materials_users():
    try:
        # Remove any imported materials.
        bpy.ops.view3d.materialutilities_remove_all_material_slots(only_active=False)
        
        # Delete any old materials that might have the same name as the imported object.
        purge_orphans()
        
        for material in bpy.data.materials:
            material.user_clear()

        print("Cleared all users of all materials")
        logging.info("Cleared all users of all materials")

    except Exception as Argument:
        logging.exception("Could not clear all users of all materials")


# Select all objects again before exporting. The previously actively selected object should still be a MESH type object, although this should no longer matter.
def select_all():
    try:
        bpy.ops.object.select_all(action='SELECT')

        print("Selected all objects of all types")
        logging.info("Selected all objects of all types")

    except Exception as Argument:
        logging.exception("Could not select all objects of all types")
		

# Select all objects again before exporting. The previously actively selected object should still be a MESH type object, although this should no longer matter.
def deselect_all():
    try:
        bpy.ops.object.select_all(action='DESELECT')

        print("Deselected all objects of all types")
        logging.info("Deselected all objects of all types")

    except Exception as Argument:
        logging.exception("Could not deselect all objects of all types")
		

# Prevent an empty from being actively selected object. This prevents a later error from happening when imported materials are removed later.
def select_only_meshes():
    try:
        objects = bpy.context.scene.objects

        for object in objects:
            object.select_set(object.type == "MESH")
            object = bpy.context.window.scene.objects[0]
            bpy.context.view_layer.objects.active = object

        print("Selected only mesh-type objects")
        logging.info("Selected only mesh-type objects")

    except Exception as Argument:
        logging.exception("Could not select only mesh-type objects")
		

# Select all objects again before exporting. The previously actively selected object should still be a MESH type object, although this should no longer matter.
def select_by_material(material):
    try:
        bpy.ops.view3d.materialutilities_select_by_material_name(material_name = material.name)

        print(f"Selected objects with material: {material.name}")
        logging.info(f"Selected objects with material: {material.name}")

    except Exception as Argument:
        logging.exception(f"Could not select objects with material: {material.name}")
		

# Copy textures from custom directory to item_name directory.
def copy_textures_from_custom_source(textures_custom_dir, item_dir, textures_dir, preserve_original_textures):
    try:
        if Path(textures_custom_dir).exists():
            if Path(textures_dir).exists():  # Cannot create another textures folder if one already exists.
                if copy_textures_custom_dir and not preserve_original_textures:  # If User elected to replace an existing textures directory that might be inside the item_name folder, then delete it.
                    shutil.rmtree(textures_dir)
                else:  # If not, preserve existing textures folder by renaming adding an "_original" suffix.
                    textures_dir_name = [d.name for d in Path.iterdir(item_dir) if "textures" in d.name.lower()][0]  # Need to get specific textures_dir folder characters in case any other files are pathed to it.
                    textures_dir_original_name = [d.name for d in Path.iterdir(item_dir) if "textures" in d.name.lower() and "_original" not in d.name.lower()][0] + "_original"
                    textures_dir_original = Path(item_dir, textures_dir_original_name)
                    if Path(textures_dir_original).exists():  # If a textures folder had already existed and had been preserved as "textures_original", assume that the item_dir has already been transmogrified and the current textures_dir is a copy from the custom source.
                        shutil.rmtree(textures_dir)
                    elif not Path(textures_dir_original).exists():  # If a textures folder already exists but had not yet been preserved as a "textures_orignal" folder, then rename it so.
                        Path(textures_dir).rename(textures_dir_original)
            shutil.copytree(textures_custom_dir, textures_dir)  # Temporarily copy textures from custom directory as the current textures_dir.
        else:
            print("Custom textures directory does not exist.")
            logging.info("Custom textures directory does not exist.")

        print("Copied textures from custom source")
        logging.info("Copied textures from custom source")

    except Exception as Argument:
        logging.exception("Could not copy textures from custom source")
		

# If User elected not to copy the custom textures directory to each item_name folder, delete the temporary copy of it there.
def remove_copy_textures_custom_dir(item_dir, textures_dir):
    try:
        if Path(textures_dir).exists():
            shutil.rmtree(textures_dir)

        textures_dir_original_name = [d.name for d in Path.iterdir(item_dir) if "textures_original" in d.name.lower()]
        if textures_dir_original_name:  # If there was a textures_dir there before transmogrification, return its name to its original form.
            textures_dir_original_name = textures_dir_original_name[0]  # If the list is not empty, get the first item_name in the list.
            textures_dir_original = Path(item_dir, textures_dir_original_name)
            if Path(textures_dir_original).exists():
                Path(textures_dir_original).rename(Path(item_dir, textures_dir_original_name.replace("_original", "")))  # Return original textures_dir back to its former name before the conversion.

        print("Removed copied textures from custom source")
        logging.info("Removed copied textures from custom source")

    except Exception as Argument:
        logging.exception("Could not remove copied textures from custom source")
		

# Define list of supported image texture extensions.
def supported_image_ext():
    try:
        supported_image_ext = (
            ".bmp",
            ".sgi",
            ".rgb",
            ".bw",
            ".png",
            ".jpg",
            ".jpeg",
            ".jp2",
            ".j2c",
            ".tga",
            ".cin",
            ".dpx",
            ".exr",
            ".hdr",
            ".tif",
            ".tiff",
            ".webp"
        )

        return supported_image_ext

        print("Got supported image extensions")
        logging.info("Got supported image extensions")

    except Exception as Argument:
        logging.exception("Could not  get supported image extensions")
		

# Remove textures_temp_dir
def delete_textures_temp(textures_temp_dir):
    try:
        # Delete "textures_temp" if folder already exists. It will already exist if the User elected to save a .blend file, and it may exist if Transmogrifier quit after an error.
        if Path(textures_temp_dir).exists():
            shutil.rmtree(textures_temp_dir)
        
        print("Deleted temporary textures directory")
        logging.info("Deleted temporary textures directory")

    except Exception as Argument:
        logging.exception("Could not delete temporary textures directory")
		

# Create a temporary textures folder where images can be resized and exported with specified models without affecting the quality of the original texture files. 
# If multiple texture sets exist, assign each image texture file a prefix of the name of it's parent texture set directory folder.
# If image textures already have a prefix of the same name as the texture set, don't add the same prefix again.
def create_textures_temp(item_dir, textures_dir, textures_temp_dir):
    try:
        # Delete "textures_temp" if folder already exists. It will already exist if the User elected to save a .blend file, and it may exist if Transmogrifier quit after an error.
        delete_textures_temp(textures_temp_dir)
        
        # Check if a "textures" directory exists and is not empty. Copy it and call it textures_[item_name]_temp if it does, otherwise create an empty directory and fill it with image textures found in the item_dir.
        if Path(textures_dir).exists():
            # If a textures directory exists but is empty, make one and fill it with images.
            if not any(Path.iterdir(textures_dir)):
                print("Textures directory is empty. Looking for textures in parent directory...")
                logging.info("Textures directory is empty. Looking for textures in parent directory...")
                Path.mkdir(textures_temp_dir)
                image_ext = supported_image_ext()  # Get a list of image extensions that could be used as textures
                image_list = [file.name for file in Path.iterdir(item_dir) if file.name.lower().endswith(image_ext) and not file.name.startswith("Preview_")]  # Make a list of all potential texture candidates except for the preview images.
                if not image_list:  # i.e. if image_list is empty
                    print(f"No potential image textures found in {item_dir}")
                    logging.info(f"No potential image textures found in {item_dir}")
                else:
                    print(f"The following images will be copied to textures_temp: {image_list}")
                    logging.info(f"The following images will be copied to textures_temp: {image_list}")
                    for image in image_list:
                        image_src = Path(item_dir, image)
                        image_dest = Path(textures_temp_dir, image)
                        shutil.copy(image_src, image_dest)  # Copy each potential image texture to textures_temp

            # If a textures directory exists and is not empty, assume it contains images or texture set subdirectories containing images.
            else:
                shutil.copytree(textures_dir, textures_temp_dir)
        
        # If no textures directory exists, make one and fill it with images.
        else: 
            Path.mkdir(textures_temp_dir)
            image_ext = supported_image_ext()  # Get a list of image extensions that could be used as textures
            image_list = [file.name for file in Path.iterdir(item_dir) if file.name.lower().endswith(image_ext) and not file.name.startswith("Preview_")]  # Make a list of all potential texture candidates except for the preview images.
            if not image_list:  # i.e. if image_list is empty
                print(f"No potential image textures found in {item_dir}")
                logging.info(f"No potential image textures found in {item_dir}")
            else:
                print(f"The following images will be copied to textures_temp: {image_list}")
                logging.info(f"The following images will be copied to textures_temp: {image_list}")
                for image in image_list:
                    image_src = Path(item_dir, image)
                    image_dest = Path(textures_temp_dir, image)
                    shutil.copy(image_src, image_dest)  # Copy each potential image texture to textures_temp

        print("Created temporary textures directory")
        logging.info("Created temporary textures directory")

    except Exception as Argument:
        logging.exception("Could not create temporary textures directory")
		

# Split image texture name into components to be regexed in find_replace_pbr_tag function.
# The following code is adapted from Blender 3.5, Node Wrangler 3.43, __util.py__, Line 7
def split_into_components(string):
    try:
        """
        Split filename into components
        'WallTexture_diff_2k.002.jpg' -> ['WallTexture', 'diff', '2k', '002', 'jpg']
        """
        # Get original string name for printout.
        string_original = string

        # Remove file path.
        string = Path(string).name
        
        # Replace common separators with SPACE.
        separators = ["_", ",", ".", "-", "__", "--", "#"]
        for sep in separators:
            string = string.replace(sep, " ")

        components = string.split(" ")
        
        print(f"Split into components: {Path(string_original).name} --> {components}")
        logging.info(f"Split into components: {Path(string_original).name} --> {components}")

        return components

    except Exception as Argument:
        logging.exception(f"Could not split into components: {Path(string_original).name} --> {components}")
		

# Regex, i.e. find and replace messy/misspelled PBR tag with clean PBR tag in a given image texture's name supplied by the regex_textures_external function.
def find_replace_pbr_tag(texture):
    try:
        # Set original texture name.
        texture_original = texture

        # Dictionary with regex keys will be used as the pattern by turning it into a list then to a string.
        pbr_dict = {
            '(?i)^basecolou?r$|^albedo$|^d?iffuse$|^d?iff$|^colou?r$|^col$': 'BaseColor',
            '(?i)^subsurf.*|^sss$': 'Subsurface',
            '(?i)^m?etall?ic$|^m?etalness?$|^metal$|^mtl$': 'Metallic', 
            '(?i)^specul.*|^spe?c$': 'Specular',
            '(?i)^rou?gh$|^rou?ghn.*|^rgh$': 'Roughness',
            '(?i)^gloss?y?$|^gloss?iness?$|^gls$': 'Gloss',
            '(?i)^no?rma?l?$|^nor$': 'Normal',
            '(?i)^bu?mp$|^bumpiness?$': 'Bump',
            '(?i)^displacem?e?n?t?$|^di?sp$|^he?i?ght$|^hi?e?ght$': 'Height',
            '(?i)^tra?nsmi?ss?i?o?n$': 'Transmission',
            '(?i)^emiss.*|^emit$': 'Emission',
            '(?i)^alpha$|^opac.*|^tra?ns?pa.*|^transpr.*': 'Opacity',
            '(?i)^ambi?e?nt$|^occ?lus.*|^ambi?e?ntocc?lusion$|^ao$': 'Occlusion'
        }

        dictkeys_pattern = re.compile('|'.join(pbr_dict), re.IGNORECASE)

        #If string is found in the pattern, match to key in the dictionary and return corresponding value.
        texture_found = re.findall(dictkeys_pattern, texture)
        if texture_found:
            texture = []
            for i in texture_found: 
                for k, v in pbr_dict.items():
                    if re.match(k, i, re.IGNORECASE):
                        texture.append(v)
            return texture
        else:
            texture = None
            return texture

        print(f"Found and replaced pbr tag: {texture_original} --> {texture}")
        logging.info(f"Found and replaced pbr tag: {texture_original} --> {texture}")

    except Exception as Argument:
        logging.exception(f"Could not find and replace pbr tag: {texture_original} --> {texture}")
		

# Regex, i.e. find and replace messy/misspelled transparency tag with clean PBR tag in a given object's name supplied by the regex_transparent_objects function.
def find_replace_transparency_tag(mesh_object):
    try:
        # Set original mesh_object name.
        mesh_object_original = mesh_object

        # Dictionary with regex keys will be used as the pattern by turning it into a list then to a string.
        pbr_dict = {
            '(?i)^alpha$|^opac.*|^tra?ns?pa.*|^transpr.*|^glass$': 'transparent',
            '(?i)^cutout$|^cut$|^out$': 'cutout',
        }

        dictkeys_pattern = re.compile('|'.join(pbr_dict), re.IGNORECASE)

        #If string is found in the pattern, match to key in the dictionary and return corresponding value.
        mesh_object_found = re.findall(dictkeys_pattern, mesh_object)
        if mesh_object_found:
            mesh_object = []
            for i in mesh_object_found: 
                for k, v in pbr_dict.items():
                    if re.match(k, i, re.IGNORECASE):
                        mesh_object.append(v)
            return mesh_object
        else:
            mesh_object = None
            return mesh_object

        print(f"Found and replaced transparency tag: {mesh_object_original} --> {mesh_object}")
        logging.info(f"Found and replaced transparency tag: {mesh_object_original} --> {mesh_object}")

    except Exception as Argument:
        logging.exception(f"Could not find and replaced transparency tag: {mesh_object_original} --> {mesh_object}")


# Find and rename image textures from a dictionary with regex keys.
def regex_textures_external(textures_temp_dir):
    try:
        for subdir, dirs, files in os.walk(textures_temp_dir):
            for file in files:
                file = Path(subdir, file)
                texture = file
                texture_path = Path(texture).parent.resolve()
                components_original = split_into_components(texture)
                components = split_into_components(texture)

                for component in components:
                    pbr_tag_renamed = find_replace_pbr_tag(component)
                    if pbr_tag_renamed != None:
                        pbr_tag_renamed = pbr_tag_renamed[0]
                        print(f"Found a match for {pbr_tag_renamed}")
                        logging.info(f"Found a match for {pbr_tag_renamed}")
                        tag_index = components.index(component)
                        components[tag_index] = pbr_tag_renamed
                        if pbr_tag_renamed == "BaseColor" and components[tag_index-1].lower() == "base":
                            components.pop(tag_index-1)  # Was getting "...base_BaseColor..." when original name was "base_color"
                        elif pbr_tag_renamed == "Occlusion" and components[tag_index-1].lower() == "occlusion":
                            components.pop(tag_index+1)  # Was getting "...Ambient_Occlusion_Occlusion..." when original name was "Ambient_Occlusion"
                        break

                if components_original != components:
                    texture = Path(texture_path, texture)
                    texture_renamed = '_'.join(components[:-1])
                    texture_renamed = Path(texture_path, texture_renamed + '.' + components[-1])
                    print(f"Renamed texture: {Path(texture).name} --> {Path(texture_renamed).name}")
                    logging.info(f"Renamed texture: {Path(texture).name} --> {Path(texture_renamed).name}")
                    Path(texture).rename(texture_renamed)
                        
                else:
                    print("No PBR match found for current texture.")
                    logging.info("No PBR match found for current texture.")

        print("Regexed external textures")
        logging.info("Regexed external textures")

    except Exception as Argument:
        logging.exception("Could not regex external textures")
		

# Find and rename image textures from a dictionary with regex keys.
def regex_textures_packed():
    try:
        for texture in bpy.data.images:
            texture_name = texture.name
            components_original = split_into_components(texture_name)
            components = split_into_components(texture_name)

            for component in components:
                pbr_tag_renamed = find_replace_pbr_tag(component)
                if pbr_tag_renamed != None:
                    pbr_tag_renamed = pbr_tag_renamed[0]
                    print(f"Found a match for {pbr_tag_renamed}")
                    logging.info(f"Found a match for {pbr_tag_renamed}")
                    tag_index = components.index(component)
                    if pbr_tag_renamed == "Opacity" and len(components) - tag_index != -2:  # Don't rename any transparency string if it's not at the end of the texture name.
                        continue
                    components[tag_index] = pbr_tag_renamed
                    if pbr_tag_renamed == "BaseColor" and components[tag_index-1].lower() == "base":
                        components.pop(tag_index-1)  # Was getting "...base_BaseColor..." when original name was "base_color"
                    elif pbr_tag_renamed == "Occlusion" and components[tag_index+1].lower() == "occlusion":
                        components.pop(tag_index+1)  # Was getting "...Ambient_Occlusion_Occlusion..." when original name was "Ambient_Occlusion"

            if components_original != components:
                texture_renamed = '_'.join(components[:-1])
                texture.name = texture_renamed
                print(f"Renamed texture: {Path(texture).name} --> {Path(texture_renamed).name}")
                logging.info(f"Renamed texture: {Path(texture).name} --> {Path(texture_renamed).name}")
                        
            else:
                print("No PBR match found for current texture.")
                logging.info("No PBR match found for current texture.")

        print("Regexed packed textures")
        logging.info("Regexed packed textures")

    except Exception as Argument:
        logging.exception("Could not regex packed textures")


# Find and rename transparent objects that have mispellings of transparency with regex keys.
def regex_transparent_objects():
    try:
        objects = bpy.context.selected_objects
        for object in objects:
            object_name = object.name
            components_original = split_into_components(object_name)
            components = split_into_components(object_name)

            for component in components:
                transparency_tag_renamed = find_replace_transparency_tag(component)
                if transparency_tag_renamed != None:
                    transparency_tag_renamed = transparency_tag_renamed[0]
                    print(f"Found a match for {transparency_tag_renamed}")
                    logging.info(f"Found a match for {transparency_tag_renamed}")
                    tag_index = components.index(component)
                    components[tag_index] = transparency_tag_renamed

            if components_original != components:
                object_renamed = '_'.join(components)
                object.name = object_renamed
                print(f"Renamed object: {object_name} --> {object_renamed}")
                logging.info(f"Renamed object: {object_name} --> {object_renamed}")
                        
            else:
                print("No transparency tag match found for current object.")
                logging.info("No transparency tag match found for current object.")

        print("Regexed transparent objects")
        logging.info("Regexed transparent objects")

    except Exception as Argument:
        logging.exception("Could not regex transparent objects")
		

# Determine if current item_name has multiple texture sets present in textures_temp_dir. If so, loop through each texture set and create a material from the image textures in that set.
def create_materials(item_name, textures_temp_dir):
    try:
        image_ext = supported_image_ext()  # Get a list of image extensions that could be used as textures

        # Check if textures are stored in subdirectories.
        # Check if there are subdirectories.
        texture_set_dir_list = next(os.walk(textures_temp_dir))[1]

        # Check if there are images in subdirectories or if these folders are used for other purposes.
        if texture_set_dir_list:
            for texture_set_dir in texture_set_dir_list:
                texture_set_dir = Path(textures_temp_dir, texture_set_dir)
                textures_in_subdirs = [texture.name for texture in Path.iterdir(texture_set_dir) if texture.name.lower().endswith(image_ext)]
            # If there are images stored in subdirectories, assume all texture sets are organized in subdirectories and use these to create materials.
            if textures_in_subdirs:
                for texture_set_dir in texture_set_dir_list:
                    texture_set_dir = Path(textures_temp_dir, texture_set_dir)
                    texture_set = Path(texture_set_dir).name # Get the subdirectory's name, which will be used as the material name.
                    # Add texture set prefix to images based on texture set directory name.
                    for texture in Path.iterdir(texture_set_dir):
                        texture_path = Path(texture_set_dir, texture)
                        texture_renamed = texture_set + "_" + texture.name
                        texture_renamed_path = Path(texture_set_dir, texture_renamed)
                        if not texture.name.startswith(texture_set) and texture_set != "textures_temp":  # If all textures exist directly in textures_temp_dir, don't add that directory name as a prefix.
                            Path(texture_path).rename(texture_renamed_path)
                        else:
                            continue
                    textures = [texture.name for texture in Path.iterdir(texture_set_dir)]

                    create_a_material(item_name=texture_set, textures_temp_dir=texture_set_dir, textures=textures)  # Parameters are temporarily reassigned in order that the create_a_material function can be reused.
            
            # If there are no subdirectories containing images, then determine how many texture sets exists in textures_temp directory.
            elif not textures_in_subdirs:
                textures_list = [image.name for image in Path.iterdir(textures_temp_dir) if image.name.lower().endswith(image_ext)]
                basecolor_count = 0
                # Count how many times the regexed "BaseColor" string occurs in the list of images.
                for texture in textures_list:
                    if "BaseColor" in texture:
                        basecolor_count += 1
                # If there is more than one BaseColor image, assume that there are multiple texture sets.
                if basecolor_count > 1:
                    texture_sets = list(set([image.split('_')[0] for image in textures_list]))
                    print(f"Detected {basecolor_count} texture sets: {texture_sets}")
                    logging.info(f"Detected {basecolor_count} texture sets: {texture_sets}")
                    for texture_set in texture_sets:
                        textures = [texture for texture in textures_list if texture.startswith(texture_set)]
                        create_a_material(item_name=texture_set, textures_temp_dir=textures_temp_dir, textures=textures)
                # If there are less than or equal to 6 images in textures_temp, assume there is only one texture set.
                elif basecolor_count <= 1:
                    print(f"Detected {basecolor_count} texture set")
                    logging.info(f"Detected {basecolor_count} texture set")
                    textures = textures_list

                    create_a_material(item_name, textures_temp_dir, textures)

        # If there are no subdirectories containing images, then determine how many texture sets exists in textures_temp directory.
        elif not texture_set_dir_list:
            textures_list = [image.name for image in Path.iterdir(textures_temp_dir) if image.name.lower().endswith(image_ext)]
            basecolor_count = 0
            # Count how many times the regexed "BaseColor" string occurs in the list of images.
            for texture in textures_list:
                if "BaseColor" in texture:
                    basecolor_count += 1
            # If there is more than one BaseColor image, assume that there are multiple texture sets.
            if basecolor_count > 1:
                texture_sets = list(set([image.split('_')[0] for image in textures_list]))
                print(f"Detected {basecolor_count} texture sets: {texture_sets}")
                logging.info(f"Detected {basecolor_count} texture sets: {texture_sets}")
                for texture_set in texture_sets:
                    textures = [texture for texture in textures_list if texture.startswith(texture_set)]
                    create_a_material(item_name=texture_set, textures_temp_dir=textures_temp_dir, textures=textures)
            # If there are less than or equal to 6 images in textures_temp, assume there is only one texture set.
            elif basecolor_count <= 1:
                print(f"Detected {basecolor_count} texture set")
                logging.info(f"Detected {basecolor_count} texture set")
                textures = textures_list

                create_a_material(item_name, textures_temp_dir, textures)
        
        # If there are no textures, print a message.
        else:
            print("No textures were found.")
            logging.info("No textures were found.")
                
        print("Created materials")
        logging.info("Created materials")

    except Exception as Argument:
        logging.exception("Could not create materials")
		

# Add principled setup with Node Wrangler.
def add_principled_setup(material, textures_temp_dir, textures):
    try:
        # Select shader before importing textures.
        material.use_nodes = True
        tree = material.node_tree
        nodes = tree.nodes

        # Make sure the Principled BSDF shader is selected.
        material.node_tree.nodes['Material Output'].select = False
        material.node_tree.nodes['Principled BSDF'].select = True
        material.node_tree.nodes.active = material.node_tree.nodes.get("Principled BSDF")

        # Log the textures to be used for this material.
        print("Textures for " + str(material.name) + ": " + str(textures))
        logging.info("Textures for " + str(material.name) + ": " + str(textures))

        # Get context.
        win = bpy.context.window
        scr = win.screen
        areas = [area for area in scr.areas if area.type == 'NODE_EDITOR']
        areas[0].spaces.active.node_tree = material.node_tree
        override = override_context('NODE_EDITOR', 'WINDOW')
        
        # Get textures to import.
        files = []
        for texture in textures:
            if texture == '.DS_Store':
                continue

            files.append(
                {
                    "name": texture,
                    "name": texture
                }
            )
            
        filepath = str(textures_temp_dir) + '/'
        directory = str(textures_temp_dir) + '/'
        relative_path = True
        
        # Add principled setup.
        with bpy.context.temp_override(**override):
            bpy.ops.node.nw_add_textures_for_principled(
                filepath=filepath,
                directory=directory,
                files=files,
                relative_path=relative_path
            )
        
        print(f"Added Principled Setup for {material.name}")
        logging.info(f"Added Principled Setup for {material.name}")
    
    except Exception as Argument:
        logging.exception(f"Could not Add Principled Setup for {material.name}")


# Add materials, import textures, and assign materials to objects.
def create_a_material(item_name, textures_temp_dir, textures):
    try:
        # Create a new material. This will be the opaque material.
        material = bpy.data.materials.new(name=item_name) # Create new material from item_name name.
        
        # Import textures with Node Wrangler addon
        textures = textures
        
        # Add principled setup via Node Wrangler.
        add_principled_setup(material, textures_temp_dir, textures)
        
        # Check if this material includes an opacity map.
        transparency_check = [node for node in material.node_tree.nodes if node.type == 'BSDF_PRINCIPLED' and node.inputs['Alpha'].is_linked]
        if transparency_check:
            # Copy current material and make opaque version in case there are any opaque objects in scene using the same texture set.
            material_opaque = material.copy()
            material_opaque.blend_method = 'OPAQUE'
            bpy.data.materials[item_name + ".001"].name = item_name
            # Remove opacity map from opaque material.
            opacity_map = material_opaque.node_tree.nodes["Principled BSDF"].inputs['Alpha'].links[0].from_node
            material_opaque.node_tree.nodes.remove(opacity_map)
            # Add transparency tag to material name and set alpha blend.
            material.name = item_name + "_transparent"
            material.blend_method = "BLEND"
            print(f"Found an opacity map for texture set: {material_opaque.name}. Created transparent version of material, {material.name}")
            logging.info(f"Found an opacity map for texture set: {material_opaque.name}. Created transparent version of material, {material.name}")

        print(f"Created a material: {item_name}")
        logging.info(f"Created a material: {item_name}")

    except Exception as Argument:
        logging.exception(f"Could not create a material: {item_name}")
		

# Get alpha tags from Node Wrangler Preferences to use for checking if an object's indicates that it should be assigned a transparent material.
def get_nw_alpha_tags():
    try:
        # The following code is adapted from Blender 3.5, Node Wrangler 3.43, __init.py__, Line 2725
        tags = bpy.context.preferences.addons['node_wrangler'].preferences.principled_tags

        normal_abbr = tags.normal.split(' ')
        bump_abbr = tags.bump.split(' ')
        gloss_abbr = tags.gloss.split(' ')
        rough_abbr = tags.rough.split(' ')
        socketnames = [
            ['Displacement', tags.displacement.split(' '), None],
            ['Base Color', tags.base_color.split(' '), None],
            ['Subsurface Color', tags.sss_color.split(' '), None],
            ['Metallic', tags.metallic.split(' '), None],
            ['Specular', tags.specular.split(' '), None],
            ['Roughness', rough_abbr + gloss_abbr, None],
            ['Normal', normal_abbr + bump_abbr, None],
            ['Transmission', tags.transmission.split(' '), None],
            ['Emission', tags.emission.split(' '), None],
            ['Alpha', tags.alpha.split(' '), None],
            ['Ambient Occlusion', tags.ambient_occlusion.split(' '), None],
        ]

        alpha_tags = tuple(socketnames[9][1])  # Get a tuple of only the alpha tags.

        return alpha_tags

        print("Got Node Wrangler alpha tags")
        logging.info("Got Node Wrangler alpha tags")

    except Exception as Argument:
        logging.exception("Could not get Node Wrangler alpha tags")
		

# Assign previously created materials to objects based on 1) how many texture sets were present in the textures_dir, 2) the objects' name prefixes (which texture set goes to what objects), and 3) the objects' name suffixes (determines transparency).
def assign_materials(item_name):
    try:
        # Determine how many mesh objects are in the scene.
        object_count = 0
        for object in bpy.context.selected_objects: # Loop only through selected MESH type objects.
            object_count += 1

        # Determine how many texture sets were imported.
        material_count = 0
        for material in bpy.data.materials:
            material_count += 1

        # Assuming object names have been regexed for transparency tags, assign the transparency regex dictionary value to variable.
        transparency_tag = "transparent"
        cutout_tag = "cutout"
        # Test for presence of transparent versions of opaque materials.
        transparent_materials = [material.name for material in bpy.data.materials if transparency_tag in material.name and material.name.replace("_" + transparency_tag, "") in bpy.data.materials]

        # Only one texture set was imported (one opaque or one transparent material)
        if material_count == 1:
            material = bpy.data.materials[0]
            material_name = str(material.name) # Get the material's name from that material's data block list.
            for object in bpy.context.selected_objects: # Loop only through selected MESH type objects.
                if object.type == 'MESH':
                    object.data.materials.append(material)
                    print(f"Assigned material, {material_name}, to object, {object.name}")
                    logging.info(f"Assigned material, {material_name}, to object, {object.name}")

        # Only one texture set was imported (one opaque material, one transparent version/copy of that opaque material).
        elif material_count == 2 and transparent_materials:
            for material in bpy.data.materials:
                material_name = str(material.name) # Get the material's name from that material's data block list.
                for object in bpy.context.selected_objects: # Loop only through selected MESH type objects.
                    if object.type == 'MESH' and material_name.replace("_" + transparency_tag, "") == item_name: # Ignore the "_transparent" suffix of the transparent material.
                        if object_count == 1 and material_name.endswith(transparency_tag):
                            object.data.materials.append(material)
                            print(f"Assigned transparent material, {material_name}, to transparent object, {object.name}")
                            logging.info(f"Assigned transparent material, {material_name}, to transparent object, {object.name}")
                        elif object_count > 1:
                            if (transparency_tag in object.name or cutout_tag in object.name) and material_name.endswith(transparency_tag):
                                object.data.materials.append(material)
                                if cutout_tag in object.name:
                                    material.blend_method = "CLIP"
                                print(f"Assigned transparent material, {material_name}, to transparent object, {object.name}")
                                logging.info(f"Assigned transparent material, {material_name}, to transparent object, {object.name}")
                            elif not transparency_tag in object.name and not cutout_tag in object.name and not material_name.endswith(transparency_tag):
                                object.data.materials.append(material)
                                print(f"Assigned opaque material, {material_name}, to opaque object, {object.name}")
                                logging.info(f"Assigned opaque material, {material_name}, to opaque object, {object.name}")
                            else:
                                continue

        # More than one texture set was imported.
        elif material_count >= 2:
            for material in bpy.data.materials:
                material_name = str(material.name) # Get the material's name from that material's data block list.
                for object in bpy.context.selected_objects:
                    if object.type == 'MESH': # Loop only through selected MESH type objects.
                        if material_name.replace("_" + transparency_tag, "") in object.name and (transparency_tag in object.name or cutout_tag in object.name) and material_name.endswith(transparency_tag):
                            object.data.materials.append(material)
                            if cutout_tag in object.name:
                                material.blend_method = "CLIP"
                            print(f"Assigned transparent material, {material_name}, to transparent object, {object.name}")
                            logging.info(f"Assigned transparent material, {material_name}, to transparent object, {object.name}")
                        elif material_name in object.name and not transparency_tag in object.name and not cutout_tag in object.name and not material_name.endswith(transparency_tag):
                            object.data.materials.append(material)
                            print(f"Assigned opaque material, {material_name}, to opaque object, {object.name}")
                            logging.info(f"Assigned opaque material, {material_name}, to opaque object, {object.name}")
                        else:
                            continue

        # If there aren't any mesh-type objects in the scene (e.g. an empty FBX), continue on to the next item_name.
        else:
            print("There are no mesh-type objects in the scene")
            logging.info("There are no mesh-type objects in the scene")

        print("Assigned materials to objects")
        logging.info("Assigned materials to objects")

    except Exception as Argument:
        logging.exception("Could not assign materials to objects")
		

# Resize image textures in textures_temp folder before export.
def resize_textures(texture_map, texture_resolution, resize_all):
    try:
        for image in bpy.data.images:
            try:
                if texture_map in image.name or resize_all:
                    width, height = image.size
                    if texture_resolution < width:
                        image.scale(texture_resolution, texture_resolution) # (width, height)
                        image.save()
                        print(f"Resized Image ({image.name}): {width, height} --> {texture_resolution, texture_resolution}")
                        logging.info(f"Resized Image ({image.name}): {width, height} --> {texture_resolution, texture_resolution}")
                    
                    elif texture_resolution > width:
                        print(f"Skipped Resize Image ({image.name}) to avoid upscaling: {width, height} --> {texture_resolution, texture_resolution}")
                        logging.info(f"Skipped Resize Image ({image.name}) to avoid upscaling: {width, height} --> {texture_resolution, texture_resolution}")
            except:
                pass

        print("Resized textures")
        logging.info("Resized textures")

    except Exception as Argument:
        logging.exception("Could not resize textures")
		

# Image types to save as.
def image_texture_ext_dict():
    try:
        image_texture_ext = {
            "BMP": ".bmp",
            "PNG": ".png",
            "JPEG": ".jpg",
            "JPEG2000": ".jp2",
            "TARGA": ".tga",
            "CINEON": ".cin",
            "DPX": ".dpx",
            "OPEN_EXR": ".exr",
            "HDR": ".hdr",
            "TIFF": ".tiff",
            "WEBP": ".webp"
        }
        
        return image_texture_ext

        print("Got image texture extension dictionary")
        logging.info("Got image texture extension dictionary")

    except Exception as Argument:
        logging.exception("Could not get image texture extension dictionary")
		

# Get image type from extension.
def get_image_ext_key(val):
    try:
        for key, value in ext_dict.items():
            if val == value:
                return key
        return "key doesn't exist"

        print("Got image extension key")
        logging.info("Got image extension key")

    except Exception as Argument:
        logging.exception("Could not get image extension key")
		

# Change scene color management. Needed for converting image texture formats
def set_color_management(
    texture_format, 
    image_quality,
    display_device, 
    view_transform, 
    look, 
    exposure, 
    gamma, 
    sequencer, 
    use_curves, 
):
    try:
        # Output-specific settings.
        image_settings = bpy.context.scene.render.image_settings
        image_settings.file_format = texture_format
        image_settings.quality = image_quality
        image_settings.color_management = 'FOLLOW_SCENE'

        # Scene color management.
        scene = bpy.context.scene
        scene.display_settings.display_device = display_device
        scene.view_settings.view_transform = view_transform
        scene.view_settings.look = look
        scene.view_settings.exposure = exposure
        scene.view_settings.gamma = gamma
        scene.sequencer_colorspace_settings.name = sequencer
        scene.view_settings.use_curve_mapping = use_curves

        print("Set color management")
        logging.info("Set color management")

    except Exception as Argument:
        logging.exception("Could not set color management")
		

# Convert images to specified format.
def reformat_images(texture_map, texture_format, image_quality, reformat_all, include_normal_map):
    try:
        # Get dictionary.
        ext_dict = image_texture_ext_dict()

        # Set color management to sRGB Standard.
        set_color_management(
            texture_format=texture_format, 
            image_quality=image_quality,
            display_device='sRGB', 
            view_transform='Standard', 
            look='None', 
            exposure=0, 
            gamma=1, 
            sequencer='sRGB', 
            use_curves=False, 
        )

        # Convert each relevant image.
        for image in bpy.data.images:
            
            # Ignore images other than image textures.
            if image.name == "Render Result" or image.name == "Viewer Node":
                continue

            # Skip normal map if auto-optimizing file size and it's not elected to be reformatted.
            if reformat_all and "Normal" in image.name and not include_normal_map:
                continue
            
            if texture_map in image.name or reformat_all:
                image_path = str(Path.resolve(Path(bpy.path.abspath(image.filepath))))

                # Get image name from saved image filepath, not the image in the editor. (This is to account for GLB's not including the image extension in the image name when importing a GLB and exporting again with packed textures.)
                image.name = Path(image_path).name

                # Change image extension and pathing.
                image_ext = "." + image.name.split(".")[-1].lower()
                image_ext_new = ext_dict[texture_format]
                image_path_new = str(Path.resolve(Path(bpy.path.abspath(image.filepath.replace(image_ext, image_ext_new)))))
                
                # Don't reformat image if converting between identical formats.
                if image_ext == image_ext_new:
                    print(f"Skipped Reformat Image ({image.name}): Current format ({image_ext.upper()[1:]}) = New format ({texture_format})")
                    logging.info(f"Skipped Reformat Image ({image.name}): Current format ({image_ext.upper()[1:]}) = New format ({texture_format})")
                    continue

                # Change image name.
                image_name = image.name
                image_name_new = image.name.replace(image_ext, image_ext_new)

                # Save image as input specified by the User.
                image.save_render(filepath = image_path_new)
                if image_path != image_path_new and Path(image_path).exists():  # Don't delete image if converting to the same file format.
                    Path.unlink(Path(image_path))

                # Repath the image textures to the new format.
                image.name = image_name_new
                bpy.data.images[image.name].filepath = image_path_new

                # Ensure alpha modes and color spaces are set appropriately for EXR format.
                if texture_format == "OPEN_EXR":
                    image.alpha_mode = 'PREMUL'
                    print(f"{image.name}'s alpha mode was set to 'Premultiplied' for EXR format.")
                    logging.info(f"{image.name}'s alpha mode was set to 'Premultiplied' for EXR format.")
                    if pbr_tag == "BaseColor":
                        image.colorspace_settings.name = 'Linear'
                        print(f"{image.name}'s BaseColor texture's color space was set to 'Linear' for EXR format.")
                        logging.info(f"{image.name}'s BaseColor texture's color space was set to 'Linear' for EXR format.")

                # Ensure alpha modes and color spaces are set appropriately for non-EXR formats.
                elif texture_format != "OPEN_EXR" and image_ext == ".exr":
                    image.alpha_mode = 'STRAIGHT'
                    print(f"{image.name}'s alpha mode was set to 'Straight'.")
                    logging.info(f"{image.name}'s alpha mode was set to 'Straight'.")
                    if pbr_tag == "BaseColor":
                        image.colorspace_settings.name = 'sRGB'
                        print(f"{image.name}'s BaseColor texture's color space was set to 'sRGB'.")
                        logging.info(f"{image.name}'s BaseColor texture's color space was set to 'sRGB'.")

                print(f"Reformatted Image ({image_name}): {image_ext.upper()[1:]} --> {texture_format}")
                logging.info(f"Reformatted Image ({image_name}): {image_ext.upper()[1:]} --> {texture_format}")

        print("Reformatted images")
        logging.info("Reformatted images")

    except Exception as Argument:
        logging.exception("Could not reformat images")
		    

def save_blend(blend):
    try:
        # Reset color management to the default Blender file, sRGB Filmic.
        set_color_management(
            texture_format='PNG', 
            image_quality=90,
            display_device='sRGB', 
            view_transform='Filmic', 
            look='None', 
            exposure=0, 
            gamma=1, 
            sequencer='sRGB', 
            use_curves=False, 
        )

        # Preserve unused materials & textures by setting fake user(s).
        use_fake_user()

        # Frame object(s) in the viewport before saving.
        override = override_context('VIEW_3D', 'WINDOW')
        with bpy.context.temp_override(**override):
            bpy.ops.view3d.view_all(center=False)

        # Save the file.
        bpy.ops.wm.save_as_mainfile(
            filepath=str(blend), 
        )

        # Delete Blender "save version" backup file (also known as a "blend1" file).
        blend1 = Path(f"{blend}1")
        if Path(blend1).is_file():
            Path.unlink(blend1)

        print(f"Saved blend file: {Path(blend).name}")
        logging.info(f"Saved blend file: {Path(blend).name}")

    except Exception as Argument:
        logging.exception(f"Could not save blend file: {Path(blend).name}")


# Save a .blend file preserving all materials created even if some are not assigned to any objects.
def pack_and_save_blend(blend, textures_temp_dir, pack_textures, absolute_paths):
    try:
        # Always pack textures and then determine whether to unpack and repath.
        bpy.ops.file.pack_all()
        
        # Unpack, copy unpacked textures to directory matching Blend name, and then repath textures to new directory.
        if not pack_textures:
            unpack_textures(blend.parent, textures_temp_dir, blend)
            blend_textures = blend.parent / (f"textures_{blend.stem}_blend")
            if blend_textures.exists():
                shutil.rmtree(blend_textures)
            shutil.copytree(textures_temp_dir, blend_textures)
            repath_blend_textures(blend, blend_textures)
            if not absolute_paths:
                bpy.ops.file.make_paths_relative()            

        # Save the Blend
        save_blend(blend)

    except Exception as Argument:
        logging.exception(f"Could not save blend file: {Path(blend).name}")
		

# Save.blend file and unpack images to textures_temp whenever packed images are used for conversion and are to be resized and/or reformatted.
def unpack_textures(item_dir, textures_temp_dir, blend):
    try:
        # Check if a textures_dir exists already
        textures_dir_check = "".join([i.name for i in Path(item_dir).iterdir() if i.name.lower() == "textures"])  # Assumes a GNU/Linux or MacOS User does not have something like "textures" and "Textures" directories in item_dir.
        if textures_dir_check != "":
            textures_dir = Path(item_dir) / textures_dir_check  # Reset textures_dir to be case-sensitive for GNU/Linux or MacOS Users.
            textures_original = textures_dir.parent / (f"{textures_dir.name}_original") 
            textures_dir.rename(textures_original)

        # Save blend file.
        save_blend(blend)
        
        # Unpack images
        bpy.ops.file.unpack_all(method='WRITE_LOCAL')
        textures_dir_unpack = Path(item_dir) / "textures"
        
        # Create textures_temp_dir
        if Path(textures_temp_dir).exists():
            shutil.rmtree(textures_temp_dir)
        textures_dir_unpack.rename(textures_temp_dir)

        # Return textures_original to textures if there was a textures directory to begin with.
        if textures_dir_check != "":
            textures_original.rename(textures_dir)

        print("Unpacked textures")
        logging.info("Unpacked textures")

    except Exception as Argument:
        logging.exception("Could not unpack textures")
		

# Returns a dictionary of which textures are assigned to which materials.
def map_textures_to_materials(import_file):
    try:
        materials = []
        texture_sets = []
        for material in bpy.data.materials:
            if material.node_tree:
                material_name = material.name
                materials.append(material_name)
                texture_set = []
                for node in material.node_tree.nodes:
                    if node.type=='TEX_IMAGE':
                        texture = Path(node.image.name).stem  # Remove any leftover image texture extensions.
                        if import_file.suffix == ".glb":
                            if "BaseColor" in texture:
                                base_color = texture.replace("_Opacity", "")
                                texture_set.append(base_color)
                                if node.outputs['Alpha'].is_linked:
                                    opacity = texture.replace("_BaseColor", "")
                                    texture_set.append(opacity)
                            elif "Roughness" in texture:
                                roughness = texture.replace("_Metallic", "")
                                metallic = texture.replace("_Roughness", "")
                                occlusion = texture.replace("_Roughness", "").replace("Metallic", "Occlusion")
                                texture_set.append(roughness)
                                texture_set.append(metallic)
                                texture_set.append(occlusion)
                            else:
                                texture_set.append(texture)
                        else:
                            texture_set.append(texture)
                texture_sets.append(texture_set)

        mapped_textures = dict(zip(materials, texture_sets))
        
        return mapped_textures

        print("Mapped textures to materials")
        logging.info("Mapped textures to materials")

    except Exception as Argument:
        logging.exception("Could not map textures to materials")


# Add material name as prefix to objects for later texture set matching.
def rename_objects_by_material_prefixes():
    try:
        objects = bpy.context.selected_objects
        for object in objects:
            if object.active_material:
                material_name_prefix = split_into_components(object.active_material.name)[0]
                object_name_prefix = split_into_components(object.name)[0]
                original_object_name = object.name
                if material_name_prefix != object_name_prefix:
                    object.name = f"{material_name_prefix}_{object.name}"
                    print(f"Renamed object with prefix of linked material ({object.active_material.name}): {original_object_name} --> {object.name}")
                    logging.info(f"Renamed object with prefix of linked material ({object.active_material.name}): {original_object_name} --> {object.name}")
                else:
                    print(f"Skipped Rename object: Object already shares prefix of linked material ({object.active_material.name}): {object.name}")
                    logging.info(f"Skipped Rename object: Object already shares prefix of linked material ({object.active_material.name}): {object.name}")

        print("Renamed objects by material prefixes")
        logging.info("Renamed objects by material prefixes")

    except Exception as Argument:
        logging.exception("Could not rename objects by material prefixes")
		

# Find and rename transparent materials that have mispellings of transparency with regex keys. Regex transparent materials to prepare for the next function, which deletes any opaque versions of those transparent materials by relying on "transparent" existing in the material name.
def regex_transparent_materials():
    try:
        for material in bpy.data.materials:
            material_name = material.name
            components_original = split_into_components(material_name)
            components = split_into_components(material_name)

            for component in components:
                transparency_tag_renamed = find_replace_transparency_tag(component)
                if transparency_tag_renamed != None:
                    transparency_tag_renamed = transparency_tag_renamed[0]
                    print(f"Found a match for {transparency_tag_renamed}")
                    logging.info(f"Found a match for {transparency_tag_renamed}")
                    tag_index = components.index(component)
                    components[tag_index] = transparency_tag_renamed

            if components_original != components:
                material_renamed = '_'.join(components)
                material.name = material_renamed
                print(f"Renamed {material_name} to {material_renamed}")
                logging.info(f"Renamed {material_name} to {material_renamed}")
                        
            else:
                print("No transparency tag match found for current material.")
                logging.info("No transparency tag match found for current material.")

        print("Regexed transparent materials")
        logging.info("Regexed transparent materials")

    except Exception as Argument:
        logging.exception("Could not regex transparent materials")


# Remove opaque versions of transparent materials to avoid duplicate textures bug, which resulted in models converting untextured.
def remove_opaque_material():
    try:
        transparent_material_list = [material.name for material in bpy.data.materials if "transparent" in material.name]
        if transparent_material_list:
            for material in transparent_material_list:
                opaque_material_name = material.replace("_transparent", "")
                if opaque_material_name in bpy.data.materials:
                    opaque_material = bpy.data.materials[opaque_material_name]
                    bpy.data.materials.remove(opaque_material)
                    print(f"Removed {opaque_material_name} material data block.")
                    logging.info(f"Removed {opaque_material_name} material data block.")

        print("Removed opaque material version of transparent material")
        logging.info("Removed opaque material version of transparent material")

    except Exception as Argument:
        logging.exception("Could not remove opaque material version of transparent material")


# Rename the separated output images with something similar to the combined image name.
def rename_output(image_texture_ext, image, image_name, add_tag, tag_1, tag_2, tag_3, textures_temp_dir, output):
    try:
        # Get the original image's extension to use.
        image_ext = image_texture_ext[image.file_format]

        # Remove any existing tags from image name.
        if tag_1 == "BaseColor":
            image_name = image_name.replace("_" + tag_1, "").replace("_" + tag_2, "")
        else:
            image_name = image_name.replace("_" + tag_1, "").replace("_" + tag_2, "").replace("_" + tag_3, "")
        
        # Create new image name from un-tagged image name.
        new_image_name = image_name + "_" + add_tag + image_ext

        # Create placeholder path for the tag image name
        new_image_path = Path(textures_temp_dir, new_image_name)

        # Get the output path of the current output.
        output_path = Path(textures_temp_dir, output)

        # Rename the output to something closer to the combined image name.
        if Path(output_path).exists() and not Path(new_image_path).exists():
            Path(output_path).rename(new_image_path)
            print(f"Output renamed from {output} to {new_image_name}")
            logging.info(f"Output renamed from {output} to {new_image_name}")
        else:
            if Path(output_path).exists():
                Path.unlink(output_path)
                print(f"{new_image_path} already exists. Deleted output.")
                logging.info(f"{new_image_path} already exists. Deleted output.")
        
    except Exception as Argument:
        logging.exception("Could not rename output")
		

# Render the output of the compositor, then rename outputs with something similar to the combined image name.
def render_output(textures_temp_dir, image_node, tag_1, tag_2, tag_3, image_texture_ext):
    try:
        # Get a list of either ORM images or BO images.
        combined_images_list = [i for i in bpy.data.images if tag_1.lower() in i.name.lower() and tag_2.lower() in i.name.lower()]
        combined_images_list_names = [i.name for i in combined_images_list]
        print(f"Combined images detected: {combined_images_list_names}")
        logging.info(f"Combined images detected: {combined_images_list_names}")

        if combined_images_list:
            for image in combined_images_list:
                # Get image name without an extension
                image_name = Path(image.name).stem
                # Set the current image in the Image Node BO to current image from combined_images_list
                # Set compositor variables.
                scene = bpy.context.scene
                compositing_node_tree = scene.node_tree
                compositing_node_tree.nodes[image_node].image = image
                # Output the images to textures_temp_dir
                bpy.ops.render.render(use_viewport=False)
                
                # Create variable with "0001" appended to tags
                keyframe = "0001"
                tag_1_k = tag_1 + keyframe
                tag_2_k = tag_2 + keyframe
                if tag_3 == "":  # When separating BO, only two arguments are used, so make the 3rd one null, in a sense.
                    tag_3_k = tag_2_k
                elif tag_3 != "":  # When separating ORM, three arguments are used.
                    tag_3_k = tag_3 + keyframe
                # Now get a list of images and rename them before the next combined map output overwrites them.
                output_list = [i.name for i in Path.iterdir(textures_temp_dir) if tag_1_k in i.name or tag_2_k in i.name or tag_3_k in i.name]
                print(f"Output list: {output_list}")
                logging.info(f"Output list: {output_list}")
                if output_list:
                    for output in output_list:
                        if tag_1_k in output:
                            add_tag = tag_1
                            rename_output(image_texture_ext, image, image_name, add_tag, tag_1, tag_2, tag_3, textures_temp_dir, output)
                        elif tag_2_k in output:
                            add_tag = tag_2
                            rename_output(image_texture_ext, image, image_name, add_tag, tag_1, tag_2, tag_3, textures_temp_dir, output)
                        elif tag_3_k in output and tag_3_k != tag_2_k:
                            add_tag = tag_3
                            rename_output(image_texture_ext, image, image_name, add_tag, tag_1, tag_2, tag_3, textures_temp_dir, output)
                
                # Finally, remove the original combined image.
                image_path = textures_temp_dir / Path(bpy.path.abspath(image.filepath)).name
                if image_path.exists():
                    Path.unlink(image_path)
                else:
                    print("No such combined image exists")
                    logging.info("No such combined image exists")

        print("Rendered output")
        logging.info("Rendered output")

    except Exception as Argument:
        logging.exception("Could not render output")
		

# Separate any combined image maps if imported model extension is ".glb".
def separate_gltf_maps(textures_temp_dir):
    try:
        # Set color management to sRGB Standard. If view_transform is set to Filmic, then BaseColor images containing transparency will separate as at least a 5MB file. 
        set_color_management(
            texture_format='PNG', 
            image_quality=90,
            display_device='sRGB', 
            view_transform='Standard', 
            look='None', 
            exposure=0, 
            gamma=1, 
            sequencer='sRGB', 
            use_curves=False, 
        )

        # Get image extension dictionary
        image_texture_ext = image_texture_ext_dict()
        
        # Set tags
        tag_basecolor = "BaseColor"
        tag_opacity = "Opacity"
        tag_occlusion = "Occlusion"
        tag_roughness = "Roughness"
        tag_metallic = "Metallic"
        # Make a list from the tags for later loops
        tags_BO = [tag_basecolor, tag_opacity]
        tags_ORM = [tag_roughness, tag_metallic, tag_occlusion]
        # Assign node names to variables
        image_node_BO = 'Image Node BO'
        image_node_ORM = 'Image Node ORM'
        file_output_ORM_node_name = 'File Output ORM'
        file_output_BO_node_name = 'File Output BO'
        # Make a list from the tags for later loops
        file_output_node_list = [file_output_ORM_node_name, file_output_BO_node_name]
        
        # Set compositor variables.
        scene = bpy.context.scene
        compositing_node_tree = scene.node_tree
        bpy.data.scenes["Scene"].node_tree.nodes["File Output BO"].base_path = str(textures_temp_dir)
        bpy.data.scenes["Scene"].node_tree.nodes["File Output ORM"].base_path = str(textures_temp_dir)
        
        # Mute the opposite File Output node before rendering any outputs.
        for file_output in file_output_node_list:
            # Separate and rename ORM map channels. 
            if file_output == file_output_ORM_node_name:
                compositing_node_tree.nodes[file_output_ORM_node_name].mute = False
                compositing_node_tree.nodes[file_output_BO_node_name].mute = True
                image_node = image_node_ORM
                tag_1 = tags_ORM[0]
                tag_2 = tags_ORM[1]
                tag_3 = tags_ORM[2] 
                render_output(textures_temp_dir, image_node, tag_1, tag_2, tag_3, image_texture_ext)

            # Separate and rename BO map channels.             
            elif file_output == file_output_BO_node_name:
                compositing_node_tree.nodes[file_output_ORM_node_name].mute = True
                compositing_node_tree.nodes[file_output_BO_node_name].mute = False
                image_node = image_node_BO
                tag_1 = tags_BO[0]
                tag_2 = tags_BO[1]
                tag_3 = ""
                render_output(textures_temp_dir, image_node, tag_1, tag_2, tag_3, image_texture_ext)
                
            else:
                print("Is there another File Output node?")
                logging.info("Is there another File Output node?")
                        
        # Mute both nodes after finishing.
        compositing_node_tree.nodes[file_output_ORM_node_name].mute = True
        compositing_node_tree.nodes[file_output_BO_node_name].mute = True

        print("Separated glTF 'ORM' and 'BO' image texture maps")
        logging.info("Separated glTF 'ORM' and 'BO' image texture maps")

    except Exception as Argument:
        logging.exception("Could not separate glTF 'ORM' and 'BO' image texture maps")


# If there is more than one material imported with the GLB but there exists at least one objects with two or more material slots, 
# separate meshes by their material assignment as distinct objects each with their own single material.
def separate_by_material():
    # If object type is mesh and mode is set to object
    try:
        if bpy.context.object.type == 'MESH' and bpy.context.mode == 'OBJECT':
            # Edit Mode
            bpy.ops.object.mode_set(mode='EDIT')
            # Seperate by material
            bpy.ops.mesh.separate(type='MATERIAL')
            # Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')
        
        print("Separated meshes into objects by materials")
        logging.info("Separated meshes into objects by materials")

    except Exception as Argument:
        logging.exception("Could not separate meshes into objects by materials")


# Rename textures based on associated material's prefix (for packed textures only)
def rename_textures_packed(textures_temp_dir):
    try:
        # Get Principled BSDF inputs as list of pairs of image texture names and pbr tag names.
        def get_node_inputs(node):
            texture_list = []
            for input in node.inputs:
                for node_links in input.links:
                    pbr_tag = input.name
                    texture = node_links.from_node.name
                    if pbr_tag == "Base Color" or pbr_tag == "Alpha":
                        image = material.node_tree.nodes.get(texture)
                        if image.outputs["Alpha"].is_linked:
                            pbr_tag = "BaseColor_Opacity"
                        elif not image.outputs["Alpha"].is_linked:
                            if pbr_tag == "Base Color":
                                pbr_tag = "BaseColor"
                            elif pbr_tag == "Alpha":
                                pbr_tag = "Opacity"
                    elif texture == "Normal Map":
                        normal_map = material.node_tree.nodes.get("Normal Map")
                        texture = normal_map.inputs["Color"].links[0].from_node.name
                    elif texture == "Separate Color":
                        orm_map = material.node_tree.nodes.get("Separate Color")
                        texture = orm_map.inputs["Color"].links[0].from_node.name
                        pbr_tag = "Metallic_Roughness"
                    node_pair = [texture, pbr_tag]
                    texture_list.append(node_pair)
            
            # Remove duplicates
            texture_list = [list(i) for i in set(map(tuple, texture_list))]

            return texture_list


        # Rename the textures based from retrieved list.
        def rename_textures(texture_list, material, materials, transparent_tag, image_texture_ext):
            try:
                for node_pair in texture_list:
                    node = bpy.data.materials[material.name].node_tree.nodes[node_pair[0]]
                    # Skip over an image texture in opaque material if it's shared between that material and a sister transparent material. Only get shared textures (including opacity map) from transparent material
                    if transparent_tag not in material.name and material.name + transparent_tag in materials and node.image.users != 1:
                        continue

                    # Get original image name.
                    image_name = node.image.name
                    # Get the original image's extension to use.
                    image_ext = image_texture_ext[node.image.file_format]

                    # Rename the image texture.
                    new_image_name = material.name + "_" + node_pair[1] + image_ext
                    #  If there's a transparent material and a sister opaque material that uses all the same textures except opacity, don't include "transparent" in name
                    if transparent_tag in material.name and material.name.replace(transparent_tag, "") in materials:
                        new_image_name = new_image_name.replace(transparent_tag, "")
                    node.image.name = new_image_name
                    
                    print(f"Renamed texture with prefix of associated material ({material.name}): {image_name} --> {new_image_name}")
                    logging.info(f"Renamed texture with prefix of associated material ({material.name}): {image_name} --> {new_image_name}")
            
            except AttributeError:
                print("Image texture node does not contain an image")
                logging.error("Image texture node does not contain an image")


        materials = [material.name for material in bpy.data.materials]  # Get a list of materials.
        transparent_tag = "_transparent"
        image_texture_ext = image_texture_ext_dict()  # Get image extension dictionary

        # Add material prefix to images before regexing.
        for material in bpy.data.materials:
            if material.node_tree:
                print(f"material: {material.name}")
                logging.info(f"material: {material.name}")

                bsdf = material.node_tree.nodes.get("Principled BSDF")
                texture_list = get_node_inputs(bsdf)
                rename_textures(texture_list, material, materials, transparent_tag, image_texture_ext)

        # Regex image textures before unpacking.
        if regex_textures:
            regex_textures_packed()
        
        print("Renamed packed textures")
        logging.info("Renamed packed textures")

    except Exception as Argument:
        logging.exception("Could not rename packed textures")
		

# Rename unpacked textures to match image names, since images packed into .blend have original texture filepaths
# and names baked into their data, which is what is used when unpacking textures.
def rename_textures_unpacked(textures_temp_dir):
    try:
        for image in bpy.data.images:
            path_old = Path(textures_temp_dir) / Path.resolve(Path(bpy.path.abspath(image.filepath))).name
            path_new = Path(textures_temp_dir) / image.name

            path_old.rename(path_new)

            image.filepath = str(path_new)

            print(f"Renamed {path_old.name} to {path_new.name}")
            logging.info(f"Renamed {path_old.name} to {path_new.name}")

        print("Renamed unpacked textures")
        logging.info("Renamed unpacked textures")

    except Exception as Argument:
        logging.exception("Could not rename unpacked textures")


# For packed textures, reimport textures to respective existing materials after they have been unpacked and separated.
def reimport_textures_to_existing_materials(textures_temp_dir, mapped_textures):
    try:
        for material in bpy.data.materials:
            if material.name == "Dots Stroke":
                continue
            
            # Define material for handoff to add principled setup function.
            material = material

            # Import textures with Node Wrangler addon
            image_ext = supported_image_ext()  # Get a list of image extensions that could be used as textures
            textures_available = [image.name for image in Path.iterdir(textures_temp_dir) if image.name.lower().endswith(image_ext)]
            textures = [texture for texture in textures_available if Path(texture).stem in mapped_textures[material.name]]

           # Add principled setup via Node Wrangler.
            add_principled_setup(material, textures_temp_dir, textures)

        print("Re-imported textures to existing materials")
        logging.info("Re-imported textures to existing materials")
    
    except Exception as Argument:
        logging.exception("Could not re-import textures to existing materials")


# Delete all nodes for all materials except Principled BSDF's and Material Outputs.
def remove_nodes_except_shaders():
        # Sever all input connections to the Principled shader to prepare for texture reimport.
        for material in bpy.data.materials:
            if material.name == "Dots Stroke":
                continue
            material_node = material.node_tree.nodes
            for node in material_node:
                if node.name == "Principled BSDF" or node.name == "Material Output":
                    continue
                material_node.remove(node)
            

# Set object data names as object names. Sometimes, upon export, object data names are used instead of object names, depending on the export format (e.g. USD).
# Code adapted from Simple Renaming Panel (GPL-3.0 License, https://github.com/Weisl/simple_renaming_panel/), renaming_operators.py, Line 609
def data_name_from_object():
    try:
        for obj in bpy.context.selected_objects:
            objName = obj.name
            if hasattr(obj, 'data') and obj.data != None:
                old_name = obj.data.name
                new_name = objName
                obj.data.name = new_name
                print(f"Renamed object data from {old_name} to {new_name}")
                logging.info(f"Renamed object data from {old_name} to {new_name}")

        print("Set data names from objects")
        logging.info("Set data names from objects")
    
    except Exception as Argument:
        logging.exception("Could not set data names from objects")


# Set all UV map names to "UVMap". This prevents a material issue with USDZ's - when object A and object B share the same material, but their UV
# map names differ, the material has to pick one UVMap in the UV Map node inputs connected to each texture channel. So if object A's UV map is called
# "UVMap" but object B's UV map is called "UV_Channel", then the shared material may pick "UV_Channel" as the UV inputs, thus causing object A to appear
# untextured despite the fact that it shares the same material as object B.
def rename_UV_maps():
    try:
        for obj in bpy.context.selected_objects:
            uv_index = 1
            # Loop through every UV map except the first one and rename as "[UVMap]_1", "[UVMap]_2", etc.
            for uvmap in obj.data.uv_layers[1:]:
                old_name = uvmap.name
                uvmap.name = str(rename_uvs_name) + str(uv_index)
                new_name = uvmap.name
                uv_index += 1

                print(f"Renamed UV map for object ({obj.name}): {old_name} --> {new_name}")
                logging.info(f"Renamed UV map for object ({obj.name}): {old_name} --> {new_name}")
            
            # Now go back to the first UV map and rename. If this was done first and another UV channel existed with that name, then the first UV channel would be named
            # like "UV_Map.001" which is not desirable and may contain a character compatible with USD format or Maya (i.e. ".").
            old_name = obj.data.uv_layers[0].name
            obj.data.uv_layers[0].name = str(rename_uvs_name)
            new_name = obj.data.uv_layers[0].name

            print(f"Renamed UV map for object ({obj.name}): {old_name} --> {new_name}")
            logging.info(f"Renamed UV map for object ({obj.name}): {old_name} --> {new_name}")
                

        print("Renamed uv maps")
        logging.info("Renamed uv maps")
    
    except Exception as Argument:
        logging.exception("Could not rename uv maps")


# Scale all objects by the factors provided.
def transform_resize(scales_list):
    try:
        bpy.ops.transform.resize(
            value=tuple(scales_list), 
            orient_type='GLOBAL', 
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
            orient_matrix_type='GLOBAL', 
            center_override=(0, 0, 0)
            )

        print(f"Scaled objects: {scales_list}")
        logging.info(f"Scaled objects: {scales_list}")

    except Exception as Argument:
        logging.exception("Could not scale objects")


# Rotate all objects by angles provided.
def transform_rotate(angles_list):
    try:
        axes = ["X", "Y", "Z"]
        axis_index = 0
        for angle in angles_list:
            constraint_axes = [False, False, False]
            constraint_axes[axis_index] = True
            bpy.ops.transform.rotate(
                value=angle, 
                orient_axis=axes[axis_index], 
                orient_type='GLOBAL', 
                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                orient_matrix_type='GLOBAL',
                constraint_axis=tuple(constraint_axes),
                center_override=(0, 0, 0)
            )
            axis_index += 1

        print(f"Rotated objects: {angles_list}")
        logging.info(f"Rotated objects: {angles_list}")

    except Exception as Argument:
        logging.exception("Could not rotate objects")


# Move all objects by lengths provided.
def transform_translate(lengths_list):
    try:
        bpy.ops.transform.translate(
            value=tuple(lengths_list), 
            orient_type='GLOBAL'
        )

        print(f"Translated objects: {lengths_list}")
        logging.info(f"Translated objects: {lengths_list}")

    except Exception as Argument:
        logging.exception("Could not translate objects")


# Set custom transformations if requested by the User.
def set_transformations(set_transforms_filter, set_location, set_rotation, set_scale):
    try:
        # All objects (including empties) have already been selected.
        if "Location" in set_transforms_filter:
            transform_translate(set_location)
        if "Rotation" in set_transforms_filter:
            transform_rotate(set_rotation)
        if "Scale" in set_transforms_filter:
            transform_resize(set_scale)

        print(f"Set transformations: {set_transforms_filter}")
        logging.info(f"Set transformations: {set_transforms_filter}")

    except Exception as Argument:
        logging.exception("Could not set transformations")
		

# Set scene units before exporting.
def set_scene_units(unit_system, length_unit):
    try:
        bpy.context.scene.unit_settings.system = unit_system
        print(f"Set scene unit system: {unit_system}")
        logging.info(f"Set scene unit system: {unit_system}")

        bpy.context.scene.unit_settings.length_unit = length_unit
        print(f"Set scene length unit: {length_unit}")
        logging.info(f"Set scene length unit: {length_unit}")

        print("Set scene units")
        logging.info("Set scene units")

    except Exception as Argument:
        logging.exception("Could not set scene units")


# Create a new directory in a given directory.
def make_directory(destination, name):
    try:
        new_dir = destination / name  # destination needs to be a Path.
        if destination.exists():
            if not new_dir.exists():
                Path.mkdir(new_dir)

        print(f"Made directory: {new_dir}")
        logging.info(f"Made directory: {new_dir}")

        return new_dir

    except Exception as Argument:
        logging.exception(f"Could not make directory: {new_dir}")


# Export a model.
def export_a_model(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, draco_compression):  # MAYBE ADD DRACO COMPRESSION FLAG HERE, E.G. draco_compression
    try:
        # Set scale
        export_scale = export_settings_dict["scale"]
        transform_resize([export_scale, export_scale, export_scale])
        print(f"Scaled models: {export_scale}")
        logging.info(f"Scaled models: {export_scale}")
        
        # Apply transforms if requested
        if apply_transforms:
            apply_transformations(apply_transforms_filter)
        
        # Get export options as a dictionary.
        options = eval(export_settings_dict["options"])

        # Set filepath to the location of the model to be exported.
        options["filepath"] = str(export_file)

        # Turn on Draco compression if auto-optimizing files and exporting a GLB.
        if draco_compression and export_settings_dict["extension"] == ".glb":
            options["export_draco_mesh_compression_enable"] = True
            options["export_draco_mesh_compression_level"] = compression_level

        # Get export operator.
        operator = export_settings_dict["operator"]
        operator = f"{operator}{options})"  # Concatenate the export command with the export options dictionary.

        # Create export directory if it doesn't yet exist (e.g. when exporting to a non-adjacent directory with subdirectories)
        make_directory(export_dir.parent, export_dir.name)

        # Use pack_and_save_blend function instead of generic "bpy.ops.wm.save_as_mainfile" that doesn't take into account some User options.
        if export_file.suffix == ".blend":
            pack_and_save_blend(export_file, textures_temp_dir, export_settings_dict["pack_resources"], export_settings_dict["use_absolute_paths"])

        # Run operator, which is stored as a string and won't run otherwise.
        else:
            exec(operator)
            print(operator)
            logging.info(operator)

        # Reset scale
        export_scale_reset = 1 / export_scale
        transform_resize([export_scale_reset, export_scale_reset, export_scale_reset])
        print(f"Reset model scale: {export_scale_reset}")
        logging.info(f"Reset model scale: {export_scale_reset}")
       
        # Apply transforms if requested
        if apply_transforms:
            apply_transformations(apply_transforms_filter)
        
        print(f"Exported a model: {export_file.name}")
        logging.info(f"Exported a model: {export_file.name}")

    except Exception as Argument:
        logging.exception("Could not export a model")


# Deletes the temporary textures folder.
def delete_textures_temp(textures_temp_dir):
    try:
        if Path(textures_temp_dir).exists():
            shutil.rmtree(textures_temp_dir)

        print("Deleted temporary textures directory")
        logging.info("Deleted temporary textures directory")

    except Exception as Argument:
        logging.exception("Could not delete temporary textures directory")
		

# Get file size of export_file
def get_export_file_size(export_file):
    try:
        if Path(export_file).exists():
            # Get current file size (in MB)
            export_file_size = round((Path(export_file).stat().st_size / 1048576), 2)
        
        else:
            export_file_size = 0
            print(f"{Path(export_file).name} doesn't exist.")
            logging.info(f"{Path(export_file).name} doesn't exist.")
        
        print(f"Got exported file size: {Path(export_file).name} = {export_file_size} MB")
        logging.info(f"Got exported file size: {Path(export_file).name} = {export_file_size} MB")
        
        return export_file_size

    except Exception as Argument:
        logging.exception(f"Could not get exported file size: {Path(export_file).name}")
		

# Decimate objects to reduce file size.
def decimate_objects():
    try:
        # Add a decimate modifier.
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = 0.5
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True

        # Add a weighted normal modifier to try to keep the original shading.
        bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = 3.14159

        # Copy modifiers to all selected objects.
        bpy.ops.object.make_links_data(type='MODIFIERS')

        # Apply modifiers.
        for ob in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = ob
            for name in [m.name for m in ob.modifiers]:
                bpy.ops.object.modifier_apply(modifier = name)
        
        print("Decimated meshes by a factor of 0.5")
        logging.info("Decimated meshes by a factor of 0.5")

    except Exception as Argument:
        logging.exception("Could not decimate objects")


# Auto resize premise: Get maximum image texture dimensions to use as a starting point for resizing textures.
def get_texture_resolution_maximum():
    try:
        resolution_list = []
        for image in bpy.data.images:
            width, height = image.size
            resolution_list.append(width)
            resolution_list.append(height)  # Check both in case non-square textures are used.
        
        texture_resolution_maximum = max(resolution_list)
        return texture_resolution_maximum

        print("Got texture resolution maximum for Auto Resize Files")
        logging.info("Got texture resolution maximum for Auto Resize Files")

    except Exception as Argument:
        logging.exception("Could not get texture resolution maximum for Auto Resize Files")


# Turn on draco-compression if elected and if exporting a GLB.
def draco_compression_check(export_settings_dict):
    try:
        if optimize_draco and export_settings_dict["extension"] == ".glb":
            return True
        return False

    except Exception as Argument:
        logging.exception("Could not check Draco compression")


# Auto resize method: Draco-Compress
def draco_compress_and_export(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file):
    try:
        # Turn on draco-compression if elected and if exporting a GLB.
        draco_compression = draco_compression_check(export_settings_dict)
        
        print("#################  Draco-Compress  #################")
        logging.info("#################  Draco-Compress  #################")

        export_a_model(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, draco_compression)

    except Exception as Argument:
        logging.exception("Could not Draco-compress model for Auto Resize Files")


# Auto resize method: Resize textures
def resize_textures_and_export(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, texture_resolution_current):
    try:
        if optimize_texture_resize:
            if texture_resolution_current / 2 >= resize_textures_limit:
                print("#################  Resize Textures  #################")
                logging.info("#################  Resize Textures  #################")
                texture_resolution_current = int(texture_resolution_current / 2)
                # Resize textures (again) and re-export.
                resize_textures("BaseColor", texture_resolution_current, resize_all = True)

                # Turn on draco-compression if elected and if exporting a GLB.
                draco_compression = draco_compression_check(export_settings_dict)

                export_a_model(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, draco_compression)
            
            elif texture_resolution_current / 2 < resize_textures_limit:
                print("#################  Resize Textures  #################")
                logging.info("#################  Resize Textures  #################")
                print(f"Skipped Resize Textures: Current Resolution ({texture_resolution_current}) <= Resize Limit ({resize_textures_limit})")
                logging.info(f"Skipped Resize Textures: Current Resolution ({texture_resolution_current}) <= Resize Limit ({resize_textures_limit})")

        # Return current resolution.
        return texture_resolution_current

    except Exception as Argument:
        logging.exception("Could not resize textures for Auto Resize Files")


# Auto resize method: Reformat textures
def reformat_textures_and_export(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file):
    try:
        if optimize_texture_reformat:
            print("#################  Reformat Textures  #################")
            logging.info("#################  Reformat Textures  #################")
            texture_format = 'JPEG'
            image_quality = 90
                       
            reformat_images("BaseColor", texture_format, image_quality, True, include_normal_maps)

            # Turn on draco-compression if elected and if exporting a GLB.
            draco_compression = draco_compression_check(export_settings_dict)
            
            export_a_model(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, draco_compression)

    except Exception as Argument:
        logging.exception("Could not reformat textures for Auto Resize Files")


# Auto resize method: Decimate meshes
def decimate_meshes_and_export(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, decimate_counter):
    try:
        if optimize_decimate:
            if decimate_counter <= decimate_limit:
                print("#################  Decimate Meshes  #################")
                logging.info("#################  Decimate Meshes  #################")
                select_only_meshes()
                decimate_objects()
                select_all()

                # Turn on draco-compression if elected and if exporting a GLB.
                draco_compression = draco_compression_check(export_settings_dict)

                export_a_model(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, draco_compression)
                decimate_counter += 1

            elif decimate_counter > decimate_limit:
                print("#################  Decimate Meshes  #################")
                logging.info("#################  Decimate Meshes  #################")
                print(f"Skipped Decimate Meshes: Decimation iteration ({decimate_counter}) = Decimate Limit ({decimate_limit})")
                logging.info(f"Skipped Decimate Meshes: Decimation iteration ({decimate_counter}) = Decimate Limit ({decimate_limit})")
        
        return decimate_counter

    except Exception as Argument:
        logging.exception("Could not decimate meshes for Auto Resize Files")


# Try to automatically to optimize the exported file's size.
def optimize_export_file(item_dir, item_name, import_file, textures_dir, textures_temp_dir, export_settings_dict, export_dir, export_file):
    try:
        # Get current file size (in MB)
        export_file_size = get_export_file_size(export_file)
        texture_resolution_start = get_texture_resolution_maximum()  # Always start with largest existing resolution. That way resizing textures will always occur before reformatting.
        texture_resolution_current = texture_resolution_start
        decimate_counter = 0

        while export_file_size > optimize_target_file_size:
            print("#############################  NEW AUTO FILE RESIZE ITERATION  #############################")
            logging.info("#############################  NEW AUTO FILE RESIZE ITERATION  #############################")
            
            # 1. Draco
            draco_compress_and_export(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file)
            # check
            export_file_size = get_export_file_size(export_file)
            if export_file_size < optimize_target_file_size:
                break

            # 2. Resize
            texture_resolution_current = resize_textures_and_export(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, texture_resolution_current)
            # check
            export_file_size = get_export_file_size(export_file)
            if export_file_size < optimize_target_file_size:
                break
           
            # 3. Reformat
            reformat_textures_and_export(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file)
            # check
            export_file_size = get_export_file_size(export_file)
            if export_file_size < optimize_target_file_size:
                break

            # (4.) Decimate
            decimate_counter = decimate_meshes_and_export(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, decimate_counter)
            # check
            export_file_size = get_export_file_size(export_file)
            if export_file_size < optimize_target_file_size:
                break
            
            # Repeat unless all methods are exhausted.
            if not optimize_texture_resize and not optimize_decimate:
                break
            elif optimize_texture_resize and optimize_decimate:
                if texture_resolution_current <= resize_textures_limit and decimate_counter >= decimate_limit:
                    break
            if optimize_texture_resize and not optimize_decimate:
                if texture_resolution_current <= resize_textures_limit:
                    break
            elif not optimize_texture_resize and optimize_decimate:
                if decimate_counter >= decimate_limit:
                    break

        # Report on how the auto-resizing turned out.
        if export_file_size < optimize_target_file_size:
            print(f"{Path(export_file).name} ({export_file_size} MB) < File Size Limit ({optimize_target_file_size} MB).")
            logging.info(f"{Path(export_file).name} ({export_file_size} MB) < File Size Limit ({optimize_target_file_size} MB).")
        elif export_file_size > optimize_target_file_size:
            print(f"Exhausted Auto Resize Files methods. Exiting. {Path(export_file).name} file size ({export_file_size} MB) > File Size Limit ({optimize_target_file_size} MB).")
            logging.info(f"Exhausted Auto Resize Files methods. Exiting. {Path(export_file).name} file size ({export_file_size} MB) > File Size Limit ({optimize_target_file_size} MB).")
        
        print("Auto Resized Files")
        logging.info("Auto Resized Files")

    except Exception as Argument:
        logging.exception("Could not Auto Resize Files")


# Modify textures if requested.
def modify_textures():
    try:
        for edit_textures_dict in textures:
            texture_map = edit_textures_dict["texture_map"]
            texture_resolution = edit_textures_dict["texture_resolution"]
            texture_format = edit_textures_dict["texture_format"]
            image_quality = edit_textures_dict["image_quality"]
            
            if texture_resolution != "Default":
                resize_textures(texture_map, texture_resolution, False)
            
            if texture_format != "Default":
                reformat_images(texture_map, texture_format, image_quality, False, False)

        print("Modified textures")
        logging.info("Modified textures")

    except Exception as Argument:
        logging.exception("Could not determine whether to modify textures")


# Apply "Custom" textures to objects.
def apply_textures_custom(item_dir, item_name, import_file, textures_dir, textures_temp_dir, blend, conversion_count):
    try:
        # Regex transparent objects before creating materials and searching for matches between transparent material(s) and transparent object(s).
        if regex_textures:
            regex_transparent_objects()
        
        # Clear all users of all materials.
        clear_materials_users()

        # Remove existing materials and textures from Converter.blend file only once.
        clean_data_block(bpy.data.materials)
        clean_data_block(bpy.data.images)

        if conversion_count == 0:
            # Create a temporary textures directory beside the custom textures directory.
            create_textures_temp(Path(textures_custom_dir), Path(textures_custom_dir), textures_temp_dir)
            
            # Regex external custom textures.
            if regex_textures:
                regex_textures_external(textures_temp_dir)

            # Create materials.
            create_materials(item_name, textures_temp_dir)
            
            # Modify textures if requested.
            modify_textures()

            # Remove existing materials and textures again.
            clean_data_block(bpy.data.materials)
            clean_data_block(bpy.data.images)

        # Copy textures_temp from custom textures directory to item_name directory.
        copy_file(item_dir, textures_temp_dir)

        # Rename and use the local copy of textures_temp_dir so it's possible to archive assets later.
        textures_temp_dir = item_dir / textures_temp_dir.name
        textures_temp_dir_renamed = item_dir / (f"textures_{blend.stem}")
        if Path(textures_temp_dir_renamed).exists():  # Remove the local copy of temporary textures directory if it already exists from a prior conversion.
            shutil.rmtree(textures_temp_dir_renamed)
        Path(textures_temp_dir).rename(textures_temp_dir_renamed)
        textures_temp_dir = textures_temp_dir_renamed

        # Create materials.
        create_materials(item_name, textures_temp_dir)

        # Assign materials to objects.
        assign_materials(item_name)

        # Copy original custom textures to item_name directory if elected.
        if copy_textures_custom_dir:
            copy_textures_from_custom_source(textures_custom_dir, item_dir, textures_dir, preserve_original_textures)
        
        print("Applied custom textures to objects")
        logging.info("Applied custom textures to objects")

    except Exception as Argument:
        logging.exception("Could not apply custom textures to objects")


# Rename textures_temp_dir and repath images inside the .blend.
def repath_blend_textures(blend, path_new):
    try:
        for image in bpy.data.images:  # Repath the textures.
            bpy.data.images[image.name].filepath = str(path_new / image.name)
        
        print("Renamed modified textures directory and repathed blend")
        logging.info("Renamed modified textures directory and repathed blend")
        
        save_blend(blend)  # Save the .blend.

    except Exception as Argument:
        logging.exception("Could not rename modified textures directory or repath blend")


# Apply "Packed" textures to objects.
def apply_textures_packed(item_dir, item_name, import_file, textures_dir, textures_temp_dir, blend):
    try:
        # Find and rename transparent materials that have mispellings of transparency with regex keys. 
        regex_transparent_materials()

        # Purge orphaned opaque image textures if they are duplicates, rather than shared/instanced data blocks.
        purge_orphans()

        # Make sure image textures have their material's prefix before unpacking to avoid any duplicate texture names if they were all lower-cased.
        rename_textures_packed(textures_temp_dir)

        # Delete any existing textures_temp_dir before unpacking.
        delete_textures_temp(textures_temp_dir)

        # Unpack textures before modifying them.
        unpack_textures(item_dir, textures_temp_dir, blend)

        # Rename unpacked textures to match image name, since images packed into .blend use names from 
        #  original texture filepath baked into their data instead of the image name.
        if import_file.suffix == ".blend":
            rename_textures_unpacked(textures_temp_dir)

        # Modify textures if requested.
        if import_file.suffix != ".glb":
            modify_textures()

        # Only separate image textures if imported file is a GLB.
        elif import_file.suffix == ".glb":
            # Get a dictionary of which textures are assigned to which materials.
            mapped_textures = map_textures_to_materials(import_file)

            # Separate the combined maps.
            separate_gltf_maps(textures_temp_dir)

            # Remove existing images from Converter.blend file.
            clean_data_block(bpy.data.images)
            
            # Delete all nodes for all materials except Principled BSDF's and Material Outputs.
            remove_nodes_except_shaders()

            # Reimport unpacked & separated textures to their original materials.
            reimport_textures_to_existing_materials(textures_temp_dir, mapped_textures)
            
            # Modify textures if requested.
            modify_textures()
        
        # Delete saved .blend that was used for unpacking textures.
        Path.unlink(blend)
                
        print("Applied packed textures to objects")
        logging.info("Applied packed textures to objects")

    except Exception as Argument:
        logging.exception("Could not apply packed textures to objects")


# Apply "External" textures to objects.
def apply_textures_external(item_dir, item_name, import_file, textures_dir, textures_temp_dir, blend):
    try:    
        if import_file.suffix == ".blend" and use_linked_blend_textures:  # Skip apply textures to objects if they're already set up in the imported .blend file.
            print("Using external textures already linked to .blend for conversion")
            logging.info("Using external textures already linked to .blend for conversion")

            # Pack linked textures into .blend since they may be sourced from many different directories.
            bpy.ops.file.pack_all()

            # Pretend that these textures were "Packed" all along.
            apply_textures_packed(item_dir, item_name, import_file, textures_dir, textures_temp_dir, blend)

            return

        # Regex transparent objects before creating materials and searching for matches between transparent material(s) and transparent object(s).
        if regex_textures:
            regex_transparent_objects()

        # Clear all users of all materials.
        clear_materials_users()
        
        # Brute force-remove all materials and images.
        clean_data_block(bpy.data.materials)
        clean_data_block(bpy.data.images)

        # Check if a "textures" directory exists.
        textures_dir_check = "".join([i.name for i in Path(item_dir).iterdir() if i.name.lower() == "textures"])  # Assumes a GNU/Linux or MacOS User does not have something like "textures" and "Textures" directories in item_dir.
        if textures_dir_check != "":
            textures_dir = Path(item_dir) / textures_dir_check  # Reset textures_dir to be case-sensitive for GNU/Linux or MacOS Users.
        
        # Create temporary textures directory.
        create_textures_temp(item_dir, textures_dir, textures_temp_dir)

        # Regex textures if requested.
        if regex_textures:
            regex_textures_external(textures_temp_dir)

        # Create materials.
        create_materials(item_name, textures_temp_dir)

        # Modify textures if requested.
        modify_textures()

        # Assign materials to objects.
        assign_materials(item_name)

        print("Applied external textures to objects")
        logging.info("Applied external textures to objects")

    except Exception as Argument:
        logging.exception("Could not apply external textures to objects")


# Determine where textures should be sourced, then texture the model.
def apply_textures(item_dir, item_name, import_file, textures_dir, textures_temp_dir, blend):
    try:
        if textures_source == "External":
            apply_textures_external(item_dir, item_name, import_file, textures_dir, textures_temp_dir, blend)
            
        elif textures_source == "Packed":
            apply_textures_packed(item_dir, item_name, import_file, textures_dir, textures_temp_dir, blend)
            
        elif textures_source == "Custom":
            apply_textures_custom(item_dir, item_name, import_file, textures_dir, textures_temp_dir, blend, conversion_count)
            
        print("Applied textures to objects")
        logging.info("Applied textures to objects")

    except Exception as Argument:
        logging.exception("Could not apply textures to objects")
		
        
# Import UV images to Blender for reformatting.
def import_uv_image(uv_path):
    try:
        bpy.ops.image.open(filepath=str(uv_path))

        print(f"Imported UV image: {Path(uv_path).name}")
        logging.info(f"Imported UV image: {Path(uv_path).name}")

    except Exception as Argument:
        logging.exception(f"Could not import UV image: {Path(uv_path).name}")


# Export UV Layout.
def export_a_uv_layout(item_name, name, directory, export_all):
    try:
        uv_name = prefix + item_name + name + suffix + "_UV." + uv_format.lower()
        uv_path = str(Path(directory) / uv_name)
        export_uv_layout_options = {
            "filepath": uv_path,
            "export_all": export_all, 
            "modified": modified_uvs, 
            "mode": uv_format, 
            "size": (uv_resolution, uv_resolution),
            "opacity": uv_fill_opacity, 
            "check_existing": True
        }

        uv_default_formats = ("PNG", "SVG", "EPS")
        if uv_format not in uv_default_formats:
            export_uv_layout_options["mode"] = "PNG"  # Save as bitmap because all other image non-default options are bitmaps.
            uv_path_png = uv_path.replace(uv_format.lower(), "png")
            export_uv_layout_options["filepath"] = uv_path_png

        export_uv_layout_command = "bpy.ops.uv.export_layout(**" + str(export_uv_layout_options) + ")"
        print(export_uv_layout_command)
        logging.info(export_uv_layout_command)
        exec(export_uv_layout_command)
        
        if uv_format not in uv_default_formats:
            import_uv_image(uv_path_png)

        print("Exported UV layout")
        logging.info("Exported UV layout")

    except Exception as Argument:
        logging.exception("Could not export UV layout")


# Create a directory.  Overwrite if exists.
def create_a_directory(directory):
    try:
        if Path(directory).exists():
            return
        elif not Path(directory).exists():
            Path(directory).mkdir()

        print(f"Created a directory: {Path(directory)}")
        logging.info(f"Created a directory: {Path(directory)}")

    except Exception as Argument:
        logging.exception(f"Could not create a directory: {Path(directory)}")


# Get UV directory based on menu option.
def determine_uv_directory(textures_dir):
    try:
        if uv_export_location == "Textures":
            directory = textures_dir
            create_a_directory(directory)
        elif uv_export_location == "UV":
            directory = Path(textures_dir).parent / "UV"
            create_a_directory(directory)
        elif uv_export_location == "Adjacents":
            directory = Path(textures_dir).parent
        elif uv_export_location == "Custom":
            directory = Path(uv_directory_custom)

        print("Determined UV directory")
        logging.info("Determined UV directory")
        return directory
    
    except Exception as Argument:
        logging.exception("Could not determine UV directory")


# Determine whether to keep modified or copied textures after the conversion is over for a given item_name.
def determine_keep_edited_textures(item_dir, import_file, export_file, textures_dir, textures_temp_dir, blend):
    try:        
        # Delete temporary textures directory (local copy for Custom textures scenario) if elected.
        if not keep_edited_textures:
            textures_temp_dir = item_dir / (f"textures_{blend.stem}")
            delete_textures_temp(textures_temp_dir)
        
        # Delete local copy of textures directory for Custom textures scenario if elected.
        elif textures_source == "Custom" and not copy_textures_custom_dir:
            remove_copy_textures_custom_dir(item_dir, textures_dir)

        print("Determined whether to keep modified textures")
        logging.info("Determined whether to keep modified textures")
    
    except Exception as Argument:
        logging.exception("Could not determine whether to keep modified textures")


# Determine how to export UV layouts.
def determine_export_uv_layout(item_name, textures_dir):
    try:
        directory = determine_uv_directory(textures_dir)
        if uv_combination == "All":
            export_all = True
            name = ""
            export_a_uv_layout(item_name, name, directory, export_all)
        elif uv_combination == "Object":
            export_all = False
            select_only_meshes()
            objects = [object for object in bpy.context.selected_objects]
            for object in objects:
                deselect_all()
                object.select_set(object.type == "MESH")
                bpy.context.view_layer.objects.active = object
                export_a_uv_layout(item_name + "_", object.name, directory, export_all)
        elif uv_combination == "Material":
            export_all = False
            for material in bpy.data.materials:
                deselect_all()
                select_by_material(material)
                item_name = ""
                export_a_uv_layout(item_name, material.name, directory, export_all)
        
        uv_default_formats = ("PNG", "SVG", "EPS")
        if uv_format not in uv_default_formats:
            uv_tag = "_UV"
            reformat_images(uv_tag, uv_format, uv_image_quality, False, False)

        print("Determined how to export UV layout(s)")
        logging.info("Determined how to export UV layout(s)")

    except Exception as Argument:
        logging.exception("Could not determine how to export UV layout(s)")


# Run a custom script.
def run_custom_scripts(trigger):
    try:
        for script in scripts:
            if script["trigger"] != trigger:  # Skip the script if it's not the right time to run it.
                continue
            
            # Get script name.
            script_name = script["name"]

            # Run script in the current "Converter.blend" session (not as a subprocess).
            exec(compile(open(script["file"]).read(), script["file"], 'exec'))

            print(f"Ran custom script: {script_name}")
            logging.info(f"Ran custom script: {script_name}")

    except Exception as Argument:
        logging.exception(f"Could not run custom script: {script_name}")


# Determine whether asset preview has finished generating.
# Source: https://projects.blender.org/blender/blender/issues/93893#issuecomment-168540
def preview_finished(asset):
    try:
        arr = np.zeros((asset.preview.image_size[0] * asset.preview.image_size[1]) * 4, dtype=np.float32)
        asset.preview.image_pixels_float.foreach_get(arr)
        if np.all((arr == 0)):
            return False
        return True

    except Exception as Argument:
        logging.exception("Could not determine if Asset Preview finished.")


# Generate preview image for asset browser.
def generate_preview(asset):
    try:
        with bpy.context.temp_override(id=asset):
            bpy.ops.ed.lib_id_generate_preview()
        
        while True:
            if preview_finished(asset):
                break
            time.sleep(0.1)

        print(f"Generated Asset Preview: {asset.name}")
        logging.info(f"Generated Asset Preview: {asset.name}")

    except Exception as Argument:
        logging.exception(f"Could not generate Asset Preview: {asset.name}")


# Determine whether the asset can have a preview image generated for it.
# Source: Gorgious56's "asset_browser_utilities" addon: https://github.com/Gorgious56/asset_browser_utilities,
# asset_browser_utilities/module/preview/tool.py, Line 11
def can_preview_be_generated(asset):
    try:
        if isinstance(
            asset,
            (
                bpy.types.Action,
                bpy.types.Brush,
                bpy.types.Collection,
                bpy.types.ShaderNodeTree,
                bpy.types.Light,
                bpy.types.Material,
                bpy.types.Screen,
                bpy.types.Texture,
                bpy.types.World,
            ),
        ):
            return True
        elif isinstance(asset, bpy.types.Object):
            if asset.type in ("MESH", "FONT", "LIGHT", "GREASEPENCIL", "SURFACE", "META"):
                if asset.type == "MESH" and len(asset.data.polygons) == 0:
                    return False
                return True
        elif isinstance(asset, bpy.types.Image):
            return bool(asset.pixels)
        return False

    except Exception as Argument:
        logging.exception(f"Could not determine whether Asset Preview could be generated for: {asset.name}")


# Add tag to asset.
def add_asset_tag(asset, tag):
    try:
        asset.asset_data.tags.new(tag)

        print(f"Added tag: {tag}")
        logging.info(f"Added tag: {tag}")

    except Exception as Argument:
        logging.exception(f"Could not add tag: {tag}")


# Add tags to asset.
def add_asset_tags(asset):
    try:
        if asset_tags == "":  # Don't add a blank tag.
            return

        tags = split_into_components(asset_tags)
        for tag in tags:
            add_asset_tag(asset, tag)

        print(f"Added Tags to Asset: {asset.name}")
        logging.info(f"Added Tags to Asset: {asset.name}")

    except Exception as Argument:
        logging.exception(f"Could not Add Tags to Asset: {asset.name}")


# Add metadata to asset.
def add_metadata_to_asset(asset):
    try:
        asset.asset_data.description = asset_description
        asset.asset_data.license = asset_license
        asset.asset_data.copyright = asset_copyright
        asset.asset_data.author = asset_author
        add_asset_tags(asset)

        print(f"Added Metadata to Asset: {asset.name}")
        logging.info(f"Added Metadata to Asset: {asset.name}")

    except Exception as Argument:
        logging.exception(f"Added Metadata to Asset: {asset.name}")


# Create an image in bpy.data.images
# Source: Gorgious56's "asset_browser_utilities" addon: https://github.com/Gorgious56/asset_browser_utilities,
# module/preview/tool.py, Line 38
def create_image(name, width, height, alpha=True):
    try:
        image = bpy.data.images.new(
            name=name, 
            width=width, 
            height=height, 
            alpha=alpha
        )
        return image

    except Exception as Argument:
        logging.exception(f"Could not create image: {name}")


# Extract generated asset preview to disk.
# Source: Gorgious56's "asset_browser_utilities" addon: https://github.com/Gorgious56/asset_browser_utilities,
# asset_browser_utilities/module/preview/operator/extract.py, Line 29
def extract_preview_to_disk(asset, asset_type, item_name, blend):
    try:
        folder = Path(blend).parent
        asset_preview = asset.preview
        
        if asset_preview is not None and asset_type in asset_extract_previews_filter:
            image_name = f"Preview_{item_name}_{asset_type}_{asset.name}"
            image = create_image(image_name, asset_preview.image_size[0], asset_preview.image_size[1])
            image.file_format = "PNG"
            for char in ("/", "\\", ":", "|", '"', "!", "?", "<", ">", "*"):
                if char in image.name:
                    image.name = image.name.replace(char, "_")
            image.filepath = str(folder / f"{image.name}.png")
            
            try:
                image.pixels.foreach_set(asset_preview.image_pixels_float)
            except TypeError:
                logging.exception(f"Could not Extract Asset Preview: {image_name}")
            else:
                image.save()
                print(f"Extracted Asset Preview: {image_name}")
                logging.info(f"Extracted Asset Preview: {image_name}")

            bpy.data.images.remove(image)
        
        else:
            return False

    except Exception as Argument:
        logging.exception(f"Could not Extract Asset Preview: {image_name}")


# Mark asset.
def mark_asset(asset, asset_type, assets_in_library, item_name, blend):
    try:
        if not assets_allow_duplicates and asset_type not in assets_allow_duplicates_filter and asset.name in assets_in_library[asset_type]:  # Don't mark data-block as an asset if an asset with that name already exists in the selected Asset Library.
            print(f"Skipped Mark Asset: {asset.name}.  Asset already exists in Library: {asset_library}")
            logging.info(f"Skipped Mark Asset: {asset.name}.  Asset already exists in Library: {asset_library}")
            return
        
        asset.asset_mark()  # Mark asset.

        if asset_library != "NO_LIBRARY" and asset_catalog != "NO_CATALOG":
            asset.asset_data.catalog_id = asset_catalog  # Assign to catalog.

        if asset_add_metadata:
            add_metadata_to_asset(asset)  # Add metadata.

        if can_preview_be_generated(asset):
            generate_preview(asset)  # Generate preview.

        if asset_extract_previews:
            extract_preview_to_disk(asset, asset_type, item_name, blend)  # Extract preview.

        print(f"Marked Asset: {asset.name}")
        logging.info(f"Marked Asset: {asset.name}")

    except Exception as Argument:
        logging.exception(f"Could not Mark Asset: {asset.name}")


# Get a dictionary of asset names by data-block type that exist in a given asset library.
def get_assets_in_library(library_name):
    try:
        keys = ["Actions", "Collections", "Materials", "Node_Groups", "Objects", "Worlds"]   # Keys are the asset types for which duplicates should be allow.
        values = [[] for key in keys]  # Placeholder lists to be filled later.
        assets_in_library = dict(zip(keys, values))  # Create an template dictionary to fill.
        
        if library_name == "NO_LIBRARY" or library_name == "(no library)":
            return assets_in_library  # Return a dictionary with empty values if User did not select an asset library.

        asset_libraries = bpy.context.preferences.filepaths.asset_libraries
        asset_library = asset_libraries.data.asset_libraries[library_name]
        library_path = Path(asset_library.path)
        blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]
        print(f"Checking the contents of library '{library_name}':")
        for blend_file in blend_files:
            with bpy.data.libraries.load(str(blend_file), assets_only=True) as (file_contents, _):
                for key in keys:
                    assets = eval(f"file_contents.{key.lower()}")
                    assets_in_library[key] += assets  # Add assets of given data block to their associated list in the dictionary.
        
        print(f"Got Assets in Library ({library_name}): {assets_in_library}")
        logging.info(f"Got Assets in Library ({library_name}): {assets_in_library}")
        
        return assets_in_library

    except Exception as Argument:
        logging.exception(f"Could not get Assets in Library ({library_name}): {assets_in_library}")


# Mark assets in asset data filter.
def mark_assets(item_name, blend):
    try:
        assets_in_library = get_assets_in_library(asset_library)  # Get a dictionary of assets in the selected asset library.

        if "Actions" in asset_types_to_mark:
            for action in bpy.data.actions:
                mark_asset(action, "Actions", assets_in_library, item_name, blend)
        
        if "Collections" in asset_types_to_mark:
            master_collection_name = item_name
            for collection in bpy.data.collections:
                if mark_only_master_collection and collection.name != master_collection_name:
                    continue
                mark_asset(collection, "Collections", assets_in_library, item_name, blend)
                
        if "Materials" in asset_types_to_mark:
            for material in bpy.data.materials:
                mark_asset(material, "Materials", assets_in_library, item_name, blend)

        if "Node_Groups" in asset_types_to_mark:
            for node_group in bpy.data.node_groups:
                mark_asset(node_group, "Node_Groups", assets_in_library, item_name, blend)
    
        if "Objects" in asset_types_to_mark:
            for object in bpy.data.objects:
                if not object.type in asset_object_types_filter:  # Mark only certain selected object types as assets.
                    continue
                mark_asset(object, "Objects", assets_in_library, item_name, blend)

        if "Worlds" in asset_types_to_mark:
            for world in bpy.data.worlds:
                mark_asset(world, "Worlds", assets_in_library, item_name, blend)

        print("Marked assets")
        logging.info("Marked assets")

    except Exception as Argument:
        logging.exception("Could not mark assets")


# Move/Copy blend file and textures to selected Asset Library.
def move_copy_blend_to_asset_library(item_name, blend):
    try:
        if asset_library != "NO_LIBRARY" and asset_library != "(no library)":
            asset_library_path = Path(bpy.context.preferences.filepaths.asset_libraries[asset_library].path)
            
            if asset_blend_location == "None":  # Return early if User elected to leave blend adjacent to each converted item_name.
                return

            asset_dir = make_directory(asset_library_path, blend.stem)
            blend_textures = blend.parent / (f"textures_{blend.stem}_blend")
            blend_and_associated_files = [blend, blend_textures]
            asset_previews = [file for file in blend.parent.iterdir() if file.name.startswith("Preview_") and file.suffix == ".png"]  # Get a list of extracted asset previews.
            
            for asset_preview in asset_previews:
                blend_and_associated_files.append(asset_preview)  # Append asset previews to list of files to be copied/moved.

            for file in blend_and_associated_files:
                if asset_blend_location == "Move":
                    move_file(asset_dir, file)
                elif asset_blend_location == "Copy":
                    copy_file(asset_dir, file)

        print("Moved/Copied Blend and Associated Files to Asset Library")
        logging.info("Moved/Copied Blend and Associated Files to Asset Library")

    except Exception as Argument:
        logging.exception("Could not Move/Copy Blend and Associated Files to Asset Library")


# Archive assets to Asset Library by marking, tagging, and cataloging.
def archive_assets_to_library(item_name, blend, textures_temp_dir):
    try:
        mark_assets(item_name, blend)
        pack_and_save_blend(blend, textures_temp_dir, asset_pack_resources, asset_use_absolute_paths)
        move_copy_blend_to_asset_library(item_name, blend)

        print(f"Archived Assets to library: {asset_library}")
        logging.info(f"Archived Assets to library: {asset_library}")

    except Exception as Argument:
        logging.exception(f"Could not archive Assets to library: {asset_library}")


def converter_stage_export(import_settings_dict, import_file, item_name, item_dir, export_name, textures_dir, textures_temp_dir, blend, export_settings_dict, export_dir, export_file):
    try:
        # Export a model.
        export_a_model(item_name, item_dir, textures_temp_dir, export_settings_dict, export_dir, export_file, False)
        
        # Try to automatically to optimize the exported file's size.
        if optimize:
            optimize_export_file(item_dir, item_name, import_file, textures_dir, textures_temp_dir, export_settings_dict, export_dir, export_file)
        
        # Run custom scripts with triggers "After Export".
        run_custom_scripts("After_Export")

        # Copy files adjacent to the import_file to the custom export directory.
        if not link_export_settings and not export_settings_dict["export_adjacent"] and export_settings_dict["use_subdirectories"] and export_settings_dict["copy_original_contents"]:
            for file in Path.iterdir(item_dir):
                if file == textures_temp_dir:
                    continue
                copy_file(export_dir, file)

        print("-------------------------------------------------------------------")
        print(f"CONVERTER END: {import_file.name}")
        print("-------------------------------------------------------------------")
        logging.info("-------------------------------------------------------------------")
        logging.info(f"CONVERTER END: {import_file.name}")
        logging.info("-------------------------------------------------------------------")

    except Exception as Argument:
        logging.exception("COULD NOT COMPLETE CONVERTER STAGE EXPORT")


def converter_stage_import(import_settings_dict, import_file, item_name, item_dir, textures_dir, textures_temp_dir, blend):
    try:
        print("-------------------------------------------------------------------")
        print(f"CONVERTER START: {import_file.name}")
        print("-------------------------------------------------------------------")
        logging.info("-------------------------------------------------------------------")
        logging.info(f"CONVERTER START: {import_file.name}")
        logging.info("-------------------------------------------------------------------")

         # Set up scene.
        setup_scene(item_name)

        # Brute force-remove all materials and images.
        if textures_source != "Custom":
            clean_data_block(bpy.data.materials)
            clean_data_block(bpy.data.images)

        # Run custom scripts with triggers "Before Import".
        run_custom_scripts("Before_Import")

        # Import the file.
        import_a_file(import_file, import_settings_dict)

        # Move all objects and collections to item_name collection.
        move_objects_and_collections_to_item_collection(item_name)

        # Delete animations.
        if not use_animations:
            clear_animation_data()
        
        # Apply transformations.
        if apply_transforms:
            apply_transformations(apply_transforms_filter)

        # Select only mesh-type objects.
        select_only_meshes()

        # Determine whether to use textures and from where they should come.
        if use_textures:
            apply_textures(item_dir, item_name, import_file, textures_dir, textures_temp_dir, blend)
        elif not use_textures:
            clear_materials_users()  # Clear all users of all materials.
            clean_data_block(bpy.data.materials)  # Brute force-remove all materials and images.
            clean_data_block(bpy.data.images)
            
        # Set scene units.
        set_scene_units(unit_system, length_unit)

        # Set data name from object name if requested by User.
        if set_data_names:
            data_name_from_object()

        # Rename UV maps if requested by User.
        if rename_uvs:
            rename_UV_maps()

        # Select all objects in the scene before exporting, including empty objects.
        select_all()

        # Set transforms if requested by the User.
        if set_transforms:
            set_transformations(set_transforms_filter, set_location, set_rotation, set_scale)

        # Run custom scripts with triggers "Before Export".
        run_custom_scripts("Before_Export")

    except Exception as Argument:
        logging.exception("COULD NOT COMPLETE CONVERTER STAGE IMPORT")


# Convert the file for every file found inside the given directory.
def converter(import_settings_dict, import_file, item_name, item_dir, export_name, textures_dir, textures_temp_dir, blend, export_settings_dict, export_dir, export_file):
    try:
        converter_stage_import(import_settings_dict, import_file, item_name, item_dir, textures_dir, textures_temp_dir, blend)
        
        converter_stage_export(import_settings_dict, import_file, item_name, item_dir, export_name, textures_dir, textures_temp_dir, blend, export_settings_dict, export_dir, export_file)
    
    except Exception as Argument:
        logging.exception(f"COULD NOT CONVERT FILE: {import_file.name}")
		

# Write conversion report to a JSON file.
def report_conversion_count(conversion_count):
    try:
        # Data to be written
        conversion_report_dict = {
            "conversion_count": conversion_count,
        }
        
        json_file = Path(Path(__file__).parent.resolve(), "Converter_Report.json")

        with open(json_file, "w") as outfile:
            json.dump(conversion_report_dict, outfile)

        print("Reported conversion count")
        logging.info("Reported conversion count")

    except Exception as Argument:
        logging.exception("Could not report conversion count")
		

# Make a list of exports for the current item_name, which will then be appended to the full conversion_list to be reported in the log.
def list_exports(export_file):
    try:
        exports_list = []
        export_file_size = get_export_file_size(export_file)
        export_file_list = [export_file.name, export_file_size]
        exports_list.append(export_file_list)

        print("Listed exports")
        logging.info("Listed exports")

        return exports_list

    except Exception as Argument:
        logging.exception("Could not list exports")


# Determine whether to import a model before converting in order to save time.
def determine_import(import_file, export_settings_dict, export_dir, export_file):    
    try:
        if export_settings_dict["overwrite_files"]:
            # If export file exists and the target filter is set to only overwrite files above target, get the existing file's size and determine whether to import.
            if export_file.is_file() and optimize_overwrite_filter == "Only Above Target":
                export_file_size = get_export_file_size(export_file)
                if export_file_size < optimize_target_file_size:
                    return False
            # In all other cases where overwrite_files is True, import the file.
            return True

        elif not export_settings_dict["overwrite_files"]:
            # Don't import the file when not overwriting exports and the export file already exists.
            if export_file.is_file():
                return False
        
        # In all other cases, import the file.
        return True

    except Exception as Argument:
        logging.exception(f"Could not determine imports: {item_name}")


# Get export file and parent directory.
def get_export_file_and_directory(item_dir, export_settings_dict, export_name):
    try: 
        # Determine where to export the model.
        if export_settings_dict["export_adjacent"]:
            export_dir = item_dir
        
        # Replace the export directory with the custom export directory if not exporting models adjacent to each other.
        elif not export_settings_dict["export_adjacent"]:
            export_dir = Path(export_settings_dict["directory"])
            
            # Convert the export directory to a subdirectory after the item_name.
            if export_settings_dict["use_subdirectories"]:
                export_dir = export_dir / export_name
            
        export_ext = export_settings_dict["extension"]
        export_file = export_dir / f"{export_name}{export_ext}"

        return export_dir, export_file
    
    except Exception as Argument:
        logging.exception(f"Could not determine get export file")


# Main function that loops through specified directory and creates variables for the converter
def batch_converter():
    try:
        print("-------------------------------------------------------------------")
        print("---------------------  BATCH CONVERTER START  ---------------------")
        print("-------------------------------------------------------------------")
        logging.info("-------------------------------------------------------------------")
        logging.info("---------------------  BATCH CONVERTER START  ---------------------")
        logging.info("-------------------------------------------------------------------")

        # Set up a conversion count and list to report how many conversions took place and the final file sizes of each item_name.
        conversion_count = 0
        conversion_list = []

        # Create path to blender.exe and get version
        blender_dir = bpy.app.binary_path
        blender_version = bpy.app.version_string[:3]

        # Enable addons
        enable_addons()

        # Run custom scripts with triggers "Before Batch".
        run_custom_scripts("Before_Batch")

        # Loop through every import instance dictionary defined in Settings.json > "imports" setting.
        for import_settings_dict in imports:

            # Get a list of imports for the given import instance's format from the Imports.json dictionary.
            imports_list = import_settings_dict["files"]

            # Loop through files in the current imports list and determine imports/run converter for each.
            for import_file in imports_list:
                import_file = Path(import_file)
                item_name = import_file.stem
                item_dir = import_file.parent
                textures_dir = item_dir / "textures"
                textures_temp_dir = item_dir / f"{textures_dir}_{item_name}"
                if textures_source == "Custom":  
                    textures_temp_dir = Path(textures_custom_dir).parent / (f"{Path(textures_custom_dir).name}_temp")
                blend = item_dir / f"{item_name}.blend"

                # If auto-optimizing files, always re-import the import file for every export. 
                # This will take longer to convert, but provides the flexibility required for optimizing only as much as needed per export format.
                # e.g. a model with a high polycount can simply be Draco-compressed when exporting a GLB, but would require a destructive Decimate
                # modifier to achieve the same file size when exporting a USDZ.
                if optimize:
                    # Loop through exports and determine whether to import the file for each.
                    for export_settings_dict in exports:
                        # Set export_name-dependent variables.
                        export_prefix = export_settings_dict["prefix"]
                        export_suffix = export_settings_dict["suffix"]
                        export_name = f"{export_prefix}{item_name}{export_suffix}"
                        
                        # Get export file and parent directory.
                        export_dir, export_file = get_export_file_and_directory(item_dir, export_settings_dict, export_name)

                        # Determine which models are eligible for conversion.
                        import_check = determine_import(import_file, export_settings_dict, export_dir, export_file)
                                        
                        # If item is eligible for export, run the converter.
                        if import_check:
                            converter(import_settings_dict, import_file, item_name, item_dir, export_name, textures_dir, textures_temp_dir, blend, export_settings_dict, export_dir, export_file)
                            
                            conversion_count += 1

                
                # If not auto-optimizing files, only import the file once and edit the textures once, then export the file in every requested format.
                elif not optimize:
                    # Loop through exports and determine whether to import the file for each.
                    import_checklist = []
                    for export_settings_dict in exports:
                        # Set export_name-dependent variables.
                        export_prefix = export_settings_dict["prefix"]
                        export_suffix = export_settings_dict["suffix"]
                        export_name = f"{export_prefix}{item_name}{export_suffix}"

                        # Get export file and parent directory.
                        export_dir, export_file = get_export_file_and_directory(item_dir, export_settings_dict, export_name)

                        # Determine which models are eligible for conversion.
                        import_check = determine_import(import_file, export_settings_dict, export_dir, export_file)
                        
                        # Note eligibility on list.
                        import_checklist.append(import_check)
                        
                        # Update each export dictionary with import eligibility.
                        export_settings_dict.update(
                            {
                            "determine_import": import_check,
                            "export_name": export_name,
                            }
                        )
                    
                    # If at least one export file is eligible for export, import the file.
                    if True in import_checklist:
                        # Import the file.
                        converter_stage_import(import_settings_dict, import_file, item_name, item_dir, textures_dir, textures_temp_dir, blend)
                        
                        # Export files per import file.
                        for export_settings_dict in exports:
                            if export_settings_dict["determine_import"]:
                                export_name = export_settings_dict["export_name"]
                                
                                # Get export file and parent directory.
                                export_dir, export_file = get_export_file_and_directory(item_dir, export_settings_dict, export_name)
                                
                                # Convert and export the file.
                                converter_stage_export(import_settings_dict, import_file, item_name, item_dir, export_name, textures_dir, textures_temp_dir, blend, export_settings_dict, export_dir, export_file)
                                conversion_count += 1
        
                # Copy files adjacent to the import_file to the custom export directory.
                if link_export_settings and not export_adjacent and use_subdirectories and copy_original_contents:
                    for file in Path.iterdir(item_dir):
                        if file == textures_temp_dir:
                            continue
                        copy_file((Path(export_directory) / export_name), file)

                # Archive assets to library.
                if mark_as_assets:
                    archive_assets_to_library(item_name, blend, textures_temp_dir)

                # Save only single preview image of collections if desired when not archiving assets to library.
                if not mark_as_assets and asset_extract_previews:
                    asset_extract_previews_filter = ["Collections"]
                    asset_types_to_mark = ["Collections"]
                    mark_assets(item_name, blend)

                # Export UV Layout(s).
                if export_uv_layout:
                    determine_export_uv_layout(item_name, textures_dir)

                # Modified or copied textures can now be deleted after the conversion is over.
                if use_textures:
                    determine_keep_edited_textures(item_dir, import_file, export_file, textures_dir, textures_temp_dir, blend)
                
                # If using custom textures, delete temporary textures directory only after all items have been converted.
                if use_textures and textures_source == "Custom" and not keep_edited_textures:
                    textures_temp_dir = Path(textures_custom_dir).parent / (Path(textures_custom_dir).name + "_temp")
                    if Path(textures_temp_dir).exists():
                        delete_textures_temp(textures_temp_dir)

        # Run custom scripts with triggers "After Batch".
        run_custom_scripts("After_Batch")

        # Report conversion count to Converter_Report.json
        report_conversion_count(conversion_count)

        # Report final conversion count.
        print(f"{conversion_count} files were converted.")
        logging.info(f"{conversion_count} files were converted.")
        
        # Report list of files converted and their corresponding file sizes.
        print("ITEMS EXPORTED:")
        logging.info("ITEMS EXPORTED:")
        # for i in conversion_list:
        #     print(f"{i[0]} = {i[1]} MB.")
        #     logging.info(f"{i[0]} = {i[1]} MB.")

        print("-----------------------------------------------------------------")
        print("---------------------  BATCH CONVERTER END  ---------------------")
        print("-----------------------------------------------------------------")
        logging.info("-----------------------------------------------------------------")
        logging.info("---------------------  BATCH CONVERTER END  ---------------------")
        logging.info("-----------------------------------------------------------------")

    except Exception as Argument:
        logging.exception("Could not end Batch Converter")
		

# Quit Blender after batch conversion is complete.
def quit_blender():
    try:
        bpy.ops.wm.quit_blender()

        print("Quit Blender")
        logging.info("Quit Blender")

    except Exception as Argument:
        logging.exception("Could not quit Blender")
		

# Transmogrify.
def transmogrify():
    # Step 1: Set global variables.
    get_settings(["Settings.json"])

    # Step 2: Start logging conversion if requested by User.
    if save_conversion_log:
        make_log_file()

    # Step 3: Run the batch converter.
    batch_converter()

    # Step 4: Quit Blender after batch conversion is complete.
    quit_blender()


### Transmogrify! ###
transmogrify()