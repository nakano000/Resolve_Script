import json
from pathlib import Path

# import BlackmagicFusion as bmd

X_OFFSET = 1
Y_OFFSET = 4

# fu = bmd.scriptapp('Fusion')

selectedPath = fu.RequestFile(
    '',  # dir
    '',  # file
    {
        'FReqB_SeqGather': False,
        'FReqS_Filter': 'JSON File (*.json)|*.json',
        'FReqS_Title': 'Choose JSON',
    },
)
org_comp = None
comp = None
if selectedPath is not None:
    org_comp = fu.CurrentComp
    comp = fu.NewComp()


def add_node(pos_x, pos_y, size_x, size_y, data, name):
    xf = comp.AddTool('Transform', pos_x * X_OFFSET, pos_y * Y_OFFSET)
    xf.SetAttrs({'TOOLS_Name': name})
    pre_node = comp.AddTool('Background', pos_x * X_OFFSET, (pos_y - 1) * Y_OFFSET)
    pre_node.Width = size_x
    pre_node.Height = size_y
    pre_node.TopLeftAlpha = 0
    pos_x += 1
    pos_y -= 2
    user_controls = {}
    cb_name = ''
    cb_cnt: int = 0
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
            node.PostMultiplyByAlpha = 1
            # node.PostMultiplyByAlpha = 0
            pos_x += 1
        mg.ConnectInput('Foreground', node)
        mg.ConnectInput('Background', pre_node)
        if layer_name.startswith('*'):
            if cb_name == '':
                cb_name = 'N' + str(i).zfill(3)
                user_controls[cb_name] = {
                    'LINKID_DataType': 'Number',
                    'INPID_InputControl': 'ComboControl',
                    'LINKS_Name': 'Select',
                    'INP_Integer': True,
                    'INP_Default': 0,
                    'ICS_ControlPage': 'User',
                }
            dct = user_controls[cb_name]
            dct[cb_cnt + 1] = {'CCS_AddString': '%s' % layer_name}
            if visible:
                dct['INP_Default'] = cb_cnt
            mg.Blend.SetExpression('iif(%s.%s == %d, 1, 0)' % (xf.Name, cb_name, cb_cnt))
            cb_cnt += 1
        else:
            uc_name = 'N' + str(i).zfill(3) + '_' + layer_name_en
            user_controls[uc_name] = {
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'CheckboxControl',
                'LINKS_Name': layer_name,
                'INP_Integer': True,
                'CBC_TriState': False,
                'INP_Default': 1 if visible else 0,
                'ICS_ControlPage': 'User',
                # 'ICS_ControlPage': 'Controls',
            }
            mg.Blend.SetExpression('%s.%s' % (xf.Name, uc_name))

        pre_node = mg
    user_controls['Grp_' + name] = {
        'LINKS_Name': name,
        'LINKID_DataType': 'Number',
        'INPID_InputControl': 'LabelControl',
        'LBLC_DropDownButton': True,
        'LBLC_NumInputs': len(user_controls),
        # 'LBLC_NestLevel': nest_level,
        'INP_Default': 1,
        'ICS_ControlPage': 'User',
    }
    xf.ConnectInput('Input', pre_node)
    uc = {}
    for k, v in reversed(list(user_controls.items())):
        uc[k] = v
    xf.UserControls = uc
    return xf, pos_x


def make(dct):
    add_node(0, 0, dct['x'], dct['y'], dct['data'], dct['name'])


if selectedPath is not None:
    comp.Lock()
    comp.StartUndo('Add some tools')
    json_path: Path = Path(comp.MapPath(comp.MapPath(selectedPath)))
    make(json.loads(json_path.read_text(encoding='utf-8')))
    # UserCtrlの順番が、勝手に入れ変わるのでコピペしせ確定させる。
    flow = comp.CurrentFrame.FlowView
    tool_list = comp.GetToolList()
    for key in tool_list:
        flow.Select(tool_list[key])
    comp.Copy()
    comp.EndUndo(True)
    # comp.Undo()
    comp.Close()
    comp.Unlock()
    org_comp.Paste()
    org_comp.AskUser('Done!', {})
    print('Done!')
