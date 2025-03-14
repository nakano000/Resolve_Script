import json
from pathlib import Path

X_OFFSET = 1
Y_OFFSET = 4

selectedPath = fu.RequestFile(
    '',  # dir
    '',  # file
    {
        'FReqB_SeqGather': False,
        'FReqS_Filter': 'JSON File (*.json)|*.json',
        'FReqS_Title': 'Choose JSON',
    },
)
ver = fu.Version
comp = None
if selectedPath is not None:
    comp = fu.CurrentComp


def add_node(pos_x, pos_y, size_x, size_y, data, name):
    xf = comp.AddTool('Transform', pos_x * X_OFFSET, pos_y * Y_OFFSET)
    xf.SetAttrs({'TOOLS_Name': name})
    pre_node = comp.AddTool('Background', pos_x * X_OFFSET, (pos_y - 1) * Y_OFFSET)
    pre_node.UseFrameFormatSettings = 0
    pre_node.Width = size_x
    pre_node.Height = size_y
    pre_node.TopLeftAlpha = 0
    pre_node.Depth = 1
    pos_x += 1
    pos_y -= 2
    user_controls = {}
    cb_name = ''
    pub_combobox = None
    pub_combobox_uc = {
        '__flags': 2097152,
        'Value': {
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'ComboControl',
            'LINKS_Name': name,
            'INP_Integer': True,
            'INP_Default': 0,
            'ICS_ControlPage': 'User',
        },
    }
    pub_combobox_def = 0
    cb_cnt: int = 0
    connect_list = []
    for i, layer in enumerate(data):
        node = None
        layer_name: str = layer['name']
        layer_name_en: str = layer['name_en']
        visible: bool = layer['visible']
        layer_data = layer['data']
        mg = comp.AddTool('Merge', pos_x * X_OFFSET, (pos_y + 1) * Y_OFFSET)
        if type(layer_data) is list:
            node, pos_x = add_node(pos_x, pos_y, size_x, size_y, layer_data, layer_name)
        else:
            node = comp.AddTool('Loader', pos_x * X_OFFSET, pos_y * Y_OFFSET)
            node.Clip[1] = comp.ReverseMapPath(layer_data.replace('/', '\\'))
            node.Loop[1] = 1
            node.PostMultiplyByAlpha = 1 if ver < 10 else 0
            pos_x += 1
        mg.ConnectInput('Foreground', node)
        mg.ConnectInput('Background', pre_node)
        if layer_name.startswith('*'):
            if pub_combobox is None:
                pub_combobox = comp.AddTool('PublishNumber')
                pub_combobox_name = name if name != 'Root' else 'Select'
                pub_combobox.SetAttrs({'TOOLS_Name': 'PARAM%s_%s' % (str(i).zfill(3), pub_combobox_name)})
                cb_name = 'N' + str(i).zfill(3)
                user_controls[cb_name] = {
                    'LINKID_DataType': 'Number',
                    'INPID_InputControl': 'ComboControl',
                    'LINKS_Name': pub_combobox_name,
                    'INP_Integer': True,
                    'INP_Default': 0,
                    'ICS_ControlPage': 'User',
                }
            dct = user_controls[cb_name]
            pub_dct = pub_combobox_uc['Value']
            dct[cb_cnt + 1] = {'CCS_AddString': '%s' % layer_name}
            pub_dct[cb_cnt + 1] = {'CCS_AddString': '%s' % layer_name}
            if visible:
                dct['INP_Default'] = cb_cnt
                pub_dct['INP_Default'] = cb_cnt
                pub_combobox_def = cb_cnt
            exp = comp.AddTool('Expression')
            exp.NumberExpression = 'n1 == %d' % cb_cnt
            mg.ConnectInput('Blend', exp.NumberResult)
            exp.ConnectInput('n1', pub_combobox)
            exp.Refresh()
            cb_cnt += 1
        else:
            pub = comp.AddTool('PublishNumber')
            pub.SetAttrs({'TOOLS_Name': 'PARAM%s_%s' % (str(i).zfill(3), layer_name)})
            uc_name = 'N' + str(i).zfill(3) + '_' + layer_name_en
            pub_uc = {
                '__flags': 2097152,
                'Value': {
                    'LINKID_DataType': 'Number',
                    'INPID_InputControl': 'CheckboxControl',
                    'LINKS_Name': layer_name,
                    'INP_Integer': True,
                    'CBC_TriState': False,
                    'INP_Default': 1 if visible else 0,
                    'ICS_ControlPage': 'User',
                },
            }
            user_controls[uc_name] = {
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'CheckboxControl',
                'LINKS_Name': layer_name,
                'INP_Integer': True,
                'CBC_TriState': False,
                'INP_Default': 1 if visible else 0,
                'ICS_ControlPage': 'User',
            }
            mg.ConnectInput('Blend', pub)
            connect_list.append([uc_name, pub, 1 if visible else 0])
            pub.UserControls = pub_uc

        pre_node = mg
    user_controls['Grp_' + name] = {
        'LINKS_Name': name,
        'LINKID_DataType': 'Number',
        'INPID_InputControl': 'LabelControl',
        'LBLC_DropDownButton': True,
        'LBLC_NumInputs': len(user_controls),
        'INP_Default': 1,
        'ICS_ControlPage': 'User',
    }
    xf.ConnectInput('Input', pre_node)
    uc = {'__flags': 2097152}  # 順番を保持するフラグ
    for k, v in reversed(list(user_controls.items())):
        uc[k] = v
    xf.UserControls = uc
    xf = xf.Refresh()
    if pub_combobox is not None:
        xf.ConnectInput(cb_name, pub_combobox)
        pub_combobox.UserControls = pub_combobox_uc
        pub_combobox.Value = pub_combobox_def
        pub_combobox.Refresh()
    for c in connect_list:
        xf.ConnectInput(c[0], c[1])
        c[1].Value = c[2]
        c[1].Refresh()
    xf.TileColor = {
        '__flags': 256,
        'R': 0.92156862745098,
        'G': 0.431372549019608,
        'B': 0,
    }
    return xf, pos_x


def make(dct):
    add_node(0, 0, dct['x'], dct['y'], dct['data'], dct['name'])


if selectedPath is not None and comp is not None:
    comp.Lock()
    comp.StartUndo('Add some tools')
    json_path: Path = Path(comp.MapPath(comp.MapPath(selectedPath)))
    make(json.loads(json_path.read_text(encoding='utf-8')))
    comp.EndUndo(True)
    comp.Unlock()
    comp.AskUser('Done!', {})
    print('Done!')
