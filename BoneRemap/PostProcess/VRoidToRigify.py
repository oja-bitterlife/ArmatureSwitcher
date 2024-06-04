import bpy

def PostProcess(context, src_pos, dist_armature):
    # 首ボーンは分割されている
    dist_armature.data.edit_bones["spine.005"].head = (dist_armature.data.edit_bones["spine.004"].head + dist_armature.data.edit_bones["spine.004"].tail) * 0.5

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
            bone.roll = hand_bone.roll

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
    # dist_armature.data.edit_bones["spine.006"].tail += (dist_armature.data.edit_bones["spine.006"].tail - dist_armature.data.edit_bones["spine.006"].head)*2

