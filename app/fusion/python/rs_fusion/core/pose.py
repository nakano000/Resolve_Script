import json
from pathlib import Path

import pyperclip

from rs.core import (
    pipe as p,
)

from rs_fusion.core import chara_sozai as cs_cmd


def get_connected(node):
    if node.ID == 'Merge':
        output = node.Foreground.GetConnectedOutput()
    else:
        output = node.Input.GetConnectedOutput()
    if output is None:
        return None
    return output.GetTool()


def get_pair(node):
    connected = get_connected(node)
    connected_name = connected.Name if connected is not None else None
    return [node.Name, connected_name]


def apply(comp, lst, is_chara_sozai=False):
    comp.Lock()
    comp.StartUndo('RS Pose')
    for x in lst:
        node_name = x[0]
        connected_name = x[1]
        if is_chara_sozai:
            connected = comp.FindTool(connected_name)
            if connected is None:
                continue
            key = connected.GetInput('Comments')
            cs_cmd.connect(comp, node_name, key)
        else:
            node = comp.FindTool(node_name)
            if node is None or node.ID not in ['Merge', 'Transform']:
                continue
            if connected_name is None:
                connected = None
            else:
                connected = comp.FindTool(connected_name)
                if connected is None:
                    continue
            if node.ID == 'Merge':
                parm = 'Foreground'
            else:
                parm = 'Input'

            node.ConnectInput(parm, connected)
            node.Center.HideViewControls()
            node.Angle.HideViewControls()
            node.Size.HideViewControls()
    comp.EndUndo(True)
    comp.Unlock()


def comment2json(comp):
    root_name = 'Root'
    tool = comp.FindTool(root_name)
    if tool is None:
        print('Tool not found: {}'.format(root_name))
        return None
    lst = tool.GetInput('Comments').split('\n')
    tools = p.pipe(
        lst,
        p.map(lambda x: x.strip()),
        p.filter(lambda x: x != ''),
        p.map(lambda x: comp.FindTool(x)),
        p.filter(lambda x: x is not None),
        p.filter(lambda x: x.ID in ['Merge', 'Transform']),
        list,
    )
    data = p.pipe(
        tools,
        p.map(get_pair),
        list,
    )
    return json.dumps(data, indent=4, ensure_ascii=False)


def copy(comp):
    text = comment2json(comp)
    if text is None:
        return
    pyperclip.copy(text)


def paste(comp, is_chara_sozai=False):
    text = pyperclip.paste()
    try:
        lst = json.loads(text)
    except json.JSONDecodeError:
        print('Invalid JSON')
        return
    if isinstance(lst, list):
        apply(comp, lst, is_chara_sozai=is_chara_sozai)


def save(comp, fusion):
    text = comment2json(comp)
    if text is None:
        return
    path = fusion.RequestFile(
        '',
        '',
        {
            'FReqB_Saving': True,
            'FReqB_SeqGather': False,
            'FReqS_Filter': 'JSON File (*.json)|*.json',
            'FReqS_Title': 'Save POSE',
        }
    )
    if path is None:
        return

    Path(path).write_text(text, encoding='utf-8')


def load(comp, fusion, is_chara_sozai=False):
    path = fusion.RequestFile(
        '',
        '',
        {
            'FReqB_Saving': False,
            'FReqB_SeqGather': False,
            'FReqS_Filter': 'JSON File (*.json)|*.json',
            'FReqS_Title': 'Load POSE',
        }
    )
    if path is None:
        return
    text = Path(path).read_text(encoding='utf-8')
    try:
        lst = json.loads(text)
    except json.JSONDecodeError:
        print('Invalid JSON')
        return
    if isinstance(lst, list):
        apply(comp, lst, is_chara_sozai=is_chara_sozai)


def get_uc(page, is_chara_sozai=False):
    width = 0.5
    _text = ', is_chara_sozai=True' if is_chara_sozai else ''
    paste_lua = 'comp:Execute([[!Py3: from rs_fusion.core import pose; pose.paste(comp%s)]])' % _text
    load_lua = 'comp:Execute([[!Py3: from rs_fusion.core import pose; pose.load(comp, fu%s)]])' % _text
    return {
        '__flags': 2097152,
        'CopyPose': {
            'LINKS_Name': 'Copy Pose',
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'ButtonControl',
            'INP_Integer': False,
            'BTNCS_Execute': 'comp:Execute([[!Py3: from rs_fusion.core import pose; pose.copy(comp)]])',
            'INP_External': False,
            'ICS_ControlPage': page,
            'ICD_Width': width,
        },
        'PastePose': {
            'LINKS_Name': 'Paste Pose',
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'ButtonControl',
            'INP_Integer': False,
            'BTNCS_Execute': paste_lua,
            'INP_External': False,
            'ICS_ControlPage': page,
            'ICD_Width': width,
        },
        'SavePose': {
            'LINKS_Name': 'Save Pose',
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'ButtonControl',
            'INP_Integer': False,
            'BTNCS_Execute': 'comp:Execute([[!Py3: from rs_fusion.core import pose; pose.save(comp, fu)]])',
            'INP_External': False,
            'ICS_ControlPage': page,
            'ICD_Width': width,
        },
        'LoadPose': {
            'LINKS_Name': 'Load Pose',
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'ButtonControl',
            'INP_Integer': False,
            'BTNCS_Execute': load_lua,
            'INP_External': False,
            'ICS_ControlPage': page,
            'ICD_Width': width,
        },
    }
