bl_info = {
    "name": "Gamify Rig",
    "author": "Cullen Dallas",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Object Data",
    "description": "Creates a simplified version of a rigify rig for use in game engines",
    "warning": "",
    "wiki_url": "",
    "category": "Rigging",
}

from . import Gamify_Rig_Operators
from . import Gamify_Rig_Panels
from . import Gamify_Rig_Properties

modules = [Gamify_Rig_Operators, Gamify_Rig_Panels, Gamify_Rig_Properties]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
