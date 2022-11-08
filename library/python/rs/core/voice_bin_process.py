import re
from pathlib import Path

import soundfile

from rs.core import (
    config,
    pipe as p,
    srt,
    lab,
    util,
    chara_data,
)
from rs.core.chara_data import CharaData

SCRIPT_DIR: Path = config.ROOT_PATH.joinpath('data', 'app', 'VoiceBin')
TEXT_SCRIPT_BASE: str = SCRIPT_DIR.joinpath('text_script_base.txt').read_text(encoding='utf-8')
TATIE_SCRIPT_BASE: str = SCRIPT_DIR.joinpath('tatie_script_base.txt').read_text(encoding='utf-8')
TATIE_SETTING_BASE: str = SCRIPT_DIR.joinpath('tatie_setting_base.txt').read_text(encoding='utf-8')


def read_text(f: Path, c_code: str):
    import chardet
    # 文字コード
    _code = c_code.strip().lower()

    if _code in ['auto', '']:
        with open(f, 'rb') as _f:
            content = _f.read()
            char_code = chardet.detect(content)
        enc: str = char_code['encoding']

        if enc is None or enc.lower() not in [
            'utf-8',
            'utf-8-sig',
            'utf-16',
            'utf-16be',
            'utf-16le',
            'utf-32',
            'utf-32be',
            'utf-32le',
            'cp932',
            'shift_jis',
        ]:
            try:
                t = content.decode(encoding='utf-8')
            except:
                t = content.decode(encoding='cp932')
        else:
            if enc.lower() == 'shift_jis':
                enc = 'cp932'
            t = content.decode(encoding=enc)
    else:
        t = f.read_text(encoding=_code)

    # 改行コード
    t = t.replace('\r\n', '\n')
    return t


def run(f: Path, fps):
    r = False
    #
    d = f.parent
    txt_file = d.joinpath(f.stem + '.txt')
    if not txt_file.is_file():
        return r

    srt_file = d.joinpath(f.stem + '.srt')
    lab_file = d.joinpath(f.stem + '.lab')

    lua_file = d.joinpath(f.stem + '.lua')
    tatie_lua_file = d.joinpath(f.stem + '.tatie.lua')
    setting_file = d.joinpath(f.stem + '.setting')

    # flag
    srt_exists = srt_file.is_file()
    lua_exists = lua_file.is_file()
    setting_exists = setting_file.is_file()
    if srt_exists and lua_exists and setting_exists:
        return r

    # キャラクター設定
    ch_data = CharaData()
    for cd in chara_data.get_chara_list():
        cd: CharaData
        m = re.fullmatch(cd.reg_exp, f.stem)
        if m is not None:
            ch_data = cd
            break

    t = read_text(txt_file, ch_data.c_code)

    # SRT
    if not srt_exists:
        wave_data, samplerate = soundfile.read(str(f))
        _d: float = float(wave_data.shape[0]) / samplerate

        srt_data = srt.Srt()

        srt_data.subtitles.append(srt.Subtitle(0, _d, t))

        srt_data.save(srt_file)
        r = True

    # Text+
    if not lua_exists:
        lua = TEXT_SCRIPT_BASE % (
            t,
            ch_data.color,
            ch_data.track_name,
            str(ch_data.setting_file)
        )
        util.write_text(
            lua_file,
            lua,
        )

    # 立ち絵
    if setting_exists:
        return r
    anim = ''
    if ch_data.anim_type == 'open':
        anim = lab.wav2anim(f, fps)
    elif lab_file.is_file():
        anim = lab.lab2anim(lab_file, fps)

    if anim != '':
        util.write_text(
            setting_file,
            TATIE_SETTING_BASE % (
                t.replace('\n', '\\n').replace('"', '\\"'),
                ch_data.anim_parameter,
                ch_data.anim_parameter,
                ch_data.anim_parameter,
                anim,
            ),
        )
        util.write_text(
            tatie_lua_file,
            TATIE_SCRIPT_BASE % (
                ch_data.color,
                ch_data.track_name,
                ch_data.anim_parameter,
                str(setting_file)
            ),
        )
    return r
