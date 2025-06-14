from psd_tools import PSDImage


def ungroup_and_save(input_path, output_path):
    # PSDファイルを開く
    psd = PSDImage.open(input_path)

    # rename
    def rename_layer(layer, s):
        if s == '':
            s = layer.name
        else:
            s = s + '::' + layer.name
        if layer.is_group():
            for child in layer:
                rename_layer(child, s)
        else:
            layer.name = s

    for layer in psd:
        if layer.is_group():
            rename_layer(layer, '')

    # グループレイヤーを解除
    for layer in reversed(list(psd.descendants())):
        if layer.is_group():
            continue
        layer.move_to_group(psd)

    # グループレイヤーを削除
    for layer in reversed(list(psd.descendants())):
        if layer.is_group():
            layer.delete_layer()

    # rev
    for layer in reversed(list(psd.descendants())):
        layer.move_to_group(psd)

    psd.save(output_path)


# 使用例
src_path = 'D:/work/春日部つむぎ立ち絵_公式_v2.0.psd'
dst_path = 'D:/work/春日部つむぎccc.psd'
ungroup_and_save(src_path, dst_path)
print(f"グループを解除して保存しました: {dst_path}")
