import bpy
from .BoneRemap import Remap, ListOP, SaveLoad
from .LoadPreset import LoadPreset

modules = [
    SaveLoad,
    Remap,
    ListOP,
    LoadPreset,
] 

# メインUi
# *****************************************************************************
class ARMATUE_SWITCHER_PT_armature_remap(bpy.types.Panel):
    bl_label = "Armature Remap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "ARMATUE_SWITCHER_PT_UI"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        # 設定用
        setting_box = self.layout.box()
        setting_box.label(text="Mapping Data")
 
        # Armature設定
        box = setting_box.box()
        box.label(text="Armature")
        box.prop(context.scene, "ARMATURE_SWITCHER_armature_src")
        box.prop(context.scene, "ARMATURE_SWITCHER_armature_dist")

        # Armatureが有効になるまで続きは無視
        setting_box = self.layout.box()
        if context.scene.ARMATURE_SWITCHER_armature_src == "NoArmature" or context.scene.ARMATURE_SWITCHER_armature_dist == "NoArmature":
            setting_box.enabled = False
        if context.scene.ARMATURE_SWITCHER_armature_src == context.scene.ARMATURE_SWITCHER_armature_dist:
            setting_box.enabled = False

        box = setting_box.box()
        box.label(text="Bone Mapping")

        # Save/Loadボタン
        SaveLoad.draw(self, context, box)

        # Bone設定
        ListOP.draw(self, context, box)

        # 設定実行
        Remap.draw(self, context, box)

        # プリセット読み込み
        LoadPreset.draw(self, context, setting_box)


# 設定用データ
# =================================================================================================
# セレクトボックスに表示したいArmatureのリストを作成する関数
def get_armature_list(self, context):
    return [("NoArmature", "(Select Armature)", "")] + [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == "ARMATURE" and obj.data.users > 0]

# セレクトボックスに表示したいBoneのリストを作成する関数
def get_src_bone_list(self, context):
    armature_name = context.scene.ARMATURE_SWITCHER_armature_src
    if armature_name == "NoArmature":  # アーマチュア未選択
        return [("NoBone", "(Select Armature)", "")]

    armature = bpy.data.objects[armature_name]
    deform_only = context.scene.ARMATURE_SWITCHER_bone_deform
    bones = list((bone.name, bone.name, "") for bone in armature.data.bones if bone.name and (not deform_only or bone.use_deform))
    if len(bones) > 0:
        return bones
    else:  # Boneが存在しない
        return [("NoBone", "(No Bone)", "")]

def get_dist_bone_list(self, context):
    armature_name = context.scene.ARMATURE_SWITCHER_armature_dist
    if armature_name == "NoArmature":  # アーマチュア未選択
        return [("NoBone", "(Select Armature)", "")]

    armature = bpy.data.objects[armature_name]
    deform_only = context.scene.ARMATURE_SWITCHER_bone_deform
    bones =  list((bone.name, bone.name, "") for bone in armature.data.bones if bone.name and (not deform_only or bone.use_deform))
    if len(bones) > 0:
        return bones
    else:  # Boneが存在しない
        return [("NoBone", "(No Bone)", "")]


# ボーン対応表データ
class BONE_MAP_DATA(bpy.types.PropertyGroup):
    src_bone: bpy.props.StringProperty(name="Src Bone")
    dist_bone: bpy.props.StringProperty(name="Dist Bone")

    def toJSON(self):
        return json.dumps({
            "src_bone": self.src_bone,
            "dist_bone": self.dist_bone,
        })


# AOVの状況プロパティ表示の仕方
class ARMATUE_SWITCHER_UL_bonemap_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # print(data, item, active_data, active_propname)
        layout.prop(item, "src_bone", text="", emboss=False)
        layout.label(icon="RIGHTARROW_THIN")
        layout.prop(item, "dist_bone", text="", emboss=False)
        layout.operator("armature_switcher.remove_bonemap", icon="PANEL_CLOSE").id = index


def register():
    for module in modules:
        if hasattr(module, "register"):
            module.register()

    # ArmatureのSrc/DistのEnumPropertyを追加する
    bpy.types.Scene.ARMATURE_SWITCHER_armature_src = bpy.props.EnumProperty(name="Src Armature", items=get_armature_list)
    bpy.types.Scene.ARMATURE_SWITCHER_armature_dist = bpy.props.EnumProperty(name="Dist Armature", items=get_armature_list)

    # Boneの対応設定
    bpy.types.Scene.ARMATURE_SWITCHER_bonemap_list = bpy.props.CollectionProperty(type=BONE_MAP_DATA)
    bpy.types.Scene.ARMATURE_SWITCHER_bonemap_index = bpy.props.IntProperty()  # template_list使うときはこれも必要
    bpy.types.Scene.ARMATURE_SWITCHER_bone_deform = bpy.props.BoolProperty(name="Deform Only")
    bpy.types.Scene.ARMATURE_SWITCHER_bone_src = bpy.props.EnumProperty(name="Src Bone", items=get_src_bone_list)
    bpy.types.Scene.ARMATURE_SWITCHER_bone_dist = bpy.props.EnumProperty(name="Dist Bone", items=get_dist_bone_list)


def unregister():
    for module in modules:
        if hasattr(module, "unregister"):
            module.unregister()
