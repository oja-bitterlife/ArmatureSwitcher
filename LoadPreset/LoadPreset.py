import os
import bpy
import addon_utils
import json


class ARMATUE_SWITCHER_OT_load_preset(bpy.types.Operator):
    bl_idname = "armature_switcher.load_preset"
    bl_label = "VG: VRoidStudio => AutoRigPro"

    def execute(self, context):
        # アドオンのフォルダを取得する
        for mod in addon_utils.modules():
            if mod.bl_info.get("name") == "ArmatureSwitcher":
                asset_path = os.path.join(os.path.dirname(mod.__file__), "assets")
                break

        # ファイルアクセス失敗
        if not asset_path:
            self.report({"ERROR"}, "cannot open asset dir")
            return {'CANCELLED'}
        
        # jsonファイルの読み込み
        path_vroid = os.path.join(asset_path, "vroid.json")
        path_arp = os.path.join(asset_path, "auto_rig_pro_vg.json")
        with open(path_vroid, "r", encoding="utf-8") as f_vroid:
            with open(path_arp, "r", encoding="utf-8") as f_arp:
                # UIにセット
                try:
                    error = set_bone_mapping(context, json.load(f_vroid), json.load(f_arp))
                except Exception as e:
                    error = "cannot read json file:" + str(e)

                # エラー終了
                if error:
                    self.report({"ERROR"}, error)
                    return {'CANCELLED'}

        return{'FINISHED'}

def set_bone_mapping(context, src, dist):
    try:
        # 両方に同じキーがあれば置き換え対象
        context.scene.ARMATURE_SWITCHER_bonemap_list.clear()
        for key in src.keys():
            if key in dist.keys():
                # 対応Boneが無いときにnullにしてあるので飛ばす
                if not src[key] or not dist[key]:
                    continue

                # bonemapリストに追加する
                item = context.scene.ARMATURE_SWITCHER_bonemap_list.add()
                item.src_bone = src[key]
                item.dist_bone = dist[key]

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
    row = box.row()
    row.operator("armature_switcher.load_preset")


# register/unregister
# *****************************************************************************
classes = [
    ARMATUE_SWITCHER_OT_load_preset,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
