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
)



#   █████████    █████████  ███████████   █████ ███████████  ███████████  █████████ 
#  ███░░░░░███  ███░░░░░███░░███░░░░░███ ░░███ ░░███░░░░░███░█░░░███░░░█ ███░░░░░███
# ░███    ░░░  ███     ░░░  ░███    ░███  ░███  ░███    ░███░   ░███  ░ ░███    ░░░ 
# ░░█████████ ░███          ░██████████   ░███  ░██████████     ░███    ░░█████████ 
#  ░░░░░░░░███░███          ░███░░░░░███  ░███  ░███░░░░░░      ░███     ░░░░░░░░███
#  ███    ░███░░███     ███ ░███    ░███  ░███  ░███            ░███     ███    ░███
# ░░█████████  ░░█████████  █████   █████ █████ █████           █████   ░░█████████ 
#  ░░░░░░░░░    ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░ ░░░░░           ░░░░░     ░░░░░░░░░  
# Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), bake_passes.py

class CustomScript(PropertyGroup):

    name: bpy.props.StringProperty(name="Name", default="Unknown")

    directory: StringProperty(
        name="Directory",
        description="",
        default="//",
        subtype='DIR_PATH',
    )

    Trigger: EnumProperty(
        name="Run Script at",
        description="Set when custom script should be triggered",
        items=[
            ("Before_Import", "Before Import", "", 1),
            ("After_Import", "After Import", "", 2),
            ("Before_Export", "Before Export", "", 3),
            ("After_Export", "After Export", "", 4),
        ],
        default="After_Import",
    )


def add_customscript(context):
    new_custom_script = context.scene.custom_scripts.add()
    new_custom_script.name = "Custom Script"



#  ███████████   ██████████   █████████  █████  █████████  ███████████ ███████████   █████ █████
# ░░███░░░░░███ ░░███░░░░░█  ███░░░░░███░░███  ███░░░░░███░█░░░███░░░█░░███░░░░░███ ░░███ ░░███ 
#  ░███    ░███  ░███  █ ░  ███     ░░░  ░███ ░███    ░░░ ░   ░███  ░  ░███    ░███  ░░███ ███  
#  ░██████████   ░██████   ░███          ░███ ░░█████████     ░███     ░██████████    ░░█████   
#  ░███░░░░░███  ░███░░█   ░███    █████ ░███  ░░░░░░░░███    ░███     ░███░░░░░███    ░░███    
#  ░███    ░███  ░███ ░   █░░███  ░░███  ░███  ███    ░███    ░███     ░███    ░███     ░███    
#  █████   █████ ██████████ ░░█████████  █████░░█████████     █████    █████   █████    █████   
# ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░░░░░  ░░░░░  ░░░░░░░░░     ░░░░░    ░░░░░   ░░░░░    ░░░░░    

classes = (
    CustomScript,
)

# Register Classes.
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.custom_scripts = bpy.props.CollectionProperty(type=CustomScript)

# Unregister Classes.
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.custom_scripts