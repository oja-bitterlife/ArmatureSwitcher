import bpy
import math

def VRoid_to_ARP(context, dist_armature):
    # 追加Roll。主に指のボーンを-90度曲げる(Rは追従するのでLのみ)
    additional_roll = (
        ("shoulder_ref.l", -90),
        ("arm_ref.l", -90),
        ("forearm_ref.l", -90),
        ("hand_ref.l", -90),
        ("thumb1_ref.l", -90),
        ("thumb2_ref.l", -90),
        ("thumb3_ref.l", -90),
        ("index1_ref.l", -90),
        ("index2_ref.l", -90),
        ("index3_ref.l", -90),
        ("middle1_ref.l", -90),
        ("middle2_ref.l", -90),
        ("middle3_ref.l", -90),
        ("ring1_ref.l", -90),
        ("ring2_ref.l", -90),
        ("ring3_ref.l", -90),
        ("pinky1_ref.l", -90),
        ("pinky2_ref.l", -90),
        ("pinky3_ref.l", -90),
        ("thigh_ref.l", -90),
        ("leg_ref.l", -90),
        ("foot_ref.l", 180),
        ("toes_ref.l", 180),
    )
    for key, roll in additional_roll:
        dist_armature.data.edit_bones[key].roll += roll * math.pi / 180

    # 手のひらボーンの再配置
    move_base_value = (dist_armature.data.edit_bones["ring1_ref.l"].head- dist_armature.data.edit_bones["middle1_ref.l"].head)  # 中指、薬指間を基準長とする
    hand_bone = dist_armature.data.edit_bones["hand_ref.l"]  # 手のひらの付け根を元に配置する
    palms = ( # Bone名, z軸移動割合
        ("index1_base_ref.l", -0.6),
        ("middle1_base_ref.l", 0),
        ("ring1_base_ref.l", 0.6),
        ("pinky1_base_ref.l", 1.2),
    )
    for key, val in palms:
        # 手首基準で配置
        bone = dist_armature.data.edit_bones[key]
        bone.head = hand_bone.head + move_base_value * val
        bone.roll = hand_bone.roll

        # ちょっと短くする
        v = (bone.tail - bone.head)*0.8
        bone.head = bone.tail - v

    # 踵ボーンの再配置
    foot_bone = dist_armature.data.edit_bones["foot_ref.l"]  # 足の付け根を元に配置する
    heels = (  # Bone名, ｘ軸移動量
        ("foot_heel_ref.l", 0),
        ("foot_bank_01_ref.l", -0.03),
        ("foot_bank_02_ref.l", 0.015),
    )
    for key, val in heels:
        bone = dist_armature.data.edit_bones[key]
        bone.head.x = foot_bone.head.x + val
        bone.tail.x = bone.head.x
        bone.tail.y = foot_bone.head.y
        bone.head.y = foot_bone.head.y + 0.03  # ボーンの長さをひとまず固定で
        bone.head.z = bone.tail.z = 0
        bone.roll = 0


def VRoid_to_Rigify(context, dist_armature):
    pass