import subprocess
import dataclasses
from pathlib import Path
from typing import List

from rs.core.read_aloud import cmd


EXE_NAME = 'SeikaSay2.exe'


@dataclasses.dataclass
class Data(cmd.Data):
    cid: str = '4000'

    volume: str = ''
    speed: str = ''
    pitch: str = ''
    alpha: str = ''
    intonation: str = ''
    emotion01: str = ''
    emotion02: str = ''

    def export(self, path: Path) -> None:
        command: List[str] = [
            str(self.exe_path),
            '-cid',
            self.cid,
            '-save',
            str(path),
        ]
        if self.volume.strip() != '':
            command.append('-volume')
            command.append(self.volume.strip())
        if self.speed.strip() != '':
            command.append('-speed')
            command.append(self.speed.strip())
        if self.pitch.strip() != '':
            command.append('-pitch')
            command.append(self.pitch.strip())
        if self.alpha.strip() != '':
            command.append('-alpha')
            command.append(self.alpha.strip())
        if self.intonation.strip() != '':
            command.append('-intonation')
            command.append(self.intonation.strip())
        if self.emotion01.strip() != '' and self.emotion02.strip() != '':
            command.append('-emotion')
            command.append(self.emotion01.strip())
            command.append(self.emotion02.strip())
        command.append('-t')
        command.append(self.text.replace('\n', ' '))
        subprocess.run(command, shell=True)


if __name__ == '__main__':
    s = Data()
    s.cid = '4000'
    s.volume = '50'
    s.speed = '120'
    s.pitch = '100'
    s.exe_path = 'D:/App/assistantseika20220205c/SeikaSay2/SeikaSay2.exe'
    s.text = 'おはようございます。'
    s.export(Path('D:/App/assistantseika20220205c/SeikaSay2/out.wav'))
    s2 = Data()
    s2.cid = '7009'
    s2.volume = '1'
    s2.speed = '1'
    s2.pitch = '0'
    s2.intonation = '1'
    s2.exe_path = 'D:/App/assistantseika20220205c/SeikaSay2/SeikaSay2.exe'
    s2.text = 'おはようございます。'
    s2.export(Path('D:/App/assistantseika20220205c/SeikaSay2/out2.wav'))
