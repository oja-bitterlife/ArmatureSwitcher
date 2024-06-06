import bpy, mathutils


# BoneMapのペアを登録する
class ARMATUE_SWITCHER_OT_bonemap_add(bpy.types.Operator):
    bl_idname = "armature_switcher.add_bonemap"
    bl_label = "Add Last"

    def execute(self, context):
        item = context.scene.ARMATURE_SWITCHER_bonemap_list.add()
        item.src_bone = context.scene.ARMATURE_SWITCHER_bone_src
        item.dist_bone = context.scene.ARMATURE_SWITCHER_bone_dist

        # 選択をいま追加したものに
        context.scene.ARMATURE_SWITCHER_bonemap_index = len(context.scene.ARMATURE_SWITCHER_bonemap_list) - 1

        return{'FINISHED'}

# BoneMapのペアを登録する
class ARMATUE_SWITCHER_OT_bonemap_insert(bpy.types.Operator):
    bl_idname = "armature_switcher.insert_bonemap"
    bl_label = "Insert"

    def execute(self, context):
        item = context.scene.ARMATURE_SWITCHER_bonemap_list.add()
        item.src_bone = context.scene.ARMATURE_SWITCHER_bone_src
        item.dist_bone = context.scene.ARMATURE_SWITCHER_bone_dist

        # itemの場所を移動する
        added_index = len(context.scene.ARMATURE_SWITCHER_bonemap_list) - 1
        insert_index = context.scene.ARMATURE_SWITCHER_bonemap_index
        context.scene.ARMATURE_SWITCHER_bonemap_list.move(added_index, insert_index)

        return{'FINISHED'}

# BoneMapのリストを一つ削除する
class ARMATUE_SWITCHER_OT_bonemap_remove(bpy.types.Operator):
    bl_idname = "armature_switcher.remove_bonemap"
    bl_label = ""

    id: bpy.props.IntProperty()

    def execute(self, context):
        context.scene.ARMATURE_SWITCHER_bonemap_list.remove(self.id)

        # 選択をいま削除した行に
        context.scene.ARMATURE_SWITCHER_bonemap_index = self.id

        return{'FINISHED'}


# draw
# *****************************************************************************
def draw(cls, context, layout):
    box = layout
    box.template_list("ARMATUE_SWITCHER_UL_bonemap_list", "", context.scene, "ARMATURE_SWITCHER_bonemap_list", context.scene, "ARMATURE_SWITCHER_bonemap_index")
    box = box.box()
    box.prop(context.scene, "ARMATURE_SWITCHER_bone_deform")
    row = box.row()
    row.prop(context.scene, "ARMATURE_SWITCHER_bone_src")
    row.prop(context.scene, "ARMATURE_SWITCHER_bone_dist")

    row = box.row()
    # Boneが設定されているか
    if context.scene.ARMATURE_SWITCHER_bone_src == "NoBone" or context.scene.ARMATURE_SWITCHER_bone_dist == "NoBone":
        row.enabled = False
    # SrcBoneがすでにリストに存在するかチェック
    src_bones = (bonemap.src_bone for bonemap in context.scene.ARMATURE_SWITCHER_bonemap_list)
    if context.scene.ARMATURE_SWITCHER_bone_src in src_bones:
        row.enabled = False
    row.operator("armature_switcher.add_bonemap")
    row.operator("armature_switcher.insert_bonemap")


# register/unregister
# *****************************************************************************
classes = [
    ARMATUE_SWITCHER_OT_bonemap_add,
    ARMATUE_SWITCHER_OT_bonemap_insert,
    ARMATUE_SWITCHER_OT_bonemap_remove,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
