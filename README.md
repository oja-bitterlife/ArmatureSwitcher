# VRoidStudioで出力したVRM1.0形式モデルのボーンをBlenderのRig(AutoRigPro/Rigify)に置き換えるアドオン

- [VRoidStudio](https://vroid.com/studio)
- [AutoRigPro](https://blendermarket.com/products/auto-rig-pro)
- Rigify(※Blender標準アドオン)

VRM1.0形式のボーンをBlenderのArmatureで置き換えるアドオンです。置き換え先としてAutoRigProやRigifyが使えるので、いちいち自分でリグを組む必要が無くなります。

メインキャラにはちょっと使えないかなーってクオリティのVRoidStudioの生成モデルですが、モブを出すにはわりと便利なのではないかと思います。しかしVRoidStudioで作ったモデルを取り込もうとすると、リグやウェイトで結構手間がかかってしまいむしろBlenderのアドオンで素体を生成する方がトータルでは楽だったりします。

逆に言うとリグやウェイトがそのまま使えればだいぶ楽ができるので、Blenderでデファクトスタンダードと言えるAutoRigProやRigifyで置き換えられるようにしてみました。

ボーンとスキンウェイトの処理が分かれていますので、リグをカスタマイズした後でもボーンに大きな変更が無ければ(身長や手足胴の長さに大きな変更がない)、VRoidStudioで修正したモデルをBlenderでImportし直してスキンウェイトだけ再設定することができ、イテレーションしやすくなっています。

## AutoRigProでの使い方

AutoRigProはリファレンスボーンを修正した後Match to Rigボタンでリグを生成し、そのリグのDeformボーンでスキンウェイトを設定する方式です。


## Rigifyでの使い方

Rigifyはmetarig(リファレンスボーン)を修正した後Generate Rigボタンでリグを生成し、そのリグのDeformボーンでスキンウェイトを設定する方式です。

