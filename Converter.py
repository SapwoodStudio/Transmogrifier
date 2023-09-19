# BEGIN GPL LICENSE BLOCK #####
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
#
# END GPL LICENSE BLOCK #####

import bpy
import os
import os.path
import datetime
import sys
import shutil
import pathlib
import json
import re
import logging


# Read Converter_Variables.json file where the user variables are stored.
def read_json():
    try:
        # Open JSON file
        json_file = os.path.join(pathlib.Path(__file__).parent.resolve(), "Converter_Variables.json")

        with open(json_file, 'r') as openfile:
        
            # Read from JSON file
            json_object = json.load(openfile)
        
        return json_object
        print("------------------------  READ CONVERTER_VARIABLES.JSON  ------------------------")
        logging.info("READ CONVERTER_VARIABLES.JSON")

    except Exception as Argument:
        logging.exception("COULD NOT READ CONVERTER_VARIABLES.JSON")


# Read dictionary of variables from JSON file.
def get_variables():
    try:
        # Assign variables from dictionary and make all variables global
        variables_dict = read_json()

        for key, value in variables_dict.items():
            # Preserve quotation marks during exec() if value is a string type object.
            if type(value) == str:
                value = repr(value)
            # Don't preserve quotation marks during exec() if value is not a string type object.
            else:
                value = str(value)

            # Concatenate command.
            variable_assignment_command = "globals()" + "['" + str(key) + "']" + " = " + value
            # Execute variable assignment.
            exec(variable_assignment_command)

        print("------------------------  GOT VARIABLES FROM JSON  ------------------------")
        logging.info("GOT VARIABLES FROM JSON")

    except Exception as Argument:
        logging.exception("COULD NOT GET VARIABLES FROM JSON")


# Make a log file to log conversion process.
def make_log_file():
    # Set path to log file with timestamp
    timestamp = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    if directory_output_location == "Custom":
        log_file = os.path.join(directory_output_custom, "Transmogrifier_Log_" + timestamp + ".txt")
    elif directory_output_location != "Custom":
        log_file = os.path.join(directory, "Transmogrifier_Log_" + timestamp + ".txt")
    
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

        print("------------------------  ENABLED ADDONS  ------------------------")
        logging.info("ENABLED ADDONS")

    except Exception as Argument:
        logging.exception("COULD NOT ENABLE ADDONS")


# Temporarily change interface theme to force a white background in Material Preview viewport mode for rendering Preview images.
def set_theme_light(blender_dir, blender_version):
    try:
        theme_white = os.path.join(pathlib.Path(blender_dir).parent.resolve(), blender_version, "scripts", "addons", "presets", "interface_theme", "White.xml")
        
        # White theme
        bpy.ops.script.execute_preset(
            filepath=theme_white, 
            menu_idname="USERPREF_MT_interface_theme_presets"
        )

        print("------------------------  SET THEME TO BLENDER LIGHT  ------------------------")
        logging.info("SET THEME TO BLENDER LIGHT")

    except Exception as Argument:
        logging.exception("COULD NOT SET THEME TO BLENDER LIGHT")


# Enable addon dependencies and clear the scene
def scene_setup():
    try:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        print("------------------------  SET UP SCENE  ------------------------")
        logging.info("SET UP SCENE")

    except Exception as Argument:
        logging.exception("COULD NOT SET UP SCENE")
		

# Recursively delete orphaned data blocks.
def purge_orphans():
    try:
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        print("------------------------  PURGED ORPHANED DATA BLOCKS RECURSIVELY  ------------------------")
        logging.info("PURGED ORPHANED DATA BLOCKS RECURSIVELY")

    except Exception as Argument:
        logging.exception("COULD NOT PURGE ORPHANED DATA BLOCKS RECURSIVELY")
		

# Sometimes purge orphans won't delete data blocks (e.g. images) even though they have no users. This will force the deletion of any data blocks within a specified bpy.data.[data type]
def clean_data_block(block):
    try:
        # iterate over every entry in the data block
        for data in block:
            block.remove(data)

        print("------------------------  CLEANED DATA BLOCK: " + str(block).upper() + "  ------------------------")
        logging.info("CLEANED DATA BLOCK: " + str(block).upper())

    except Exception as Argument:
        logging.exception("COULD NOT CLEAN DATA BLOCK: " + str(block).upper())
		

# Sometimes purge orphans won't delete data blocks (e.g. images) even though they have no users. This will force the deletion of any data blocks within a specified bpy.data.[data type]
def clean_data_block_except_custom(block, custom_data):
    try:
        # iterate over every entry in the data block
        for data in block:
            if data.name in custom_data:
                print("Preserved custom data: " + data.name)
                logging.info("Preserved custom data: " + data.name)
                continue
            block.remove(data)

        print("------------------------  CLEANED DATA BLOCK: " + str(block).upper() + "  ------------------------")
        logging.info("CLEANED DATA BLOCK: " + str(block).upper())

    except Exception as Argument:
        logging.exception("COULD NOT CLEAN DATA BLOCK: " + str(block).upper())


# Import file of a format type supplied by the user.
def import_file_function(import_file_command, import_file_options, import_file):
    try:
        import_file_options["filepath"] = import_file  # Set filepath to the location of the model to be imported
        import_file_command = str(import_file_command) + str(import_file_options) + ")"  # Concatenate the import command with the import options dictionary
        print(import_file_command)
        logging.info(import_file_command)
        exec(import_file_command)  # Run import_file_command, which is stored as a string and won't run otherwise.

        print("------------------------  IMPORTED FILE: " + str(os.path.basename(import_file)) + "  ------------------------")
        logging.info("IMPORTED FILE: " + str(os.path.basename(import_file)))

    except Exception as Argument:
        logging.exception("COULD NOT IMPORT FILE: " + str(os.path.basename(import_file)))
		

# Remove all animation data from imported objects. Sometimes 3DS Max exports objects with keyframes that cause scaling/transform issues in a GLB and USDZ.
def clear_animation_data():
    try:
        bpy.ops.object.select_all(action='SELECT')
        objects = bpy.context.scene.objects

        for object in objects:
            object.animation_data_clear()
            print("Deleted animations for " + object.name + ".")
            logging.info("Deleted animations for " + object.name + ".")
        
        print("------------------------  CLEARED ANIMATION DATA  ------------------------")
        logging.info("CLEARED ANIMATION DATA")

    except Exception as Argument:
        logging.exception("COULD NOT CLEARED ANIMATION DATA")
		

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

        print("------------------------  " + "APPLIED TRANSFORMATIONS: " + str(apply_transforms_filter) + "  ------------------------")
        logging.info("APPLIED TRANSFORMATIONS: " + str(apply_transforms_filter))

    except Exception as Argument:
        logging.exception("COULD NOT APPLY TRANSFORMATIONS: " + str(apply_transforms_filter))
		

# Clear all users of all materials.
def clear_materials_users():
    try:
        # Remove any imported materials.
        bpy.ops.view3d.materialutilities_remove_all_material_slots(only_active=False)
        
        # Delete any old materials that might have the same name as the imported object.
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        
        for material in bpy.data.materials:
            material.user_clear()

        print("------------------------  CLEARED ALL USERS OF ALL MATERIALS  ------------------------")
        logging.info("CLEARED ALL USERS OF ALL MATERIALS")

    except Exception as Argument:
        logging.exception("COULD NOT CLEAR ALL USERS OF ALL MATERIALS")


# Prevent an empty from being actively selected object. This prevents a later error from happening when imported materials are removed later.
def select_only_meshes():
    try:
        objects = bpy.context.scene.objects

        for object in objects:
            object.select_set(object.type == "MESH")
            object = bpy.context.window.scene.objects[0]
            bpy.context.view_layer.objects.active = object

        print("------------------------  SELECTED ONLY MESH-TYPE OBJECTS  ------------------------")
        logging.info("SELECTED ONLY MESH-TYPE OBJECTS")

    except Exception as Argument:
        logging.exception("COULD NOT SELECT ONLY MESH-TYPE OBJECTS")
		

# Copy textures from custom directory and apply to all models in directory.
def copy_textures_from_custom_source(textures_custom_dir, item_dir, textures_dir, replace_textures):
    try:
        if os.path.exists(textures_custom_dir):
            if os.path.exists(textures_dir):  # Cannot create another textures folder if one already exists.
                if replace_textures and copy_textures_custom_dir:  # If User elected to replace an existing textures directory might be inside the item folder, then delete it.
                    shutil.rmtree(textures_dir)
                else:  # If not, preserve existing textures folder by renaming adding an "_original" suffix.
                    textures_dir_name = [d for d in os.listdir(item_dir) if "textures" in d.lower()][0]  # Need to get specific textures_dir folder characters in case any other files are pathed to it.
                    textures_dir_original_name = [d for d in os.listdir(item_dir) if "textures" in d.lower()][0] + "_original"
                    textures_dir_original = os.path.join(item_dir, textures_dir_original_name)
                    if os.path.exists(textures_dir_original):  # If a textures folder had already existed and had been preserved as "textures_original", assume that the item_dir has already been transmogrified and the current textures_dir is a copy from the custom source.
                        shutil.rmtree(textures_dir)
                    elif not os.path.exists(textures_dir_original):  # If a textures folder already exists but had not yet been preserved as a "textures_orignal" folder, then rename it so.
                        os.rename(textures_dir, textures_dir_original)
            shutil.copytree(textures_custom_dir, textures_dir)  # Temporarily copy textures from custom directory as the current textures_dir.
        else:
            print("Custom textures directory does not exist.")
            logging.info("Custom textures directory does not exist.")

        print("------------------------  COPIED TEXTURES FROM CUSTOM SOURCE  ------------------------")
        logging.info("COPIED TEXTURES FROM CUSTOM SOURCE")

    except Exception as Argument:
        logging.exception("COULD NOT COPY TEXTURES FROM CUSTOM SOURCE")
		

# If User elected not to copy the custom textures directory to each item folder, delete the temporary copy of it there.
def remove_copy_textures_custom_dir(item_dir, textures_dir):
    try:
        if os.path.exists(textures_dir):
            shutil.rmtree(textures_dir)

        textures_dir_original_name = [d for d in os.listdir(item_dir) if "textures_original" in d.lower()]
        if textures_dir_original_name:  # If there was a textures_dir there before transmogrification, return its name to its original form.
            textures_dir_original_name = textures_dir_original_name[0]  # If the list is not empty, get the first item in the list.
            textures_dir_original = os.path.join(item_dir, textures_dir_original_name)
            if os.path.exists(textures_dir_original):  
                os.rename(textures_dir_original, os.path.join(item_dir, textures_dir_original_name.replace("_original", "")))  # Return original textures_dir back to its former name before the conversion.

        print("------------------------  REMOVED COPIED TEXTURES FROM CUSTOM SOURCE  ------------------------")
        logging.info("REMOVED COPIED TEXTURES FROM CUSTOM SOURCE")

    except Exception as Argument:
        logging.exception("COULD NOT REMOVE COPIED TEXTURES FROM CUSTOM SOURCE")
		

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

        print("------------------------  GOT SUPPORTED IMAGE EXTENSIONS  ------------------------")
        logging.info("GOT SUPPORTED IMAGE EXTENSIONS")

    except Exception as Argument:
        logging.exception("COULD NOT  GET SUPPORTED IMAGE EXTENSIONS")
		

# Remove textures_temp_dir
def delete_textures_temp(textures_temp_dir):
    try:
        # Delete "textures_temp" if folder already exists. It will already exist if the User elected to save a .blend file, and it may exist if Transmogrifier quit after an error.
        if os.path.exists(textures_temp_dir):
            shutil.rmtree(textures_temp_dir)
        
        print("------------------------  DELETED TEMPORARY TEXTURES DIRECTORY  ------------------------")
        logging.info("DELETED TEMPORARY TEXTURES DIRECTORY")

    except Exception as Argument:
        logging.exception("COULD NOT DELETE TEMPORARY TEXTURES DIRECTORY")
		

# Create a temporary textures folder where images can be resized and exported with specified models without affecting the quality of the original texture files. 
# If multiple texture sets exist, assign each image texture file a prefix of the name of it's parent texture set directory folder.
# If image textures already have a prefix of the same name as the texture set, don't add the same prefix again.
def create_textures_temp(item_dir, textures_dir, textures_temp_dir):
    try:
        # Delete "textures_temp" if folder already exists. It will already exist if the User elected to save a .blend file, and it may exist if Transmogrifier quit after an error.
        delete_textures_temp(textures_temp_dir)
        
        # Check if a "textures" directory exists and is not empty. Copy it and call it textures_temp if it does, otherwise create an empty directory and fill it with image textures found in the item_dir.
        if os.path.exists(textures_dir):
            # If a textures directory exists but is empty, make one and fill it with images.
            if not os.listdir(textures_dir):
                print("Textures directory is empty. Looking for textures in parent directory...")
                logging.info("Textures directory is empty. Looking for textures in parent directory...")
                os.makedirs(textures_temp_dir)
                image_ext = supported_image_ext()  # Get a list of image extensions that could be used as textures
                image_list = [file for file in os.listdir(item_dir) if file.lower().endswith(image_ext) and not file.endswith("_Preview.jpg")]  # Make a list of all potential texture candidates except for the Preview Image.
                if not image_list:  # i.e. if image_list is empty
                    print("No potential image textures found in " + str(item_dir))
                    logging.info("No potential image textures found in " + str(item_dir))
                else:
                    print("The following images will be copied to textures_temp: " + str(image_list))
                    logging.info("The following images will be copied to textures_temp: " + str(image_list))
                    for image in image_list:
                        image_src = os.path.join(item_dir, image)
                        image_dest = os.path.join(textures_temp_dir, image)
                        shutil.copy(image_src, image_dest)  # Copy each potential image texture to textures_temp

            # If a textures directory exists and is not empty, assume it contains images or texture set subdirectories containing images.
            else:
                shutil.copytree(textures_dir, textures_temp_dir)
        
        # If no textures directory exists, make one and fill it with images.
        else: 
            os.makedirs(textures_temp_dir)
            image_ext = supported_image_ext()  # Get a list of image extensions that could be used as textures
            image_list = [file for file in os.listdir(item_dir) if file.lower().endswith(image_ext) and not file.endswith("_Preview.jpg")]  # Make a list of all potential texture candidates except for the Preview Image.
            if not image_list:  # i.e. if image_list is empty
                print("No potential image textures found in " + str(item_dir))
                logging.info("No potential image textures found in " + str(item_dir))
            else:
                print("The following images will be copied to textures_temp: " + str(image_list))
                logging.info("The following images will be copied to textures_temp: " + str(image_list))
                for image in image_list:
                    image_src = os.path.join(item_dir, image)
                    image_dest = os.path.join(textures_temp_dir, image)
                    shutil.copy(image_src, image_dest)  # Copy each potential image texture to textures_temp

        print("------------------------  CREATED TEMPORARY TEXTURES DIRECTORY  ------------------------")
        logging.info("CREATED TEMPORARY TEXTURES DIRECTORY")

    except Exception as Argument:
        logging.exception("COULD NOT CREATE TEMPORARY TEXTURES DIRECTORY")
		

# Split image texture name into components to be regexed in find_replace_pbr_tag function.
# The following code is adapted from Blender 3.5, Node Wrangler 3.43, __util.py__, Line 7
def split_into_components(texture):
    try:
        """
        Split filename into components
        'WallTexture_diff_2k.002.jpg' -> ['WallTexture', 'diff', '2k', '002', 'jpg']
        """
        # Get original texture name for printout.
        texture_original = texture

        # Remove file path
        texture = texture.split(os.path.sep)[-1]
        
        # Replace common separators with SPACE
        separators = ["_", ".", "-", "__", "--", "#"]
        for sep in separators:
            texture = texture.replace(sep, " ")

        components = texture.split(" ")
        
        print("------------------------  SPLIT INTO COMPONENTS: " + str(os.path.basename(texture_original)) + " to " + str(components) + "  ------------------------")
        logging.info("SPLIT INTO COMPONENTS: " + str(os.path.basename(texture_original)) + " to " + str(components))

        return components


    except Exception as Argument:
        logging.exception("COULD NOT SPLIT INTO COMPONENTS: " + str(os.path.basename(texture)))
		

# Regex, i.e. find and replace messy/misspelled PBR tag with clean PBR tag in a given image texture's name supplied by the regex_textures_external function.
def find_replace_pbr_tag(texture):
    try:
        # Set original texture name.
        texture_original = texture

        # Dictionary with regex keys will be used as the pattern by turning it into a list then to a string.
        pbr_dict = {
            '[Bb]?ase*\s?_?[Cc]?olou?r|[Aa]?lbedo|[Dd]?iffuse|[Dd]?iff|[Cc]?olou?r': 'BaseColor',
            '[Ss]?ubsurface': 'Subsurface',
            '[Mm]?etall?ic|[Mm]?etalness?|[Mm]?etaln.*|[Mm]etal': 'Metallic', 
            '[Ss]?pecul.*|[Ss]pec': 'Specular',
            '[Rr]?ou?gh|[Rr]?ou?ghness': 'Roughness',
            '[Gg]?loss.*': 'Gloss',
            '[Nn]?ormal|[Nn]orm|[Nn]rml': 'Normal',
            '[Bb]?ump': 'Bump',
            '[Dd]?ispl.*|[Hh]?e?ight|[Hh]?i?eght': 'Height',
            '[Tt]?ransmission|[Tt]ransmiss|[Tt]rnsmss|[Tt]?ransm.*': 'Transmission',
            '[Ee]?miss.*|[Ee]mit': 'Emission',
            '[Aa]?lph.*|[Oo]?pac.*|[Tt]?ranspa.*|[Tt]?ranspr.*': 'Opacity',
            '[Aa]?mbient*\s?_?[Oo]?cc?lusion|[Aa]?mbient|[Oo]?cc?lus.*': 'Occlusion'
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

        print("------------------------  FOUND AND REPLACED PBR TAG: " + str(texture_original) + " to " + str(texture) + "  ------------------------")
        logging.info("FOUND AND REPLACED PBR TAG: " + str(texture_original) + " to " + str(texture))

    except Exception as Argument:
        logging.exception("COULD NOT FIND AND REPLACED PBR TAG: " + str(texture_original) + " to " + str(texture))
		

# Regex, i.e. find and replace messy/misspelled transparency tag with clean PBR tag in a given object's name supplied by the regex_transparent_objects function.
def find_replace_transparency_tag(mesh_object):
    try:
        # Set original mesh_object name.
        mesh_object_original = mesh_object

        # Dictionary with regex keys will be used as the pattern by turning it into a list then to a string.
        pbr_dict = {
            '[Aa]?lph.*|[Oo]?pac.*|[Tt]?ranspa.*|[Tt]?ranspr.*|[Tt]?rns.*|[Tt]?ranp.*|[Gg]?lass': 'transparent',
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

        print("------------------------  FOUND AND REPLACED TRANSPARENCY TAG: " + str(mesh_object_original) + " to " + str(mesh_object) + "  ------------------------")
        logging.info("FOUND AND REPLACED TRANSPARENCY TAG: " + str(mesh_object_original) + " to " + str(mesh_object))

    except Exception as Argument:
        logging.exception("COULD NOT FIND AND REPLACED TRANSPARENCY TAG: " + str(mesh_object_original) + " to " + str(mesh_object))


# Find and rename image textures from a dictionary with regex keys.
def regex_textures_external(textures_temp_dir):
    try:
        for subdir, dirs, files in os.walk(textures_temp_dir):
            for file in files:
                file = os.path.join(subdir, file)
                texture = file
                texture_path = pathlib.Path(texture).parent.resolve()
                components_original = split_into_components(texture)
                components = split_into_components(texture)

                for component in components:
                    pbr_tag_renamed = find_replace_pbr_tag(component)
                    if pbr_tag_renamed != None:
                        pbr_tag_renamed = pbr_tag_renamed[0]
                        print("Found a match for " + pbr_tag_renamed + ".")
                        logging.info("Found a match for " + pbr_tag_renamed + ".")
                        tag_index = components.index(component)
                        components[tag_index] = pbr_tag_renamed
                        if pbr_tag_renamed == "BaseColor" and components[tag_index-1].lower() == "base":
                            components.pop(tag_index-1)  # Was getting "...base_BaseColor..." when original name was "base_color"
                        elif pbr_tag_renamed == "Occlusion" and components[tag_index+1].lower() == "occlusion":
                            components.pop(tag_index+1)  # Was getting "...Ambient_Occlusion_Occlusion..." when original name was "Ambient_Occlusion"
                        break

                if components_original != components:
                    texture = os.path.join(texture_path, texture)
                    texture_renamed = '_'.join(components[:-1])
                    texture_renamed = os.path.join(texture_path, texture_renamed + '.' + components[-1])
                    print("Renamed texture from " + str(os.path.basename(texture)) + " to " + str(os.path.basename(texture_renamed)))
                    logging.info("Renamed texture from " + str(os.path.basename(texture)) + " to " + str(os.path.basename(texture_renamed)))
                    os.rename(texture, texture_renamed)
                        
                else:
                    print("No PBR match found for current texture.")
                    logging.info("No PBR match found for current texture.")

        print("------------------------  REGEXED EXTERNAL TEXTURES  ------------------------")
        logging.info("REGEXED EXTERNAL TEXTURES")

    except Exception as Argument:
        logging.exception("COULD NOT REGEX EXTERNAL TEXTURES")
		

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
                    print("Found a match for " + pbr_tag_renamed + ".")
                    logging.info("Found a match for " + pbr_tag_renamed + ".")
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
                print("Renamed texture from " + str(os.path.basename(texture)) + " to " + str(os.path.basename(texture_renamed)))
                logging.info("Renamed texture from " + str(os.path.basename(texture)) + " to " + str(os.path.basename(texture_renamed)))
                texture.name = texture_renamed
                print("Renamed " + texture_name + " to " + texture_renamed)
                logging.info("Renamed " + texture_name + " to " + texture_renamed)
                        
            else:
                print("No PBR match found for current texture.")
                logging.info("No PBR match found for current texture.")

        print("------------------------  REGEXED PACKED TEXTURES  ------------------------")
        logging.info("REGEXED PACKED TEXTURES")

    except Exception as Argument:
        logging.exception("COULD NOT REGEX PACKED TEXTURES")


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
                    print("Found a match for " + transparency_tag_renamed + ".")
                    logging.info("Found a match for " + transparency_tag_renamed + ".")
                    tag_index = components.index(component)
                    components[tag_index] = transparency_tag_renamed

            if components_original != components:
                object_renamed = '_'.join(components)
                object.name = object_renamed
                print("Renamed " + str(object_name) + " to " + str(object_renamed))
                logging.info("Renamed " + str(object_name) + " to " + str(object_renamed))
                        
            else:
                print("No transparency tag match found for current object.")
                logging.info("No transparency tag match found for current object.")

        print("------------------------  REGEXED TRANSPARENT OBJECTS  ------------------------")
        logging.info("REGEXED TRANSPARENT OBJECTS")

    except Exception as Argument:
        logging.exception("COULD NOT REGEX TRANSPARENT OBJECTS")
		

# Determine if current item has multiple texture sets present in textures_temp_dir. If so, loop through each texture set and create a material from the image textures in that set.
def create_materials(item, textures_temp_dir):
    try:
        image_ext = supported_image_ext()  # Get a list of image extensions that could be used as textures

        # Check if textures are stored in subdirectories.
        # Check if there are subdirectories.
        texture_set_dir_list = next(os.walk(textures_temp_dir))[1]

        # Check if there are images in subdirectories or if these folders are used for other purposes.
        if texture_set_dir_list:
            for texture_set_dir in texture_set_dir_list:
                texture_set_dir = os.path.join(textures_temp_dir, texture_set_dir)
                textures_in_subdirs = [texture for texture in os.listdir(texture_set_dir) if texture.lower().endswith(image_ext)]
            # If there are images stored in subdirectories, assume all texture sets are organized in subdirectories and use these to create materials.
            if textures_in_subdirs:
                for texture_set_dir in texture_set_dir_list:
                    texture_set_dir = os.path.join(textures_temp_dir, texture_set_dir)
                    texture_set = texture_set_dir.split(os.path.sep)[-1] # Get the subdirectory's name, which will be used as the material name.
                    # Add texture set prefix to images based on texture set directory name.
                    for texture in os.listdir(texture_set_dir):
                        texture_path = os.path.join(texture_set_dir, texture)
                        texture_renamed = texture_set + "_" + texture
                        texture_renamed_path = os.path.join(texture_set_dir, texture_renamed)
                        if not texture.startswith(texture_set) and texture_set != "textures_temp":  # If all textures exist directly in textures_temp_dir, don't add that directory name as a prefix.
                            os.rename(texture_path, texture_renamed_path)
                        else:
                            continue
                    textures = [texture for texture in os.listdir(texture_set_dir)]

                    create_a_material(item=texture_set, textures_temp_dir=texture_set_dir, textures=textures)  # Parameters are temporarily reassigned in order that the create_a_material function can be reused.
            
            # If there are no subdirectories containing images, then determine how many texture sets exists in textures_temp directory.
            elif not textures_in_subdirs:
                textures_list = [image for image in os.listdir(textures_temp_dir) if image.lower().endswith(image_ext)]
                basecolor_count = 0
                # Count how many times the regexed "BaseColor" string occurs in the list of images.
                for texture in textures_list:
                    if "BaseColor" in texture:
                        basecolor_count += 1
                # If there is more than one BaseColor image, assume that there are multiple texture sets.
                if basecolor_count > 1:
                    print("Detected " + str(basecolor_count) + " texture sets.")
                    logging.info("Detected " + str(basecolor_count) + " texture sets.")
                    texture_sets = list(set([image.split('_')[0] for image in textures_list]))
                    for texture_set in texture_sets:
                        textures = [texture for texture in textures_list if texture.startswith(texture_set)]
                        create_a_material(item=texture_set, textures_temp_dir=textures_temp_dir, textures=textures)
                # If there are less than or equal to 6 images in textures_temp, assume there is only one texture set.
                elif basecolor_count <= 1:
                    print("Detected " + str(basecolor_count) + " texture set.")
                    logging.info("Detected " + str(basecolor_count) + " texture set.")
                    textures = textures_list

                    create_a_material(item, textures_temp_dir, textures)

        # If there are no subdirectories containing images, then determine how many texture sets exists in textures_temp directory.
        elif not texture_set_dir_list:
            textures_list = [image for image in os.listdir(textures_temp_dir) if image.lower().endswith(image_ext)]
            basecolor_count = 0
            # Count how many times the regexed "BaseColor" string occurs in the list of images.
            for texture in textures_list:
                if "BaseColor" in texture:
                    basecolor_count += 1
            # If there is more than one BaseColor image, assume that there are multiple texture sets.
            if basecolor_count > 1:
                print("Detected " + str(basecolor_count) + " texture sets.")
                logging.info("Detected " + str(basecolor_count) + " texture sets.")
                texture_sets = list(set([image.split('_')[0] for image in textures_list]))
                for texture_set in texture_sets:
                    textures = [texture for texture in textures_list if texture.startswith(texture_set)]
                    create_a_material(item=texture_set, textures_temp_dir=textures_temp_dir, textures=textures)
            # If there are less than or equal to 6 images in textures_temp, assume there is only one texture set.
            elif basecolor_count <= 1:
                print("Detected " + str(basecolor_count) + " texture set.")
                logging.info("Detected " + str(basecolor_count) + " texture set.")
                textures = textures_list

                create_a_material(item, textures_temp_dir, textures)
        
        # If there are no textures, print a message.
        else:
            print("No textures were found.")
            logging.info("No textures were found.")
                
        print("------------------------  CREATED MATERIALS  ------------------------")
        logging.info("CREATED MATERIALS")

    except Exception as Argument:
        logging.exception("COULD NOT CREATE MATERIALS")
		

# Add materials, import textures, and assign materials to objects.
def create_a_material(item, textures_temp_dir, textures):
    try:
        # Assign currently active object to variable.
        object = bpy.context.view_layer.objects.active
        
        # Create a new material. This will be the opaque material.
        material = bpy.data.materials.new(name=item) # Create new material from item name.

        # Select shader before importing textures.
        material.use_nodes = True
        tree = material.node_tree
        nodes = tree.nodes

        # Make sure the Principled BSDF shader is selected.
        material.node_tree.nodes['Material Output'].select = False
        material.node_tree.nodes['Principled BSDF'].select = True
        material.node_tree.nodes.active = material.node_tree.nodes.get("Principled BSDF")
        
        # Import textures with Node Wrangler addon
        textures = textures

        # Log the textures to be used for this material.
        print("Textures for " + str(material.name) + ": " + str(textures))
        logging.info("Textures for " + str(material.name) + ": " + str(textures))

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
            
            filepath = textures_temp_dir + '/'
            directory = textures_temp_dir + '/'
            relative_path = True
            
            win = bpy.context.window
            scr = win.screen
            areas  = [area for area in scr.areas if area.type == 'NODE_EDITOR']
            areas[0].spaces.active.node_tree = material.node_tree
            regions = [region for region in areas[0].regions if region.type == 'WINDOW']

            override = {
                'window': win,
                'screen': scr,
                'area': areas[0],
                'region': regions[0],
            }
            
            bpy.ops.node.nw_add_textures_for_principled(
                override,
                filepath=filepath,
                directory=directory,
                files=files,
                relative_path=relative_path
            ) 
        
        # Check if this material includes an opacity map.
        transparency_check = [node for node in material.node_tree.nodes if node.type == 'BSDF_PRINCIPLED' and node.inputs['Alpha'].is_linked]
        if transparency_check:
            # Copy current material and make opaque version in case there are any opaque objects in scene using the same texture set.
            material_opaque = material.copy()
            material_opaque.blend_method = 'OPAQUE'
            bpy.data.materials[item + ".001"].name = item
            # Remove opacity map from opaque material.
            opacity_map = material_opaque.node_tree.nodes["Principled BSDF"].inputs['Alpha'].links[0].from_node
            material_opaque.node_tree.nodes.remove(opacity_map)
            # Add transparency tag to material name and set alpha blend.
            material.name = item + "_transparent"
            material.blend_method = "BLEND"
            print("Found an opacity map for texture set: " + str(material_opaque.name) + ". Created transparent version of material, " + str(material.name))
            logging.info("Found an opacity map for texture set: " + str(material_opaque.name) + ". Created transparent version of material, " + str(material.name))

        print("------------------------  CREATED A MATERIAL: " + str(item) + "  ------------------------")
        logging.info("CREATED A MATERIAL: " + str(item))

    except Exception as Argument:
        logging.exception("COULD NOT CREATE A MATERIAL: " + str(item))
		

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

        print("------------------------  GOT NODE WRANGLER ALPHA TAGS  ------------------------")
        logging.info("GOT NODE WRANGLER ALPHA TAGS")

    except Exception as Argument:
        logging.exception("COULD NOT GET NODE WRANGLER ALPHA TAGS")
		

# Assign previously created materials to objects based on 1) how many texture sets were present in the textures_dir, 2) the objects' name prefixes (which texture set goes to what objects), and 3) the objects' name suffixes (determines transparency).
def assign_materials(item):
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
                    print("Assigned material, " + str(material_name) + ", to object, " + str(object.name))
                    logging.info("Assigned material, " + str(material_name) + ", to object, " + str(object.name))

        # Only one texture set was imported (one opaque material, one transparent version/copy of that opaque material).
        elif material_count == 2 and transparent_materials:
            for material in bpy.data.materials:
                material_name = str(material.name) # Get the material's name from that material's data block list.
                for object in bpy.context.selected_objects: # Loop only through selected MESH type objects.
                    if object.type == 'MESH' and material_name.replace("_" + transparency_tag, "") == item: # Ignore the "_transparent" suffix of the transparent material.
                        if object_count == 1 and material_name.endswith(transparency_tag):
                            object.data.materials.append(material)
                            print("Assigned transparent material, " + str(material_name) + ", to transparent object, " + str(object.name))
                            logging.info("Assigned transparent material, " + str(material_name) + ", to transparent object, " + str(object.name))
                        elif object_count > 1:
                            if (transparency_tag in object.name or cutout_tag in object.name) and material_name.endswith(transparency_tag):
                                object.data.materials.append(material)
                                if cutout_tag in object.name:
                                    material.blend_method = "CLIP"
                                print("Assigned transparent material, " + str(material_name) + ", to transparent object, " + str(object.name))
                                logging.info("Assigned transparent material, " + str(material_name) + ", to transparent object, " + str(object.name))
                            elif not transparency_tag in object.name and not cutout_tag in object.name and not material_name.endswith(transparency_tag):
                                object.data.materials.append(material)
                                print("Assigned opaque material, " + str(material_name) + ", to opaque object, " + str(object.name))
                                logging.info("Assigned opaque material, " + str(material_name) + ", to opaque object, " + str(object.name))
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
                            print("Assigned transparent material, " + str(material_name) + ", to transparent object, " + str(object.name))
                            logging.info("Assigned transparent material, " + str(material_name) + ", to transparent object, " + str(object.name))
                        elif material_name in object.name and not transparency_tag in object.name and not cutout_tag in object.name and not material_name.endswith(transparency_tag):
                            object.data.materials.append(material)
                            print("Assigned opaque material, " + str(material_name) + ", to opaque object, " + str(object.name))
                            logging.info("Assigned opaque material, " + str(material_name) + ", to opaque object, " + str(object.name))
                        else:
                            continue

        # If there aren't any mesh-type objects in the scene (e.g. an empty FBX), continue on to the next item.
        else:
            print("There are no mesh-type objects in the scene")
            logging.info("There are no mesh-type objects in the scene")

        print("------------------------  ASSIGNED MATERIALS TO OBJECTS  ------------------------")
        logging.info("ASSIGNED MATERIALS TO OBJECTS")

    except Exception as Argument:
        logging.exception("COULD NOT ASSIGN MATERIALS TO OBJECTS")
		

# Resize image textures in textures_temp folder before export.
def resize_textures(texture_resolution, texture_resolution_include):
    try:
        for image in bpy.data.images:
            try:
                width, height = image.size
                if texture_resolution < width and image.name != "Render Result":
                    for pbr_type in texture_resolution_include:
                        if pbr_type in image.name:
                            image.scale(texture_resolution, texture_resolution) # (width, height)
                            image.save() # save images to textures_temp folder so USDZip will use smaller textures when zipping USD. 
                            print(image.name + " resized to " + str(texture_resolution) + ", " + str(texture_resolution) + ".")
                            logging.info(image.name + " resized to " + str(texture_resolution) + ", " + str(texture_resolution) + ".")
                        else:
                            continue
                elif texture_resolution > width and image.name != "Render Result":
                    print("The requested texture resolution of " + str(texture_resolution) + " for " + image.name + " is greater than its original dimensions of " + "(" + str(width) + ", " + str(height) + "). Skipping image to avoid upscaling.")
                    logging.info("The requested texture resolution of " + str(texture_resolution) + " for " + image.name + " is greater than its original dimensions of " + "(" + str(width) + ", " + str(height) + "). Skipping image to avoid upscaling.")
            except:
                pass

        print("------------------------  RESIZED TEXTURES  ------------------------")
        logging.info("RESIZED TEXTURES")

    except Exception as Argument:
        logging.exception("COULD NOT RESIZE TEXTURES")
		

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

        print("------------------------  GOT IMAGE TEXTURE EXTENSION DICTIONARY  ------------------------")
        logging.info("GOT IMAGE TEXTURE EXTENSION DICTIONARY")

    except Exception as Argument:
        logging.exception("COULD NOT GET IMAGE TEXTURE EXTENSION DICTIONARY")
		

# Get image type from extension.
def get_image_ext_key(val):
    try:
        for key, value in ext_dict.items():
            if val == value:
                return key
        return "key doesn't exist"

        print("------------------------  GOT IMAGE EXTENSION KEY  ------------------------")
        logging.info("GOT IMAGE EXTENSION KEY")

    except Exception as Argument:
        logging.exception("COULD NOT GET IMAGE EXTENSION KEY")
		

# Change scene color management. Needed for converting image texture formats
def set_color_management(
    image_format, 
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
        image_settings.file_format = image_format
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

        print("------------------------  SET COLOR MANAGEMENT  ------------------------")
        logging.info("SET COLOR MANAGEMENT")

    except Exception as Argument:
        logging.exception("COULD NOT SET COLOR MANAGEMENT")
		

# Convert images to specified format.
def convert_image_format(image_format, image_quality, image_format_include, textures_source):
    try:
        # Get dictionary.
        ext_dict = image_texture_ext_dict()
        
        # Convert each relevant image.
        for image in bpy.data.images:
            
            # Ignore images other than image textures.
            if image.name == "Render Result" or image.name == "Viewer Node":
                continue
            
            # Include only the images specified by the User.
            for pbr_type in image_format_include:
                if pbr_type in image.name:        
                    image_path = bpy.path.abspath(image.filepath)

                    # Get image name from saved image filepath, not the image in the editor. (This is to account for GLB's not including the image extension in the image name when importing a GLB and exporting again with packed textures.)
                    image.name = pathlib.Path(image_path).name
                    
                    # Change image extension and pathing.
                    image_ext = "." + image.name.split(".")[-1]
                    image_ext_new = ext_dict[image_format]
                    image_path_new = bpy.path.abspath(image.filepath.replace(image_ext, image_ext_new))
                    
                    # Change image name.
                    image_name = image.name
                    image_name_new = image.name.replace(image_ext, image_ext_new)

                    # Set color management to sRGB Standard.
                    set_color_management(
                        image_format=image_format, 
                        image_quality=image_quality,
                        display_device='sRGB', 
                        view_transform='Standard', 
                        look='None', 
                        exposure=0, 
                        gamma=1, 
                        sequencer='sRGB', 
                        use_curves=False, 
                    )

                    # Save image as input specified by the User.
                    image.save_render(filepath = image_path_new)
                    if image_path != image_path_new and os.path.exists(image_path):  # Don't delete image if converting to the same file format.
                        os.remove(image_path)

                    # Repath the image textures to the new format.
                    image.name = image_name_new
                    bpy.data.images[image.name].filepath = bpy.path.abspath(image_path_new)

                    print(image_name + " was converted to a " + image_format + ".")
                    logging.info(image_name + " was converted to a " + image_format + ".")

                else:
                    continue

        print("------------------------  CONVERTED IMAGE FORMAT  ------------------------")
        logging.info("CONVERTED IMAGE FORMAT")

    except Exception as Argument:
        logging.exception("COULD NOT CONVERT IMAGE FORMAT")
		    

# Select all objects again before exporting. The previously actively selected object should still be a MESH type object, although this should no longer matter.
def select_all():
    try:
        bpy.ops.object.select_all(action='SELECT')

        print("------------------------  SELECTED ALL OBJECTS OF ALL TYPES  ------------------------")
        logging.info("SELECTED ALL OBJECTS OF ALL TYPES")

    except Exception as Argument:
        logging.exception("COULD NOT SELECT ALL OBJECTS OF ALL TYPES")
		

# Render a preview image of the scene for archiving.
def render_preview_image(preview_image):
    try:
        # Set color management to sRGB Filmic JPEG.
        set_color_management(
            image_format='JPEG', 
            image_quality=90,
            display_device='sRGB', 
            view_transform='Filmic', 
            look='None', 
            exposure=0, 
            gamma=1, 
            sequencer='sRGB', 
            use_curves=False, 
        )

        # Set render path
        sce = bpy.context.scene.name
        bpy.data.scenes[sce].render.filepath = str(preview_image)

        # Override context to 3D Viewport
        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        space = next(space for space in area.spaces if space.type == 'VIEW_3D')

        # Change 3D Viewport shading settings
        space.shading.type = 'MATERIAL'
        
        # In case the User did not copy neutral.hdr from addon directory to Blender Preferences directory, pass and just use default hdr.
        try:
            space.shading.studio_light = 'neutral.hdr'
        except:
            pass
        space.shading.studiolight_background_alpha = 0
        space.overlay.show_overlays = False

        # Override context to 3D Viewport again, but in a different way to allow view_all and render.opengl to work.
        win = bpy.context.window
        scr = win.screen
        areas  = [area for area in scr.areas if area.type == 'VIEW_3D']
        regions = [region for region in areas[0].regions if region.type == 'WINDOW']

        override = {
            'window': win,
            'screen': scr,
            'area': areas[0],
            'region': regions[0],
        }

        # Frame all objects into viewport so objects are neither too small nor too large in the render. 
        # They tend to be a bit small, but it's better than not at all for the time being.
        bpy.ops.view3d.view_selected(override, use_all_regions=False)

        # Render image through viewport and save the image to location provided above.
        bpy.ops.render.opengl(write_still=True)

        print("------------------------  RENDERED PREVIEW IMAGE THUMBNAIL  ------------------------")
        logging.info("RENDERED PREVIEW IMAGE THUMBNAIL")

    except Exception as Argument:
        logging.exception("COULD NOT RENDER PREVIEW IMAGE THUMBNAIL")
		

# Save a .blend file preserving all materials created even if some are not assigned to any objects.
def save_blend_file(blend):
    try:
        # Reset color management to the default Blender file, sRGB Filmic.
        set_color_management(
            image_format='PNG', 
            image_quality=90,
            display_device='sRGB', 
            view_transform='Filmic', 
            look='None', 
            exposure=0, 
            gamma=1, 
            sequencer='sRGB', 
            use_curves=False, 
        )

        # Purge orphaned data blocks before saving.
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        from bpy.app.handlers import persistent
        from itertools import chain

        for datablock in chain(bpy.data.materials, bpy.data.textures):
            datablock.use_fake_user = True
        bpy.ops.wm.save_as_mainfile(filepath=blend)

        # Delete Blender "save version" backup file (also known as a .blend1 file).
        blend1 = blend + "1"
        if os.path.isfile(blend1):
            os.remove(blend1)

        print("------------------------  SAVED BLEND FILE: " + str(os.path.basename(blend)) + "  ------------------------")
        logging.info("SAVED BLEND FILE: " + str(os.path.basename(blend)))

    except Exception as Argument:
        logging.exception("COULD NOT SAVE BLEND FILE: " + str(os.path.basename(blend)))
		

# Save.blend file and unpack images to textures_temp whenever packed images are used for conversion and are to be resized and/or reformatted.
def unpack_textures(textures_temp_dir, blend):
    try:
        # Create textures_temp_dir
        if not os.path.exists(textures_temp_dir):
            os.makedirs(textures_temp_dir)
        elif os.path.exists(textures_temp_dir):
            shutil.rmtree(textures_temp_dir)
            os.makedirs(textures_temp_dir)

        # Repath blend location to inside textures_temp_dir
        blend = os.path.join(textures_temp_dir, pathlib.Path(blend).name)

        # Save blend inside textures_temp_dir
        save_blend_file(blend)
        
        # Unpack images
        bpy.ops.file.unpack_all(method='WRITE_LOCAL')

        print("------------------------  UNPACKED TEXTURES  ------------------------")
        logging.info("UNPACKED TEXTURES")

    except Exception as Argument:
        logging.exception("COULD NOT UNPACK TEXTURES")
		
# Returns a dictionary of which textures are assigned to which materials.
def map_textures_to_materials():
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
                        texture = os.path.splitext(node.image.name)[0]  # Remove any leftover image texture extensions.
                        if import_file_ext == ".glb":
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

        print("------------------------ MAPPED TEXTURES TO MATERIALS  ------------------------")
        logging.info("MAPPED TEXTURES TO MATERIALS")

    except Exception as Argument:
        logging.exception("COULD NOT MAP TEXTURES TO MATERIALS")


# Add material name as prefix to objects for later texture set matching.
def rename_objects_by_material_prefixes():
    try:
        objects = bpy.context.selected_objects
        for object in objects:
            if object.active_material:
                material_name_prefix = split_into_components(texture = object.active_material.name)[0]
                object_name_prefix = split_into_components(texture = object.name)[0]
                original_object_name = object.name
                if material_name_prefix != object_name_prefix:
                    object.name = material_name_prefix + "_" + object.name
                    print(original_object_name + " now shares the prefix of its currently assigned material, " + object.active_material.name + ". New object name: " + object.name)
                    logging.info(original_object_name + " now shares the prefix of its currently assigned material, " + object.active_material.name + ". New object name: " + object.name)
                else:
                    print(original_object_name + " already shares the same prefix as its currently assigned material, " + object.active_material.name + ". Skipped renaming.")
                    logging.info(original_object_name + " already shares the same prefix as its currently assigned material, " + object.active_material.name + ". Skipped renaming.")

        print("------------------------  RENAMED OBJECTS BY MATERIAL PREFIXES  ------------------------")
        logging.info("RENAMED OBJECTS BY MATERIAL PREFIXES")

    except Exception as Argument:
        logging.exception("COULD NOT RENAME OBJECTS BY MATERIAL PREFIXES")
		

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
                    print("Found a match for " + transparency_tag_renamed + ".")
                    logging.info("Found a match for " + transparency_tag_renamed + ".")
                    tag_index = components.index(component)
                    components[tag_index] = transparency_tag_renamed

            if components_original != components:
                material_renamed = '_'.join(components)
                material.name = material_renamed
                print("Renamed " + str(material_name) + " to " + str(material_renamed))
                logging.info("Renamed " + str(material_name) + " to " + str(material_renamed))
                        
            else:
                print("No transparency tag match found for current material.")
                logging.info("No transparency tag match found for current material.")

        print("------------------------  REGEXED TRANSPARENT MATERIALS  ------------------------")
        logging.info("REGEXED TRANSPARENT MATERIALS")

    except Exception as Argument:
        logging.exception("COULD NOT REGEX TRANSPARENT MATERIALS")


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
                    print("Removed " + opaque_material_name + " material data block.")
                    logging.info("Removed " + opaque_material_name + " material data block.")

        print("------------------------  REMOVED OPAQUE MATERIAL VERSION OF TRANSPARENT MATERIAL  ------------------------")
        logging.info("REMOVED OPAQUE MATERIAL VERSION OF TRANSPARENT MATERIAL")

    except Exception as Argument:
        logging.exception("COULD NOT REMOVE OPAQUE MATERIAL VERSION OF TRANSPARENT MATERIAL")


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
        new_image_path = os.path.join(textures_temp_dir, new_image_name)

        # Get the output path of the current output.
        output_path = os.path.join(textures_temp_dir, output)

        # Rename the output to something closer to the combined image name.
        if os.path.exists(output_path) and not os.path.exists(new_image_path):
            os.rename(output_path, new_image_path)
            print("Output renamed from " + output + " to " + new_image_name)
            logging.info("Output renamed from " + output + " to " + new_image_name)
        else:
            if os.path.exists(output_path):
                os.remove(output_path)
                print(new_image_path + " already exists. Deleted output.")
                logging.info(new_image_path + " already exists. Deleted output.")
        
        print("------------------------  RENAMED OUTPUT  ------------------------")
        logging.info("RENAMED OUTPUT")

    except Exception as Argument:
        logging.exception("COULD NOT RENAME OUTPUT")
		

# Render the output of the compositor, then rename outputs with something similar to the combined image name.
def render_output(textures_temp_dir, image_node, tag_1, tag_2, tag_3, image_texture_ext):
    try:
        # Get a list of either ORM images or BO images.
        combined_images_list = [i for i in bpy.data.images if tag_1.lower() in i.name.lower() and tag_2.lower() in i.name.lower()]
        combined_images_list_names = [i.name for i in combined_images_list]
        print("Combined images detected: " + str(combined_images_list_names))
        logging.info("Combined images detected: " + str(combined_images_list_names))

        if combined_images_list:
            for image in combined_images_list:
                # Get image name without an extension
                image_name = os.path.splitext(image.name)[0]
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
                output_list = [i for i in os.listdir(textures_temp_dir) if tag_1_k in i or tag_2_k in i or tag_3_k in i]
                print("Output list: " + str(output_list))
                logging.info("Output list: " + str(output_list))
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
                image_path = bpy.path.abspath(image.filepath)
                if os.path.exists(image_path):
                    os.remove(image_path)
                else:
                    print("No such combined image exists")
                    logging.info("No such combined image exists")

        print("------------------------  RENDERED OUTPUT  ------------------------")
        logging.info("RENDERED OUTPUT")

    except Exception as Argument:
        logging.exception("COULD NOT RENDER OUTPUT")
		

# Separate any combined image maps if imported model extension is ".glb".
def separate_gltf_maps(textures_temp_dir):
    try:
        # Set color management to sRGB Standard. If view_transform is set to Filmic, then BaseColor images containing transparency will separate as at least a 5MB file. 
        set_color_management(
            image_format='PNG', 
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
        bpy.data.scenes["Scene"].node_tree.nodes["File Output BO"].base_path = textures_temp_dir
        bpy.data.scenes["Scene"].node_tree.nodes["File Output ORM"].base_path = textures_temp_dir
        
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

        print("------------------------  SEPARATED GLTF 'ORM' AND 'BO' IMAGE TEXTURE MAPS  ------------------------")
        logging.info("SEPARATED GLTF 'ORM' AND 'BO' IMAGE TEXTURE MAPS")

    except Exception as Argument:
        logging.exception("COULD NOT SEPARATE GLTF 'ORM' AND 'BO' IMAGE TEXTURE MAPS")


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
        
        print("------------------------  SEPARATED MESHES INTO OBJECTS BY MATERIALS  ------------------------")
        logging.info("SEPARATED MESHES INTO OBJECTS BY MATERIALS")

    except Exception as Argument:
        logging.exception("COULD NOT SEPARATE MESHES INTO OBJECTS BY MATERIALS")


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
                    
                    print(image_name + " now shares its material's prefix of " + str(material.name) + ". New texture name: " + new_image_name)
                    logging.info(image_name + " now shares its material's prefix of " + str(material.name) + ". New texture name: " + new_image_name)
            
            except AttributeError:
                print("Image texture node does not contain an image")
                logging.error("Image texture node does not contain an image")


        materials = [material.name for material in bpy.data.materials]  # Get a list of materials.
        transparent_tag = "_transparent"
        image_texture_ext = image_texture_ext_dict()  # Get image extension dictionary

        # Add material prefix to images before regexing.
        for material in bpy.data.materials:
            if material.node_tree:
                print("material: " + str(material.name))
                logging.info("material: " + str(material.name))

                bsdf = material.node_tree.nodes.get("Principled BSDF")
                texture_list = get_node_inputs(bsdf)
                rename_textures(texture_list, material, materials, transparent_tag, image_texture_ext)

        # Regex image textures before unpacking.
        if regex_textures:
            regex_textures_packed()
        
        print("------------------------  RENAMED PACKED TEXTURES  ------------------------")
        logging.info("RENAMED PACKED TEXTURES")

    except Exception as Argument:
        logging.exception("COULD NOT RENAME PACKED TEXTURES")
		

# For packed textures, reimport textures to respective existing materials after they have been unpacked and separated.
def reimport_textures_to_existing_materials(textures_temp_dir, mapped_textures):
    try:
        # Sever all input connections to the Principled shader to prepare for texture reimport.
        for material in bpy.data.materials:
            if material.name == "Dots Stroke":
                continue
            material_node = material.node_tree.nodes
            for node in material_node:
                if node.name == "Principled BSDF" or node.name == "Material Output":
                    continue
                material_node.remove(node)

            # Select shader before importing textures.
            material.use_nodes = True
            tree = material.node_tree
            nodes = tree.nodes

            # Make sure the Principled BSDF shader is selected.
            material.node_tree.nodes['Material Output'].select = False
            material.node_tree.nodes['Principled BSDF'].select = True
            material.node_tree.nodes.active = material.node_tree.nodes.get("Principled BSDF")
            
            # Import textures with Node Wrangler addon
            image_ext = supported_image_ext()  # Get a list of image extensions that could be used as textures
            textures_available = [image for image in os.listdir(textures_temp_dir) if image.lower().endswith(image_ext)]
            textures = [texture for texture in textures_available if os.path.splitext(texture)[0] in mapped_textures[material.name]]

            print("Textures for " + str(material.name) + ": " + str(textures))
            logging.info("Textures for " + str(material.name) + ": " + str(textures))

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
                
                filepath = textures_temp_dir + '/'
                directory = textures_temp_dir + '/'
                relative_path = True
                
                win = bpy.context.window
                scr = win.screen
                areas  = [area for area in scr.areas if area.type == 'NODE_EDITOR']
                areas[0].spaces.active.node_tree = material.node_tree
                regions = [region for region in areas[0].regions if region.type == 'WINDOW']

                override = {
                    'window': win,
                    'screen': scr,
                    'area': areas[0],
                    'region': regions[0],
                }
                
                bpy.ops.node.nw_add_textures_for_principled(
                    override,
                    filepath=filepath,
                    directory=directory,
                    files=files,
                    relative_path=relative_path
                )
                
            print("Reimported textures to material: " + str(material.name))
            logging.info("Reimported textures to material: " + str(material.name))

        print("------------------------  RE-IMPORTED TEXTURES TO EXISTING MATERIALS  ------------------------")
        logging.info("RE-IMPORTED TEXTURES TO EXISTING MATERIALS")
    
    except Exception as Argument:
        logging.exception("COULD NOT RE-IMPORT TEXTURES TO EXISTING MATERIALS")


# Set object data names as object names. Sometimes, upon export, object data names are used instead of object names, depending on the export format (e.g. USD).
# Code adapted from Simple Renaming Panel (GPL-3.0 License, https://github.com/Weisl/simple_renaming_panel/), renaming_operators.py, Line 609
def data_name_from_object():
    try:
        for obj in bpy.context.selected_objects:
            objName = obj.name
            if hasattr(obj, 'data') and obj.data != None:
                oldName = obj.data.name
                newName = objName
                obj.data.name = newName
                print("Renamed object data from " + str(oldName) + " to " + str(newName))
                logging.info("Renamed object data from " + str(oldName) + " to " + str(newName))

        print("------------------------  SET DATA NAMES FROM OBJECTS  ------------------------")
        logging.info("SET DATA NAMES FROM OBJECTS")
    
    except Exception as Argument:
        logging.exception("COULD NOT SET DATA NAMES FROM OBJECTS")


# Set all UV map names to "UVMap". This prevents a material issue with USDZ's - when object A and object B share the same material, but their UV
# map names differ, the material has to pick one UVMap in the UV Map node inputs connected to each texture channel. So if object A's UV map is called
# "UVMap" but object B's UV map is called "UV_Channel", then the shared material may pick "UV_Channel" as the UV inputs, thus causing object A to appear
# untextured despite the fact that it shares the same material as object B.
def rename_UV_maps():
    try:
        for obj in bpy.context.selected_objects:
            uv_index = 1
            # Loop through every UV map except the first one and rename as "UVMap_1", "UVMap_2", etc.
            for uvmap in obj.data.uv_layers[1:]:
                oldName = uvmap.name
                uvmap.name = "UVMap_" + str(uv_index)
                newName = uvmap.name
                uv_index += 1

                print("Renamed UV map for object " + str(obj.name) + " from " + str(oldName) + " to " + str(newName))
                logging.info("Renamed UV map for object " + str(obj.name) + " from " + str(oldName) + " to " + str(newName))
            
            # Now go back to the first UV map and rename as "UVMap". If this was done first and another UV channel existed with that name, then the first UV channel would be named
            # like "UV_Map.001" which is not desirable and may contain a character compatible with USD format or Maya (i.e. ".").
            oldName = obj.data.uv_layers[0].name
            obj.data.uv_layers[0].name = "UVMap"
            newName = obj.data.uv_layers[0].name

            print("Renamed UV map for object " + str(obj.name) + " from " + str(oldName) + " to " + str(newName))
            logging.info("Renamed UV map for object " + str(obj.name) + " from " + str(oldName) + " to " + str(newName))
                

        print("------------------------  RENAMED UV MAPS  ------------------------")
        logging.info("RENAMED UV MAPS")
    
    except Exception as Argument:
        logging.exception("COULD NOT RENAME UV MAPS")


# Scale objects before exporting. Reset for each model if exporting 2 formats at once.
def set_export_scale(scale):
    try:
        bpy.ops.transform.resize(
            value=(scale, scale, scale), 
            orient_type='GLOBAL', 
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
            orient_matrix_type='GLOBAL', 
            mirror=False, 
            use_proportional_edit=False, 
            proportional_edit_falloff='SMOOTH', 
            proportional_size=1, 
            use_proportional_connected=False, 
            use_proportional_projected=False, 
            snap=False, 
            snap_elements={'INCREMENT'}, 
            use_snap_project=False, 
            snap_target='CLOSEST', 
            use_snap_self=True, 
            use_snap_edit=True, 
            use_snap_nonedit=True, 
            use_snap_selectable=False
            )

        print("------------------------  SET EXPORT SCALE  ------------------------")
        logging.info("SET EXPORT SCALE")

    except Exception as Argument:
        logging.exception("COULD NOT SET EXPORT SCALE")
		

# Set scene units before exporting.
def set_scene_units(unit_system, length_unit):
    try:
        bpy.context.scene.unit_settings.system = unit_system
        bpy.context.scene.unit_settings.length_unit = length_unit
        print("Set scene unit system to " + unit_system + ".")
        logging.info("Set scene unit system to " + unit_system + ".")
        print("Set scene length unit to " + length_unit + ".")
        logging.info("Set scene length unit to " + length_unit + ".")

        print("------------------------  SET SCENE UNITS  ------------------------")
        logging.info("SET SCENE UNITS")

    except Exception as Argument:
        logging.exception("COULD NOT SET SCENE UNITS")
		

# Set custom transformations if requested by the User.
def set_transformations(set_transforms_filter, set_location, set_rotation, set_scale):
    try:
        print("Set the following transformations: " + str(set_transforms_filter))
        logging.info("Set the following transformations: " + str(set_transforms_filter))

        # All objects (including empties) have already been selected.
        for object in bpy.context.selected_objects:
            # Don't transform an object if it has a parent since the parent will control it's childrens' transformations.
            if not object.parent:
                if "Location" in set_transforms_filter:
                    object.location = set_location
                    print("Moved " + object.name + " to " + str(set_location))
                    logging.info("Moved " + object.name + " to " + str(set_location))
                if "Rotation" in set_transforms_filter:
                    object.rotation_mode = 'XYZ'
                    object.rotation_euler = set_rotation
                    print("Rotated " + object.name + " to " + str(set_rotation))
                    logging.info("Rotated " + object.name + " to " + str(set_rotation))
                if "Scale" in set_transforms_filter:
                    object.scale = set_scale
                    print("Scaled " + object.name + " to " + str(set_scale))
                    logging.info("Scaled " + object.name + " to " + str(set_scale))

        print("------------------------  SET TRANSFORMATIONS  ------------------------")
        logging.info("SET TRANSFORMATIONS")

    except Exception as Argument:
        logging.exception("COULD NOT SET TRANSFORMATIONS")
		

# Export a model.
def export_a_model(export_file_scale, export_file_command, export_file_options, export_file):
    try:
        # Set scale
        set_export_scale(export_file_scale)
        print("Scaled models by " + str(export_file_scale))
        logging.info("Scaled models by " + str(export_file_scale))
        # Apply transforms if requested
        if apply_transforms:
            apply_transformations(apply_transforms_filter)
        
        # Export the model.
        export_file_options["filepath"] = export_file  # Set filepath to the location of the model to be imported
        export_file_command = str(export_file_command) + str(export_file_options) + ")"  # Concatenate the import command with the import options dictionary
        print(export_file_command)
        logging.info(export_file_command)
        exec(export_file_command)  # Run export_file_command, which is stored as a string and won't run otherwise.

        # Reset scale
        export_file_scale = 1 / export_file_scale
        # Apply transforms if requested
        if apply_transforms:
            apply_transformations(apply_transforms_filter)
        set_export_scale(export_file_scale)
        print("Reset scale of models by " + str(export_file_scale))
        logging.info("Reset scale of models by " + str(export_file_scale))
        # Apply transforms if requested
        if apply_transforms:
            apply_transformations(apply_transforms_filter)
        print("------------------------  EXPORTED A MODEL: " + str(os.path.basename(export_file)) + "  ------------------------")
        logging.info("EXPORTED A MODEL: " + str(os.path.basename(export_file)))

    except Exception as Argument:
        logging.exception("COULD NOT EXPORT A MODEL")


# Determine how many, if any, models to export.
def export_models(export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2):
    try:
        if model_quantity == "2 Formats":
            # Export file 1
            export_a_model(export_file_1_scale, export_file_1_command, export_file_1_options, export_file_1)
            # Export file 2
            export_a_model(export_file_2_scale, export_file_2_command, export_file_2_options, export_file_2)
            
        elif model_quantity == "1 Format":
            # Export file 1
            export_a_model(export_file_1_scale, export_file_1_command, export_file_1_options, export_file_1)
            
        elif model_quantity == "No Formats":
            print("No models will be exported")
            logging.info("No models will be exported")

        print("------------------------  EXPORTED MODELS  ------------------------")
        logging.info("EXPORTED MODELS")

    except Exception as Argument:
        logging.exception("COULD NOT EXPORT MODELS")
		

# Deletes the temporary textures folder.
def delete_textures_temp(textures_temp_dir):
    try:
        if os.path.exists(textures_temp_dir):
            shutil.rmtree(textures_temp_dir)

        print("------------------------  DELETED TEMPORARY TEXTURES DIRECTORY  ------------------------")
        logging.info("DELETED TEMPORARY TEXTURES DIRECTORY")

    except Exception as Argument:
        logging.exception("COULD NOT DELETE TEMPORARY TEXTURES DIRECTORY")
		

# Reset interface theme dark after rendering all Preview images.
def set_theme_dark(blender_dir, blender_version):
    try:
        # Reset interface theme to dark theme.
        theme_dark = os.path.join(pathlib.Path(blender_dir).parent.resolve(), blender_version, "scripts", "presets", "interface_theme", "Blender_Dark.xml")
        
        # Default dark theme.
        bpy.ops.script.execute_preset(
            filepath=theme_dark, 
            menu_idname="USERPREF_MT_interface_theme_presets"
        )

        print("------------------------  SET BLENDER THEME DARK  ------------------------")
        logging.info("SET BLENDER THEME DARK")

    except Exception as Argument:
        logging.exception("COULD NOT SET BLENDER THEME DARK")
		

# Get file size of export_file_1
def get_export_file_1_size(export_file_1):
    try:
        if os.path.exists(export_file_1):
            # Get current file size (in MB)
            export_file_1_file_size = pathlib.Path(export_file_1).stat().st_size / 1048576
        
        else:
            print(export_file_1 + " doesn't exist.")
            logging.info(export_file_1 + " doesn't exist.")
            export_file_1_file_size = 0
        
        return export_file_1_file_size

        print("------------------------  GOT EXPORTED FILE SIZE  ------------------------")
        logging.info("GOT EXPORTED FILE SIZE")

    except Exception as Argument:
        logging.exception("COULD NOT GET EXPORTED FILE SIZE")
		

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
        print("------------------------  DECIMATED OBJECTS  ------------------------")
        logging.info("DECIMATED OBJECTS")

    except Exception as Argument:
        logging.exception("COULD NOT DECIMATE OBJECTS")


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

        print("------------------------  GOT TEXTURE RESOLUTION MAXIMUM FOR AUTO RESIZE FILES  ------------------------")
        logging.info("GOT TEXTURE RESOLUTION MAXIMUM FOR AUTO RESIZE FILES")

    except Exception as Argument:
        logging.exception("COULD NOT GET TEXTURE RESOLUTION MAXIMUM FOR AUTO RESIZE FILES")


# Auto resize method: Draco-Compress
def draco_compress_and_export(export_file_1, export_file_2):
    try:
        if "Draco-Compress" in file_size_methods and export_file_1_ext == ".glb":
            print("#################  Draco-Compress  #################")
            logging.info("#################  Draco-Compress  #################")
            export_file_1_options["export_draco_mesh_compression_enable"] = True
            
            # Determine how many 3D files to export, then export.
            export_models(export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2)

    except Exception as Argument:
        logging.exception("COULD NOT DRACO-COMPRESS MODEL FOR AUTO RESIZE FILES")


# Auto resize method: Resize textures
def resize_textures_and_export(export_file_1, export_file_2, texture_resolution_current):
    try:
        if "Resize Textures" in file_size_methods:
            if texture_resolution_current / 2 >= resize_textures_limit:
                print("#################  Resize Textures  #################")
                logging.info("#################  Resize Textures  #################")
                texture_resolution_current = int(texture_resolution_current / 2)
                # Resize textures (again) and re-export.
                resize_textures(texture_resolution = texture_resolution_current, texture_resolution_include = texture_resolution_include)

                # Determine how many 3D files to export, then export.
                export_models(export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2)
            
            elif texture_resolution_current / 2 < resize_textures_limit:
                print("#################  Resize Textures  #################")
                logging.info("#################  Resize Textures  #################")
                print("Current texture resolution is at or below resizing limit. Skipping texture resizing.")
                logging.info("Current texture resolution is at or below resizing limit. Skipping texture resizing.")

        # Return current resolution.
        return texture_resolution_current

    except Exception as Argument:
        logging.exception("COULD NOT RESIZE TEXTURES FOR AUTO RESIZE FILES")


# Auto resize method: Reformat textures
def reformat_textures_and_export(export_file_1, export_file_2):
    try:
        if "Reformat Textures" in file_size_methods:
            print("#################  Reformat Textures  #################")
            logging.info("#################  Reformat Textures  #################")
            image_format = 'JPEG'
            image_quality = 90
            image_format_include = ["Occlusion", "Roughness", "BaseColor", "Metallic", "Emission", "Opacity", "Bump", "Displacement", "Specular", "Subsurface"]
            convert_image_format(image_format, image_quality, image_format_include, textures_source)
            
            # Determine how many 3D files to export, then export.
            export_models(export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2)

    except Exception as Argument:
        logging.exception("COULD NOT REFORMAT TEXTURES FOR AUTO RESIZE FILES")


# Auto resize method: Decimate meshes
def decimate_meshes_and_export(export_file_1, export_file_2, decimate_counter, decimate_maximum):
    try:
        if "Decimate Meshes" in file_size_methods:
            if decimate_counter <= decimate_maximum:
                print("#################  Decimate Meshes  #################")
                logging.info("#################  Decimate Meshes  #################")
                select_only_meshes()
                decimate_objects()
                select_all()

                # Determine how many 3D files to export, then export.
                export_models(export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2)
                decimate_counter += 1

            elif decimate_counter > decimate_maximum:
                print("#################  Decimate Meshes  #################")
                logging.info("#################  Decimate Meshes  #################")
                print("Decimation iteration maximum reached. Skipping Decimation.")
                logging.info("Decimation iteration maximum reached. Skipping Decimation.")
        
        return decimate_counter

    except Exception as Argument:
        logging.exception("COULD NOT DECIMATE MESHES FOR AUTO RESIZE FILES")


# Automatically try to resize the exported file (only takes export_file_1 into account)
def auto_resize_exported_files(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2):
    try:
        # Get current file size (in MB)
        export_file_1_file_size = get_export_file_1_size(export_file_1)
        texture_resolution_start = get_texture_resolution_maximum()  # Always start with largest existing resolution. That way resizing textures will always occur before reformatting.
        texture_resolution_current = texture_resolution_start
        decimate_counter = 0
        decimate_maximum = decimate_limit

        while export_file_1_file_size > file_size_maximum:
            print("#############################  NEW AUTO FILE RESIZE ITERATION  #############################")
            logging.info("#############################  NEW AUTO FILE RESIZE ITERATION  #############################")
            
            # 1. Draco
            draco_compress_and_export(export_file_1, export_file_2)
            # check
            export_file_1_file_size = get_export_file_1_size(export_file_1)
            if export_file_1_file_size < file_size_maximum:
                break

            # 2. Resize
            texture_resolution_current = resize_textures_and_export(export_file_1, export_file_2, texture_resolution_current)
            # check
            export_file_1_file_size = get_export_file_1_size(export_file_1)
            if export_file_1_file_size < file_size_maximum:
                break
           
            # 3. Reformat
            reformat_textures_and_export(export_file_1, export_file_2)
            # check
            export_file_1_file_size = get_export_file_1_size(export_file_1)
            if export_file_1_file_size < file_size_maximum:
                break

            # (4.) Decimate
            decimate_counter = decimate_meshes_and_export(export_file_1, export_file_2, decimate_counter, decimate_maximum)
            # check
            export_file_1_file_size = get_export_file_1_size(export_file_1)
            if export_file_1_file_size < file_size_maximum:
                break
            
            # repeat unless all methods are exhausted
            if "Resize Textures" not in file_size_methods and "Decimate Meshes" not in file_size_methods:
                break
            elif "Resize Textures" in file_size_methods and "Decimate Meshes" in file_size_methods:
                if texture_resolution_current <= resize_textures_limit and decimate_counter >= decimate_maximum:
                    break
            if "Resize Textures" in file_size_methods and "Decimate Meshes" not in file_size_methods:
                if texture_resolution_current <= resize_textures_limit:
                    break
            elif "Resize Textures" not in file_size_methods and "Decimate Meshes" in file_size_methods:
                if decimate_counter >= decimate_maximum:
                    break

        # Report on how the auto-resizing turned out.
        if export_file_1_file_size < file_size_maximum:
            print("Exported model is now below the specified maximum.")
            logging.info("Exported model is now below the specified maximum.")
        elif export_file_1_file_size > file_size_maximum:
            print("Exported model is still above the specified maximum, but ran out of methods. Exiting.")
            logging.info("Exported model is still above the specified maximum, but ran out of methods. Exiting.")
        
        print("------------------------  AUTO-RESIZED EXPORTED FILES  ------------------------")
        logging.info("AUTO-RESIZED EXPORTED FILES")

    except Exception as Argument:
        logging.exception("COULD NOT AUTO-RESIZE EXPORTED FILES")


# Determine where textures should be sourced, then texture the model.
def apply_textures(item_dir, item, import_file, textures_dir, textures_temp_dir, blend, conversion_count):
    try:
        # Regex transparent objects before creating materials and searching for matches between transparent material(s) and transparent object(s).
        if regex_textures and textures_source != "Packed":
            regex_transparent_objects()
        
        # Determine from where to import textures.
        if textures_source == "External":
            print("Using external textures for conversion")
            logging.info("Using external textures for conversion")
            
            # Clear all users of all materials.
            clear_materials_users()
            
            # Brute force-remove all materials and images.
            clean_data_block(bpy.data.materials)
            clean_data_block(bpy.data.images)

            create_textures_temp(item_dir, textures_dir, textures_temp_dir)
            if regex_textures:
                regex_textures_external(textures_temp_dir)
            create_materials(item, textures_temp_dir)
            assign_materials(item)

        elif textures_source == "Packed":
            print("Using imported textures for conversion")
            logging.info("Using imported textures for conversion")
            
            # Find and rename transparent materials that have mispellings of transparency with regex keys. 
            regex_transparent_materials()

            # Purge orphaned opaque image textures if they are duplicates, rather than shared/instanced data blocks.
            purge_orphans()

            # Make sure image textures have their material's prefix before unpacking to avoid any duplicate texture names if they were all lower-cased.
            rename_textures_packed(textures_temp_dir)

            # Delete any existing textures_temp_dir before unpacking.
            delete_textures_temp(textures_temp_dir)

            # Unpack textures before modifying them.
            unpack_textures(textures_temp_dir, blend)

            # Only separate image textures if imported file is a GLB.
            if import_file_ext == ".glb":
                # Get a dictionary of which textures are assigned to which materials.
                mapped_textures = map_textures_to_materials()
                
                # Set textures_temp_dir to location of unpacked images.
                textures_temp_dir = os.path.join(textures_temp_dir, "textures")

                # Separate the combined maps.
                separate_gltf_maps(textures_temp_dir)

                # Remove existing images from Converter.blend file.
                clean_data_block(bpy.data.images)

                # Reimport unpacked & separated textures to their original materials.
                reimport_textures_to_existing_materials(textures_temp_dir, mapped_textures)

        elif textures_source == "Custom":
            print("Using custom textures for conversion")
            logging.info("Using custom textures for conversion")
            
            # Clear all users of all materials.
            clear_materials_users()

            # Copy original custom textures to item directory.
            copy_textures_from_custom_source(textures_custom_dir, item_dir, textures_dir, replace_textures)
            
            # Reassign textures_temp to be beside custom textures source.
            textures_temp_dir = textures_custom_dir + "_temp"
            
            # Reassign item as "Custom_Textures"
            item = "Custom_Textures"

            if conversion_count == 0:
                create_textures_temp(textures_custom_dir, textures_custom_dir, textures_temp_dir)
                
                # Remove existing materials and textures from Converter.blend file only once.
                clean_data_block(bpy.data.materials)
                clean_data_block(bpy.data.images)
                
                # Only regex textures and create materials once.
                if regex_textures:
                    regex_textures_external(textures_temp_dir)
                create_materials(item, textures_temp_dir)
                
                # Modify textures if requested.
                if texture_resolution != "Default":
                    resize_textures(texture_resolution, texture_resolution_include)
                if image_format != "Default":
                    convert_image_format(image_format, image_quality, image_format_include, textures_source)
                    
                # Get custom materials and textures not to be deleted during conversion.
                global custom_materials
                global custom_textures
                custom_materials = [material.name for material in bpy.data.materials]
                custom_textures = [texture.name for texture in bpy.data.images]
            
            elif conversion_count > 0:
                clean_data_block_except_custom(bpy.data.materials, custom_materials)
                clean_data_block_except_custom(bpy.data.images, custom_textures)

            assign_materials(item)

        print("------------------------  APPLIED TEXTURES TO OBJECTS  ------------------------")
        logging.info("APPLIED TEXTURES TO OBJECTS")

    except Exception as Argument:
        logging.exception("COULD NOT APPLY TEXTURES TO OBJECTS")
		

# Decide whether to export files (again) or not based on auto_resize_files menu.
def determine_exports(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2):
    try:
        # Force global variables to reset to original settings, specifically export_file_1(or 2)_options["export_draco_mesh_compression_enable"], otherwise all GLB's after the first one above target maximum will be draco compressed because that variable is global and was altered in the auto file resize method if Draco compression was included in the filter.
        # Assign variables from dictionary.
        variables_dict = read_json()
        export_file_1_options = variables_dict["export_file_1_options"]
        export_file_2_options = variables_dict["export_file_2_options"]

        if auto_resize_files == "All":
            # Determine how many 3D files to export, then export.
            export_models(export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2)
            
            # Get current file size (in MB)
            export_file_1_file_size = get_export_file_1_size(export_file_1)
            
            # If exported file is already above maximum, skip ahead.
            if export_file_1_file_size < file_size_maximum:
                print("File is below target maximum. Skipping automatic file resizing for " + str(item) + ".")
                logging.info("File is below target maximum. Skipping automatic file resizing for " + str(item) + ".")
                return
            
            # If User elected to automatically resize the file, get the current file size and keep exporting until it's lower than the specified maximum or methods have been exhausted.
            elif export_file_1_file_size > file_size_maximum:
                auto_resize_exported_files(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2)

        elif auto_resize_files == "Only Above Max":
            # Get current file size (in MB)
            export_file_1_file_size = get_export_file_1_size(export_file_1)

            # If exported file is already above maximum, skip ahead.
            if export_file_1_file_size > 0 and export_file_1_file_size < file_size_maximum:
                print("File already exists and is below target maximum. Skipping automatic file resizing for " + str(item) + ".")
                logging.info("File already exists and is below target maximum. Skipping automatic file resizing for " + str(item) + ".")
                return
            
            elif export_file_1_file_size > file_size_maximum:
                print("File already exists and is above target maximum. Initiating automatic file resizing for " + str(item) + ".")
                logging.info("File already exists is above target maximum. Initiating automatic file resizing for " + str(item) + ".")
                # Determine how many 3D files to export, then export.
                export_models(export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2)
                # If User elected to automatically resize the file, get the current file size and keep exporting until it's lower than the specified maximum or methods have been exhausted.
                auto_resize_exported_files(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2)

            elif export_file_1_file_size == 0:
                print("File doesn't exist. Exporting item and initiating automatic file resizing for " + str(item) + ".")
                logging.info("File doesn't exist. Exporting item and initiating automatic file resizing for " + str(item) + ".")
                # Determine how many 3D files to export, then export.
                export_models(export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2)
                # If User elected to automatically resize the file, get the current file size and keep exporting until it's lower than the specified maximum or methods have been exhausted.
                auto_resize_exported_files(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2)

        elif auto_resize_files == "None":
            # Determine how many 3D files to export, then export.
            export_models(export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2)

        print("------------------------  DETERMINED WHETHER/WHAT TO EXPORT  ------------------------")
        logging.info("DETERMINED WHETHER/WHAT TO EXPORT")

    except Exception as Argument:
        logging.exception("COULD NOT DETERMINE WHETHER/WHAT TO EXPORT")


# Convert the file for every file found inside the given directory.
def converter(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image, conversion_count):
    try:
        print("-------------------------------------------------------------------")
        print("------------------------  CONVERTER START: " + str(os.path.basename(import_file)) + "  ------------------------")
        print("-------------------------------------------------------------------")
        logging.info("-------------------------------------------------------------------")
        logging.info("------------------------  CONVERTER START: " + str(os.path.basename(import_file)) + "  ------------------------")
        logging.info("-------------------------------------------------------------------")
        
        # Set up scene.
        scene_setup()

        # Brute force-remove all materials and images.
        if textures_source != "Custom":
            clean_data_block(bpy.data.materials)
            clean_data_block(bpy.data.images)

        # Import the file.
        import_file_function(import_file_command, import_file_options, import_file)

        # Delete animations.
        if delete_animations:
            clear_animation_data()
        
        # Apply transformations.
        if apply_transforms:
            apply_transformations(apply_transforms_filter)

        # Select only mesh-type objects.
        select_only_meshes()

        # Determine whether to use textures and from where they should come.
        if use_textures:
            apply_textures(item_dir, item, import_file, textures_dir, textures_temp_dir, blend, conversion_count)
        elif not use_textures:
            # Clear all users of all materials.
            clear_materials_users()
            
            # Brute force-remove all materials and images.
            clean_data_block(bpy.data.materials)
            clean_data_block(bpy.data.images)
            
        # Set scene units.
        set_scene_units(unit_system, length_unit)

        # Set data name from object name if requested by User.
        if set_data_names:
            data_name_from_object()

        # Rename UV maps if requested by User.
        if set_UV_map_names:
            rename_UV_maps()
        
        # Save .blend file.
        if save_blend:
            save_blend_file(blend)

        # Select all objects in the scene before exporting, including empty objects.
        select_all()

        # Set transforms if requested by the User.
        if set_transforms:
            set_transformations(set_transforms_filter, set_location, set_rotation, set_scale)

        # Save preview image.
        if save_preview_image:
            render_preview_image(preview_image)
        
        # Decide whether to export files or not based on auto_resize_files menu.
        determine_exports(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1_command, export_file_1_options, export_file_1_scale, export_file_1, export_file_2_command, export_file_2_options, export_file_2_scale, export_file_2)

        # If User elected not to save a .blend file, delete any existing .blend.
        if not save_blend:
            if os.path.isfile(blend):
                os.remove(blend)

        # Modified or copied textures can now be delete after the conversion is over.
        if use_textures:
            if not keep_modified_textures:
                if os.path.exists(textures_temp_dir):
                    delete_textures_temp(textures_temp_dir)
            if textures_source == "Custom":
                if not copy_textures_custom_dir:
                    remove_copy_textures_custom_dir(item_dir, textures_dir)

        print("-------------------------------------------------------------------")
        print("----------------  CONVERTER END: " + str(os.path.basename(import_file)) + "  ----------------")
        print("-------------------------------------------------------------------")
        logging.info("-------------------------------------------------------------------")
        logging.info("----------------  CONVERTER END: " + str(os.path.basename(import_file)) + "  ----------------")
        logging.info("-------------------------------------------------------------------")

    except Exception as Argument:
        logging.exception("COULD NOT CONVERT FILE: " + str(os.path.basename(import_file)))
		

# Write conversion report to a JSON file.
def report_conversion_count(conversion_count):
    try:
        # Data to be written
        conversion_report_dict = {
            "conversion_count": conversion_count,
        }
        
        json_file = os.path.join(pathlib.Path(__file__).parent.resolve(), "Converter_Report.json")

        with open(json_file, "w") as outfile:
            json.dump(conversion_report_dict, outfile)

        print("------------------------  REPORTED CONVERSION COUNT  ------------------------")
        logging.info("REPORTED CONVERSION COUNT")

    except Exception as Argument:
        logging.exception("COULD NOT REPORT CONVERSION COUNT")
		

# Make a list of exports for the current item, which will then be appended to the full conversion_list to be reported in the log.
def list_exports(export_file_1, export_file_2):
    try:
        exports_list = []
        if model_quantity != "No Formats":
            export_file_1_file_size = round(get_export_file_1_size(export_file_1), 2)
            export_file_1 = os.path.basename(export_file_1)
            export_file_1_list = [export_file_1, export_file_1_file_size]
            exports_list.append(export_file_1_list)

            if model_quantity == "2 Formats":
                export_file_2_file_size = round(get_export_file_1_size(export_file_1 = export_file_2), 2)
                export_file_2 = os.path.basename(export_file_2)
                export_file_2_list = [export_file_2, export_file_2_file_size]
                exports_list.append(export_file_2_list)
        
        return exports_list
        
        print("------------------------  LISTED EXPORTS  ------------------------")
        logging.info("LISTED EXPORTS")

    except Exception as Argument:
        logging.exception("COULD NOT LIST EXPORTS")


# Move file from source to destination
def move_file(directory, file_source):
    try:
        # Set destination based on custom output directory
        file_destination = os.path.join(directory, os.path.basename(file_source))
        # Check if "file" is a directory.
        if os.path.isdir(file_source):
            if os.path.exists(file_destination):
                shutil.rmtree(file_destination)
            shutil.move(file_source, file_destination)

        # Check if "file" is a file
        if not os.path.isdir(file_source):
            if os.path.isfile(file_destination):
            # Remove any existing destination file
                os.remove(file_destination)
            # Move file, if source exists
            if os.path.isfile(file_source):
                shutil.move(file_source, file_destination)
                
        print("Moved " + str(os.path.basename(file_source)) + " to " + str(directory))
        logging.info("Moved " + str(os.path.basename(file_source)) + " to " + str(directory))

    except Exception as Argument:
        logging.exception("COULD NOT MOVE FILE")


# Move and or copy files from item directory to custom directory specified by the User.
def move_copy_to_custom_dir(item, item_dir, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image):
    try:
        # Make the custom directory if it doesn't exist
        if not os.path.exists(directory_output_custom):
            os.makedirs(directory_output_custom)
        
        # File list of items to move
        file_list = [export_file_1]
        if model_quantity == "2 Formats":
            file_list.append(export_file_2)
        if keep_modified_textures:
            file_list.append(textures_temp_dir)
        if save_blend:
            file_list.append(blend)
        if save_preview_image:
            file_list.append(preview_image)
        
        # Scenario 1: No subdirectories
        if not use_subdirectories:
            # Delete any pre-existing textures_temp folders in the custom directory.
            textures_temp_custom = os.path.join(directory_output_custom, os.path.basename(textures_temp_dir))
            if os.path.exists(textures_temp_custom):
                shutil.rmtree(textures_temp_custom)
                
            # Move files
            for file in file_list:
                move_file(directory = directory_output_custom, file_source = file)
        
        if use_subdirectories:
            # Scenario 2: Subdirectories, no copy original item directory
            item_dir_custom = os.path.join(directory_output_custom, prefix + item + suffix)
            
            # Always start fresh by removing existing custom item directories.
            if os.path.exists(item_dir_custom):
                shutil.rmtree(item_dir_custom)
            os.makedirs(item_dir_custom)
            
            # Move files
            for file in file_list:
                move_file(directory = item_dir_custom, file_source = file)
            
            # Scenario 3: Subdirectories, copy original item directory
            if use_subdirectories and copy_item_dir_contents:
                # Copy leftover/original subfolders and files
                for file in os.listdir(item_dir):
                    # Copy subfolders
                    if os.path.isdir(os.path.join(item_dir, file)):
                        file_custom = os.path.join(item_dir_custom, file)
                        file = os.path.join(item_dir, file)
                        if os.path.exists(file_custom):
                            shutil.rmtree(file_custom)
                        shutil.copytree(file, file_custom)
                        print("Copied " + str(file) + " to " + str(item_dir_custom))
                        logging.info("Copied " + str(file) + " to " + str(item_dir_custom))
                    # Copy files
                    else:
                        file_custom = os.path.join(item_dir_custom, file)
                        file = os.path.join(item_dir, file)
                        shutil.copy(file, file_custom)
                        print("Copied " + str(os.path.basename(file)) + " to " + str(item_dir_custom))
                        logging.info("Copied " + str(os.path.basename(file)) + " to " + str(item_dir_custom))
        
        print("------------------------  MOVED/COPIED ITEMS TO CUSTOM OUTPUT DIRECTORY  ------------------------")
        logging.info("MOVED/COPIED ITEMS TO CUSTOM OUTPUT DIRECTORY")

    except Exception as Argument:
        logging.exception("COULD NOT MOVE/COPY ITEMS TO CUSTOM OUTPUT DIRECTORY")
        

# Determine whether to import a model before converting in order to save time.
def determine_imports(item, item_dir, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image, conversion_count, conversion_list):
    try:
        # Don't waste time converting files that already exist and are below the target maximum if auto file resizing.
        if auto_resize_files == "Only Above Max":
            # Get current file size (in MB) in order to determine whether to import the current item at all.
            # Get current file size (in MB) of export_file_1 in the custom location
            if directory_output_location == "Custom":
                if use_subdirectories:
                    item_dir_custom = os.path.join(directory_output_custom, prefix + item + suffix)
                    export_file_1_custom = os.path.join(item_dir_custom, os.path.basename(export_file_1))
                    export_file_1_file_size = get_export_file_1_size(export_file_1_custom)
                else:    
                    export_file_1_custom = os.path.join(directory_output_custom, os.path.basename(export_file_1))
                    export_file_1_file_size = get_export_file_1_size(export_file_1_custom)
            # Get current file size (in MB) of export_file_1 in adjacent locations
            else: 
                export_file_1_file_size = get_export_file_1_size(export_file_1)

            # If export_file_1 exists and is above maximum when auto_resize_files is set to "Only Above Max", convert item.
            if export_file_1_file_size > file_size_maximum:
                print("File either already exists and is above target maximum. Initiating conversion and automatic file resizing for " + str(item) + ".")
                logging.info("File either already exists and is above target maximum. Initiating conversion and automatic file resizing for " + str(item) + ".")
                # Run the converter on the item that was found.
                converter(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image, conversion_count)
                # Increment conversion counter and add converted item(s) to list.
                exports_list = list_exports(export_file_1, export_file_2)
                # Add export(s) to conversion list.
                conversion_list.extend(exports_list)
                conversion_count += 1
                # Now determine whether to copy/move contents to a custom directory after the conversion has taken place.
                if directory_output_location == "Custom":
                    move_copy_to_custom_dir(item, item_dir, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image)
                return conversion_list, conversion_count
            
            # If export_file_1 already exists and is already below maximum when auto_resize_files is set to "Only Above Max", skip item.
            elif export_file_1_file_size > 0 and export_file_1_file_size < file_size_maximum:
                print("File already exists and is below target maximum. Skipping conversion for " + str(item) + ".")
                logging.info("File already exists and is below target maximum. Skipping conversion for " + str(item) + ".")
                return conversion_list, conversion_count

            # If file size is zero, then the file cannot exist and requires export.
            elif export_file_1_file_size == 0:
                print("File doesn't exist. Initiating conversion and automatic file resizing for " + str(item) + ".")
                logging.info("File doesn't exist. Initiating conversion and automatic file resizing for " + str(item) + ".")
                # Run the converter on the item that was found.
                converter(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image, conversion_count)
                # Increment conversion counter and add converted item(s) to list.
                exports_list = list_exports(export_file_1, export_file_2)
                # Add export(s) to conversion list.
                conversion_list.extend(exports_list)
                conversion_count += 1
                # Now determine whether to copy/move contents to a custom directory after the conversion has taken place.
                if directory_output_location == "Custom":
                    move_copy_to_custom_dir(item, item_dir, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image)
                return conversion_list, conversion_count

        # Always convert files if auto file resizing "All" or not auto file resizing at all ("None").
        elif auto_resize_files != "Only Above Max":
            print("Initiating converter for " + str(item) + ".")
            logging.info("Initiating converter for " + str(item) + ".")
            # Run the converter on the item that was found.
            converter(item_dir, item, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image, conversion_count)
            # Increment conversion counter and add converted item(s) to list.
            exports_list = list_exports(export_file_1, export_file_2)
            # Add export(s) to conversion list.
            conversion_list.extend(exports_list)
            conversion_count += 1
            # Now determine whether to copy/move contents to a custom directory after the conversion has taken place.
            if directory_output_location == "Custom":
                move_copy_to_custom_dir(item, item_dir, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image)
            return conversion_list, conversion_count

        print("------------------------  DETERMINED CONVERSION FOR " + str(item) + "  ------------------------")
        logging.info("DETERMINED CONVERSION FOR " + str(item))

    except Exception as Argument:
        logging.exception("COULD NOT DETERMINE CONVERSION FOR " + str(item))


# Main function that loops through specified directory and creates variables for the converter
def batch_converter():
    try:
        print("-------------------------------------------------------------------")
        print("---------------------  BATCH CONVERTER START  ---------------------")
        print("-------------------------------------------------------------------")
        logging.info("-------------------------------------------------------------------")
        logging.info("---------------------  BATCH CONVERTER START  ---------------------")
        logging.info("-------------------------------------------------------------------")

        # Set up a conversion count and list to report how many conversions took place and the final file sizes of each item.
        conversion_count = 0
        conversion_list = []

        # Create path to blender.exe and get version
        blender_dir = bpy.app.binary_path
        blender_version = bpy.app.version_string[:3]

        # Enable addons
        enable_addons()

        # Temporarily change interface theme to force a white background in Material Preview viewport mode for rendering Preview images.
        #set_theme_light(blender_dir, blender_version)

        # Run converter in every subdirectory that contains a model of the specified file type.
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                item = os.path.splitext(file)[0]
                file = os.path.join(subdir, file.lower())
                item_dir = subdir
                if file.endswith(import_file_ext):
                    import_file = os.path.join(subdir, item + import_file_ext)
                    textures_dir = os.path.join(subdir, 'textures')
                    textures_temp_dir = os.path.join(subdir, 'textures_' + prefix + item + suffix)
                    export_file_1 = os.path.join(subdir, prefix + item + suffix + export_file_1_ext)
                    export_file_2 = os.path.join(subdir, prefix + item + suffix + export_file_2_ext)
                    blend = os.path.join(subdir, prefix + item + suffix + ".blend")
                    preview_image = os.path.join(subdir, prefix + item + suffix + '_Preview.jpg')

                    # Determine which models to import, then convert the ones that are eligible for import.
                    conversion_list, conversion_count = determine_imports(item, item_dir, import_file, textures_dir, textures_temp_dir, export_file_1, export_file_2, blend, preview_image, conversion_count, conversion_list)

                else:
                    continue
        
        # Reset interface theme dark after rendering all Preview images.
        #set_theme_dark(blender_dir, blender_version)

        # Report conversion count to Converter_Report.json
        report_conversion_count(conversion_count)

        # Report final conversion count.
        print(str(conversion_count) + " files were converted.")
        logging.info(str(conversion_count) + " files were converted.")
        
        # Report list of files converted and their corresponding file sizes.
        print("LIST OF EXPORTED ITEMS:")
        logging.info("ITEMS EXPORTED:")
        for i in conversion_list:
            print(str(i[0]) + " exported at " + str(i[1]) + " MB.")
            logging.info(str(i[0]) + " exported at " + str(i[1]) + " MB.")

        print("-----------------------------------------------------------------")
        print("---------------------  BATCH CONVERTER END  ---------------------")
        print("-----------------------------------------------------------------")
        logging.info("-----------------------------------------------------------------")
        logging.info("---------------------  BATCH CONVERTER END  ---------------------")
        logging.info("-----------------------------------------------------------------")

    except Exception as Argument:
        logging.exception("COULD NOT END BATCH CONVERTER")
		

# Quit Blender after batch conversion is complete.
def quit_blender():
    try:
        bpy.ops.wm.quit_blender()

        print("------------------------  QUIT BLENDER  ------------------------")
        logging.info("QUIT BLENDER")

    except Exception as Argument:
        logging.exception("COULD NOT QUIT BLENDER")
		

# Transmogrify.
def transmogrify():
    # Step 1: Set global variables.
    get_variables()

    # Step 2: Start logging conversion if requested by User.
    print(import_file)
    if save_conversion_log:
        make_log_file()

    # Step 3: Run the batch converter.
    batch_converter()

    # Step 4: Quit Blender after batch conversion is complete.
    quit_blender()


### Transmogrify! ###
transmogrify()