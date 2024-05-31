import bpy, json
import traceback


class ARMATUE_SWITCHER_OT_bonemap_save(bpy.types.Operator):
    bl_idname = "armature_switcher.bonemap_save"
    bl_label = "Save JSON"

    # ファイル選択ダイアログ
    filepath: bpy.props.StringProperty()
    filter_glob: bpy.props.StringProperty(
        default="*.json",
    )
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    # execute
    def execute(self, context):
        # かならず.jsonに
        if not self.filepath.lower().endswith(".json"):
            self.filepath += ".json"

        # JSON保存データ構築
        data = {
            "bonemap": {}
        }
        for bonemap in context.scene.ARMATURE_SWITCHER_bonemap_list:
            data["bonemap"][bonemap.src_bone] = bonemap.dist_bone

        # ファイル保存
        try:
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except:
            print(traceback.format_exc())
            self.report({'ERROR'}, traceback.format_exc())
            return {'CANCELLED'}

        return {'FINISHED'}

class ARMATUE_SWITCHER_OT_bonemap_load(bpy.types.Operator):
    bl_idname = "armature_switcher.bonemap_load"
    bl_label = "Load JSON"

    # ファイル選択ダイアログ
    filepath: bpy.props.StringProperty()
    filter_glob: bpy.props.StringProperty(
        default="*.json",
    )
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    # execute
    def execute(self, context):
        # JSON読み込み
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
        except:
            print(traceback.format_exc())
            self.report({'ERROR'}, traceback.format_exc())
            return {'CANCELLED'}

        # データの設定
        context.scene.ARMATURE_SWITCHER_bonemap_list.clear()
        for src_bone in data["bonemap"]:
            item = context.scene.ARMATURE_SWITCHER_bonemap_list.add()
            item.src_bone = src_bone
            item.dist_bone = data["bonemap"][src_bone]

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
