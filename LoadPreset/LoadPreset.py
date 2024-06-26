import bpy, addon_utils
import os, json


def LoadPreset(context):
    for data in PRESET_DATA:
        if data[0] == context.scene.ARMATURE_SWITCHER_bonemap_preset:
            # アドオンのフォルダを取得する
            for mod in addon_utils.modules():
                if mod.bl_info.get("name") == "ArmatureSwitcher":
                    asset_path = os.path.join(os.path.dirname(mod.__file__), "assets")
                    break

            if not asset_path:
                return"cannot find asset dir"

            # jsonファイルの読み込み
            path_src = os.path.join(asset_path, data[1])
            path_dist = os.path.join(asset_path, data[2])
            with open(path_src, "r", encoding="utf-8") as f_src:
                with open(path_dist, "r", encoding="utf-8") as f_dist:
                    return _set_bone_mapping(context, f_src, f_dist)

    # ファイルをオープンできなかった
    return "File Open Error"

def _set_bone_mapping(context, f_src, f_dist):
    # UIにセット
    try:
        src = json.load(f_src)
        dist = json.load(f_dist)

        src_bones = src["bones"]
        dist_bones = dist["bones"]
        dist_bone_keys = dist_bones.keys()  # 何度も実行しないようキャッシュ

        # 両方に同じキーがあれば置き換え対象
        context.scene.ARMATURE_SWITCHER_bonemap_list.clear()
        for key in src_bones.keys():
            # nullは無視
            if not src_bones[key]:
                continue

            # 対応Boneがなければ無視(nullも無視)
            if key not in dist_bone_keys or not dist_bones[key]:
                continue

            # bonemapリストに追加する
            item = context.scene.ARMATURE_SWITCHER_bonemap_list.add()
            item.src_bone = src_bones[key]
            item.dist_bone = dist_bones[key]

        # post_processの設定
        if "post_process" in dist:
            context.scene.ARMATURE_SWITCHER_match_postprocess = dist["post_process"]
        else:
            context.scene.ARMATURE_SWITCHER_match_postprocess = "None"

    except Exception as e:
        # 失敗
        context.scene.ARMATURE_SWITCHER_bonemap_list.clear()
        return "cannot read json file:" + str(e)

    return None



# draw
# *****************************************************************************
def draw(cls, context, layout):
    box = layout.box()
    box.label(text="Load Mapping Preset")
    box.prop(context.scene, "ARMATURE_SWITCHER_bonemap_preset", text="")
    

PRESET_DATA = (
    # ID, src_json, dist_json
    ("Select Preset", None, None),
    ("VRoidStudio => AutoRigPro(Vertex Groups)", "vroid.json", "auto_rig_pro_vg.json"),
    ("VRoidStudio => AutoRigPro(Reference Bones)", "vroid.json", "auto_rig_pro_ref.json"),
    ("VRoidStudio => Rigify(Vertex Groups)", "vroid.json", "rigify_vg.json"),
    ("VRoidStudio => Rigify(Metarig)", "vroid.json", "rigify_meta.json"),
)

def get_bonemap_presets(self, context):
    return ((preset_data[0], preset_data[0], "") for preset_data in PRESET_DATA)

def onchange_bonemap_presets(self, context):
    # 一番上以外が選択されていたらLoadして一番上の選択肢に戻す
    if context.scene.ARMATURE_SWITCHER_bonemap_preset != PRESET_DATA[0][0]:
        error = LoadPreset(context)
        context.scene.ARMATURE_SWITCHER_bonemap_preset = PRESET_DATA[0][0]

        if error:
            print(error)


# register/unregister
# *****************************************************************************
classes = [
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.ARMATURE_SWITCHER_bonemap_preset = bpy.props.EnumProperty(name="Bonemap Preset", items=get_bonemap_presets, update=onchange_bonemap_presets)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
