import bpy, mathutils, math

def PostProcess(context, src_pos, dist_armature):
    # 首ボーンは分割されている
    dist_armature.data.edit_bones["spine.005"].head = (dist_armature.data.edit_bones["spine.004"].head + dist_armature.data.edit_bones["spine.004"].tail) * 0.5
    dist_armature.data.edit_bones["spine.003"].tail = dist_armature.data.edit_bones["spine.004"].head  # くっつける必要がある

    # 追加Roll。主に指のボーンを-90度曲げる(Rは追従するのでLのみ)
    additional_roll = (
        ("shoulder.L", -90),
        ("thumb.01.L", 90),
        ("thumb.02.L", 90),
        ("thumb.03.L", 90),
        ("f_index.01.L", 90),
        ("f_index.02.L", 90),
        ("f_index.03.L", 90),
        ("f_middle.01.L", 90),
        ("f_middle.02.L", 90),
        ("f_middle.03.L", 90),
        ("f_ring.01.L", 90),
        ("f_ring.02.L", 90),
        ("f_ring.03.L", 90),
        ("f_pinky.01.L", 90),
        ("f_pinky.02.L", 90),
        ("f_pinky.03.L", 90),
        ("thigh.L", 180),
        ("shin.L", 180),
        ("toe.L", 180),
    )
    for key, roll in additional_roll:
        dist_armature.data.edit_bones[key].roll += roll * math.pi / 180
    for key, roll in additional_roll:
        key = key.replace(".L", ".R")
        dist_armature.data.edit_bones[key].roll += -roll * math.pi / 180

    # 手のひらボーンの再配置
    move_base_value = (dist_armature.data.edit_bones["f_ring.01.L"].head- dist_armature.data.edit_bones["f_middle.01.L"].head)  # 中指、薬指間を基準長とする
    palms_L = ( # Bone名, z軸移動割合
        ("palm.01.L", "f_index.01.L", -0.6),
        ("palm.02.L", "f_middle.01.L", 0),
        ("palm.03.L", "f_ring.01.L", 0.6),
        ("palm.04.L", "f_pinky.01.L", 1.2),
    )
    palms_R = ( # Bone名, z軸移動割合
        ("palm.01.R", "f_index.01.R", -0.6),
        ("palm.02.R", "f_middle.01.R", 0),
        ("palm.03.R", "f_ring.01.R", 0.6),
        ("palm.04.R", "f_pinky.01.R", 1.2),
    )
    def _func(palms, hand_name):
        hand_bone = dist_armature.data.edit_bones[hand_name]  # 手のひらの付け根を元に配置する
        for key, tail_bone, val in palms:
            # 手首基準で配置
            bone = dist_armature.data.edit_bones[key]
            bone.tail = dist_armature.data.edit_bones[tail_bone].head
            bone.head = hand_bone.head + move_base_value * val
            bone.roll = dist_armature.data.edit_bones[tail_bone].roll

            # ちょっと短くする
            v = (bone.tail - bone.head)*0.8
            bone.head = bone.tail - v

    _func(palms_L, "hand.L")
    _func(palms_R, "hand.R")

    # 腰ボーンの移動
    def _move_weist(weist_name, thigh_name):
        weist_bone = dist_armature.data.edit_bones[weist_name]
        thigh_bone = dist_armature.data.edit_bones[thigh_name]
        weist_move = thigh_bone.head - (weist_bone.head + weist_bone.tail) * 0.5
        weist_bone.head += weist_move
        weist_bone.tail += weist_move

    _move_weist("pelvis.L", "thigh.L")
    _move_weist("pelvis.R", "thigh.R")

    # VRMのheadが短いのでARP用に長くしておく
    dist_armature.data.edit_bones["spine.006"].tail += (dist_armature.data.edit_bones["spine.006"].tail - dist_armature.data.edit_bones["spine.006"].head)*2

    # headより上のボーンをまとめて移動
    # まずは現在位置の保存
    head_pos = dist_armature.data.edit_bones["spine.006"].tail
    face_pos = {}
    for bone in dist_armature.data.edit_bones:
        if bone.head.z > head_pos.z:
            face_pos[bone.name] = (mathutils.Vector(bone.head), mathutils.Vector(bone.tail))

    # 顔の位置を合わせる
    move_face_value = dist_armature.data.edit_bones["face"].head - dist_armature.data.edit_bones["spine.006"].head
    for bone_name in face_pos:
        dist_armature.data.edit_bones[bone_name].head = face_pos[bone_name][0] - move_face_value
        dist_armature.data.edit_bones[bone_name].tail = face_pos[bone_name][1] - move_face_value
