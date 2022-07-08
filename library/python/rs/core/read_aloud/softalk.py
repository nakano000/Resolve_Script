import subprocess
import dataclasses
from pathlib import Path
from typing import List

from rs.core.read_aloud import cmd

VOICE_LIST: List[str] = [
    '女性01',
    '女性02',
    '男性01',
    '男性02',
    'ロボット',
    '中性',
    '機械',
    '特殊',
    '女性 (defo1)',
    '女性 (f1c)',
    '女性 (f3a)',
    '女性 (f4)',
    '女性 (rm)',
    '女性 (rm3)',
    '女性 (teto1)',
    '女性 (huskey)',
    '女性 (momo1)',
    '女性 (nonbiri)',
    '男性 (m4b)',
    '男性 (m5)',
    '中性 (mf1)',
    '中性 (mf2)',
    'ロボット (robo)',
    'ロボット (rb2)',
    'ロボット (rb3)',
    '女性 (F1E)',
    '女性 (F2E)',
    '男性 (M1E)',
    'Microsoft Haruka Desktop - Japanese',
    'Microsoft Zira Desktop - English (United States)',
]

EXE_NAME = 'softalkw.exe'


@dataclasses.dataclass
class Data(cmd.Data):
    voice: str = '女性01'

    volume: int = 50
    speed: int = 120
    pitch: int = 100

    def export(self, path: Path) -> None:
        command: List[str] = [
            str(self.exe_path),
            '/R:' + str(path),
            '/NM:' + self.voice,
            '/V:' + str(self.volume),
            '/S:' + str(self.speed),
            '/O:' + str(self.pitch),
            '/W:' + self.text.replace('\n', ' '),
        ]
        subprocess.run(command, shell=True)


if __name__ == '__main__':
    s = Data()
    s.exe_path = 'D:/App/softalk/softalkw.exe'
    s.text = 'おはようございます。'
    s.export(Path('D:/App/softalk/out.wav'))
