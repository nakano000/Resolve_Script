import json
from pathlib import Path

import pyperclip

from rs.core import (
    pipe as p,
)


def get_foreground(mg):
    output = mg.Foreground.GetConnectedOutput()
    if output is None:
        return None
    return output.GetTool()


def get_pair(mg):
    fg = get_foreground(mg)
    fg_name = fg.Name if fg is not None else None
    return [mg.Name, fg_name]


def apply(comp, lst):
    comp.Lock()
    comp.StartUndo('RS Pose')
    for x in lst:
        mg_name = x[0]
        fg_name = x[1]
        mg = comp.FindTool(mg_name)
        if mg is None or mg.ID != 'Merge':
            continue
        if fg_name is None:
            fg = None
        else:
            fg = comp.FindTool(fg_name)
            if fg is None:
                continue
        mg.ConnectInput('Foreground', fg)
        mg.Center.HideViewControls()
        mg.Angle.HideViewControls()
        mg.Size.HideViewControls()
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
        p.filter(lambda x: x.ID == 'Merge'),
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


def paste(comp):
    text = pyperclip.paste()
    try:
        lst = json.loads(text)
    except json.JSONDecodeError:
        print('Invalid JSON')
        return
    if isinstance(lst, list):
        apply(comp, lst)


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


def load(comp, fusion):
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
        apply(comp, lst)
