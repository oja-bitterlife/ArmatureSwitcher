import bpy, addon_utils
import os, json


class ARMATUE_SWITCHER_OT_load_preset_base(bpy.types.Operator):
    def set_bone_mapping(self, context, file_src, file_dist):
        # アドオンのフォルダを取得する
        for mod in addon_utils.modules():
            if mod.bl_info.get("name") == "ArmatureSwitcher":
                asset_path = os.path.join(os.path.dirname(mod.__file__), "assets")
                break

        if not asset_path:
            return"cannot find asset dir"

        # jsonファイルの読み込み
        path_src = os.path.join(asset_path, file_src)
        path_dist = os.path.join(asset_path, file_dist)
        with open(path_src, "r", encoding="utf-8") as f_src:
            with open(path_dist, "r", encoding="utf-8") as f_dist:
                return self._set_bone_mapping(context, f_src, f_dist)
        

    def _set_bone_mapping(self, context, f_src, f_dist):
        # UIにセット
        try:
            src = json.load(f_src)
            dist = json.load(f_dist)

            src_added = []

            # 両方に同じキーがあれば置き換え対象
            context.scene.ARMATURE_SWITCHER_bonemap_list.clear()
            for key in src.keys():
                # すでに追加済みなら飛ばす
                if src[key] in src_added:
                    continue
                src_added.append(src[key])

                # 対応Boneが存在すればリストに追加
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


class ARMATUE_SWITCHER_OT_load_preset(ARMATUE_SWITCHER_OT_load_preset_base):
    bl_idname = "armature_switcher.load_preset"
    bl_label = "Load"

    def execute(self, context):
        error = "Fatal Error"

        for data in PRESET_DATA:
            if data[0] == context.scene.ARMATURE_SWITCHER_bonemap_preset:
                error = self.set_bone_mapping(context, data[1], data[2])
                break

        if error:
            self.report({"ERROR"}, error)
            return {'CANCELLED'}

        return{'FINISHED'}



# draw
# *****************************************************************************
def draw(cls, context, layout):
    box = layout.box()
    box.label(text="Load Mapping Preset")
    box.prop(context.scene, "ARMATURE_SWITCHER_bonemap_preset", text="")
    box.operator("armature_switcher.load_preset")

PRESET_DATA = (
    # ("Load Preset", "", "auto_rig_pro_vg.json"),
    ("VRoidStudio => AutoRigPro(Vertex Groups)", "vroid.json", "auto_rig_pro_vg.json"),
    ("VRoidStudio => AutoRigPro(Reference Bones)", "vroid.json", "auto_rig_pro_ref.json"),
    ("VRoidStudio => Rigify(Metarig)", "vroid.json", "rigify-meta.json"),
)

def get_bonemap_presets(self, context):
    return ((preset_data[0], preset_data[0], "") for preset_data in PRESET_DATA)


# register/unregister
# *****************************************************************************
classes = [
    ARMATUE_SWITCHER_OT_load_preset,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.ARMATURE_SWITCHER_bonemap_preset = bpy.props.EnumProperty(name="Bonemap Preset", items=get_bonemap_presets)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
