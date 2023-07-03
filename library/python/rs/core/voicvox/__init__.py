import io
import soundfile as sf

import rs.core.voicvox.api as api


def get_speakers(max_retry: int):
    data = api.speakers(max_retry)
    print(data)
    r = {}
    for d in data:
        for style in d['styles']:
            r[d['name'] + '（' + style['name'] + '）'] = style['id']
    return r


def get_voice(speaker: int, data, max_retry: int):
    voice_data = api.synthesis(speaker, data, max_retry)
    return sf.read(io.BytesIO(voice_data))


if __name__ == "__main__":
    for k, v in get_speakers(10).items():
        print(k, v)
    _speaker = 8
    _query_data = api.audio_query('こんにちは', _speaker, 10)
    _data, _samplerate = get_voice(_speaker, _query_data, 10)
    print(_samplerate)
    print(_data)
