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
import importlib



#  █████ ██████   █████ ███████████    ███████   
# ░░███ ░░██████ ░░███ ░░███░░░░░░█  ███░░░░░███ 
#  ░███  ░███░███ ░███  ░███   █ ░  ███     ░░███
#  ░███  ░███░░███░███  ░███████   ░███      ░███
#  ░███  ░███ ░░██████  ░███░░░█   ░███      ░███
#  ░███  ░███  ░░█████  ░███  ░    ░░███     ███ 
#  █████ █████  ░░█████ █████       ░░░███████░  
# ░░░░░ ░░░░░    ░░░░░ ░░░░░          ░░░░░░░    

bl_info = {
    "name": "Transmogrifier",
    "author": "Sapwood Studio",
    "version": (1, 5, 0),
    "blender": (3, 6),
    "category": "Import-Export",
    "location": "Set in preferences below. Default: 3D Viewport Side Panel (Transmogrifier Tab)",
    "description": "Batch converts 3D files and associated textures into other formats.",
    "doc_url": "github.com/SapwoodStudio/Transmogrifier",
    "tracker_url": "github.com/sapwoodstudio/Transmogrifier/issues",
}



#  ██████   ██████    ███████    ██████████   █████  █████ █████       ██████████  █████████ 
# ░░██████ ██████   ███░░░░░███ ░░███░░░░███ ░░███  ░░███ ░░███       ░░███░░░░░█ ███░░░░░███
#  ░███░█████░███  ███     ░░███ ░███   ░░███ ░███   ░███  ░███        ░███  █ ░ ░███    ░░░ 
#  ░███░░███ ░███ ░███      ░███ ░███    ░███ ░███   ░███  ░███        ░██████   ░░█████████ 
#  ░███ ░░░  ░███ ░███      ░███ ░███    ░███ ░███   ░███  ░███        ░███░░█    ░░░░░░░░███
#  ░███      ░███ ░░███     ███  ░███    ███  ░███   ░███  ░███      █ ░███ ░   █ ███    ░███
#  █████     █████ ░░░███████░   ██████████   ░░████████   ███████████ ██████████░░█████████ 
# ░░░░░     ░░░░░    ░░░░░░░    ░░░░░░░░░░     ░░░░░░░░   ░░░░░░░░░░░ ░░░░░░░░░░  ░░░░░░░░░  

# Adapted from Bystedts Blender Baker (GPL-3.0 License, https://3dbystedt.gumroad.com/l/JAqLT), __init__.py
modules = (
    '.Custom_Scripts',
    '.Functions',
    '.Operators',
    '.Settings',
    '.UI',
)

def import_modules():
    for mod in modules:
        importlib.import_module(mod, bl_info["name"])

def reimport_modules():
    for mod in modules:
        # Reimporting modules during addon development
        want_reload_module = importlib.import_module(mod, bl_info["name"])
        importlib.reload(want_reload_module)   

import_modules()
reimport_modules()

from . import Custom_Scripts
from . import Functions
from . import Operators
from . import Settings
from . import UI



#  ███████████   ██████████   █████████  █████  █████████  ███████████ ███████████   █████ █████
# ░░███░░░░░███ ░░███░░░░░█  ███░░░░░███░░███  ███░░░░░███░█░░░███░░░█░░███░░░░░███ ░░███ ░░███ 
#  ░███    ░███  ░███  █ ░  ███     ░░░  ░███ ░███    ░░░ ░   ░███  ░  ░███    ░███  ░░███ ███  
#  ░██████████   ░██████   ░███          ░███ ░░█████████     ░███     ░██████████    ░░█████   
#  ░███░░░░░███  ░███░░█   ░███    █████ ░███  ░░░░░░░░███    ░███     ░███░░░░░███    ░░███    
#  ░███    ░███  ░███ ░   █░░███  ░░███  ░███  ███    ░███    ░███     ░███    ░███     ░███    
#  █████   █████ ██████████ ░░█████████  █████░░█████████     █████    █████   █████    █████   
# ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░░░░░  ░░░░░  ░░░░░░░░░     ░░░░░    ░░░░░   ░░░░░    ░░░░░    

# Register Classes.
def register():
    import_modules()
    Custom_Scripts.register()
    Operators.register()
    Settings.register()
    UI.register()

# Unregister Classes.
def unregister():
    Custom_Scripts.unregister()
    Operators.unregister()
    Settings.unregister()
    UI.unregister()

if __name__ == '__main__':
    register()