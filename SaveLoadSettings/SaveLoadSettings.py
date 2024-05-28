import bpy


class ARMATUE_SWITCHER_OT_save_settings(bpy.types.Operator):
    bl_idname = "armature_switcher.save_settings"
    bl_label = "Save JSON"

    # execute
    def execute(self, context):
        print("save")
        return{'FINISHED'}

class ARMATUE_SWITCHER_OT_load_settings(bpy.types.Operator):
    bl_idname = "armature_switcher.load_settings"
    bl_label = "Load JSON"

    # execute
    def execute(self, context):
        print("load")
        return{'FINISHED'}


# draw
# *****************************************************************************
def draw(cls, context, layout):
    box = layout.box()
    box.label(text="Save/Load Settings")
    row = box.row()
    row.operator("armature_switcher.save_settings")
    row.operator("armature_switcher.load_settings")


# register/unregister
# *****************************************************************************
classes = [
    ARMATUE_SWITCHER_OT_save_settings,
    ARMATUE_SWITCHER_OT_load_settings,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
