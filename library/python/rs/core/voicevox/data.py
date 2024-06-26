import dataclasses
from typing import Optional

from rs.core import (
    config,
    pipe as p,
    note,
)

from rs.core.voicevox import api
from rs.core.voicevox.mora_list import openjtalk_text2mora as text2mora


@dataclasses.dataclass
class Speaker(config.DataInterface):
    id: int = 0
    name: str = ''
    style: str = ''

    def get_display_name(self):
        return f'{self.name}({self.style})'


@dataclasses.dataclass
class SpeakerList(config.Data):
    _list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(Speaker))

    def to_list(self):
        return self._list.to_list()

    def to_dict(self):
        return self._list.to_list_of_dict()

    def get_display_name_list(self):
        return p.pipe(
            self._list,
            p.map(p.call.get_display_name()),
            list,
        )

    def get_display_name(self, id: int):
        display_name = None
        for s in self._list:
            if s.id == id:
                display_name = s.get_display_name()
                break
        return display_name

    def get_id_from_display_name(self, display_name):
        speaker_id = None
        for s in self._list:
            if display_name == s.get_display_name():
                speaker_id = s.id
                break
        return speaker_id

    def set_from_voicevox(self, max_retry: int = 10, port: int = 50021):
        self._list.set_list(p.pipe(
            api.speakers(max_retry, port),
            p.map(lambda x: p.pipe(
                x['styles'],
                p.map(
                    lambda y: Speaker(
                        y['id'],
                        x['name'],
                        y['name'],
                    )
                ),
                list,
            )),
            list,
            lambda x: sum(x, []),
        ))

@dataclasses.dataclass
class Mora(config.DataInterface):
    text: str = 'ラ'
    consonant: Optional[str] = 'r'
    consonant_length: Optional[float] = 0.1
    vowel: str = 'a'
    vowel_length: float = 0.4
    pitch: float = p.pipe(
        'A4',
        note.name2index,
        note.index2pitch,
    )

    def set_rest(self, length: float):
        self.text = '、'
        self.consonant = None
        self.consonant_length = None
        self.vowel = 'pau'
        self.vowel_length = length
        self.pitch = 0.0

    def set_note(self, text: str, note_index: int, length: float):
        consonant_max_length = 0.1
        # 音素
        if text in text2mora:
            self.text = text
            self.consonant, self.vowel = text2mora[text]
            if self.consonant == '':
                self.consonant = None
        # length
        if self.consonant is None:
            self.consonant_length = None
            self.vowel_length = length
        else:
            if length / 2.0 < consonant_max_length:
                self.consonant_length = length / 2.0
                self.vowel_length = length / 2.0
            else:
                self.consonant_length = consonant_max_length
                self.vowel_length = length - consonant_max_length

        # pitch
        self.pitch = note.index2pitch(note_index)

    def get_sec(self):
        if self.consonant is None:
            return self.vowel_length
        return self.consonant_length + self.vowel_length

    def get_phoneme_list(self):
        lst = []
        if self.consonant is not None:
            lst.append({
                'sign': self.consonant,
                'length': self.consonant_length,
            })
        lst.append({
            'sign': self.vowel,
            'length': self.vowel_length,
        })
        return lst


@dataclasses.dataclass
class AccentPhrase(config.DataInterface):
    moras: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(Mora))
    accent: int = 1
    pause_mora: Optional[Mora] = None
    is_interrogative: bool = False

    def get_text(self):
        text = p.pipe(
            self.moras,
            p.map(lambda x: x.text),
            ''.join,
        )
        if self.pause_mora is not None:
            text += self.pause_mora.text
        return text

    def get_phoneme_list(self):
        lst = []
        for m in self.moras:
            lst.extend(m.get_phoneme_list())
        if self.pause_mora is not None:
            lst.extend(self.pause_mora.get_phoneme_list())
        return lst


@dataclasses.dataclass
class AudioQuery(config.DataInterface):
    accent_phrases: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(AccentPhrase))
    speedScale: float = 1.0
    pitchScale: float = 0.0
    intonationScale: float = 1.0
    volumeScale: float = 1.0
    prePhonemeLength: float = 0.0
    postPhonemeLength: float = 0.0
    outputSamplingRate: int = 24000
    outputStereo: bool = False

    def get_text(self):
        return p.pipe(
            self.accent_phrases,
            p.map(lambda x: x.get_text()),
            ''.join,
        )

    def get_phoneme_list(self):
        lst = []
        if self.prePhonemeLength > 0.0:
            lst.append({
                'sign': 'pau',
                'length': self.prePhonemeLength,
            })
        for a in self.accent_phrases:
            lst.extend(a.get_phoneme_list())
        if self.postPhonemeLength > 0.0:
            lst.append({
                'sign': 'pau',
                'length': self.postPhonemeLength,
            })
        return lst


if __name__ == "__main__":
    s_list = SpeakerList()
    s_list.set_from_voicevox()
    print(s_list)
    print(s_list.get_display_name_list())
    print(s_list.get_id_from_display_name('ずんだもん(ノーマル)'))
