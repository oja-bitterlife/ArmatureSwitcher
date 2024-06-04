import bpy, mathutils
import math

class ARMATUE_SWITCHER_OT_remap_vw(bpy.types.Operator):
    bl_idname = "armature_switcher.remap_vw"
    bl_label = "Remap Vertex Groups & Armature"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        # 頂点ウェイトのリマップ
        for obj in selected_objects:
            if obj.type == 'MESH':
                # 高速化用に頂点グループの辞書を作成しておく
                vg_dict = {vg.name: vg for vg in obj.vertex_groups}

                # 頂点グループが存在しなければRename
                vg_unremap = {}  # Rename処理しなかった頂点グループ記録用
                for bonemap in context.scene.ARMATURE_SWITCHER_bonemap_list:
                    # 対象の頂点グループチェック
                    if bonemap.src_bone in vg_dict:
                        # 存在しなければRenameできる
                        if bonemap.dist_bone not in vg_dict:
                            vg = vg_dict[bonemap.src_bone]   # 変更元
                            vg.name = bonemap.dist_bone  # Rename

                            # 辞書も更新する
                            vg_dict[bonemap.dist_bone] = vg
                        else:
                            # すでに存在する頂点グループはRenameで対応できないので記録して後で処理
                            vg_unremap[bonemap.src_bone] = bonemap.dist_bone

                # 未処理グループの頂点グループ転送
                for v in obj.data.vertices:
                    for g in v.groups:
                        # リネームしていない頂点グループだった
                        if obj.vertex_groups[g.group].name in vg_unremap:
                            # 変更先の頂点グループに追加する
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
        active_backup = context.view_layer.objects.active

        src_armature = bpy.data.objects[context.scene.ARMATURE_SWITCHER_armature_src]
        dist_armature = bpy.data.objects[context.scene.ARMATURE_SWITCHER_armature_dist]

        # edit_boneはEDITモードでかつActiveの時しか使えない
        context.view_layer.objects.active = src_armature
        bpy.ops.object.mode_set(mode='EDIT')

        # 座標を回収
        src_pos = {}
        for bonemap in context.scene.ARMATURE_SWITCHER_bonemap_list:
            src_bone = src_armature.data.edit_bones[bonemap.src_bone]
            head = mathutils.Vector(src_bone.head)
            tail = mathutils.Vector(src_bone.tail)
            roll = src_bone.roll

            src_pos[bonemap.src_bone] = (head, tail, roll)

        # 操作対象切り替え
        bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = dist_armature
        bpy.ops.object.mode_set(mode='EDIT')

        # Distボーンに適用する
        for bonemap in context.scene.ARMATURE_SWITCHER_bonemap_list:
            dist_bone = dist_armature.data.edit_bones[bonemap.dist_bone]

            dist_bone.head = src_pos[bonemap.src_bone][0]
            dist_bone.tail = src_pos[bonemap.src_bone][1]
            dist_bone.roll = src_pos[bonemap.src_bone][2]

        # モードとActiveオブジェクトを戻しておく
        bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = active_backup

        return{'FINISHED'}


# draw
# *****************************************************************************
def draw(cls, context, layout):
    # 選択中のMESHObjectを取得
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    # オブジェクトが選択されていればVW更新ボタンを有効に
    row = layout.row()
    row.operator("armature_switcher.remap_vw")
    row.enabled = len(selected_objects) > 0

    # ボーン変換ボタン
    row = layout.box()
    row.prop(context.scene, "ARMATURE_SWITCHER_match_postprocess")
    row.operator("armature_switcher.match_bones")

# register/unregister
# *****************************************************************************
classes = [
    ARMATUE_SWITCHER_OT_remap_vw,
    ARMATUE_SWITCHER_OT_match_bones,
]

MATCH_POSTPROCESS = (
    ("None", "None", ""),
    ("VRoid to ARP", "VRoid to ARP", ""),
    ("VRoid to Rigify", "VRoid to Rigify", ""),
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.ARMATURE_SWITCHER_match_postprocess = bpy.props.EnumProperty(name="PostProcess", items=MATCH_POSTPROCESS)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
