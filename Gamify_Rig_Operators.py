import bpy
from bpy.props import StringProperty

class BoneInfo:
    name = ""
    connected_to_parent = False

def create_armature(armature_name, context):
        #Create the data and object for the new armature
        armature_data = bpy.data.armatures.new(name=armature_name)
        armature_obj = bpy.data.objects.new(name=armature_name, object_data=armature_data)
        armature_data.layers[0] = False

        #Link the armature object to the active collection of the current view layer
        context.view_layer.active_layer_collection.collection.objects.link(armature_obj)
        
        return armature_obj

def create_bone_structure(rigify_armature, new_armature):
    def create_bone_hierarchy(bone_hierarchy, source_armature_data, dest_armature_data):    
        def create_bone(bone_info, parent_name, source_armature, target_armature):
            dest_bone = target_armature.edit_bones.new(bone_info.name)
            source_bone = source_armature.edit_bones[bone_info.name]
            
            dest_bone.head = source_bone.head
            dest_bone.tail = source_bone.tail
            dest_bone.layers[0] = True
            
            if parent_name is not None:
                parent_bone = target_armature.edit_bones[parent_name]
                dest_bone.parent = parent_bone
                dest_bone.use_connect = bone_info.connected_to_parent
                
            dest_bone.roll = source_bone.roll
    
        def create_bone_children(bone_name, bone_hierarchy, source_armature, dest_armature):
            for child_bone in bone_hierarchy[bone_name]:
                create_bone(child_bone, bone_name, source_armature, dest_armature)
                
                #Create child bones if it has any
                if bone_hierarchy.get(child_bone.name) is not None:
                    create_bone_children(child_bone.name, bone_hierarchy, source_armature, dest_armature)
        
        #Create a root bone to start with
        root_bone = BoneInfo()
        root_bone.name = "root" 
        create_bone(root_bone, None, source_armature_data, dest_armature_data)
        
        #Recursively create children starting with the root bone
        create_bone_children(root_bone.name, bone_hierarchy, source_armature_data, dest_armature_data)
    
    def find_bone_parent(bone, rigify_bones):
        def find_parent_def_bone(def_bone_name, current_bone, bones):
            trimmed_name = current_bone.name[4:]
            
            #Skip bones with the same name as our starting bone
            if(trimmed_name == def_bone_name):
                return find_parent_def_bone(def_bone_name, current_bone.parent, bones)
            
            #Attempt to find the correct deforming bone for the current bone
            for search_bone in bones:
                if(search_bone.name.endswith(trimmed_name) and search_bone.name.startswith("DEF-")):
                    return search_bone
            
            #Keep searching up the hierarchy until the parent is found or none are left
            if(current_bone.parent is not None):
                return find_parent_def_bone(def_bone_name, current_bone.parent, bones)
            else:
                return None
            
        if(bone.parent.name.startswith("DEF-")):
            return bone.parent, True
        
        if(bone.parent.name.startswith("ORG-")):
            return find_parent_def_bone(bone.name[4:], bone.parent, rigify_bones), False

    bone_hierarchy = {}
    
    #Find all the DEF- bones in the rigify armature
    for bone in rigify_armature.bones:
        if(bone.name.startswith("DEF-")):
            if(bone.parent is not None):
                parent_bone = None
                is_connected = False
            
                #Find the parent deforming bone
                if(bone.parent.name != "root"):
                    parent_bone, is_connected = find_bone_parent(bone, rigify_armature.bones)
                else:
                    parent_bone = bone.parent
                
                if(parent_bone is not None):
                    #Add the bone to the array of children that the parent bone has
                    if(parent_bone.name not in bone_hierarchy.keys()):
                        bone_hierarchy[parent_bone.name] = []
                    
                    bone_info = BoneInfo()
                    bone_info.name = bone.name
                    bone_info.connected_to_parent = is_connected
                    
                    bone_hierarchy[parent_bone.name].append(bone_info)
                else:
                    print("Could not determine parent bone for " + bone.name)
                    
    
    create_bone_hierarchy(bone_hierarchy, rigify_armature, new_armature)

def create_constraints(source_armature, dest_armature):
    for bone in dest_armature.pose.bones:
        print(bone.name)
        constraint = bone.constraints.new('COPY_TRANSFORMS')
        constraint.target = source_armature
        constraint.subtarget = bone.name

class GamifyRigOperator(bpy.types.Operator):
    """Creates a game-engine optimized rig from a Rigify rig"""
    bl_idname = "object.gamify_rig_operator"
    bl_label = "Rigify to Gamify Rig"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.object.type == 'ARMATURE'

    def execute(self, context):
        rigify_armature_obj = context.active_object
        properties = context.object.gamify_rig_properties
    
        if(rigify_armature_obj is None or rigify_armature_obj.type != 'ARMATURE'):
            self.report({'ERROR'}, "Please select an Armature object.")
            return { 'CANCELLED'}

        if(properties.rig_name is None or properties.rig_name == ""):
            self.report({'ERROR'}, "Please enter a name for the new rig.")
            return { 'CANCELLED'}
        
        armature_obj = create_armature(properties.rig_name, context)
        
        #Select and enter edit mode on the new armature
        armature_obj.select_set(True)
        context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        
        create_bone_structure(rigify_armature_obj.data, armature_obj.data)
        
        if properties.create_constraints:
            bpy.ops.object.mode_set(mode='POSE', toggle=False)
            create_constraints(rigify_armature_obj, armature_obj)
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(GamifyRigOperator)

def unregister():
    bpy.utils.unregister_class(GamifyRigOperator)

if __name__ == "__main__":
    register()