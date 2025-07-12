import json
from pathlib import Path

from rs.core import config
from rs_fusion.tool.make_macro import macro

DATA_PATH = config.DATA_PATH.joinpath('app', 'Psd2Tatie')
MAIN_OUTPUT_PATH = DATA_PATH.joinpath('main_output.json')
BEFORE_INPUT_PATH = DATA_PATH.joinpath('before_input.json')
AFTER_INPUT_PATH = DATA_PATH.joinpath('after_input.json')


class MacroBuilder:
    def __init__(self, comp):
        self.comp = comp
        self.flow = comp.CurrentFrame.FlowView

    def read_node(self) -> list[dict]:
        # main
        tool = self.comp.FindTool('Root')

        input_list = []
        # page
        page_names: dict = tool.GetControlPageNames()
        inp_dict: dict = tool.GetInputList()
        page_name = 'ポーズ'
        for inp in inp_dict.values():
            attrs = inp.GetAttrs()
            name = inp.Name
            if 'INPS_IC_Name' in attrs:
                name = attrs['INPS_IC_Name']
            control_group = 0
            if 'INPI_IC_ControlGroup' in attrs:
                control_group = int(attrs['INPI_IC_ControlGroup'])
            if attrs['INPI_IC_ControlPage'] not in page_names.keys():
                continue
            if page_name != page_names[attrs['INPI_IC_ControlPage']]:
                continue

            input_list.append({
                'id': inp.ID,
                'node': tool.Name,
                'name': name,
                'control_group': control_group,
                'option01': '',
                'option02': '',
                'option03': '',
            })
        return input_list

    def build(self, macro_name: str, macro_path: Path):
        main_output_list = json.loads(MAIN_OUTPUT_PATH.read_text(encoding='utf-8'))
        before_input_list = json.loads(BEFORE_INPUT_PATH.read_text(encoding='utf-8'))
        after_input_list = json.loads(AFTER_INPUT_PATH.read_text(encoding='utf-8'))

        input_list = before_input_list + self.read_node() + after_input_list

        # output
        output_list = []
        for dct in main_output_list:
            output_list.append({
                'id': dct['id'],
                'node': dct['node'],
            })

        # main input
        main_in_list = []

        # control groupの数字が被らないようにNode毎にoffsetを設定
        cg_offset_dict = {}
        for dct in input_list:
            if dct['node'] in cg_offset_dict:
                if cg_offset_dict[dct['node']] >= dct['control_group']:
                    continue
            cg_offset_dict[dct['node']] = dct['control_group']
        _pre_max = 0
        for key in cg_offset_dict.keys():
            _tmp = cg_offset_dict[key]
            cg_offset_dict[key] = _pre_max
            _pre_max += _tmp

        # get input
        in_list = []
        for dct in input_list:
            dct: dict
            name = None
            value = None
            control_group = None

            tool = self.comp.FindTool(dct['node'])
            if tool is not None:
                _v = tool.GetInput(dct['id'], self.comp.CurrentTime)
                if type(_v) == float:
                    value = _v
            if dct['id'] != dct['name']:
                name = dct['name']
            if dct['control_group'] != 0:
                control_group = dct['control_group'] + cg_offset_dict[dct['node']]
            in_list.append({
                'id': dct['id'],
                'node': dct['node'],
                'name': name,
                'value': value,
                'control_group': control_group,
                'option01': dct['option01'].strip(),
                'option02': dct['option02'].strip(),
                'option03': dct['option03'].strip(),
            })

        # select node
        for _tool in list(self.comp.GetToolList().values()):
            self.flow.Select(_tool, True)

        #
        m = '\n'.join([
            macro.get_header(macro_name, True),
            macro.get_input(main_in_list, in_list),
            macro.get_output(output_list),
            macro.get_footer(),
        ])
        print(m)

        # build
        self.comp.Execute(macro.get_save_script(
            str(macro_path),
            macro_name,
            '\n'.join([
                macro.get_header(macro_name, True),
                macro.get_input(main_in_list, in_list),
                macro.get_output(output_list),
                macro.get_footer(),
            ]),
        ))
