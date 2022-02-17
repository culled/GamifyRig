# Gamify Rig
A simple tool for creating a game engine optimized rig from a Rigify rig, while keeping compatibility between the two.

# Features
- Creates a duplicate rig that has identical DEF- bones to the Rigify rig, but with a much simpler hierarchy
- Constrains each bone in the duplicate rig to the identical DEF- bones in the Rigify rig so the Gamify rig's motion matches the Rigify rig
- Meshes with "Armature Deform" modifiers parented to a Rigify rig can be reparented to the Gamify rig with full compatibility

# Usage
1. Select a Rigify rig in object mode
2. In the object data properties (where the armature data is), click on "Rigify to Gamify Rig" under the "Gamify Rig" tab
3. A new rig will be created
