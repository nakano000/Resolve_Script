from pathlib import Path
from rs_fusion.core import (
    pose,
)


class Importer:
    def __init__(
            self,
            comp,
            root_xf,
            other_data: dict,
            eye_data: dict,
            mouth_data: dict,
            front_data: dict,
            close_layer: str,
            a_layer: str,
            i_layer: str,
            u_layer: str,
            e_layer: str,
            o_layer: str,
            n_layer: str,
            parts_data: dict,
            canvas_width: int,
            canvas_height: int,
    ):
        self.comp = comp
        self.flow = comp.CurrentFrame.FlowView
        self.root_xf = root_xf

        self.other_data = other_data
        self.eye_data = eye_data
        self.mouth_data = mouth_data
        self.front_data = front_data
        self.parts_data = parts_data

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.close_layer = close_layer
        self.close_node = None
        self.a_layer = a_layer
        self.a_node = None
        self.i_layer = i_layer
        self.i_node = None
        self.u_layer = u_layer
        self.u_node = None
        self.e_layer = e_layer
        self.e_node = None
        self.o_layer = o_layer
        self.o_node = None
        self.n_layer = n_layer
        self.n_node = None

        self.X_OFFSET = 1
        self.Y_OFFSET = 4

        self.btn_size: float = 0.25

        self.blank_node = None

        self.tree_data = None
        self.json_data = None

    def set_pos(self, node, pos_x, pos_y):
        _x, _y = self.flow.GetPosTable(node).values()
        x = _x if pos_x is None else pos_x * self.X_OFFSET
        y = _y if pos_y is None else pos_y * self.Y_OFFSET
        self.flow.SetPos(node, x, y)

    def set_x(self, node, x):
        self.set_pos(node, x, None)

    def set_y(self, node, y):
        self.set_pos(node, None, y)

    @staticmethod
    def set_orange(node):
        node.TileColor = {
            '__flags': 256,
            'R': 0.92156862745098,
            'G': 0.431372549019608,
            'B': 0,
        }

    @staticmethod
    def uc_button(mg, node, page, layer_name, width):
        if node is None:
            lua = [
                'local mg = comp:FindTool("%s")' % mg.Name,
                'mg.Foreground = nil',
            ]
        else:
            lua = [
                'local mg = comp:FindTool("%s")' % mg.Name,
                'local node = comp:FindTool("%s")' % node.Name,
                'mg:ConnectInput("Foreground", node)',
                'mg.Center:HideViewControls()',
                'mg.Angle:HideViewControls()',
                'mg.Size:HideViewControls()',
            ]
        return {
            'LINKS_Name': layer_name,
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'ButtonControl',
            'INP_Integer': False,
            'BTNCS_Execute': '\n'.join(lua),
            'INP_External': False,
            'ICS_ControlPage': page,
            'ICD_Width': width,
        }

    def setup_base_node(self):
        pos_x = 0
        pos_y = 0

        # bg
        bg_x = pos_x - 2
        bg_y = pos_y - 1
        bg = self.add_tool('Background', bg_x, bg_y)
        bg.UseFrameFormatSettings = 0
        bg.Width = self.canvas_width
        bg.Height = self.canvas_height
        bg.TopLeftAlpha = 0
        bg.Depth = 1  # 8bit int

        # set domain
        node_x = pos_x - 2
        node = self.add_tool('SetDomain', node_x, pos_y)
        node.Mode = 'Set'
        node.Left = 0
        node.Bottom = 0
        node.Right = 0
        node.Top = 0
        node.ConnectInput('Input', bg)

        # node
        self.blank_node = node

    def add_tool(self, tool_name, pos_x, pos_y):
        node = self.comp.AddTool(tool_name, pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        return node

    def add_blank(self, pos_x, pos_y):
        node = self.add_tool('Fuse.Wireless', pos_x, pos_y)
        node.ConnectInput('Input', self.blank_node)
        return node

    def add_layer(self, pos_x, pos_y, layer_name):
        data = self.parts_data[layer_name]
        if data['path'] is None or data['path'] == '':
            return self.add_blank(pos_x, pos_y)

        ld = self.add_tool('Loader', pos_x, pos_y - 1)
        ld.Clip[1] = self.comp.ReverseMapPath(data['path'].replace('/', '\\'))
        ld.Loop[1] = 1
        # ld.Clip1.PNGFormat.PostMultiply = 0
        ld.GlobalIn = -1000
        ld.GlobalOut = -1000

        offset_x = data['offset'][0] + data['size'][0] - self.canvas_width / 2.0
        offset_y = - data['offset'][1] + self.canvas_height / 2.0

        node = self.add_tool('Transform', pos_x, pos_y)
        node.Width = data['size'][0]
        node.Height = data['size'][1]
        node.Center = (
            offset_x / data['size'][0],
            offset_y / data['size'][1],
        )
        ss = layer_name.split('.')
        node.SetAttrs({'TOOLS_Name': ss[-1]})
        node.ConnectInput('Input', ld)

        if layer_name == self.close_layer:
            self.close_node = node
        if layer_name == self.a_layer:
            self.a_node = node
        if layer_name == self.i_layer:
            self.i_node = node
        if layer_name == self.u_layer:
            self.u_node = node
        if layer_name == self.e_layer:
            self.e_node = node
        if layer_name == self.o_layer:
            self.o_node = node
        if layer_name == self.n_layer:
            self.n_node = node
        return node

    def add_node(self, pos_x, pos_y, data, name, uc):
        pos_x += 1
        xf = self.add_tool('Transform', pos_x, pos_y)
        xf.SetAttrs({'TOOLS_Name': name})
        wire = self.add_blank(pos_x, pos_y - 1)
        pos_x += 1

        pos_y -= 2

        # data sort
        a_data = {}
        b_data = {}
        c_data = {}
        for layer_name, layer in data.items():
            _name = layer_name.split('.')[-1]
            if _name.startswith('*'):
                b_data[layer_name] = layer
            else:
                if len(b_data) == 0:
                    a_data[layer_name] = layer
                else:
                    c_data[layer_name] = layer
        _data = a_data | b_data | c_data

        # main
        pre_node = wire
        a_mg = None
        page_name = 'ポーズ'
        name_list = []
        user_controls = {}
        user_controls2 = {}
        uc_list = []
        for i, (layer_name, layer) in enumerate(_data.items()):
            layer_name_en: str = layer['name_en']
            visible: bool = layer['visible']
            uc_name = 'N' + str(i).zfill(3) + '_' + layer_name_en

            # add loader
            if 'data' in layer:
                node, pos_x, _uc, _name_list = self.add_node(
                    pos_x, pos_y - 2, layer['data'], layer_name, {},
                )
                uc_list.append(_uc)
                name_list += _name_list
            else:
                node = self.add_layer(pos_x, pos_y, layer_name)

            # mg
            _name = layer_name.split('.')[-1]
            if _name.startswith('*'):
                if a_mg is None:
                    a_mg = self.comp.AddTool('Merge', pos_x * self.X_OFFSET, (pos_y + 1) * self.Y_OFFSET)
                    a_mg.SetAttrs({'TOOLS_Name': xf.Name + '_MG'})
                    a_mg.ConnectInput('Background', pre_node)
                    name_list.append(a_mg.Name)
                else:
                    self.set_x(a_mg, pos_x)
                if visible or a_mg.Foreground.GetConnectedOutput() is None:
                    a_mg.ConnectInput('Foreground', node)
                pre_node = a_mg
                if not _name.startswith('!'):
                    user_controls[uc_name + str(pos_x)] = self.uc_button(
                        a_mg, node, page_name, _name, self.btn_size
                    )
            else:
                mg = self.comp.AddTool('Merge', pos_x * self.X_OFFSET, (pos_y + 1) * self.Y_OFFSET)
                mg.SetAttrs({'TOOLS_Name': _name + '_MG'})
                name_list.append(mg.Name)
                mg.ConnectInput('Background', pre_node)
                if visible or _name.startswith('!'):
                    mg.ConnectInput('Foreground', node)
                pre_node = mg
                if not _name.startswith('!'):
                    user_controls2[uc_name + '_hide_' + str(pos_x)] = self.uc_button(
                        mg, None, page_name, _name + ' hide', 0.5
                    )
                    user_controls2[uc_name + '_show_' + str(pos_x)] = self.uc_button(
                        mg, node, page_name, _name + ' show', 0.5
                    )
            pos_x += 1

        #
        for k, v in user_controls2.items():
            user_controls[k] = v
        user_controls['Grp_' + xf.Name] = {
            'LINKS_Name': name.replace('!', '').replace('*', ''),
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'LabelControl',
            'LBLC_DropDownButton': True,
            'LBLC_NumInputs': len(user_controls),
            'INP_Default': 1,
            'INP_External': False,
            'INP_Passive': True,
            'ICS_ControlPage': page_name,
        }
        for _uc in uc_list:
            uc.update(_uc)
        uc.update(user_controls)
        pos_x -= 1
        xf.ConnectInput('Input', pre_node)
        self.set_x(xf, pos_x)

        return xf, pos_x, uc, name_list

    def set_mouth_scale(self):
        xf = self.comp.FindTool('MouthScale')
        center_list = []
        lst = []
        lst.append(self.comp.FindTool('A_Mrg'))
        lst.append(self.comp.FindTool('I_Mrg'))
        lst.append(self.comp.FindTool('U_Mrg'))
        lst.append(self.comp.FindTool('E_Mrg'))
        lst.append(self.comp.FindTool('O_Mrg'))
        lst.append(self.comp.FindTool('N_Mrg'))
        for node in lst:
            outp = node.FindMainOutput(1)
            img = outp.GetValue()
            dw = img.DataWindow
            if dw is not None:
                center_x = (dw[1] + dw[3]) / 2
                center_y = (dw[2] + dw[4]) / 2
                center_list.append((center_x, center_y))
        if len(center_list) == 0:
            xf.Pivot = (0.5, 0.5)
        else:
            center_x = sum(x for x, _ in center_list) / len(center_list)
            center_y = sum(y for _, y in center_list) / len(center_list)
            xf.Pivot = (center_x / self.canvas_width, center_y / self.canvas_height)

    def make(self):
        self.setup_base_node()
        name_list = []
        uc_dict = {}
        other_xf, pas_x, _uc, _name_list = self.add_node(
            0, 0, self.other_data, 'BaseGrp', {},
        )
        name_list += _name_list
        uc_dict.update(_uc)
        mouth_xf, pas_x, _uc, _name_list = self.add_node(
            pas_x + 1, 0, self.mouth_data, 'MouthGrp', _uc,
        )
        name_list += _name_list
        uc_dict.update(_uc)
        eye_xf, pas_x, _uc, _name_list = self.add_node(
            pas_x + 1, 0, self.eye_data, 'EyeGrp', _uc,
        )
        name_list += _name_list
        uc_dict.update(_uc)
        front_xf, pas_x, _uc, _name_list = self.add_node(
            pas_x + 1, 0, self.front_data, 'FrontGrp', _uc,
        )
        name_list += _name_list
        uc_dict.update(_uc)

        # link
        link_dct = {
            'BASE_LINK': other_xf,
            'MOUSE_LINK': mouth_xf,
            'EYE_LINK': eye_xf,
            'FRONT_LINK': front_xf,
            'BLANK_LINK': self.blank_node,
            'Closed': self.close_node,
            'A': self.a_node,
            'I': self.i_node,
            'U': self.u_node,
            'E': self.e_node,
            'O': self.o_node,
            'N': self.n_node,
        }
        for k, v in link_dct.items():
            _node = self.comp.FindTool(k)
            _node.ConnectInput('Input', v)

        # set mouth scale
        self.set_mouth_scale()

        # xf
        # uc = {'__flags': 2097152}  # 順番を保持するフラグ
        uc = pose.get_uc(None)
        for k, v in reversed(list(uc_dict.items())):
            if isinstance(v, dict):
                if 'INPID_InputControl' in v and v['INPID_InputControl'] == 'LabelControl':
                    if 'LBLC_NumInputs' in v and v['LBLC_NumInputs'] == 0:
                        continue
            uc[k] = v

        self.root_xf.UserControls = uc
        self.root_xf = self.root_xf.Refresh()
        self.set_orange(self.root_xf)

        self.root_xf.Comments = '\n'.join(reversed(name_list))
