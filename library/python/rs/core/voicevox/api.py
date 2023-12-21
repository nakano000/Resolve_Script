import json
import requests
import time

VOICEVOX_PORT: int = 50021
VOICEVOX_NEMO_PORT: int = 50121
SHAREVOX_PORT: int = 50025


def get(command: str, max_retry: int, port: int = VOICEVOX_PORT):
    r = None
    for i in range(max_retry):
        r = requests.get(
            f'http://localhost:{port}/' + command,
            timeout=(10.0, 300.0),
        )
        if r.status_code == requests.codes.ok:
            break
        time.sleep(1)
    if r is None:
        raise ConnectionError(f'VOICEVOXとの通信に失敗しました。 {command}:')
    return r


def post(command: str, params, data, max_retry: int, port: int = VOICEVOX_PORT):
    r = None
    for i in range(max_retry):
        r = requests.post(
            f'http://localhost:{port}/' + command,
            params=params,
            data=json.dumps(data),
            timeout=(10.0, 300.0),
        )
        if r.status_code == requests.codes.ok:
            break
        time.sleep(1)
    if r is None:
        raise ConnectionError(f'VOICEVOXとの通信に失敗しました。 {command}:')
    return r


def core_versions(max_retry: int, port: int = VOICEVOX_PORT):
    command = 'core_versions'
    return get(command, max_retry, port).json()


def speakers(max_retry: int, port: int = VOICEVOX_PORT):
    command = 'speakers'
    return get(command, max_retry, port).json()


def audio_query(text: str, speaker: int, max_retry: int, port: int = VOICEVOX_PORT):
    command = 'audio_query'
    params = {'text': text, 'speaker': speaker}
    return post(command, params, None, max_retry, port).json()


def synthesis(speaker: int, data, max_retry: int, port: int = VOICEVOX_PORT):
    command = 'synthesis'
    params = {'speaker': speaker}
    return post(command, params, data, max_retry, port).content


if __name__ == "__main__":
    from pprint import pprint

    print(core_versions(10))
    print(speakers(10))
    query_data = audio_query('こんにちは さようなら', 8, 10)
    pprint(query_data)
    print(synthesis(8, query_data, 10))
