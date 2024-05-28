import bpy


class ARMATUE_SWITCHER_OT_run(bpy.types.Operator):
    bl_idname = "armature_switcher.run"
    bl_label = "Run"

    def execute(self, context):
        return{'FINISHED'}


# draw
# *****************************************************************************
def draw(cls, context, layout):
    layout.operator("armature_switcher.run")


# register/unregister
# *****************************************************************************
classes = [
    ARMATUE_SWITCHER_OT_run,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
