from pathlib import Path

from rs.core import config


def read(f: Path, c_code: str):
    import chardet
    # 文字コード
    _code = c_code.strip().lower()

    if _code in ['auto', '']:
        with open(f, 'rb') as _f:
            content = _f.read()
            char_code = chardet.detect(content)
        enc: str = char_code['encoding']

        if enc is None or enc.lower() not in config.ENCODING_LIST:
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
