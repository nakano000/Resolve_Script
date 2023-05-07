import json
import shutil
from pathlib import Path
from typing import List

from PIL import Image

from rs.core import (
    pipe as p,
)
from rs_fusion.core import pose
from rs_fusion.core import chara_sozai as cs_cmd

X_OFFSET = 1
Y_OFFSET = 4

OTHER = '他'
HAIR = '髪'
EYEBROW = '眉'
EYE = '目'
MOUTH = '口'
FACE = '顔'
BODY = '体'
ALL = '全'
BACK = '後'
FRONT = '前'

PARTS_LIST = [
    BACK,
    BODY,
    FACE,
    MOUTH,
    EYE,
    EYEBROW,
    HAIR,
    OTHER,
    FRONT,
]

ADD_NULL = [
    BACK,
    OTHER,
    FRONT,
    FACE,
]


def part2en(part: str) -> str:
    dct = {
        BACK: 'BACK',
        BODY: 'BODY',
        FACE: 'FACE',
        MOUTH: 'MOUTH',
        EYE: 'EYE',
        EYEBROW: 'EYEBROW',
        HAIR: 'HAIR',
        OTHER: 'OTHER',
        FRONT: 'FRONT',
    }
    if part not in dct.keys():
        return ''
    return dct[part]


def preprocess(src_dir: Path):
    src_data = {}
    height = None
    width = None

    for d in p.pipe(
            src_dir.iterdir(),
            p.filter(p.call.is_dir()),
    ):
        part_data = {}
        for f in p.pipe(
                d.iterdir(),
                p.filter(p.call.is_file()),
                p.filter(lambda x: x.name.lower().endswith('.png')),
                p.map(str),
                sorted,
                p.map(Path),
        ):
            f: Path
            if height is None:
                with Image.open(f) as im:
                    width, height = im.size

            key = f.name.split('.')[0][:2]
            if f.name.startswith(key + 'm') and f.name[len(key) + 1].isdigit():
                key = f.name[:len(key) + 2]
            if f.name.startswith(key + 'u') and f.name[len(key) + 1].isdigit():
                key = f.name[:len(key) + 2]
            if f.name[:3].isdigit():
                key = f.name[:3]
            if key not in part_data:
                part_data[key] = []
            part_data[key].append(f)
        if len(part_data) > 0:
            src_data[d.name] = part_data
    return src_data, width, height


def convert(width, height, src_data, dst_dir, print_fn):
    dst_data = {}
    for part in src_data:
        print_fn('処理中(変換,%s)' % part)
        part_data = {}
        for key in src_data[part]:
            key: str
            f0: Path = src_data[part][key][0]
            lst: List[Path] = src_data[part][key]
            # 保存先ディレクトリ
            dir_name = f0.parent.name
            dst_part_dir = dst_dir.joinpath(dir_name)
            dst_part_dir.mkdir(exist_ok=True)
            # 口と目は別処理
            if part in [MOUTH, EYE]:
                s: str = f0.stem
                # 特殊な指定は文字残すように
                suffix: str = ''
                if s.endswith('-15'):
                    suffix = '-15'
                if s.endswith('z'):
                    suffix = '+眉'
                if s.endswith('x'):
                    suffix = '+眉口'
                dst_name = key + suffix
                dst_file_list = []
                for i, f in enumerate(lst):
                    # コピー先決定
                    dst_file = dst_part_dir.joinpath(
                        # 最後だけ連番を付けない
                        dst_name + '.' + str(i).zfill(2) + '.' + part + '.png'
                    )
                    # copy
                    shutil.copy(f, dst_file)
                    dst_file_list.append(dst_file)
                part_data[dst_name] = dst_file_list
            # 他の処理
            else:
                # 名前決め
                dst_file_name = f0.stem + '.' + part + f0.suffix
                is_front = False
                if len(key) == 4 and key[2] == 'm':
                    dst_file_name = key[:2] + '.' + part + key[2:4] + f0.name[4:]
                    # 手前に表示したい
                    dst_part_dir = dst_dir.joinpath(FRONT)
                    dst_part_dir.mkdir(exist_ok=True)
                    is_front = True
                if len(key) == 4 and key[2] == 'u':
                    dst_file_name = key[:2] + '.' + part + key[2:4] + f0.name[4:]
                # コピー先決定
                dst_file = dst_part_dir.joinpath(dst_file_name)
                # copy
                shutil.copy(f0, dst_file)
                if is_front:
                    if FRONT not in dst_data.keys():
                        dst_data[FRONT] = {}
                    dst_data[FRONT][key] = [dst_file]
                else:
                    part_data[key] = [dst_file]
        if len(part_data) > 0:
            dst_data[part] = part_data
    print_fn('処理中(変換,透明素材)')
    space_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    space_file = dst_dir.joinpath('透明.png')
    space_image.save(space_file)
    for part in ADD_NULL:
        if part not in dst_data.keys():
            continue
        dst_data[part]['space'] = [space_file]
    return dst_data


class Importer:
    def __init__(self, comp, fusion_ver, width, height, dst_data, print_fn):
        self.comp = comp
        self.flow = comp.CurrentFrame.FlowView
        self.data = dst_data
        self.print = print_fn

        self.width = width
        self.height = height

        self.fusion_ver = fusion_ver

        self.X_OFFSET = 1
        self.Y_OFFSET = 4

        self.BACK_LIST = [
            BACK,
            BODY,
            FACE,
        ]
        self.ANIM_LIST = [
            MOUTH,
            EYE,
        ]
        self.FRONT_LIST = [
            EYEBROW,
            HAIR,
            OTHER,
            FRONT,
        ]

    @staticmethod
    def set_orange(node):
        node.TileColor = {
            '__flags': 256,
            'R': 0.92156862745098,
            'G': 0.431372549019608,
            'B': 0,
        }

    @staticmethod
    def set_pink(node):
        node.TileColor = {
            '__flags': 256,
            'R': 0.913725490196078,
            'G': 0.549019607843137,
            'B': 0.709803921568627,
        }

    @staticmethod
    def get_connect_lua(xf, key):
        return '''
comp:Execute([[
!Py3: from rs_fusion.core import chara_sozai
chara_sozai.connect(comp, "%s", "%s")
]])
''' % (xf.Name, key)

    @staticmethod
    def get_prev_next_lua(xf, is_next=False):
        return '''
comp:Execute([[
!Py3: from rs_fusion.core import chara_sozai
chara_sozai.prev_next(comp, "%s", %s)
]])
''' % (xf.Name, str(is_next))

    @staticmethod
    def get_blink_lua(xf):
        return '''
comp:Execute([[
!Py3: from rs_fusion.core import chara_sozai
chara_sozai.set_blink(comp, "%s")
]])
''' % xf.Name

    def add_set_dod(self, pos_x, pos_y, name, data_window):
        node = self.comp.AddTool('SetDomain', pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        node.SetAttrs({'TOOLS_Name': name})
        node.Mode = 'Set'
        node.Left = data_window[0] / self.width
        node.Bottom = data_window[1] / self.height
        node.Right = data_window[2] / self.width
        node.Top = data_window[3] / self.height
        if name is not None:
            node.SetAttrs({'TOOLS_Name': name})
        return node

    def add_bg(self, pos_x, pos_y):
        bg = self.comp.AddTool('Background', pos_x * self.X_OFFSET, (pos_y - 2) * self.Y_OFFSET)
        bg.UseFrameFormatSettings = 0
        bg.Width = self.width
        bg.Height = self.height
        bg.TopLeftAlpha = 0
        bg.Depth = 1
        node = self.add_set_dod(pos_x, pos_y - 1, None, [0, 0, 0, 0])
        node.ConnectInput('Input', bg)
        return node

    def add_ld(self, pos_x, pos_y, name, comment, path: str):
        node = self.comp.AddTool('Loader', pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        node.SetAttrs({'TOOLS_Name': name})
        node.Comments = comment
        node.Clip[1] = self.comp.ReverseMapPath(path.replace('/', '\\'))
        node.Loop[1] = 1
        node.PostMultiplyByAlpha = 1 if self.fusion_ver < 10 else 0
        node.GlobalIn = -1000
        node.GlobalOut = -1000
        return node

    @staticmethod
    def get_preview_name(part):
        return 'Preview_' + part2en(part)

    @staticmethod
    def get_prev_button_name(part):
        return 'Prev_Btn_' + part2en(part)

    @staticmethod
    def get_next_button_name(part):
        return 'Next_Btn_' + part2en(part)

    @staticmethod
    def uc_button(lua, page_name, links_name, width):
        return {
            'LINKS_Name': links_name,
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'ButtonControl',
            'INP_Integer': False,
            'BTNCS_Execute': lua,
            'INP_External': False,
            'ICS_ControlPage': page_name,
            'ICD_Width': width,
        }

    def get_uc_base(
            self,
            prev_lua,
            next_lua,
            part,
            page_name,
            num_inputs: int,
    ):
        label_name = 'Grp_' + part2en(part)
        preview_name = self.get_preview_name(part)
        prev_button_name = self.get_prev_button_name(part)
        next_button_name = self.get_next_button_name(part)
        return {
            label_name: {
                'LINKS_Name': part,
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'LabelControl',
                'LBLC_DropDownButton': True,
                'LBLC_NumInputs': num_inputs,
                'INP_Default': 1,
                'INP_External': False,
                'INP_Passive': True,
                'ICS_ControlPage': page_name,
            },
            prev_button_name: {
                'LINKS_Name': 'PREV',
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'ButtonControl',
                'INP_Integer': False,
                'BTNCS_Execute': prev_lua,
                'INP_External': False,
                'ICS_ControlPage': page_name,
                'ICD_Width': 0.4,
            },
            next_button_name: {
                'LINKS_Name': 'NEXT',
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'ButtonControl',
                'INP_Integer': False,
                'BTNCS_Execute': next_lua,
                'INP_External': False,
                'ICS_ControlPage': page_name,
                'ICD_Width': 0.4,
            },
            preview_name: {
                'LINKS_Name': '',
                'LINKID_DataType': 'Text',
                'INPID_InputControl': 'TextEditControl',
                'TEC_ReadOnly': True,
                'TEC_Lines': 1,
                'TEC_Wrap': False,
                'INP_External': False,
                'INP_Passive': True,
                'ICS_ControlPage': page_name,
                'ICD_Width': 0.2,
            },
        }

    @staticmethod
    def get_eye_uc(lua) -> dict:
        return {
            'Blink': {
                'LINKS_Name': 'Blink',
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'SliderControl',
                'INP_Integer': True,
                'INP_Default': 127,
                'INP_MinScale': 0,
                'INP_MaxScale': 500,
                'INP_External': False,
                'INP_Passive': True,
                'ICS_ControlPage': '目パチ',
            },
            'Other': {
                'LINKS_Name': 'Other',
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'SliderControl',
                'INP_Integer': True,
                'INP_Default': 1,
                'INP_MinScale': 0,
                'INP_MaxScale': 10,
                'INP_External': False,
                'INP_Passive': True,
                'ICS_ControlPage': '目パチ',
            },
            'Close': {
                'LINKS_Name': 'Close',
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'SliderControl',
                'INP_Integer': True,
                'INP_Default': 2,
                'INP_MinScale': 0,
                'INP_MaxScale': 10,
                'INP_External': False,
                'INP_Passive': True,
                'ICS_ControlPage': '目パチ',
            },
            'Apply': {
                'LINKS_Name': 'Apply',
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'ButtonControl',
                'BTNCS_Execute': lua,
                'ICD_Width': 0.5,
                'ICS_ControlPage': '目パチ',
            },
            'at00': {
                'LINKS_Name': 'ボタンを押さないと反映されません。',
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'LabelControl',
                'INP_External': False,
                'INP_Passive': True,
                'ICD_Width': 0.5,
                'ICS_ControlPage': '目パチ',
            },
        }

    def get_uc_list(self, mg_data, xf_data, eye_dx_list, ld_data):
        page_name = 'ポーズ'
        uc_list = []
        # pre json
        mg_name_data = {}
        for part in mg_data.keys():
            mg_name_data[part] = mg_data[part].Name
        xf_name_data = {}
        for part in xf_data.keys():
            xf_name_data[part] = p.pipe(
                xf_data[part],
                p.map(lambda x: x.Name),
                list,
            )
        eye_dx_name_list = p.pipe(
            eye_dx_list,
            p.map(lambda x: x.Name),
            list,
        )

        # main
        for part in mg_data.keys():
            _ld_data = ld_data[part]
            _xf_list = xf_data[part]

            # json
            data = {
                'mg': mg_name_data,
                'xf': xf_name_data,
                'eye_dx': eye_dx_name_list,
                'ld': {},
                'part': part,
                'offset': 10 / self.height,
                'preview': self.get_preview_name(part),
            }
            for key, lst in _ld_data.items():
                data['ld'][key] = p.pipe(
                    lst,
                    p.map(lambda x: x.Name),
                    list,
                )

            _xf_list[0].Comments = json.dumps(data, ensure_ascii=False, indent=2)

            # user control
            _uc = self.get_uc_base(
                self.get_prev_next_lua(_xf_list[0], is_next=False),
                self.get_prev_next_lua(_xf_list[0], is_next=True),
                part,
                page_name,
                len(_ld_data) + 3,  # +3 for prev, next, preview
            )
            for key, lst in _ld_data.items():
                base_name = part2en(part) + '_' + str(key).zfill(2)
                _uc[base_name + '_Button'] = self.uc_button(
                    self.get_connect_lua(_xf_list[0], key), page_name, key, 0.125
                )

            uc_list.append(_uc)

        return uc_list

    def add_node(self, pre_node, pos_x, pos_y, part):
        data = self.data[part]

        xf = self.comp.AddTool('Transform', pos_x * self.X_OFFSET, (pos_y - 2) * self.Y_OFFSET)
        xf.SetAttrs({'TOOLS_Name': part + '_Xf'})

        # make
        cnt = 0
        ld_data = {}
        for key, lst in data.items():
            base_name = part2en(part) + '_' + str(cnt).zfill(2)
            node = self.add_ld(
                pos_x,
                pos_y - 4,
                base_name + '_LD',
                key,
                str(lst[0]),
            )
            ld_data[key] = [node]
            cnt += 1
            pos_x += 1

        # Xf
        self.flow.SetPos(xf, (pos_x - 1) * self.X_OFFSET, (pos_y - 2) * self.Y_OFFSET)

        # mrg
        mg = self.comp.AddTool('Merge', (pos_x - 1) * self.X_OFFSET, (pos_y - 1) * self.Y_OFFSET)
        mg.SetAttrs({'TOOLS_Name': part + '_Mrg'})
        if part in [FACE]:
            mg.ApplyMode = 'Multiply'
        #
        mg.ConnectInput('Foreground', xf)
        mg.ConnectInput('Background', pre_node)
        pos_x += 1

        return mg, [xf], ld_data, pos_x

    def add_mouth_ctrl(self, size):
        ctrl = self.comp.AddTool('Calculation')
        ctrl.SetAttrs({'TOOLS_Name': 'Mouth_Ctrl'})
        ctrl.Operator = 3
        ctrl.SecondOperand = 0.7
        cal = self.comp.AddTool('Calculation')
        cal.Operator = 2
        cal.SecondOperand = size
        exp = self.comp.AddTool('Expression')
        exp.NumberExpression = 'int(n1)'
        exp.ShowNumber2 = 0
        exp.ShowNumber3 = 0
        exp.ShowNumber4 = 0
        exp.ShowNumber5 = 0
        exp.ShowNumber6 = 0
        exp.ShowNumber7 = 0
        exp.ShowNumber8 = 0
        exp.ShowNumber9 = 0
        exp.ShowPoint1 = 0
        exp.ShowPoint2 = 0
        exp.ShowPoint3 = 0
        exp.ShowPoint4 = 0
        exp.ShowPoint5 = 0
        exp.ShowPoint6 = 0
        exp.ShowPoint7 = 0
        exp.ShowPoint8 = 0
        exp.ShowPoint9 = 0

        cal.ConnectInput('FirstOperand', ctrl)
        exp.ConnectInput('n1', cal)
        return exp

    def add_anim_node(self, pre_node, pos_x, pos_y, part):
        data = self.data[part]

        max_size = p.pipe(
            data.values(),
            p.map(len),
            max,
        )
        if max_size == 1:
            return self.add_node(pre_node, pos_x, pos_y, part)

        pos_x_list = []
        pos_y_list = []
        xf_list = []
        dx_list = []

        # mouth ctrl
        mod = self.add_mouth_ctrl(max_size) if part == MOUTH else None

        # make xf dx
        for i in range(max_size):
            _pos_x = pos_x
            _pos_y = pos_y - (i * 3)
            _xf = self.comp.AddTool('Transform', pos_x * self.X_OFFSET, (_pos_y - 2) * self.Y_OFFSET)
            _xf.SetAttrs({'TOOLS_Name': part + '_' + str(i).zfill(2) + '_Xf'})
            _pos_x += 1
            if i != max_size - 1:
                _dx = self.comp.AddTool('Dissolve', pos_x * self.X_OFFSET, (_pos_y - 2) * self.Y_OFFSET)
                _dx.SetAttrs({'TOOLS_Name': part + '_' + str(i).zfill(2) + '_DX'})
                _dx.Mix = 0
                if part == MOUTH:
                    _offset = self.comp.AddTool('Calculation')
                    _offset.Operator = 1
                    _offset.SecondOperand = i
                    _offset.FirstOperand.ConnectTo(mod.NumberResult)
                    _dx.ConnectInput('Mix', _offset)
                    if i == 0:
                        self.set_orange(_dx)
                dx_list.append(_dx)
            pos_x_list.append(_pos_x)
            pos_y_list.append(_pos_y)
            xf_list.append(_xf)

        # loader
        ld_data = {}
        cnt = 0
        for key, lst in data.items():
            _ld_list = []
            for i in range(max_size):
                if i > len(lst) - 1:
                    continue
                # add loader
                base_name = part2en(part) + '_' + str(cnt).zfill(2) + '_' + str(i).zfill(2)
                node = self.add_ld(
                    pos_x_list[i],
                    pos_y_list[i] - 4,
                    base_name + '_LD',
                    key,
                    str(lst[i]),
                )
                _ld_list.append(node)
                pos_x_list[i] += 1

            ld_data[key] = _ld_list
            cnt += 1
        pos_x = max(pos_x_list)

        # setup Xf
        for i in range(max_size):
            _pos_y = pos_y_list[i]
            _xf = xf_list[i]
            self.flow.SetPos(_xf, (pos_x - 1) * self.X_OFFSET, (_pos_y - 2) * self.Y_OFFSET)

        # setup DX
        for i in range(max_size - 1):
            _pos_y = pos_y_list[i]
            _dx = dx_list[i]
            self.flow.SetPos(_dx, pos_x * self.X_OFFSET, (_pos_y - 2) * self.Y_OFFSET)
            if i == max_size - 2:
                _dx.ConnectInput('Foreground', xf_list[i + 1])
            else:
                _dx.ConnectInput('Foreground', dx_list[i + 1])
            _dx.ConnectInput('Background', xf_list[i])

        # Merge
        mg = self.comp.AddTool('Merge', pos_x * self.X_OFFSET, (pos_y - 1) * self.Y_OFFSET)
        mg.SetAttrs({'TOOLS_Name': part + '_Mrg'})
        mg.ConnectInput('Foreground', dx_list[0])
        mg.ConnectInput('Background', pre_node)
        pos_x += 1

        return mg, xf_list, dx_list, ld_data, pos_x

    def import_chara(self):
        max_size = {}
        for part in self.data.keys():
            max_size[part] = p.pipe(
                self.data[part].values(),
                p.map(len),
                max,
            )

        # bg
        bg = self.add_bg(0, 0)
        pos_x = 2
        pos_y = 0
        pre_node = bg

        # parts
        mg_data = {}
        xf_data = {}
        ld_data = {}
        eye_dx_list = []
        for part in self.BACK_LIST:
            if part not in self.data.keys():
                continue
            pre_node, _xf_list, _ld_data, pos_x = self.add_node(pre_node, pos_x, pos_y, part)
            mg_data[part] = pre_node
            ld_data[part] = _ld_data
            xf_data[part] = _xf_list
        pre_node.FlattenTransform = 1
        self.set_pink(pre_node)

        # anim parts
        for part in self.ANIM_LIST:
            if part not in self.data.keys():
                continue
            pre_node, _xf_list, _eye_dx_list, _ld_data, pos_x = self.add_anim_node(pre_node, pos_x, pos_y, part)
            mg_data[part] = pre_node
            ld_data[part] = _ld_data
            xf_data[part] = _xf_list
            if part == EYE:
                eye_dx_list = _eye_dx_list

        #  front parts
        f_pos_x = 2
        pos_y += 5
        f_pre_node = bg
        for part in self.FRONT_LIST:
            if part not in self.data.keys():
                continue
            f_pre_node, _xf_list, _ld_data, f_pos_x = self.add_node(f_pre_node, f_pos_x, pos_y, part)
            mg_data[part] = f_pre_node
            ld_data[part] = _ld_data
            xf_data[part] = _xf_list
        f_pre_node.FlattenTransform = 1
        self.set_pink(f_pre_node)

        # router
        x_pos = max(pos_x, f_pos_x)
        router = self.comp.AddTool('PipeRouter', x_pos * self.X_OFFSET, -1 * self.Y_OFFSET)

        # mrg
        mrg = self.comp.AddTool('Merge', pos_x * self.X_OFFSET, (pos_y - 1) * self.Y_OFFSET)

        # xf
        xf = self.comp.AddTool('Transform', pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        xf.SetAttrs({'TOOLS_Name': 'Root'})

        # uc
        uc = pose.get_uc(None, is_chara_sozai=True)
        uc_list = self.get_uc_list(mg_data, xf_data, eye_dx_list, ld_data)
        blink_lua = self.get_blink_lua(xf_data[EYE][0])
        uc_list = [self.get_eye_uc(blink_lua)] + uc_list
        for _uc in reversed(uc_list):
            for k, v in list(_uc.items()):
                uc[k] = v
        xf.UserControls = uc
        xf = xf.Refresh()
        self.set_orange(xf)

        # comment
        xf_name_list = []
        for lst in xf_data.values():
            xf_name_list.append(lst[0].Name)
        xf.SetInput('Comments', '\n'.join(xf_name_list))

        # connect
        router.ConnectInput('Input', pre_node)
        mrg.ConnectInput('Background', router)
        mrg.ConnectInput('Foreground', f_pre_node)
        xf.ConnectInput('Input', mrg)

        for part, lst in xf_data.items():
            _xf = lst[0]
            keys = list(ld_data[part].keys())
            key = keys[0]
            if part in [FRONT, BACK]:
                key = keys[-1]
            cs_cmd.connect(self.comp, _xf.Name, key)

        # blink
        cs_cmd.set_blink(self.comp, xf_data[EYE][0].Name)
