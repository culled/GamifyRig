import bpy
from bpy.props import (StringProperty, BoolProperty, PointerProperty)
from bpy.types import (Object, PropertyGroup)

class GamifyRigProperties(PropertyGroup):
    rig_name: StringProperty(name="New Rig Name", description="Choose a name for the new rig", default="Gamify_Rig")
    create_constraints: BoolProperty(name="Constrain to Original Rig", description="If enabled, each bone in the generated rig will be constrained to the corresponding bone in the original rig", default=True)

def register():
    bpy.utils.register_class(GamifyRigProperties)
    Object.gamify_rig_properties = PointerProperty(type=GamifyRigProperties)

def unregister():
    bpy.utils.unregister_class(GamifyRigProperties)
    del Object.gamify_rig_properties

if __name__ == "__main__":
    register()