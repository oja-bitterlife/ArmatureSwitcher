import bpy

modules = [
    # CursorToSelected,
    # PositionMode,
    # BoneSelector,
    # BoneVisible,
] 

class ARMATUE_SWITCHER_OT_save_settings(bpy.types.Operator):
    bl_idname = "armature_switcher.save_settings"
    bl_label = "Save Settings"

    # execute
    def execute(self, context):
        print("save")
        return{'FINISHED'}

class ARMATUE_SWITCHER_OT_load_settings(bpy.types.Operator):
    bl_idname = "armature_switcher.load_settings"
    bl_label = "Load Settings"

    # execute
    def execute(self, context):
        print("load")
        return{'FINISHED'}



class ARMATUE_SWITCHER_PT_setting(bpy.types.Panel):
    bl_label = "Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "ARMATUE_SWITCHER_PT_UI"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        for _, module in enumerate(modules):
            if hasattr(module, "draw"):
                if hasattr(module, "label"):
                    self.layout.label(text=module.label)
                module.draw(self, context, self.layout.box())


        # Src側設定
        src = self.layout.box()
        src.label(text="Src (copy from)")
        src.prop(context.scene, "ARMATURE_SWITCHER_src", text="Armature")

        # Dist側設定
        dist = self.layout.box()
        dist.label(text="Dist (copy to)")
        dist.prop(context.scene, "ARMATURE_SWITCHER_dist", text="Armature")


        # Save/Loadボタン
        self.layout.operator("armature_switcher.save_settings")
        self.layout.operator("armature_switcher.load_settings")



# セレクトボックスに表示したいArmatureのリストを作成する関数
def get_armature_list(scene, context):
    return ((obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == "ARMATURE" and obj.data.users > 0)

def register():
    for module in modules:
        if hasattr(module, "register"):
            module.register()

    # ArmatureのSrc/DistのEnumPropertyを追加する
    bpy.types.Scene.ARMATURE_SWITCHER_src = bpy.props.EnumProperty(items=get_armature_list)
    bpy.types.Scene.ARMATURE_SWITCHER_dist = bpy.props.EnumProperty(items=get_armature_list)

def unregister():
    for module in modules:
        if hasattr(module, "unregister"):
            module.unregister()
