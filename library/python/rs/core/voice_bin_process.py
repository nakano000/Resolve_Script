import os
import re
import time
from pathlib import Path

import soundfile

from rs.core import (
    config,
    pipe as p,
    srt,
    lab,
    util,
    chara_data,
    txt,
)
from rs.core.chara_data import CharaData

SCRIPT_DIR: Path = config.ROOT_PATH.joinpath('data', 'app', 'VoiceBin')
TEXT_SCRIPT_BASE: str = SCRIPT_DIR.joinpath('text_script_base.lua').read_text(encoding='utf-8')
TATIE_SCRIPT_BASE: str = SCRIPT_DIR.joinpath('tatie_script_base.lua').read_text(encoding='utf-8')
TATIE_SETTING_BASE: str = SCRIPT_DIR.joinpath('tatie_setting_base.txt').read_text(encoding='utf-8')


def del_script(f: Path):
    d = f.parent
    srt_file = d.joinpath(f.stem + '.srt')
    lua_file = d.joinpath(f.stem + '.lua')
    tatie_lua_file = d.joinpath(f.stem + '.tatie.lua')
    setting_file = d.joinpath(f.stem + '.setting')

    for f in [srt_file, lua_file, tatie_lua_file, setting_file]:
        if f.is_file():
            f.unlink()


def run(f: Path, fps, time_out=10.0):
    r = False
    # time out 設定
    step = 0.2
    start_time = time.time()
    is_time_out = False

    # ロック確認
    while True:
        if time.time() - start_time > time_out:
            is_time_out = True
            break
        try:
            os.rename(str(f), str(f))
            break
        except OSError:
            time.sleep(step)

    if is_time_out:
        return r
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

    t = util.str2lines(
        txt.read(txt_file, ch_data.c_code),
        ch_data.str_width * 2,
    )

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
    if ch_data.anim_type.strip().lower() == 'open':
        anim = lab.wav2anim(f, fps)
    elif lab_file.is_file():
        anim = lab.lab2anim(lab_file, fps, ch_data.anim_type.strip().lower())

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
