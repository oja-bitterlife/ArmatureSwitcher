import bpy


class ARMATUE_SWITCHER_OT_bonemap_save(bpy.types.Operator):
    bl_idname = "armature_switcher.bonemap_save"
    bl_label = "Save JSON"

    # execute
    def execute(self, context):
        print("save")
        return{'FINISHED'}

class ARMATUE_SWITCHER_OT_bonemap_load(bpy.types.Operator):
    bl_idname = "armature_switcher.bonemap_load"
    bl_label = "Load JSON"

    # execute
    def execute(self, context):
        print("load")
        return{'FINISHED'}


# draw
# *****************************************************************************
def draw(cls, context, layout):
    row = layout.row()
    row.operator("armature_switcher.bonemap_save")
    row.operator("armature_switcher.bonemap_load")


# register/unregister
# *****************************************************************************
classes = [
    ARMATUE_SWITCHER_OT_bonemap_save,
    ARMATUE_SWITCHER_OT_bonemap_load,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
