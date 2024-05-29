import bpy


class ARMATUE_SWITCHER_OT_remap_vw(bpy.types.Operator):
    bl_idname = "armature_switcher.remap_vw"
    bl_label = "Remap Vertex Weights & Armature"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        # 頂点ウェイトのリマップ
        for obj in selected_objects:
            if obj.type == 'MESH':
                # 高速化用に頂点グループの辞書を作成しておく
                vg_dict = {vg.name: vg for vg in obj.vertex_groups}

                vg_unremap = {}

                # 頂点グループが存在しなければRename
                for bonemap in context.scene.ARMATURE_SWITCHER_bonemap_list:
                    # 対象の頂点グループ
                    if bonemap.src_bone in vg_dict:
                        if bonemap.dist_bone not in vg_dict:
                            vg = vg_dict[bonemap.src_bone]   # 変更元
                            vg.name = bonemap.dist_bone  # Rename
                            vg_dict[bonemap.dist_bone] = vg
                        else:
                            vg_unremap[bonemap.src_bone] = bonemap.dist_bone

                # 未処理グループの頂点グループ転送
                for v in obj.data.vertices:
                    for g in v.groups:
                        # リネームしていない頂点グループだった
                        if obj.vertex_groups[g.group].name in vg_unremap:
                            vg_src_name = obj.vertex_groups[g.group].name
                            vg_dist_name = vg_unremap[vg_src_name]
                            vg_dist = vg_dict[vg_dist_name]
                            vg_dist.add([v.index], g.weight, 'REPLACE')

                # 未処理グループの削除
                for unremap in vg_unremap:
                    obj.vertex_groups.remove(vg_dict[unremap])

        # Armatureのリマップ
        for obj in selected_objects:
            # obj内のモディファイアを取得
            for mod in obj.modifiers:
                # 変更対象のアーマチュアだったら変更
                if mod.type == "ARMATURE" and mod.object.name == context.scene.ARMATURE_SWITCHER_armature_src:
                    mod.object = bpy.data.objects[context.scene.ARMATURE_SWITCHER_armature_dist]

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
