import bpy


class ARMATUE_SWITCHER_OT_remap_vw(bpy.types.Operator):
    bl_idname = "armature_switcher.remap_vw"
    bl_label = "Remap Vertex Weights"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            if obj.type == 'MESH':
                # 高速化用に頂点グループの辞書を作成しておく
                vw_dict = {vg.name: vg for vg in obj.vertex_groups}
                vw_keys = vw_dict.keys()

                # remap対象ボーンを変換していく
                for bonemap in context.scene.ARMATURE_SWITCHER_bonemap_list:
                    # オブジェクトが持つ頂点グループに一致するものがあるか
                    if bonemap.src_bone in vw_keys:
                        # 一致する頂点グループの名前を変更する
                        vw_dict[bonemap.src_bone].name = bonemap.dist_bone

        return{'FINISHED'}

class ARMATUE_SWITCHER_OT_match_bones(bpy.types.Operator):
    bl_idname = "armature_switcher.match_bones"
    bl_label = "Match Bones"

    def execute(self, context):
        return{'FINISHED'}


# draw
# *****************************************************************************
def draw(cls, context, layout):
    # 選択中のObjectを取得
    selected_objects = bpy.context.selected_objects

    # オブジェクトが選択されていればVW更新ボタンを有効に
    l = layout.row()
    l.operator("armature_switcher.remap_vw")
    l.enabled = len(selected_objects) > 0

    # ボーン変換ボタン
    layout.operator("armature_switcher.match_bones")


# register/unregister
# *****************************************************************************
classes = [
    ARMATUE_SWITCHER_OT_remap_vw,
    ARMATUE_SWITCHER_OT_match_bones,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
