import json
import requests
import time


def get(command: str, max_retry: int):
    r = None
    for i in range(max_retry):
        r = requests.get(
            'http://localhost:50021/' + command,
            timeout=(10.0, 300.0),
        )
        if r.status_code == requests.codes.ok:
            break
        time.sleep(1)
    if r is None:
        raise ConnectionError(f'VOICEVOXとの通信に失敗しました。 {command}:')
    return r


def post(command: str, params, data, max_retry: int):
    r = None
    for i in range(max_retry):
        r = requests.post(
            'http://localhost:50021/' + command,
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


def core_versions(max_retry: int):
    command = 'core_versions'
    return get(command, max_retry).json()


def speakers(max_retry: int):
    command = 'speakers'
    return get(command, max_retry).json()


def audio_query(text: str, speaker: int, max_retry: int):
    command = 'audio_query'
    params = {'text': text, 'speaker': speaker}
    return post(command, params, None, max_retry).json()


def synthesis(speaker: int, data, max_retry: int):
    command = 'synthesis'
    params = {'speaker': speaker}
    return post(command, params, data, max_retry).content


if __name__ == "__main__":
    print(core_versions(10))
    print(speakers(10))
    query_data = audio_query('こんにちは', 8, 10)
    print(query_data)
    print(synthesis(8, query_data, 10))
