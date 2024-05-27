import bpy

modules = [
    # CursorToSelected,
    # PositionMode,
    # BoneSelector,
    # BoneVisible,
] 

class ARMATUE_SWITCHER_OT_save_settings(bpy.types.Operator):
    bl_idname = "armature_switcher.save_settings"
    bl_label = "Save"

    # execute
    def execute(self, context):
        print("save")
        return{'FINISHED'}

class ARMATUE_SWITCHER_OT_load_settings(bpy.types.Operator):
    bl_idname = "armature_switcher.load_settings"
    bl_label = "Load"

    # execute
    def execute(self, context):
        print("load")
        return{'FINISHED'}


class ARMATUE_SWITCHER_OT_add(bpy.types.Operator):
    bl_idname = "armature_switcher.add_bonemap"
    bl_label = "Add BoneMap"

    def execute(self, context):
        context.scene.ARMATURE_SWITCHER_bonemap.add()
        return{'FINISHED'}

class ARMATUE_SWITCHER_OT_remove(bpy.types.Operator):
    bl_idname = "armature_switcher.remove_bonemap"
    bl_label = ""

    id: bpy.props.IntProperty()

    def execute(self, context):
        context.scene.ARMATURE_SWITCHER_bonemap.remove(self.id)
        return{'FINISHED'}

class ARMATUE_SWITCHER_OT_run(bpy.types.Operator):
    bl_idname = "armature_switcher.run"
    bl_label = "Run"

    def execute(self, context):
        return{'FINISHED'}


class ARMATUE_SWITCHER_PT_setting(bpy.types.Panel):
    bl_label = "Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "ARMATUE_SWITCHER_PT_UI"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        # 設定用
        setting_box = self.layout.box()

        # Armature設定
        box = setting_box.box()
        box.label(text="Armature")
        box.prop(context.scene, "ARMATURE_SWITCHER_armature_src", text="Src")
        box.prop(context.scene, "ARMATURE_SWITCHER_armature_dist", text="Dist")

        # Bone設定
        box = setting_box.box()
        box.label(text="Bone Mapping")
        for i, bonemap in enumerate(context.scene.ARMATURE_SWITCHER_bonemap):
            row = box.row()
            row.prop(bonemap, "src_bone", text="")
            row.label(icon="RIGHTARROW_THIN")
            row.prop(bonemap, "dist_bone", text="")

            # 閉じるボタン
            row.operator("armature_switcher.remove_bonemap", icon="PANEL_CLOSE").id = i

        box.operator("armature_switcher.add_bonemap")

        # 設定実行
        setting_box.operator("armature_switcher.run")

        # Save/Loadボタン
        box = self.layout.box()
        box.label(text="Save/Load Settings")
        row = box.row()
        row.operator("armature_switcher.save_settings")
        row.operator("armature_switcher.load_settings")



# セレクトボックスに表示したいArmatureのリストを作成する関数
def get_armature_list(self, context):
    return ((obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == "ARMATURE" and obj.data.users > 0)

# セレクトボックスに表示したいBoneのリストを作成する関数
def get_src_bone_list(self, context):
    armature_name = context.scene.ARMATURE_SWITCHER_armature_src
    if(not armature_name):
        return ()

    armature = bpy.data.objects[armature_name]
    return ((bone.name, bone.name, "") for bone in armature.data.bones if bone.name)

def get_dist_bone_list(self, context):
    armature_name = context.scene.ARMATURE_SWITCHER_armature_dist
    if(not armature_name):
        return ()

    armature = bpy.data.objects[armature_name]
    return ((bone.name, bone.name, "") for bone in armature.data.bones if bone.name)

# ボーン対応表データ
class BONE_MAP_DATA(bpy.types.PropertyGroup):
    src_bone: bpy.props.EnumProperty(name="Src Bone", items=get_src_bone_list)
    dist_bone: bpy.props.EnumProperty(name="Dist Bone", items=get_dist_bone_list)

    def toJSON(self):
        return json.dumps({
            "src_bone": self.src_bone,
            "dist_bone": self.dist_bone,
        })


def register():
    for module in modules:
        if hasattr(module, "register"):
            module.register()

    # ArmatureのSrc/DistのEnumPropertyを追加する
    bpy.types.Scene.ARMATURE_SWITCHER_armature_src = bpy.props.EnumProperty(name="Src Armature", items=get_armature_list)
    bpy.types.Scene.ARMATURE_SWITCHER_armature_dist = bpy.props.EnumProperty(name="Dist Armature", items=get_armature_list)

    # Boneの対応設定
    bpy.types.Scene.ARMATURE_SWITCHER_bonemap = bpy.props.CollectionProperty(type=BONE_MAP_DATA)


def unregister():
    for module in modules:
        if hasattr(module, "unregister"):
            module.unregister()
