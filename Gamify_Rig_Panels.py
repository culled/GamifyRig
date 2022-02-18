import bpy

class GamifyRigPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Gamify Rig"
    bl_idname = "OBJECT_PT_gamify_rig_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return (context.object is not None and context.object.type == 'ARMATURE')
    
    def draw(self, context):
        layout = self.layout
        
        layout.prop(context.object.gamify_rig_properties, "rig_name")
        layout.prop(context.object.gamify_rig_properties, "create_constraints")
        layout.operator("object.gamify_rig_operator", icon='ARMATURE_DATA')

def register():
    bpy.utils.register_class(GamifyRigPanel)

def unregister():
    bpy.utils.unregister_class(GamifyRigPanel)

if __name__ == "__main__":
    register()