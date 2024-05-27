import bpy

# Main UI
# ===========================================================================================
# 3DView Tools Panel
class ARMATUE_SWITCHER_PT_ui(bpy.types.Panel):
    bl_label = "ArmatureSwitcher"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ArmatureSwitcher"
    bl_idname = "ARMATUE_SWITCHER_PT_UI"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass

