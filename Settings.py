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
    PropertyGroup, 
) 
from bpy.props import (
    IntProperty,
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    PointerProperty,
    StringProperty,
    CollectionProperty,
)
from . import Functions



#   █████████  ██████████ ███████████ ███████████ █████ ██████   █████   █████████   █████████ 
#  ███░░░░░███░░███░░░░░█░█░░░███░░░█░█░░░███░░░█░░███ ░░██████ ░░███   ███░░░░░███ ███░░░░░███
# ░███    ░░░  ░███  █ ░ ░   ░███  ░ ░   ░███  ░  ░███  ░███░███ ░███  ███     ░░░ ░███    ░░░ 
# ░░█████████  ░██████       ░███        ░███     ░███  ░███░░███░███ ░███         ░░█████████ 
#  ░░░░░░░░███ ░███░░█       ░███        ░███     ░███  ░███ ░░██████ ░███    █████ ░░░░░░░░███
#  ███    ░███ ░███ ░   █    ░███        ░███     ░███  ░███  ░░█████ ░░███  ░░███  ███    ░███
# ░░█████████  ██████████    █████       █████    █████ █████  ░░█████ ░░█████████ ░░█████████ 
#  ░░░░░░░░░  ░░░░░░░░░░    ░░░░░       ░░░░░    ░░░░░ ░░░░░    ░░░░░   ░░░░░░░░░   ░░░░░░░░░  

# Groups together all the addon settings that are saved in each .blend file
class TRANSMOGRIFIER_PG_TransmogrifierSettings(PropertyGroup):
    # Save conversion log.
    save_conversion_log: BoolProperty(
        name="Save Conversion Log",
        description="Save a log of the batch conversion in the given import directory. This can help troubleshoot conversion errors",
        default=False,
    )
    # Advanced UI toggle.
    advanced_ui: BoolProperty(
        name="Advanced UI",
        description="Toggle simple/advanced user interface options",
        default=False,
    )
    # Transmogrifier Presets (aka Workflows)
    transmogrifier_preset: StringProperty(default='FBX_to_GLB')
    transmogrifier_preset_enum: EnumProperty(
        name="", options={'SKIP_SAVE'},
        description="Use batch conversion settings from a preset.\n(Create by clicking '+' after adjusting settings in the Transmogrifier menu)",
        items=lambda self, context: Functions.get_transmogrifier_presets('transmogrifier'),
        get=lambda self: Functions.get_transmogrifier_preset_index('transmogrifier', self.transmogrifier_preset),
        set=lambda self, value: setattr(self, 'transmogrifier_preset', Functions.transmogrifier_preset_enum_items_refs['transmogrifier'][value][0]),
        update=Functions.set_settings,
    )
    # Import Settings
    link_import_directories: BoolProperty(
        name="Link Directories",
        description="Synchronize import directories between all import file formats",
        default=True,
        update=Functions.link_import_directories,
    )
    import_directory: StringProperty(
        name="Directory",
        description="Parent directory to search through and import files\nDefault of // will import from the same directory as the blend file (only works if the blend file is saved)",
        default="//",
        subtype='DIR_PATH',
        update=Functions.link_import_directories,
    )
   
    # Export Settings
    export_adjacent: BoolProperty(
        name="Export Adjacent",
        description="Export models adjacent to their respective imports",
        default=True,
    )
    link_export_settings: BoolProperty(
        name="Link Export Settings",
        description="Synchronize some export settings between all export file formats",
        default=True,
        update=Functions.link_export_settings,
    )
    export_directory: StringProperty(
        name="Directory",
        description="Directory to export files\nDefault of // will import from the same directory as the blend file (only works if the blend file is saved)",
        default="//",
        subtype='DIR_PATH',
        update=Functions.link_export_settings,
    )
    scale: FloatProperty(
        name="Scale", 
        description="Set the scale of the model before exporting",
        default=1.0,
        soft_min=0.0,
        soft_max=10000.0,
        step=100,
    )
    # Pack resources into Blend.
    pack_resources: BoolProperty(
        name="Pack Resources",
        description="Pack all used external files into .blend",
        default=True,
        )
    # Make Blend paths relative.
    make_paths_relative: BoolProperty(
        name="Relative Paths",
        description="Use relative paths for textures",
        default=True,
        )
    # Option to export models to subdirectories in custom directory
    use_subdirectories: BoolProperty(
        name="Subdirectories",
        description="Export models to their own subdirectories within the given export directory",
        default=True,
        update=Functions.link_export_settings,
    )
    # Option to include only models or also copy original folder contents to custom directory
    copy_original_contents: BoolProperty(
        name="Copy Original Contents",
        description="Copy original contents of each import item's directory to each export item's subdirectory",
        default=False,
        update=Functions.link_export_settings,
    )
    prefix: StringProperty(
        name="Prefix",
        description="Text to put at the beginning of all the exported file names",
        update=Functions.link_export_settings,
    )
    suffix: StringProperty(
        name="Suffix",
        description="Text to put at the end of all the exported file names",
        update=Functions.link_export_settings,
    )
    # Set data names from object names.
    set_data_names: BoolProperty(
        name="Data Names from Objects",
        description="Rename object data names according to their corresponding object names",
        default=True,
        update=Functions.link_export_settings,
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
    keep_modified_textures: BoolProperty(
        name="Keep Modified Textures", 
        description="Don't delete the textures directory used to modify image textures by regex and resolution and/or format",
        default=False,
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
    preserve_original_textures: BoolProperty(
        name="Preserve Original Textures", 
        description="If toggled off, original textures will be replaced with textures from custom directory per model converted",
        default=True,
    )
    use_linked_blend_textures: BoolProperty(
        name="Linked to .blend", 
        description="Use textures already linked to .blend file",
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
            ('Occlusion', "Occlusion", "", 2048),
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
            'Occlusion'
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
            ("OPEN_EXR", "OPEN_EXR", "Save image textures in OpenEXR format", 8),
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
            ('Occlusion', "Occlusion", "", 2048),
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
            'Occlusion'
        },
    )
    # Set all UV map names to "UVMap". This prevents a material issue with USDZ's - when object A and object B share the same material, but their UV
    # map names differ, the material has to pick one UVMap in the UV Map node inputs connected to each texture channel. So if object A's UV map is called
    # "UVMap" but object B's UV map is called "UV_Channel", then the shared material may pick "UV_Channel" as the UV inputs, thus causing object A to appear
    # untextured despite the fact that it shares the same material as object B.
    rename_uvs: BoolProperty(
        name="Rename UV Maps",
        description="Normalize UV map names.  Multiple UV maps within the same object will increment, for example, as 'UVMap', 'UVMap_1', 'UVMap_2', and so on. This prevents an issue in USD formats when two or more objects share the same material but have different UV map names, which causes some objects to appear untextured",
        default=True,
    )
    rename_uvs_name: StringProperty(
        name="Name",
        description="Text to rename all UV maps (e.g. 'UVMap', 'UVChannel', 'map')",
        default="UVMap"
    )
    export_uv_layout: BoolProperty(
        name="Export UVs",
        description="Export UV layout to file",
        default=False,
    )
    modified_uvs: BoolProperty(
        name="Modified",
        description="Export UVs from the modified mesh",
        default=False,
    )
    uv_export_location: EnumProperty(
        name="Destination",
        description="Select directory into which UV layouts will be exported",
        items=[
            ("Textures", "Textures", "Export UVs to a Textures subfolder for each item. If none exists, create one", 'TEXTURE', 1),
            ("UV", "UV", "Export UVs to a 'UV' subfolder for each item. If none exists, create one", 'UV', 2),
            ("Model", "Model", "Export UVs to the same directories as converted models for each item", 'FILE_3D', 3),
            ("Custom", "Custom", "Export all UVs to a custom directory of choice", 'NEWFOLDER', 4),
        ],
        default="UV",
    )
    uv_directory_custom: StringProperty(
        name="Directory",
        description="Set a custom directory to which UV maps will be exported\nDefault of // will export to same directory as the blend file (only works if the blend file is saved)",
        default="//",
        subtype='DIR_PATH',
    )
    uv_combination: EnumProperty(
        name="Combination",
        description="Select how UV layouts should be combined upon export",
        items=[
            ("All", "All", "Export all UVs together (1 UV layout per converted model)", 'STICKY_UVS_LOC', 1),
            ("Object", "Object", "Export UVs by object (1 UV layout per object)", 'OBJECT_DATA', 2),
            ("Material", "Material", "Export UVs by material (1 UV layout per material)", 'MATERIAL', 3),
        ],
        default="Material",
    )
    uv_resolution: EnumProperty(
        name="Resolution",
        description="Set a custom image texture resolution for exported models without affecting resolution of original/source texture files",
        items=[
            ("8192", "8192", "Square aspect ratio", 1),
            ("4096", "4096", "Square aspect ratio", 2),
            ("2048", "2048", "Square aspect ratio", 3),
            ("1024", "1024", "Square aspect ratio", 4),
            ("512", "512", "Square aspect ratio", 5),
            ("256", "256", "Square aspect ratio", 6),
            ("128", "128", "Square aspect ratio", 7),
        ],
        default="1024",
    )
    uv_format: EnumProperty(
        name="Format",
        description="File format to export the UV layout to \n(Transparency only works for PNG, EPS, and SVG)",
        items=[
            ("PNG", "PNG", "Export the UV layout to bitmap PNG image", 1),
            ("EPS", "EPS", "Export the UV layout to a vector EPS file", 2),
            ("SVG", "SVG", "Export the UV layout to a vector SVG file", 3),
            ("JPEG", "JPEG", "Export the UV layout to bitmap JPEG format", 4),
            ("TARGA", "TARGA", "Export the UV layout to bitmap TARGA format", 5),
            ("TIFF", "TIFF", "Export the UV layout to bitmap TIFF format", 6),
            ("WEBP", "WEBP", "Export the UV layout to bitmap WEBP format", 7),
            ("BMP", "BMP", "Export the UV layout to bitmap BMP format", 8),
            ("OPEN_EXR", "OPEN_EXR", "Export the UV layout to bitmap OpenEXR format", 9),
        ],
        default="PNG",
    )
    uv_image_quality: IntProperty(
        name="Quality", 
        description="(%) Quality for image formats that support lossy compression",
        default=90,
        soft_min=0,
        soft_max=100,
        step=5,
    )
    uv_fill_opacity: FloatProperty(
        name="Fill Opacity", 
        description="Set amount of opacity for export UV layout \n(between 0.0 and 1.0)",
        default=0.0,
        soft_min=0.0,
        soft_max=1.0,
        step=1.0,
    )
    # Option to set custom transformations
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
    use_animations: BoolProperty(
        name="Use Animations", 
        description="Use animations.  If toggled off, animations will be deleted",
        default=True,
    )
    # Set unit system.
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
    # Set length unit.
    length_unit: EnumProperty(
        name="Length",
        description="Set the length unit to use for export",
        items=lambda self, context: Functions.get_length_unit(self.unit_system),
    )
    # Option to set file size maximum.
    auto_optimize: BoolProperty(
        name="Optimize Exports", 
        description="Set a maximum file size and Transmogrifier will automatically try to reduce the file size according to the requested size. If exporting 2 formats at once, it only takes the first file format into account",
        default=False,
    )
    auto_optimize_filter: EnumProperty(
        name="Include",
        description="Filter models to be automatically optimized",
        items=[
            ("All", "All", "Auto-optimize all exported files even if some previously exported files are already below the target threshold", "SELECT_EXTEND", 1),
            ("Above Target", "Above Target", "Only auto-optimize exported files are still above the target threshold. Ignore previously exported files that are already below the target maximum", "SELECT_SUBTRACT", 2),
        ],
        default="All",
    )
    # File size maximum target.
    auto_optimize_target_file_size: FloatProperty(
        name="Target (MB)", 
        description="Set the threshold below which Transmogrifier should attempt to reduce each converted file's size (Megabytes)",
        default=15.0,
        soft_min=0.0,
        soft_max=1000.0,
        step=10,
    )

    auto_optimize_show_methods: BoolProperty(
        name="Methods", 
        description="Filter methods to use for auto-optimize file size reduction",
        default=False,
    )

    auto_optimize_draco: BoolProperty(
        name="Draco", 
        description="(Only for GLB export). Try Draco-compression to lower the exported file size",
        default=True,
    )

    auto_optimize_texture_resize: BoolProperty(
        name="Resize Tex.", 
        description="Try resizing textures to lower the exported file size",
        default=True,
    )

    auto_optimize_texture_reformat: BoolProperty(
        name="Reformat Tex.", 
        description="Try reformatting all textures except the normal map to JPEG's to lower the exported file size",
        default=True,
    )

    auto_optimize_decimate: BoolProperty(
        name="Decimate", 
        description="Try decimating objects to lower the exported file size",
        default=False,
    )

    # Draco compression level.
    compression_level: IntProperty(
        name="Compression Level", 
        description="Draco compression level (0 = most speed, 6 = most compression, higher values currently not supported)",
        default=6,
        soft_min=0,
        soft_max=6,
        step=1,
    )    
    # Limit resolution that auto resize files should not go below.
    resize_textures_limit: EnumProperty(
        name="Resize Limit",
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
    # Include normal map in auto-reformatting.
    include_normal_maps: BoolProperty(
        name="Normal Maps",
        description="Include normal maps in 'Reformat Textures' (to JPG's)",
        default=False,
        )
    # Limit how many time a mesh can be decimated during auto resize files.
    decimate_limit: IntProperty(
        name="Decimate Limit", 
        description="Limit the number of times an item can be decimated. Items will be decimated by 50% each time",
        default=3,
        soft_min=0,
        soft_max=10,
        step=1,
    )
    # Mark data blocks as assets.
    mark_as_assets: BoolProperty(
        name="Mark as Assets",
        description="Mark converted models as assets.\n(Saves a Blend file for each model converted)",
        default=False,
    )
    # Mark asset data filter.
    asset_types_to_mark: EnumProperty(
        name="Mark Assets Filter",
        options={'ENUM_FLAG'},
        items=[
            ('Actions', "", "Mark individual actions (animations) as assets.", "ACTION", 1),
            ('Collections', "", "Mark individual collections as assets.", "OUTLINER_COLLECTION", 2),
            ('Materials', "", "Mark individual materials as assets.", "MATERIAL", 4),
            ('Node_Groups', "", "Mark individual node trees as assets.", "NODETREE", 8),
            ('Objects', "", "Mark individual objects as assets.", "OBJECT_DATA", 16),
            ('Worlds', "", "Mark individual worlds as assets.", "WORLD", 32),
        ],
        description="Select asset types to archive",
        default={
            'Collections',
        },
    )
    # Extract asset preview images to disk.
    asset_extract_previews: BoolProperty(
        name="Save Previews to Disk",
        description="Extract a preview image thumbnail for each asset type and save to disk as PNG.\n(Only works for assets that can have previews generated.)",
        default=False,
    )
    # Filter asset previews to extract.
    asset_extract_previews_filter: EnumProperty(
        name="Extract Previews Filter",
        options={'ENUM_FLAG'},
        items=[
            ('Actions', "", "Extract previews of Actions assets.", "ACTION", 1),
            ('Collections', "", "Extract previews of Collections assets.", "OUTLINER_COLLECTION", 2),
            ('Materials', "", "Extract previews of Materials assets.", "MATERIAL", 4),
            ('Node_Groups', "", "Extract previews of Node_Groups assets.", "NODETREE", 8),
            ('Objects', "", "Extract previews of Objects assets.", "OBJECT_DATA", 16),
            ('Worlds', "", "Extract previews of Worlds assets.", "WORLD", 32),
        ],
        description="Filter asset types from which to extract image previews to disk.",
        default={
            'Collections',
        },
    )
    # Allow duplicate assets.
    assets_allow_duplicates: BoolProperty(
        name="Allow Duplicates",
        description="Allow duplicate assets that already exist in the selected asset library.\n(i.e. Mark duplicates as assets)",
        default=False,
    )
    # Filter asset types to allow duplicates.
    assets_allow_duplicates_filter: EnumProperty(
        name="Allow Duplicates Filter",
        options={'ENUM_FLAG'},
        items=[
            ('Actions', "", "Allow duplicate actions. Actions with the same as one already\nin the selected asset library will not be marked as assets.", "ACTION", 1),
            ('Collections', "", "Allow duplicate collections. Collections with the same as one already\nin the selected asset library will not be marked as assets.", "OUTLINER_COLLECTION", 2),
            ('Materials', "", "Allow duplicate materials. Materials with the same as one already\nin the selected asset library will not be marked as assets.", "MATERIAL", 4),
            ('Node_Groups', "", "Allow duplicate node trees. Node Trees with the same as one already\nin the selected asset library will not be marked as assets.", "NODETREE", 8),
            ('Objects', "", "Allow duplicate objects. Objects with the same as one already\nin the selected asset library will not be marked as assets.", "OBJECT_DATA", 16),
            ('Worlds', "", "Allow duplicate worlds. Worlds with the same as one already\nin the selected asset library will not be marked as assets.", "WORLD", 32),
        ],
        description="Filter which asset types to allow when an asset\nof that type already exists in the selected asset library",
    )
    # Only mark master collection as asset when importing a Blend (if Collections are to be marked as assets).
    mark_only_master_collection: BoolProperty(
        name="Mark Only Master",
        description="When importing a blend file, mark only the master collection as an asset and ignore other collections.\n(For each item converted, all objects are moved to a master collection matching the item name.\nThis option is only relevant when importing .blend files that may already contain collections.)",
        default=True,
    )
    # Filter object types when marking objects as assets.
    asset_object_types_filter: EnumProperty(
        name="Object Types",
        options={'ENUM_FLAG'},
        items=[
            ('MESH', "Mesh", "", "MESH_DATA", 1),
            ('CURVE', "Curve", "", "CURVE_DATA", 2),
            ('SURFACE', "Surface", "", "SURFACE_DATA", 4),
            ('META', "Metaball", "", "META_DATA", 8),
            ('FONT', "Text", "", "FONT_DATA", 16),
            ('GPENCIL', "Grease Pencil", "", "OUTLINER_OB_GREASEPENCIL", 32),
            ('ARMATURE', "Armature", "", "ARMATURE_DATA", 64),
            ('EMPTY', "Empty", "", "EMPTY_DATA", 128),
            ('LIGHT', "Lamp", "", "LIGHT_DATA", 256),
            ('CAMERA', "Camera", "", "CAMERA_DATA", 512),
        ],
        description="Filter which object types to mark as assets.\nNot all will be able to have preview images generated",
        default={
            'MESH', 
            'CURVE', 
            'SURFACE', 
            'META', 
            'FONT', 
            'GPENCIL', 
            'ARMATURE', 
            'LIGHT', 
            'CAMERA', 
        },
    )
    # Asset Library.
    asset_library: StringProperty(default='(no library)')
    asset_library_enum: EnumProperty(
        name="Asset Library", options={'SKIP_SAVE'},
        description="Archive converted assets to selected library",
        items=lambda self, context: Functions.get_asset_libraries(),
        get=lambda self: Functions.get_asset_library_index(self.asset_library),
        set=lambda self, value: setattr(self, 'asset_library', Functions.asset_library_enum_items_refs["asset_libraries"][value][0]),
    )
    # Asset Catalog.
    asset_catalog: StringProperty(default='(no catalog)')
    asset_catalog_enum: EnumProperty(
        name="Catalog", options={'SKIP_SAVE'},
        description="Assign converted assets to selected catalog",
        items=lambda self, context: Functions.get_asset_catalogs(),
        get=lambda self: Functions.get_asset_catalog_index(self.asset_catalog),
        set=lambda self, value: setattr(self, 'asset_catalog', Functions.asset_catalog_enum_items_refs["asset_catalogs"][value][0]),
    )
    # Set location of Blend containing assets.
    asset_blend_location: EnumProperty(
        name="Blend Files",
        description="Set where the blend files containing assets will be stored",
        items=[
            ("Move", "Move to Library", "Move blend files and associated textures to selected asset library.", 1),
            ("Copy", "Copy to Library", "Copy blend files and associated textures to selected asset library.", 2),
            ("None", "Don't Move/Copy", "Don't move or copy blend files and associated textures to selected asset library.\n(Select this option when Transmogrifying inside an asset library directory.)", 3),
        ],
        default="Move",
    )
    # Add metadata to assets.
    asset_add_metadata: BoolProperty(
        name="Add Metadata",
        description="Add metadata to converted items",
        default=True,
    )
    # Metadata: Description
    asset_description: StringProperty(
        name="Description",
        description="A description of the asset to be displayed for the user",
    )
    # Metadata: License
    asset_license: StringProperty(
        name="License",
        description="The type of license this asset is distributed under. An empty license name does not necessarily indicate that this is free of licensing terms. Contact the author if any clarification is needed",
    )
    # Metadata: Copyright
    asset_copyright: StringProperty(
        name="Copyright",
        description="Copyright notice for this asset. An empty copyright notice does not necessarily indicate that this is copyright-free. Contact the author if any clarification is needed",
    )
    # Metadata: Author
    asset_author: StringProperty(
        name="Author",
        description="Name of the creator of the asset",
    )
    # Metadata: Tags
    asset_tags: StringProperty(
        name="Tags",
        description="Add new keyword tags to assets. Separate tags with a space",
    )


# Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), bake_passes.py
class TRANSMOGRIFIER_PG_TransmogrifierImports(PropertyGroup):

    name: StringProperty(
        name="Name", 
        default="FBX",
    )

    show_settings: BoolProperty(
        name="Show/Hide import settings",
        description="",
        default=True,
    )

    directory: StringProperty(
        name="Directory",
        description="Parent directory to search through and import files\nDefault of // will import from the same directory as the blend file (only works if the blend file is saved)",
        default="//",
        subtype='DIR_PATH',
    )

    format: EnumProperty(
        name="Format",
        description="Which file format to import",
        items=[
            ("DAE", "Collada (.dae)", "", 1),
            ("ABC", "Alembic (.abc)", "", 2),
            ("USD", "Universal Scene Description (.usd/.usdc/.usda/.usdz)", "", 3),
            ("OBJ", "Wavefront (.obj)", "", 4),
            ("PLY", "Stanford (.ply)", "", 5),
            ("STL", "STL (.stl)", "", 6),
            ("FBX", "FBX (.fbx)", "", 7),
            ("glTF", "glTF (.glb/.gltf)", "", 8),
            ("X3D", "X3D Extensible 3D (.x3d)", "", 9),
            ("BLEND", "Blender (.blend)", "", 10)
        ],
        default="FBX",
        update=lambda self, context: Functions.update_import_export_settings(self, context, "imports"),
    )

    # A string property for saving User option (without new presets changing User choice),...
    preset: StringProperty(
        name="Preset",
        default='NO_PRESET',
    )

    # ... and enum property for choosing.
    preset_enum: EnumProperty(
        name="Preset", 
        options={'SKIP_SAVE'},
        description="Use import settings from a preset.\n(Create in the import settings from the File > Import menu",
        items=lambda self, context: Functions.get_operator_presets(Functions.operator_dict[self.format][0][0]),
        get=lambda self: Functions.get_preset_index(Functions.operator_dict[self.format][0][0], self.preset),
        set=lambda self, value: setattr(self, 'preset', Functions.preset_enum_items_refs[Functions.operator_dict[self.format][0][0]][value][0]),
        update=lambda self, context: Functions.update_import_export_settings(self, context, "imports"),
    )

    extension: EnumProperty(
        name="Extension", 
        options={'SKIP_SAVE'},
        description="Format extension",
        items=lambda self, context: Functions.get_format_extensions(self.format),
        update=lambda self, context: Functions.update_import_export_settings(self, context, "imports"),
    )

    operator: StringProperty(
        name="Operator",
        description="Import operator string",
        default="bpy.ops.import_scene.fbx(**",
    )

    options: StringProperty(
        name="Options",
        description="Dictionary of import operator options from preset",
        default="{}",
    )



# Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), bake_passes.py
class TRANSMOGRIFIER_PG_TransmogrifierExports(PropertyGroup):

    name: StringProperty(
        name="Name", 
        default="GLB",
    )

    show_settings: BoolProperty(
        name="Show/Hide export settings",
        description="",
        default=True,
    )

    format: EnumProperty(
        name="Format",
        description="Which file format to import",
        items=[
            ("DAE", "Collada (.dae)", "", 1),
            ("ABC", "Alembic (.abc)", "", 2),
            ("USD", "Universal Scene Description (.usd/.usdc/.usda/.usdz)", "", 3),
            ("OBJ", "Wavefront (.obj)", "", 4),
            ("PLY", "Stanford (.ply)", "", 5),
            ("STL", "STL (.stl)", "", 6),
            ("FBX", "FBX (.fbx)", "", 7),
            ("glTF", "glTF (.glb/.gltf)", "", 8),
            ("X3D", "X3D Extensible 3D (.x3d)", "", 9),
            ("BLEND", "Blender (.blend)", "", 10)
        ],
        default="glTF",
        update=lambda self, context: Functions.update_import_export_settings(self, context, "exports"),
    )

    # A string property for saving User option (without new presets changing User choice),...
    preset: StringProperty(
        name="Preset",
        default='NO_PRESET',
    )

    # ... and enum property for choosing.
    preset_enum: EnumProperty(
        name="Preset", 
        options={'SKIP_SAVE'},
        description="Use import settings from a preset.\n(Create in the import settings from the File > Import menu",
        items=lambda self, context: Functions.get_operator_presets(Functions.operator_dict[self.format][1][0]),
        get=lambda self: Functions.get_preset_index(Functions.operator_dict[self.format][1][0], self.preset),
        set=lambda self, value: setattr(self, 'preset', Functions.preset_enum_items_refs[Functions.operator_dict[self.format][1][0]][value][0]),
        update=lambda self, context: Functions.update_import_export_settings(self, context, "exports"),
    )

    extension: EnumProperty(
        name="Extension", 
        options={'SKIP_SAVE'},
        description="Format extension",
        items=lambda self, context: Functions.get_format_extensions(self.format),
        update=lambda self, context: Functions.update_import_export_settings(self, context, "exports"),
    )

    operator: StringProperty(
        name="Operator",
        description="Import operator string",
        default="bpy.ops.export_scene.gltf(**",
    )

    options: StringProperty(
        name="Options",
        description="Dictionary of export operator options from preset",
        default="{}",
    )

    scale: FloatProperty(
        name="Scale", 
        description="Set the scale of the model before exporting",
        default=1.0,
        soft_min=0.0,
        soft_max=10000.0,
        step=500,
    )

    directory: StringProperty(
        name="Directory",
        description="Custom output directory. \nDefault of // will import from the same directory as the blend file (only works if the blend file is saved)",
        default="//",
        subtype='DIR_PATH',
    )

    use_subdirectories: BoolProperty(
        name="Subdirectories",
        description="Export models to their own subdirectories within the given export directory",
        default=True,
    )

    copy_original_contents: BoolProperty(
        name="Copy Original Contents",
        description="Copy original contents of each import item's directory to each export item's subdirectory",
        default=False,
    )

    prefix: StringProperty(
        name="Prefix",
        description="Text to put at the beginning of all the exported file names",
    )

    suffix: StringProperty(
        name="Suffix",
        description="Text to put at the end of all the exported file names",
    )

    set_data_names: BoolProperty(
        name="Data Names from Objects",
        description="Rename object data names according to their corresponding object names",
        default=True,
    )



# Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), bake_passes.py
class TRANSMOGRIFIER_PG_TransmogrifierScripts(PropertyGroup):
    
    name: StringProperty(
        name="Name", 
        default="Script",
    )
    
    show_settings: BoolProperty(
        name="Show/Hide custom script settings",
        description="",
        default=True,
    )

    file: StringProperty(
        name="Python File",
        description="Path to a Python script file",
        default="*.py",
        subtype='FILE_PATH',
        update=Functions.update_custom_script_names,
    )

    trigger: EnumProperty(
        name="Trigger",
        description="Set when custom script should be triggered",
        items=[
            ("Before_Batch", "Before Batch", "Run script before the batch conversion begins.", 1),
            ("Before_Import", "Before Import", "Run script immediately before importing a model.", 2),
            ("Before_Export", "Before Export", "Run script immediately before exporting a model.", 3),
            ("After_Export", "After Export", "Run script immediately after exporting a model.", 4),
            ("After_Batch", "After Batch", "Run script after the batch conversion ends.", 5),
        ],
        default="Before_Export",
    )



#  ███████████   ██████████   █████████  █████  █████████  ███████████ ███████████   █████ █████
# ░░███░░░░░███ ░░███░░░░░█  ███░░░░░███░░███  ███░░░░░███░█░░░███░░░█░░███░░░░░███ ░░███ ░░███ 
#  ░███    ░███  ░███  █ ░  ███     ░░░  ░███ ░███    ░░░ ░   ░███  ░  ░███    ░███  ░░███ ███  
#  ░██████████   ░██████   ░███          ░███ ░░█████████     ░███     ░██████████    ░░█████   
#  ░███░░░░░███  ░███░░█   ░███    █████ ░███  ░░░░░░░░███    ░███     ░███░░░░░███    ░░███    
#  ░███    ░███  ░███ ░   █░░███  ░░███  ░███  ███    ░███    ░███     ░███    ░███     ░███    
#  █████   █████ ██████████ ░░█████████  █████░░█████████     █████    █████   █████    █████   
# ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░░░░░  ░░░░░  ░░░░░░░░░     ░░░░░    ░░░░░   ░░░░░    ░░░░░    

classes = (
    TRANSMOGRIFIER_PG_TransmogrifierSettings,
    TRANSMOGRIFIER_PG_TransmogrifierImports,
    TRANSMOGRIFIER_PG_TransmogrifierExports,
    TRANSMOGRIFIER_PG_TransmogrifierScripts,
)

# Register Classes.
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Add settings to Scene type.
    bpy.types.Scene.transmogrifier_settings = PointerProperty(type=TRANSMOGRIFIER_PG_TransmogrifierSettings)
    bpy.types.Scene.transmogrifier_imports = CollectionProperty(type=TRANSMOGRIFIER_PG_TransmogrifierImports)
    bpy.types.Scene.transmogrifier_exports = CollectionProperty(type=TRANSMOGRIFIER_PG_TransmogrifierExports)
    bpy.types.Scene.transmogrifier_scripts = CollectionProperty(type=TRANSMOGRIFIER_PG_TransmogrifierScripts)
    

# Unregister Classes.
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Delete the settings from Scene type (Doesn't actually remove existing ones from scenes).
    del bpy.types.Scene.transmogrifier_imports
    del bpy.types.Scene.transmogrifier_exports
    del bpy.types.Scene.transmogrifier_settings